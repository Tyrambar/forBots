import re
import json
import datetime
from random import choice

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from default_texts import all_texts as ru_texts
from db import *


colors = {}
colors.update({i:"default" for i in (ru_texts['to_begin'],
                                     ru_texts['button_opt_edit'][0])})
colors.update({i:"primary" for i in (ru_texts['see_my_e'],
                                     ru_texts['button_opt'][0])})
colors.update({i:"negative" for i in (ru_texts['cancel'],
                                      ru_texts['show_org'])})

ru_texts['options_str'][1] = ru_texts['options_str'][1] + \
        ' - ДО 40 СИМВОЛОВ\n'

# Main classes
class Arg:
    """This class includes necessary arguments for everyone users.
    numb_see_my_e - maximum length of list for owns confirmed
    deep:
    deep < 10 - default actions bot:
        deep == 1 - has already seen greetings
        deep == 2 - seeing some event
        deep == 3 - seeing confirmed
    10 < deep < 20 - actions for creation event
    deep > 20 - actions for edit existing event
    change - helping arg for editing existing event or delete event
    """
    def __init__(self, db_id, numb_see_my_e,
                    deep, previous, see_my_e_lst, change=0):
        self.db_id = db_id
        self.numb_see_my_e = numb_see_my_e
        self.deep = deep
        self.previous = previous
        self.see_my_e_lst = see_my_e_lst
        self.change = change

    def to_default(self):
        self.numb_see_my_e = 0
        self.deep = 0
        self.previous = ''
        self.see_my_e_lst = []
        self.change = 0


# Functions for synchronization db for Telegram
def sync_db(user, password):
    execute_query(conn, DEL_USER_VK, (user, ))
    execute_query(conn, SYNC_DB_TO_TG, (user, password))
    m_send(user, ru_texts['sync_success'])


# Helping functions
def make_date(month, date, hour, min=0):
    return datetime.datetime(datetime.datetime.today().year,
                             month, date, hour, min)


# Check your sign for some event
def get_sign_db(user, curr):
    confirmed = execute_query(conn, GET_SIGNS_BY_ID, (user, curr)).fetchone()
    if confirmed:
        return user == confirmed[0]
    else: return


def make_butt(dct, *labels):
    new_line = []
    for n, label in enumerate(labels):
        new_line.append({
            "action": {
            "type": "text",
            "payload": '{"button": "%d"}' % (n+1),
            "label": label
            },
            "color": colors.get(label, "positive")
        })
    dct['buttons'].append(new_line)
    return dct


def make_menu(id=None, lst=[]):
    keyb = {"one_time": False, "buttons": []}
    c = 1
    buttons = lst[:]
    all_id = {elem[0] for elem in execute_query(conn, ALL_SIGNED_ID)
            .fetchall()}
    if users[id].deep != 3 and users[id].deep < 10:
        if users[id].db_id in all_id:
            buttons.append(ru_texts['see_my_e'])
        if users[id].db_id in all_id:
            buttons.append(ru_texts['show_org'])

    for butt in buttons:
        if not (ru_texts['see_my_e'] in buttons and \
                ru_texts['show_org'] in buttons):
            make_butt(keyb, butt)
        else:
            if butt not in (ru_texts['see_my_e'], ru_texts['show_org']):
                make_butt(keyb, butt)
    if ru_texts['see_my_e'] in buttons and ru_texts['show_org'] in buttons:
        make_butt(keyb, ru_texts['see_my_e'], ru_texts['show_org'])
    if ru_texts['main'] not in buttons:
        make_butt(keyb, ru_texts['to_begin'])

    return json.dumps(keyb, ensure_ascii=False)


def get_name_by_id(user):
    info = vk.users.get(user_ids=user)[0]
    return f"@id{user}({info['first_name']} {info['last_name']})"


def functions_with_pass(user, curr_low):
    if curr_low == ru_texts['pass_add']:
        return to_create_e_f(user)
    elif curr_low == ru_texts['pass_destroy']:
        return destroy_e_f(user)
    elif curr_low == ru_texts['pass_edit']:
        return to_edit_e_f(user)

		
def m_send(user, message, keyboard = None):
    return vk.messages.send(user_id=user, message=message,
                            keyboard=keyboard, random_id=get_random_id())

def wrong_ans(user):
    return m_send(user, ru_texts['wrong'])


def welc_ans(user):
    return m_send(user, ru_texts['welc'])


def how_a_u(user):
    return m_send(user, ru_texts['mes_a_che_tam'])

	
