from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, RegexHandler, BaseFilter
from telegram import InlineQueryResultArticle, InputTextMessageContent, KeyboardButton, ReplyKeyboardMarkup
from default_texts_eng import all_texts as en_texts
from default_texts import all_texts as ru_texts
from examples_events_eng import *
import re
import logging
import datetime

from db import *

choose_lang_txt = 'Выберите язык / Choose language'
languages = ['🇷🇺', '🇬🇧']
lang_pass = '%%% lang'
# Commands
pass_add = 'create'
pass_edit = 'edit'
pass_destroy = 'delete'

TG_URL = 'https://telegg.ru/orig/bot'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


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
                    deep, previous, see_my_e_lst, lang, change = 0):
        self.db_id = db_id
        self.numb_see_my_e = numb_see_my_e
        self.deep = deep
        self.previous = previous
        self.see_my_e_lst = see_my_e_lst
        self.change = change
        self.lang = lang

    def to_default(self):
        self.numb_see_my_e = 0
        self.deep = 0
        self.previous = ''
        self.see_my_e_lst = []
        self.change = 0

# Functions for synchronization db for VK
def sync_db(update, context):
    execute_query(conn, DEL_USER_TG, (update.message.chat_id, ))
    execute_query(conn, SYNC_DB_TO_VK, (update.message.chat_id, update.message.text.split()[1]))
    m_send(update, context, en_texts['sync_success'])
    choose_lang(update, context)

def get_passw(update, context):
    m_send(update, context, execute_query(conn, GET_PASSW_BY_TG).fetchone()[0])


# Helping funcs
def make_date(month, date, hour, min = 0):
    return datetime.datetime(datetime.datetime.today().year, month, date, hour, min)

# Check your sign for some event
def get_sign_db(user, curr):
    confirmed = execute_query(conn, GET_SIGNS_BY_ID, (user, curr)).fetchone()
    if confirmed:
        return user == confirmed[0]
    else: return

def m_send(up, co, txt, keyboard = None):
    return co.bot.send_message(chat_id=up.message.chat_id, text=txt, reply_markup=keyboard)

def make_menu(id, buttons = [], n_cols=1):
    global users
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    pre_footer_buttons = []
    all_id = {elem[0] for elem in execute_query(conn, ALL_SIGNED_ID).fetchall()}
    if buttons != languages:
        if not id in all_id:
            pre_footer_buttons = []
        if users[id].deep < 10:
            if users[id].db_id in all_id:
                if not users[id].deep == 3:
                    pre_footer_buttons.append(users[id].lang['see_my_e'])
            if users[id].db_id in all_id:
                pre_footer_buttons.append(users[id].lang['show_org'])
        if pre_footer_buttons:
            menu.append(pre_footer_buttons)
        if users[id].lang['main'] not in buttons:
            footer_buttons = [users[id].lang['to_begin']]
            menu.append(footer_buttons)

    return ReplyKeyboardMarkup(menu, resize_keyboard = True,
                               one_time_keyboard = True)


# Main with data
ac_token = ''
updater = Updater(token= ac_token, base_url = TG_URL, use_context= True)
dispatcher = updater.dispatcher

# Creating array for every users of bot and array for args for create/edit events
events = []
users = {}
args_4_create = {}
event_attrs = ()

conn = create_connection(
    db_name, db_user, db_password, db_host
)

# Additional funcs-handlers
def additional_ans(update, context):
    if users[update.message.chat_id].deep < 10 and users[update.message.chat_id].change == 0:
        if re.match(users[update.message.chat_id].lang['welcom_re'], update.message.text.lower()):
            m_send(update, context, users[update.message.chat_id].lang['welc'])
        elif re.match(users[update.message.chat_id].lang['a_che_tam'], message.text.lower()):
            m_send(update, context, users[update.message.chat_id].lang['mes_a_che_tam'])
    else:
        wrong_ans(update, context)


def wrong_ans(update, context):
    m_send(update, context, users[update.message.chat_id].lang['wrong'])


# Main funcs-handlers
def choose_lang(update, context):
    global users
    tg_id = update.message.chat_id
    if tg_id not in {exist_tg_id[0] for exist_tg_id in execute_query(conn, ALL_TG_ID).fetchall()}:
        execute_query(conn, ADD_USER, [None, tg_id, random_passw()])
    if tg_id not in users:
        found_db_id = execute_query(conn, GET_ID_USER_TG_VK, (tg_id,)).fetchone()[0]
        users[tg_id] = Arg(found_db_id, 0, 0, '', [], None)
    menu = make_menu(tg_id, buttons = languages)
    m_send(update, context, choose_lang_txt, menu)
    users[tg_id].previous = lang_pass

