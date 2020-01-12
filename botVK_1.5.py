import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from examples_events import *
from default_texts import all_texts as ru_texts
import json
import re
from datetime import datetime

from collections import OrderedDict

url_id = 'https://vk.com/id'
colors = {}
colors.update({i:"default" for i in (ru_texts['to_begin'], ru_texts['button_opt_edit'][0])})
colors.update({i:"primary" for i in (ru_texts['see_my_e'], ru_texts['button_opt'][0])})
colors.update({i:"negative" for i in (ru_texts['cancel'], ru_texts['show_org'])})

ru_texts['options_str'][1] = ru_texts['options_str'][1] + ' - ДО 40 СИМВОЛОВ\n'
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
    def __init__(self, numb_see_my_e,
                    deep, previous, see_my_e_lst, change = 0):

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

class Event:
    confirmed_all = []
    host_all = []
    def __init__(self, name, addr, date, desc, host_id):
        self.date = date
        self.address = addr
        self.description = desc
        self.name = name
        self.host_id = host_id
        Event.host_all.append(self.host_id)
        self.confirmed = [] # users id
        self.nicknames = [] # users names with link

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name + '__class_Event'

		
# Helping functions
def make_date(month, date, hour, min = 0):
    return datetime(datetime.today().year, month, date, hour, min)

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
    c=1
    buttons = lst[:]
    if users[id].deep != 3 and users[id].deep < 10:
        if id in Event.confirmed_all:
            buttons.append(ru_texts['see_my_e'])
        if id in Event.host_all:
            buttons.append(ru_texts['show_org'])
    for butt in buttons:
        if not (ru_texts['see_my_e'] in buttons and ru_texts['show_org'] in buttons):
            make_butt(keyb, butt)
        else:
            if butt not in (ru_texts['see_my_e'], ru_texts['show_org']):
                make_butt(keyb, butt)
    if ru_texts['see_my_e'] in buttons and ru_texts['show_org'] in buttons:
        make_butt(keyb, ru_texts['see_my_e'], ru_texts['show_org'])
    if ru_texts['main'] not in buttons:
        make_butt(keyb, ru_texts['to_begin'])

    return json.dumps(keyb, ensure_ascii = False)

def check_input_number(input_n_event, lst):
    if len(input_n_event) > 1:
        if re.match(r"\d", input_n_event[1]) and \
                int(input_n_event[:2]) <= len(lst) - 1:
            return int(input_n_event[:2])
        elif int(input_n_event[0]) <= len(lst) - 1:
            return int(input_n_event[0])
        else:
            return
    else:
        if int(input_n_event[0]) <= len(lst):
            return int(input_n_event[0])
        else: return

def get_name_by_id(user):
    info = vk.users.get(user_ids=user)[0]
    return f"@id{user}({info['first_name']} {info['last_name']})"

def functions_with_pass(user, curr):
    if curr == ru_texts['pass_add']:
        return begin_create_e_f(user)
    elif curr == ru_texts['pass_destroy']:
        return destroy_e_f(user)
    elif curr == ru_texts['pass_edit']:
        return to_to_edit_e_f(user)
    elif curr == ru_texts['button_opt'][0].lower():
        return to_create_e_f(user)

		
def m_send(user, message, keyboard = None):
    return vk.messages.send(user_id = user, message = message,
                            keyboard = keyboard, random_id = get_random_id())

def wrong_ans(user):
    return m_send(user, ru_texts['wrong'])

def welc_ans(user):
    return m_send(user, ru_texts['welc'])

def how_a_u(user):
    return m_send(user, ru_texts['mes_a_che_tam'])

	
# Main functions
def start(user):
    global users
    menu = make_menu(user, [ru_texts['main']])
    m_send(user, ru_texts['hi_from_bot'], menu)
    users[user].to_default()