# Main functions
def start(user):
    global users
    users[user].to_default()
    menu = make_menu(user, [ru_texts['main']])
    m_send(user, ru_texts['hi_from_bot'], menu)


def step_1(user):
    global users, events
    row_events = execute_query(conn, EVENTS_LIST).fetchall()
    events = [ev[0] for ev in row_events]
    menu = make_menu(user, events)
    text = ''
    if users[user].change == 1:
        text = ru_texts['choose_edit_e']
    for kk, i in enumerate(events):
        text += f"{kk+1}. {i}\n"
    m_send(user, text, menu)
    if not users[user].change:
        users[user].deep = 1


def step_work_with_e(user, curr):
    global users, events

    # Function-handler for see some event
    def step_e(numb = None):
        global users, events
        if curr in events:
            users[user].previous = curr
            if get_sign_db(users[user].db_id, curr):
                menu = make_menu(user, [ru_texts['cancel']])
            else:
                menu = make_menu(user, [ru_texts['agree']])
            event_attrs = execute_query(conn, GET_EVENT_ALL,
                    (curr,)).fetchone()
            text = ru_texts['format_event_repr']\
                    (event_attrs[:-2]\
                     +(get_name_by_id(event_attrs[-2]),), ru_texts)
            m_send(user, text, menu)
        # Case, when response is event serial number
        elif numb:
            if users[user].see_my_e_lst:
                users[user].previous = users[user].see_my_e_lst[numb-1]
                if get_sign_db(users[user].db_id, users[user].previous):
                    menu = make_menu(user, [ru_texts['cancel']])
                else:
                    menu = make_menu(user, [ru_texts['agree']])
                event_attrs = execute_query(conn, GET_EVENT_ALL,
                        (users[user].previous,)).fetchone()
            else:
                users[user].previous = events[numb-1]
                if get_sign_db(users[user].db_id, events[numb-1]):
                    menu = make_menu(user)
                else:
                    menu = make_menu(user, [ru_texts['agree']])
                event_attrs = execute_query(conn, GET_EVENT_ALL,
                        (events[numb-1],)).fetchone()
            text = ru_texts['format_event_repr']\
                    (event_attrs[:-2]\
                    +(get_name_by_id(event_attrs[-2]),), ru_texts)
            m_send(user, text, menu)
        else:
            return wrong_ans(user)

        if users[user].numb_see_my_e:
            users[user].numb_see_my_e = 0
        users[user].see_my_e_lst = []
        users[user].deep = 2

    # Function-handler for confirm to event
    def step_confirm():
        global users, events
        menu = make_menu(user)
        m_send(user, f'{ru_texts["confirm"]} `{users[user].previous}`', menu)
        if not get_sign_db(users[user].db_id, users[user].previous):
            eve_id = execute_query(conn, GET_ID_EVENT_BY_NAME,
                    (users[user].previous,)).fetchone()[0]
            execute_query(conn, ADD_SIGNS, (users[user].db_id, eve_id))
            host_curr_id = execute_query(conn, GET_HOST_ID_ALL,
                    (users[user].previous,)).fetchone()[0]
            m_send(host_curr_id,
                   ru_texts['step_conf_txt'] \
                    (get_name_by_id(user), users[user].previous))

    # Function-handler for cancel confirm to event
    def step_canc():
        global users, events
        menu = make_menu(user)
        m_send(user, ru_texts['cancel_all'], menu)
        eve_id = execute_query(conn, GET_ID_EVENT_BY_NAME,
                (users[user].previous,)).fetchone()[0]
        execute_query(conn, DEL_SIGNS, (users[user].db_id, eve_id))
        host_curr_id = execute_query(conn, GET_HOST_ID_ALL,
                (users[user].previous,)).fetchone()[0]
        m_send(host_curr_id, ru_texts['step_canc_txt'] \
                (get_name_by_id(user), users[user].previous))

    # Conditions returns needed function
    if users[user].change == -1:
        return succ_destroy_e_f(user, curr)
    elif (curr in events or re.match(r"[1-9]\d?", curr[:2]))\
            and users[user].deep < 10 and users[user].change == 0:
        if curr in events:
            return step_e()
        elif users[user].numb_see_my_e:
            numb_for_see_my = check_input_number(curr,
                                                 users[user].see_my_e_lst)
            return step_e(numb_for_see_my) if numb_for_see_my else \
                wrong_ans(user)
        elif users[user].deep == 1 and check_input_number(curr, events):
            return step_e(check_input_number(curr, events))
        else:
            return wrong_ans(user)
    elif curr == ru_texts['agree'] or re.match(ru_texts['ok'], curr.lower()):
        return step_confirm()
    elif 'отмен' in curr.lower() and \
            get_sign_db(users[user].db_id, users[user].previous):
        return step_canc()
    elif 10 <= users[user].deep < 20:
        return create_e_f(user, curr)
    elif users[user].change == 1 or users[user].deep >= 20:
        return edit_e_f(user, curr)
    else:
        return wrong_ans(user)

		