def has_chosen_lang(update, context):
    global users
    users[update.message.chat_id].previous = None
    if update.message.text == languages[0]:
        users[update.message.chat_id].lang = ru_texts
    elif update.message.text == languages[1]:
        users[update.message.chat_id].lang = en_texts
    start(update, context)

def start(update, context):
    global users
    tg_id = update.message.chat_id
    users[tg_id].to_default()
    menu = make_menu(tg_id, buttons = [users[tg_id].lang['main']])
    m_send(update, context, users[tg_id].lang['hi_from_bot'], menu)

def step_1(update, context):
    global users, events
    row_events = execute_query(conn, EVENTS_LIST).fetchall()
    events = [ev[0] for ev in row_events]
    menu = make_menu(update.message.chat_id, events)
    text = ''
    if update.message.chat_id not in users:
        choose_lang(update, context)
    else:
        if users[update.message.chat_id].change == 1:
            text = users[update.message.chat_id].lang['choose_edit_e']
        for kk, i in enumerate(events):
            text += f"{kk+1}. {i}\n"
        m_send(update, context, text, menu)
        if not users[update.message.chat_id].change:
            users[update.message.chat_id].deep = 1

		
# Most popular function-handler for processing events, depending from what do you want
def step_work_with_e(update, context):
    global users, events
    curr, tg_id = update.message.text, update.message.chat_id
    ef_name = update.effective_user.username
    # Function-handler for see some event
    def step_e(numb = None):
        global users, events
        if curr in events:
            users[tg_id].previous = curr
            if get_sign_db(users[tg_id].db_id, curr):
                menu = make_menu(tg_id, [users[tg_id].lang['cancel']])
            else:
                menu = make_menu(tg_id, [users[tg_id].lang['agree']])
            event_attrs = execute_query(conn, GET_EVENT_ALL, (curr,)).fetchone()
            text = users[tg_id].lang['format_event_repr']\
                (event_attrs[:-2] + ('@'+context.bot.getChat(event_attrs[-1])['username'],), users[tg_id].lang)
            m_send(update, context, text, menu)

        elif numb:
            if users[tg_id].see_my_e_lst:
                users[tg_id].previous = users[tg_id].see_my_e_lst[numb-1]

                if get_sign_db(users[tg_id].db_id, users[tg_id].previous):
                    menu = make_menu(tg_id, [users[tg_id].lang['cancel']])
                else:
                    menu = make_menu(tg_id, [users[tg_id].lang['agree']])
                event_attrs = execute_query(conn, GET_EVENT_ALL,
                                            (users[tg_id].previous,)).fetchone()
            else:
                users[tg_id].previous = events[numb-1]
                if get_sign_db(users[tg_id].db_id, events[numb-1]):
                    menu = make_menu(tg_id)
                else:
                    menu = make_menu(tg_id, [users[tg_id].lang['agree']])
                event_attrs = execute_query(conn, GET_EVENT_ALL,
                                            (events[numb-1],)).fetchone()
            text = users[tg_id].lang['format_event_repr']\
                (event_attrs[:-2] + (context.bot.getChat(event_attrs[-1])['username'],), users[tg_id].lang)
            m_send(update, context, text, menu)
        else:
            return wrong_ans(update, context)

        if users[tg_id].numb_see_my_e:
            users[tg_id].numb_see_my_e = 0
        users[tg_id].see_my_e_lst = []
        users[tg_id].deep = 2
		
    # Function-handler for confirm to event
    def step_confirm():
        global users, events
        menu = make_menu(tg_id)
        m_send(update, context, f'{users[tg_id].lang["confirm"]} '
                                f'`{users[tg_id].previous}`', menu)
        if not get_sign_db(users[tg_id].db_id, users[tg_id].previous):
            eve_id = execute_query(conn, GET_ID_EVENT_BY_NAME, (users[tg_id].previous,)).fetchone()[0]
            execute_query(conn, ADD_SIGNS, (users[tg_id].db_id, eve_id))
            host_curr_id = execute_query(conn, GET_HOST_ID_ALL, (users[tg_id].previous,)).fetchone()[1]
            context.bot.send_message(
                chat_id=host_curr_id,
                text=users[tg_id].lang['step_conf_txt']('@' + ef_name, users[tg_id].previous))

    # Function-handler for cancel confirm to event
    def step_canc():
        global users, events
        menu = make_menu(tg_id)
        m_send(update, context, users[tg_id].lang['cancel_all'], menu)
        eve_id = execute_query(conn, GET_ID_EVENT_BY_NAME, (users[tg_id].previous,)).fetchone()[0]
        execute_query(conn, DEL_SIGNS, (users[tg_id].db_id, eve_id))
        host_curr_id = execute_query(conn, GET_HOST_ID_ALL, (users[tg_id].previous,)).fetchone()[1]
        context.bot.send_message(
            chat_id=host_curr_id,
            text=users[tg_id].lang['step_canc_txt']('@' + ef_name, users[tg_id].previous))

    # Conditions returns needed function
    if users[tg_id].change == -1:
        return succ_destroy_e_f(update, context)
    elif (curr in events or re.match(r"[1-9]\d?", curr[:2]))\
            and users[tg_id].deep < 10 and users[tg_id].change == 0:
        if curr in events:
            return step_e()
        elif users[tg_id].numb_see_my_e:
            numb_for_see_my = check_input_number(curr, users[tg_id].see_my_e_lst)
            return step_e(numb_for_see_my) if numb_for_see_my else wrong_ans(update, context)
        elif users[tg_id].deep == 1 and check_input_number(curr, events):
            return step_e(check_input_number(curr, events))
        else:
            return wrong_ans(update, context)
    elif curr == users[tg_id].lang['agree'] or \
            re.match(users[tg_id].lang['ok'], curr.lower()):
        return step_confirm()
    elif ('отмен' in curr.lower() or 'cancel' in curr.lower()) and \
            get_sign_db(users[tg_id].db_id, users[tg_id].previous):
        return step_canc()
    elif 10 <= users[tg_id].deep < 20:
        return create_e_f(update, context)
    elif users[tg_id].change == 1 or users[tg_id].deep >= 20:
        return edit_e_f(update, context)
    else:
        return wrong_ans(update, context)

		