def step_1(user):
    global users
    menu = make_menu(user, list(evs.keys()))
    text = ''
    if users[user].change == 1:
        text = ru_texts['choose_edit_e']
    for kk, i in enumerate(list(evs.keys())):
        text += f"{kk+1}. {i}\n"
    m_send(user, text, menu)
    if not users[user].change:
        users[user].deep = 1

def step_work_with_e(user, curr):
    global users, evs
    # Function-handler for see some event
    def step_e(numb = None):
        global users, evs
        if curr in evs:
            users[user].previous = curr
            if user in evs[curr].confirmed:
                menu = make_menu(user, [ru_texts['cancel']])
            else:
                menu = make_menu(user, [ru_texts['agree']])
            text = ru_texts['format_event_repr'](evs[curr], users[user].previous, ru_texts)
            m_send(user, text, menu)
        # Case, when response is event serial number
        elif numb:
            if users[user].see_my_e_lst:
                users[user].previous = users[user].see_my_e_lst[numb-1]
                if user in evs[users[user].previous].confirmed:
                    menu = make_menu(user, [ru_texts['cancel']])
                else:
                    menu = make_menu(user, [ru_texts['agree']])
                text = ru_texts['format_event_repr'](users[user].previous, users[user].previous, ru_texts)
                m_send(user, text, menu)
            else:
                users[user].previous = list(evs.items())[numb-1][0]
                if user in evs[list(evs.items())[numb-1][0]].confirmed:
                    menu = make_menu(user)
                else:
                    menu = make_menu(user, [ru_texts['agree']])
                text = ru_texts['format_event_repr'](evs[list(evs.items())[numb-1][0]],
                                                     users[user].previous, ru_texts)
                m_send(user, text, menu)
        else:
            return wrong_ans(user)

        if users[user].numb_see_my_e:
            users[user].numb_see_my_e = 0
        users[user].see_my_e_lst = []
        users[user].deep = 2
    # Function-handler for confirm to event
    def step_confirm():
        global users, evs
        menu = make_menu(user)
        m_send(user, f'{ru_texts["confirm"]} `{users[user].previous}`', menu)
        if user not in evs[users[user].previous].confirmed:
            evs[users[user].previous].confirmed.append(user)
            Event.confirmed_all.append(user)
            m_send(evs[users[user].previous].host_id,
                   ru_texts['step_conf_txt'](get_name_by_id(user), evs[users[user].previous]))
            evs[users[user].previous].nicknames.append(get_name_by_id(user))

    # Function-handler for cancel confirm to event
    def step_canc():
        global users, evs
        menu = make_menu(user)
        m_send(user, ru_texts['cancel_all'], menu)
        evs[users[user].previous].confirmed.remove(user)
        Event.confirmed_all.remove(user)
        m_send(evs[users[user].previous].host_id, ru_texts['step_canc_txt'](get_name_by_id(user),
                                                                    evs[users[user].previous]))
        evs[users[user].previous].nicknames.remove(get_name_by_id(user))

    # Conditions returns needed function
    if users[user].change == -1:
        return succ_destroy_e_f(user, curr)
    elif (curr in evs or re.match(r"[1-9]\d?", curr[:2]))\
            and users[user].deep < 10 and users[user].change == 0:
        if curr in evs:
            return step_e()
        elif users[user].numb_see_my_e:
            numb_for_see_my = check_input_number(curr, users[user].see_my_e_lst)
            return step_e(numb_for_see_my) if numb_for_see_my else wrong_ans(user)
        elif users[user].deep == 1 and check_input_number(curr, list(evs.keys())):
            return step_e(check_input_number(curr, list(evs.keys())))
        else:
            return wrong_ans(user)
    elif curr == ru_texts['agree'] or re.match(ru_texts['ok'], curr.lower()):
        return step_confirm()
    elif 'отмен' in curr.lower() and \
            user in evs[users[user].previous].confirmed:
        return step_canc()
    elif 10 <= users[user].deep < 20:
        return creating_e_f(user, curr)
    elif users[user].change == 1 or users[user].deep >= 20:
        return edit_e_f(user, curr)
    else:
        return wrong_ans(user)

		