# Seeing yours confirmed
def see_my_e_f(user):
    global users, events
    see_my = ru_texts['mes_see']
    users[user].deep = 3
    row_events = execute_query(conn, EVENTS_LIST).fetchall()
    events = [ev[0] for ev in row_events]
    for i in events:
        if get_sign_db(users[user].db_id, i):
            users[user].see_my_e_lst.append(i)
            see_my += ru_texts['see_my_e_f_txt'](users[user].numb_see_my_e, i)
            users[user].numb_see_my_e += 1
    menu = make_menu(user, users[user].see_my_e_lst)
    m_send(user, see_my, menu)

	
# Functions for creating events in bot
def to_create_e_f(user):
    global users
    users[user].to_default()
    users[user].deep = 10
    menu = make_menu(user, [ru_texts['button_opt'][0]])
    m_send(user, ru_texts['options'], menu)


def create_e_f(user, curr):
    global users, args_4_create, events
    menu = make_menu(user)
    if users[user].deep == 10:
        if curr == ru_texts['button_opt'][0]:
            m_send(user, ru_texts['options_str'][1], menu)
        else:
            if len(curr) <= 40:
                args_4_create['name'] = curr
                users[user].deep = 11
                m_send(user, ru_texts['options_str'][2], menu)
            else:
                m_send(user, ru_texts['options_fail'])

    elif users[user].deep == 11:
        args_4_create['address'] = curr
        users[user].deep = 12
        m_send(user, ru_texts['options_str'][3], menu)

    elif users[user].deep == 12:
        t = curr.split(',')
        try:
            if len(t) == 4:
                args_4_create['date'] = make_date(int(t[0]), int(t[1]),
                                                  int(t[2]), int(t[3]))
            else:
                args_4_create['date'] = make_date(int(t[0]), int(t[1]),
                                                  int(t[2]))
        except (IndexError, ValueError):
            m_send(user, ru_texts['options_fail'])
        else:
            users[user].deep = 13
            m_send(user, ru_texts['options_str'][4], menu)

    elif users[user].deep == 13:
        args_4_create['description'] = txt
        users[user].deep = 14
        menu = make_menu(user, [ru_texts['button_opt'][1]])
        m_send(user, ru_texts['options_almost'], menu)

    elif users[user].deep == 14 and curr == ru_texts['button_opt'][1]:
        add_event_q = create_add_event_q(args_4_create, users[user].db_id)
        execute_query(conn, ADD_EVENT, add_event_q)
        users[user].deep = 0
        m_send(user, ru_texts['options_succ'], menu)

		
# Functions for change existing events in bot
def to_edit_e_f(user):
    global users
    users[user].to_default()
    users[user].change = 1
    step_1(user)