# Seeing yours confirmed
def see_my_e_f(update, context):
    global users, events
    see_my = users[update.message.chat_id].lang['mes_see']
    row_events = execute_query(conn, EVENTS_LIST).fetchall()
    events = [ev[0] for ev in row_events]
    for i in events:
        if get_sign_db(users[update.message.chat_id].db_id, i):
            users[update.message.chat_id].see_my_e_lst.append(i)
            see_my += users[update.message.chat_id].lang['see_my_e_f_txt']\
                (users[update.message.chat_id].numb_see_my_e, i)
            users[update.message.chat_id].numb_see_my_e += 1
    menu = make_menu(update.message.chat_id, users[update.message.chat_id].see_my_e_lst)
    m_send(update, context, see_my, menu)
    users[update.message.chat_id].deep = 3


# Functions for creating events in bot
def to_create_e_f(update, context):
    global users
    users[update.message.chat_id].to_default()
    users[update.message.chat_id].deep = 10
    menu = make_menu(update.message.chat_id,
                     buttons= [users[update.message.chat_id].lang['button_opt'][0]])
    m_send(update, context, users[update.message.chat_id].lang['options'], menu)

def create_e_f(update, context):
    global users, args_4_create, events
    curr, tg_id = update.message.text, update.message.chat_id
    menu = make_menu(tg_id)

    if users[tg_id].deep == 10:
        if curr == users[tg_id].lang['button_opt'][0]:
            m_send(update, context, users[tg_id].lang['options_str'][1], menu)
        else:
            args_4_create['name'] = curr
            users[tg_id].deep = 11
            m_send(update, context, users[tg_id].lang['options_str'][2], menu)
    elif users[tg_id].deep == 11:
        args_4_create['address'] = curr
        users[tg_id].deep = 12
        m_send(update, context, users[tg_id].lang['options_str'][3], menu)
    elif users[tg_id].deep == 12:
        t = curr.split(',')
        try:
            if len(t) == 4:
                args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]), int(t[3]))
            else:
                args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]))
        except (IndexError, ValueError):
            m_send(update, context, users[tg_id].lang['options_fail'])
        else:
            users[tg_id].deep = 13
            m_send(update, context, users[tg_id].lang['options_str'][4], menu)
    elif users[tg_id].deep == 13:
        args_4_create['description'] = curr
        users[tg_id].deep = 14
        menu = make_menu(tg_id, buttons = [users[tg_id].lang['button_opt'][1]])
        m_send(update, context, users[tg_id].lang['options_almost'], menu)
    elif users[tg_id].deep == 14 and \
            curr == users[tg_id].lang['button_opt'][1]:
        add_event_q = create_add_event_q(conn, args_4_create, users[tg_id].db_id)
        execute_query(conn, ADD_EVENT, add_event_q)
        users[tg_id].deep = 0
        m_send(update, context, users[tg_id].lang['options_succ'], menu)