# Seeing yours confirmed
def see_my_e_f(user):
    global users, evs
    see_my = ru_texts['mes_see']
    users[user].deep = 3
    for i in evs:
        if user in evs[i].confirmed:
            users[user].see_my_e_lst.append(i)
            see_my += ru_texts['see_my_e_f_txt'](users[user].numb_see_my_e, i, evs[i].address)
            users[user].numb_see_my_e += 1
    menu = make_menu(user, users[user].see_my_e_lst)
    m_send(user, see_my, menu)

	
# Functions for creating events in bot
def begin_create_e_f(user):
    global users
    users[user].to_default()
    menu = make_menu(user, [ru_texts['button_opt'][0]])
    m_send(user, ru_texts['options'], menu)

def to_create_e_f(user):
    global users
    users[user].deep = 10
    menu = make_menu(user)
    m_send(user, ru_texts['options_str'][1], menu)

def creating_e_f(user, curr):
    global users, args_4_create, evs
    menu = make_menu(user)
    if users[user].deep == 10:
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
                args_4_create['date'] = make_date(int(t[0]),
                                        int(t[1]), int(t[2]), int(t[3]))
            else:
                args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]))
        except (IndexError, ValueError):
            m_send(user, ru_texts['options_fail'])
        else:
            users[user].deep = 13
            m_send(user, ru_texts['options_str'][4], menu)
    elif users[user].deep == 13:
        if '&quot;' in curr:
            txt = re.sub(r'&quot;', '"', curr)
        else:
            txt = curr
        args_4_create['description'] = txt
        users[user].deep = 14
        menu = make_menu(user, [ru_texts['button_opt'][1]])
        m_send(user, ru_texts['options_almost'], menu)
    elif users[user].deep == 14 and curr == ru_texts['button_opt'][1]:
        new_ev_obj = Event(args_4_create['name'], args_4_create['address'],
                           args_4_create['date'], args_4_create['description'], user)
        evs[args_4_create['name']] = new_ev_obj
        evs = correct_order_ev(evs)
        users[user].deep = 0
        m_send(user, ru_texts['options_succ'], menu)

		
# Functions for change existing events in bot
def to_to_edit_e_f(user):
    global users
    users[user].to_default()
    users[user].change = 1
    step_1(user)