def edit_e_f(user, curr):
    global users, args_4_create, event_attrs
    menu = make_menu(user, [ru_texts['button_opt_edit'][0]])

    if users[user].change == 1:
        users[user].deep = 20
        users[user].change = 0
        users[user].previous = curr
        event_attrs = execute_query(conn, GET_EVENT_ALL,
                                    (curr,)).fetchone()[:-2]
        args_4_create['prev_name'] = users[user].previous
        host_curr_id = execute_query(conn, GET_HOST_ID_ALL,
                                     (curr,)).fetchone()[0]
        if host_curr_id == user:
            text = ru_texts['options_str'][1] + ru_texts['old_option'] \
                   + users[user].previous
            m_send(user, text, menu)
        else:
            m_send(user, ru_texts['fail_right_4_edit_e'])
            users[user].to_default()

    elif users[user].deep == 20:
        if curr != ru_texts['button_opt_edit'][0]:
            args_4_create['name'] = curr
        else:
            args_4_create['name'] = users[user].previous
        users[user].deep = 21
        text = ru_texts['options_str'][2] + ru_texts['old_option'] \
               + event_attrs[1]
        m_send(user, text, menu)

    elif users[user].deep == 21:
        if curr != ru_texts['button_opt_edit'][0]:
            args_4_create['address'] = curr
        else:
            args_4_create['address'] = event_attrs[1]
        users[user].deep = 22
        text = ru_texts['options_str'][3] + ru_texts['old_option'] \
               + str(event_attrs[2])
        m_send(user, text, menu)

    elif users[user].deep == 22:
        if curr != ru_texts['button_opt_edit'][0]:
            t = curr.split(',')
            try:
                if len(t) == 4:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]),
                                                      int(t[2]), int(t[3]))
                else:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]),
                                                      int(t[2]))
            except (IndexError, ValueError):
                m_send(user, ru_texts['options_fail'])
            else:
                users[user].deep = 23
                text = ru_texts['options_str'][4] + ru_texts['old_option'] \
                       + event_attrs[3]
                m_send(user, text, menu)
        else:
            args_4_create['date'] = event_attrs[2]
            users[user].deep = 23
            text = ru_texts['options_str'][4] + ru_texts['old_option'] \
                   + event_attrs[3]
            m_send(user, text, menu)

    elif users[user].deep == 23:
        if curr != ru_texts['button_opt_edit'][0]:
            args_4_create['description'] = curr
        else:
            args_4_create['description'] = event_attrs[3]
        users[user].deep = 24
        menu = make_menu(user, [ru_texts['button_opt_edit'][1]])
        m_send(user, ru_texts['options_almost'], menu)

    elif users[user].deep == 24 and curr == ru_texts['button_opt_edit'][1]:
        add_event_q = create_add_event_q(conn,
                                         args_4_create, users[user].db_id)
        execute_query(conn, EDIT_EVENT,
                      add_event_q+[args_4_create['prev_name']])
        users[user].to_default()
        menu = make_menu(user)
        m_send(user, ru_texts['options_edit_succ'], menu)

		
# Functions for delete events in bot
def destroy_e_f(user):
    global users
    users[user].change = -1
    step_1(user)


def succ_destroy_e_f(user, curr):
    global users
    users[user].change = 0
    execute_query(conn, DEL_EVENT, (curr,))
    menu = make_menu(user)
    m_send(user, ru_texts['destroy_succ'], menu)


def see_my_host(user):
    global users, events
    text = ''
    for eve in events:
        host_curr_id = execute_query(conn, GET_HOST_ID_ALL,
                (eve,)).fetchone()[0]
        if user == host_curr_id:
            all_raw_nicknames = execute_query(conn, ALL_SIGNED_ID_BY_EV_ALL,
                    (eve,)).fetchall()
            nicknames = [get_name_by_id(nick[0]) for nick in all_raw_nicknames]
            text += ru_texts['see_my_host_txt'](eve, nicknames)
    m_send(user, text)

# Creating array for every users of bot and array for args
# for create/edit events
events = []
users = {}
args_4_create = {}
event_attrs = ()


# Main with data
TOKEN = ''
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
conn = create_connection(
    db_name, db_user, db_password, db_host)
for event in longpoll.listen():
    #try:
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            current = event.text
            user_id = event.user_id
            if user_id not in {exist_vk_id[0] for exist_vk_id in \
                    execute_query(conn, ALL_VK_ID).fetchall()}:
                execute_query(conn, ADD_USER, [user_id, None, random_passw()])
            if user_id not in users:
                found_db_id = execute_query(conn, GET_ID_USER_BY_VK,
                        (user_id,)).fetchone()[0]
                users[user_id] = Arg(found_db_id, 0, 0, '', [])
            if '&amp;' in current or '&quot;' in current:
                current = re.sub('&amp;', '&', current)
                current = re.sub('&quot;', '"', current)

            if re.match(ru_texts['begin'], current.lower()) or \
                    current == ru_texts['to_begin']:
                start(user_id)
            elif 'sync' in current.lower():
                sync_db(user, current.split()[1])
            elif 'get' in current.lower():
                m_send(user_id,
                       execute_query(conn, GET_PASSW_BY_VK).fetchone()[0])

            elif current.lower() in ru_texts['passwords']:
                functions_with_pass(user_id, current.lower())
            elif current == ru_texts['see_my_e']:
                see_my_e_f(user_id)
            elif current == ru_texts['show_org']:
                see_my_host(user_id)
            elif (users[user_id].deep == 0 and \
                  re.match(ru_texts['ok'], current.lower())) or \
                  current == ru_texts['main']:
                step_1(user_id)
            else:
                step_work_with_e(user_id, current)

    #except (IndexError, KeyError, NameError):
    #    wrong_ans(event.user_id)