# Functions for change existing events in bot
def to_edit_e_f(update, context):
    global users
    users[update.message.chat_id].to_default()
    users[update.message.chat_id].change = 1
    step_1(update, context)

def edit_e_f(update, context):
    global users, args_4_create, event_attrs
    curr, tg_id = update.message.text, update.message.chat_id
    menu = make_menu(tg_id,
                     buttons=[users[tg_id].lang['button_opt_edit'][0]])
    if users[tg_id].change == 1:
        users[tg_id].deep = 20
        users[tg_id].change = 0
        users[tg_id].previous = curr
        args_4_create['prev_name'] = users[tg_id].previous
        event_attrs = execute_query(conn, GET_EVENT_ALL, (curr,)).fetchone()[:-2]
        host_curr_id = execute_query(conn, GET_HOST_ID_ALL, (curr,)).fetchone()[1]
        if host_curr_id == tg_id:
            text = users[tg_id].lang['options_str'][1] + users[tg_id].lang['old_option']+ \
                   users[tg_id].previous
            m_send(update, context, text, menu)
        else:
            context.bot.send_message(tg_id, users[tg_id].lang['fail_right_4_edit_e'])
            users[tg_id].to_default()
    elif users[tg_id].deep == 20:
        if curr != users[tg_id].lang['button_opt_edit'][0]:
            args_4_create['name'] = curr
        else:
            args_4_create['name'] = users[tg_id].previous
        users[tg_id].deep = 21
        text = users[tg_id].lang['options_str'][2] + users[tg_id].lang['old_option'] + \
               event_attrs[1]
        m_send(update, context, text, menu)
    elif users[tg_id].deep == 21:
        if curr != users[tg_id].lang['button_opt_edit'][0]:
            args_4_create['address'] = curr
        else:
            args_4_create['address'] = event_attrs[1]
        users[tg_id].deep = 22
        text = users[tg_id].lang['options_str'][3]+ users[tg_id].lang['old_option']\
               +str(event_attrs[2])
        m_send(update, context, text, menu)
    elif users[tg_id].deep == 22:
        if curr != users[tg_id].lang['button_opt_edit'][0]:
            t = curr.split(',')
            try:
                if len(t) == 4:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]), int(t[3]))
                else:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]))
            except (IndexError, ValueError):
                m_send(update, context, users[tg_id].lang['options_fail'])
            else:
                users[tg_id].deep = 23
                text = users[tg_id].lang['options_str'][4] + users[tg_id].lang['old_option'] + \
                       event_attrs[3]
                m_send(update, context, text, menu)
        else:
            args_4_create['date'] = event_attrs[2]
            users[tg_id].deep = 23
            text = users[tg_id].lang['options_str'][4] + users[tg_id].lang['old_option'] + \
                   event_attrs[3]
            m_send(update, context, text, menu)
    elif users[tg_id].deep == 23:
        if curr != users[tg_id].lang['button_opt_edit'][0]:
            args_4_create['description'] = curr
        else:
            args_4_create['description'] = event_attrs[3]
        users[tg_id].deep = 24
        menu = make_menu(tg_id, buttons=[users[tg_id].lang['button_opt_edit'][1]])
        m_send(update, context, users[tg_id].lang['options_almost'], menu)
    elif users[tg_id].deep == 24 and \
            curr == users[tg_id].lang['button_opt_edit'][1]:
        add_event_q = create_add_event_q(conn, args_4_create, users[tg_id].db_id)
        execute_query(conn, EDIT_EVENT, add_event_q + [args_4_create['prev_name']])
        users[tg_id].to_default()
        menu = make_menu(tg_id)
        m_send(update, context, users[tg_id].lang['options_edit_succ'], menu)