def edit_e_f(user, curr):
    global users, args_4_create, evs
    menu = make_menu(user, [ru_texts['button_opt_edit'][0]])
    if users[user].change == 1:
        users[user].deep = 20
        users[user].change = 0
        users[user].previous = curr
        if evs[curr].host_id == user:
            text = ru_texts['options_str'][1]+ru_texts['old_option']+\
                   users[user].previous
            m_send(user, text, menu)
        else:
            m_send(user, ru_texts['fail_right_4_edit_e'])
            users[user].to_default()
    elif users[user].deep == 20:
        if curr != ru_texts['button_opt_edit'][0]:
            args_4_create['name'] = curr
        else:
            args_4_create['name'] = users[user].previous
        obj_ev = evs.pop(users[user].previous)
        obj_ev.name = args_4_create['name']
        evs[args_4_create['name']] = obj_ev
        users[user].deep = 21
        text = ru_texts['options_str'][2] + ru_texts['old_option'] +\
               evs[args_4_create['name']].address
        m_send(user, text, menu)
    elif users[user].deep == 21:
        if curr != ru_texts['button_opt_edit'][0]:
            args_4_create['address'] = curr
        else:
            args_4_create['address'] = evs[args_4_create['name']].address
        users[user].deep = 22
        text = ru_texts['options_str'][3]+ru_texts['old_option']+\
               str(evs[args_4_create['name']].date)
        m_send(user, text, menu)
    elif users[user].deep == 22:
        if curr != ru_texts['button_opt_edit'][0]:
            t = curr.split(',')
            try:
                if len(t) == 4:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]), int(t[3]))
                else:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]))
            except (IndexError, ValueError):
                m_send(user, ru_texts['options_fail'])
            else:
                users[user].deep = 23
                text = ru_texts['options_str'][4] + ru_texts['old_option'] +\
                       evs[args_4_create['name']].description
                m_send(user, text, menu)
        else:
            args_4_create['date'] = evs[args_4_create['name']].date
            users[user].deep = 23
            text = ru_texts['options_str'][4] + ru_texts['old_option'] +\
                   evs[args_4_create['name']].description
            m_send(user, text, menu)
    elif users[user].deep == 23:
        if curr != ru_texts['button_opt_edit'][0]:
            args_4_create['description'] = curr
        else:
            args_4_create['description'] = evs[args_4_create['name']].description
        users[user].deep = 24
        menu = make_menu(user, [ru_texts['button_opt_edit'][1]])
        m_send(user, ru_texts['options_almost'], menu)
    elif users[user].deep == 24 and curr == ru_texts['button_opt_edit'][1]:
        evs[args_4_create['name']].address = args_4_create['address']
        if evs[args_4_create['name']].date != args_4_create['date']:
            evs[args_4_create['name']].date = args_4_create['date']
        evs[args_4_create['name']].description = args_4_create['description']
        evs = correct_order_ev(evs)
        users[user].to_default()
        menu = make_menu(user)
        m_send(user, ru_texts['options_edit_succ'], menu)

		
# Functions for delete events in bot
def destroy_e_f(user):
    global users
    users[user].change = -1
    step_1(user)

def succ_destroy_e_f(user, curr):
    global users, evs
    users[user].change = 0
    evs.pop(curr)
    evs = correct_order_ev(evs)
    menu = make_menu(user)
    m_send(user, ru_texts['destroy_succ'], menu)

def see_my_host(user):
    global users, evs
    text = ''
    for i in evs:
        if user == evs[i].host_id:
            text += ru_texts['see_my_host_txt'](i, evs[i].nicknames)
    m_send(user, text)

# Creating arrays for events
ex_evs_objs = {}
evs = {}
def correct_order_ev(evs_arg):
    if evs_arg:
        return OrderedDict(sorted(list(evs_arg.items()), key = lambda ev_lst: ev_lst[1].date))

# Adding examples_events into these arrays
for i in range(len(e)):
    ex_evs_objs[e[i]] = Event(e[i], e_adress[i],
                              e_dates[e[i]], events_d[e[i]], 95372442)
evs = ex_evs_objs.copy()

# Creating array for every users of bot and array for args for create/edit events
users = {}
args_4_create = {}


# Main with data
token = ''
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

for event in longpoll.listen():
    #try:
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            current = event.text
            user_id = event.user_id
            if user_id not in users:
                users[user_id] = Arg(0, 0, '', [])
            if '&amp;' in current or '&quot;' in current:
                current = re.sub('&amp;', '&', current)
                current = re.sub('&quot;', '"', current)

            if re.match(ru_texts['begin'], current.lower()) or current == ru_texts['to_begin']:
                start(user_id)
            elif current.lower() in ru_texts['passwords'] or current == ru_texts['button_opt'][0]:
                functions_with_pass(user_id, current.lower())
            elif current == ru_texts['see_my_e']:
                see_my_e_f(user_id)
            elif current == ru_texts['show_org']:
                see_my_host(user_id)
            elif (users[user_id].deep == 0 and \
                  re.match(ru_texts['ok'], current.lower())) or current == ru_texts['main']:
                step_1(user_id)
            else:
                step_work_with_e(user_id, current)

    #except (IndexError, KeyError, NameError):
    #    wrong_ans(event.user_id)