# Functions for delete events in bot
def to_destroy_e_f(update, context):
    global users
    users[update.message.chat_id].change = -1
    step_1(update, context)

def succ_destroy_e_f(update, context):
    global users, events
    users[update.message.chat_id].change = 0
    execute_query(conn, DEL_EVENT, (update.message.text,))
    menu = make_menu(update.message.chat_id)
    m_send(update, context, users[update.message.chat_id].lang['destroy_succ'], menu)

def see_my_host(update, context):
    global users, events
    text = ''
    for eve in events:
        host_curr_id = execute_query(conn, GET_HOST_ID_ALL, (eve,)).fetchone()[1]
        if update.message.chat_id == host_curr_id:
            all_raw_nicknames = execute_query(conn, ALL_SIGNED_ID_BY_EV_ALL, (eve,)).fetchall()
            nicknames = [context.bot.getChat(nick[1])['username'] for nick in all_raw_nicknames]
            text += users[update.message.chat_id].lang['see_my_host_txt'](eve, nicknames, '@')
    m_send(update, context, text)


# Filters for handlers
class F_chosen_lang(BaseFilter):
    def filter(self, message):
        return users[message.chat_id].previous == lang_pass

class F_step1(BaseFilter):
    def filter(self, message):
        return en_texts['main'] in message.text or ru_texts['main'] in message.text

class F_step_e(BaseFilter):
    def filter(self, message):
        return True

class F_see_my_e(BaseFilter):
    def filter(self, message):
        return en_texts['see_my_e'] in message.text or ru_texts['see_my_e'] in message.text

class F_to_see_my_host(BaseFilter):
    def filter(self, message):
        return en_texts['show_org'] in message.text or ru_texts['show_org'] in message.text

class F_re_for_start(BaseFilter):
    def filter(self, message):
        return re.match(en_texts['begin']+r'|'+ru_texts['begin'], message.text.lower()) or \
               message.text == en_texts['to_begin'] or message.text == ru_texts['to_begin']

class F_get_passw(BaseFilter):
    def filter(self, message):
        return re.match('get', message.text.lower())

class F_sync_db(BaseFilter):
    def filter(self, message):
        return re.match('sync', message.text.lower())

class F_re_for_additional_ans(BaseFilter):
    def filter(self, message):
        return re.match(en_texts['welcom_re']+r'|'+ru_texts['welcom_re']+r'|'+ \
                        en_texts['a_che_tam']+r'|'+ru_texts['a_che_tam'],
                        message.text.lower())

ff_chosen_lang = F_chosen_lang()
ff_re_for_start = F_re_for_start()
ff_re_for_additional_ans = F_re_for_additional_ans()

ff_get_passw = F_get_passw()
ff_sync_db = F_sync_db()

ff_step1 = F_step1()
ff_step_e = F_step_e()
ff_see_my_e = F_see_my_e()

ff_to_see_my_host = F_to_see_my_host()

st_handler = CommandHandler('start', choose_lang)
lang_handler = MessageHandler(ff_chosen_lang, has_chosen_lang)
re_for_start_handler = MessageHandler(ff_re_for_start, start)

get_passw_handler = MessageHandler(ff_get_passw, get_passw)
sync_db_handler = MessageHandler(ff_sync_db, sync_db)

additional_ans_handler = MessageHandler(ff_re_for_additional_ans, additional_ans)
wrong_handler = MessageHandler(Filters.command, wrong_ans)

to_e_handler = MessageHandler(ff_step1, step_1)
in_e_handler = MessageHandler(ff_step_e, step_work_with_e)
see_my_e_handler = MessageHandler(ff_see_my_e, see_my_e_f)

to_create_e_handler = CommandHandler(pass_add, to_create_e_f)
to_edit_e_handler = CommandHandler(pass_edit, to_edit_e_f)
to_destroy_e_handler = CommandHandler(pass_destroy, to_destroy_e_f)

to_see_my_host_handler = MessageHandler(ff_to_see_my_host, see_my_host)

for i in (
        st_handler, lang_handler, re_for_start_handler,
        get_passw_handler, sync_db_handler,
        to_create_e_handler, to_edit_e_handler, to_destroy_e_handler,
        wrong_handler, additional_ans_handler,
        to_see_my_host_handler,
        see_my_e_handler, to_e_handler, in_e_handler,
    ):
    dispatcher.add_handler(i)

updater.start_polling()