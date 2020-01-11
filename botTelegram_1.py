from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, RegexHandler, BaseFilter
from telegram import InlineQueryResultArticle, InputTextMessageContent, KeyboardButton, ReplyKeyboardMarkup
from default_texts_eng import all_texts as en_texts
from default_texts import all_texts as ru_texts
from examples_events_eng import *
import re
import logging
from datetime import datetime

from collections import OrderedDict

choose_lang_txt = 'Выберите язык / Choose language'
languages = ['🇷🇺', '🇬🇧']
lang_pass = '%%% lang'
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
    def __init__(self, numb_see_my_e,
                    deep, previous, see_my_e_lst, lang, change = 0):
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
        self.confirmed = [] # users chat_id
        self.nicknames = [] # users nicknames (@somebody)

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name + '__class_Event'

		
# Creating arrays for events
ex_evs_objs = {}
evs = OrderedDict({})

def correct_order_ev(evs_arg):
    if evs_arg:
        return OrderedDict(sorted(list(evs_arg.items()), key = lambda ev_lst: ev_lst[1].date))

# Adding examples_events into these arrays
for i in range(len(e)):
    ex_evs_objs[e[i]] = Event(e[i], e_adress[i], e_dates[e[i]], events_d[e[i]], 203292486)
evs = ex_evs_objs.copy()


# Helping funcs
def make_date(month, date, hour, min = 0):
    return datetime(datetime.today().year, month, date, hour, min)

def m_send(up, co, txt, keyboard = None):
    return co.bot.send_message(chat_id=up.message.chat_id, text=txt, reply_markup=keyboard)

def make_menu(user_arg, buttons = [], n_cols=1):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    pre_footer_buttons = []
    if user_arg not in users:
        users[user_arg] = Arg(0, 0, '', [], None)

    if buttons != languages:
        if not user_arg in Event.confirmed_all:
            pre_footer_buttons = []
        if users[user_arg].deep < 10:
            if user_arg in Event.confirmed_all:
                if not users[user_arg].deep == 3:
                    pre_footer_buttons.append(users[user_arg].lang['see_my_e'])
            if user_arg in Event.host_all:
                pre_footer_buttons.append(users[user_arg].lang['show_org'])
        if pre_footer_buttons:
            menu.append(pre_footer_buttons)
        if users[user_arg].lang['main'] not in buttons:
            footer_buttons = [users[user_arg].lang['to_begin']]
            menu.append(footer_buttons)

    return ReplyKeyboardMarkup(menu, resize_keyboard = True,
                               one_time_keyboard = True)

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

# Main with data
ac_token = ''
updater = Updater(token= ac_token, base_url = TG_URL, use_context= True)
dispatcher = updater.dispatcher

# Creating array for every users of bot and array for args for create/edit events
users = {}
args_4_create = {}


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
    menu = make_menu(update.message.chat_id, buttons = languages)
    m_send(update, context, choose_lang_txt, menu)
    users[update.message.chat_id].previous = lang_pass

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
    menu = make_menu(update.message.chat_id, buttons = [users[update.message.chat_id].lang['main']])
    m_send(update, context, users[update.message.chat_id].lang['hi_from_bot'], menu)
    users[update.message.chat_id].to_default()

def step_1(update, context):
    global users
    menu = make_menu(update.message.chat_id, list(evs.keys()))
    text = ''
    if update.message.chat_id not in users:
        choose_lang(update, context)
    else:
        if users[update.message.chat_id].change == 1:
            text = users[update.message.chat_id].lang['choose_edit_e']
        for kk, i in enumerate(list(evs.keys())):
            text += f"{kk+1}. {i}\n"
        m_send(update, context, text, menu)
        if not users[update.message.chat_id].change:
            users[update.message.chat_id].deep = 1

		
# Most popular function-handler for processing events, depending from what do you want
def step_work_with_e(update, context):
    global users, evs
    curr, u_id = update.message.text, update.message.chat_id
    ef_name = update.effective_user.username
    if u_id not in users:
        users[u_id] = Arg(0, 0, '', [], None)
    # Function-handler for see some event
    def step_e(numb = None):
        global users, evs
        if curr in evs:
            users[u_id].previous = curr
            if u_id in evs[curr].confirmed:
                menu = make_menu(u_id, [users[u_id].lang['cancel']])
            else:
                menu = make_menu(u_id, [users[u_id].lang['agree']])
            text = users[u_id].lang['format_event_repr']\
                (evs[curr],
                    users[u_id].previous, users[u_id].lang)
            m_send(update, context, text, menu)

        elif numb:
            if users[u_id].see_my_e_lst:
                users[u_id].previous = users[u_id].see_my_e_lst[numb-1]

                if u_id in evs[users[u_id].previous].confirmed:
                    menu = make_menu(u_id, [users[u_id].lang['cancel']])
                else:
                    menu = make_menu(u_id, [users[u_id].lang['agree']])
                text = users[u_id].lang['format_event_repr']\
                        (evs[users[u_id].previous],
                         users[u_id].previous, users[u_id].lang)
                m_send(update, context, text, menu)
            else:
                users[u_id].previous = list(evs.items())[numb-1][0]
                if u_id in evs[list(evs.items())[numb-1][0]].confirmed:
                    menu = make_menu(u_id)
                else:
                    menu = make_menu(u_id, [users[u_id].lang['agree']])
                text = users[u_id].lang['format_event_repr']\
                            (evs[list(evs.items())[numb-1][0]],
                            users[u_id].previous, users[u_id].lang)
                m_send(update, context, text, menu)
        else:
            return wrong_ans(update, context)

        if users[u_id].numb_see_my_e:
            users[u_id].numb_see_my_e = 0
        users[u_id].see_my_e_lst = []
        users[u_id].deep = 2
		
    # Function-handler for confirm to event
    def step_confirm():
        global users, evs
        menu = make_menu(u_id)
        m_send(update, context, f'{users[u_id].lang["confirm"]} '
                                f'`{users[u_id].previous}`', menu)
        if u_id not in evs[users[u_id].previous].confirmed:
            evs[users[u_id].previous].confirmed.append(u_id)
            Event.confirmed_all.append(u_id)
            context.bot.send_message(
                chat_id=evs[users[u_id].previous].host_id,
                text=users[u_id].lang['step_conf_txt']('@' + ef_name, evs[users[u_id].previous]))
            evs[users[u_id].previous].nicknames.append(f'@{ef_name}')

    # Function-handler for cancel confirm to event
    def step_canc():
        global users, evs
        menu = make_menu(u_id)
        m_send(update, context, users[u_id].lang['cancel_all'], menu)
        evs[users[u_id].previous].confirmed.remove(u_id)
        Event.confirmed_all.remove(u_id)
        context.bot.send_message(
            chat_id=evs[users[u_id].previous].host_id,
            text=users[u_id].lang['step_canc_txt']('@' + ef_name, evs[users[u_id].previous]))
        evs[users[u_id].previous].nicknames.remove(f'@{ef_name}')

    # Conditions returns needed function
    if users[u_id].change == -1:
        return succ_destroy_e_f(update, context)
    elif (curr in evs or re.match(r"[1-9]\d?", curr[:2]))\
            and users[u_id].deep < 10 and users[u_id].change == 0:
        if curr in evs:
            return step_e()
        elif users[u_id].numb_see_my_e:
            numb_for_see_my = check_input_number(curr, users[u_id].see_my_e_lst)
            return step_e(numb_for_see_my) if numb_for_see_my else wrong_ans(update, context)
        elif users[u_id].deep == 1 and check_input_number(curr, list(evs.keys())):
            return step_e(check_input_number(curr, list(evs.keys())))
        else:
            return wrong_ans(update, context)
    elif curr == users[u_id].lang['agree'] or \
            re.match(users[u_id].lang['ok'], curr.lower()):
        return step_confirm()
    elif 'отмен' in curr.lower() and \
            u_id in evs[users[u_id].previous].confirmed:
        return step_canc()
    elif 10 <= users[u_id].deep < 20:
        return creating_e_f(update, context)
    elif users[u_id].change == 1 or users[u_id].deep >= 20:
        return edit_e_f(update, context)
    else:
        return wrong_ans(update, context)

		
# Seeing yours confirmed
def see_my_e_f(update, context):
    global users, evs
    if update.message.chat_id not in users:
        users[update.message.chat_id] = Arg(0, 0, '', [], None)
        return wrong_ans(update, context)
    see_my = users[update.message.chat_id].lang['mes_see']
    for i in evs:
        if update.message.chat_id in evs[i].confirmed:
            users[update.message.chat_id].see_my_e_lst.append(i)
            see_my += users[update.message.chat_id].lang['see_my_e_f_txt']\
                (users[update.message.chat_id].numb_see_my_e, i, evs[i].address)
            users[update.message.chat_id].numb_see_my_e += 1
    menu = make_menu(update.message.chat_id, users[update.message.chat_id].see_my_e_lst)
    m_send(update, context, see_my, menu)
    users[update.message.chat_id].deep = 3


# Functions for creating events in bot
def begin_create_e_f(update, context):
    global users
    users[update.message.chat_id].to_default()
    users[update.message.chat_id].deep = 10
    menu = make_menu(update.message.chat_id,
                     buttons= [users[update.message.chat_id].lang['button_opt'][0]])
    m_send(update, context, users[update.message.chat_id].lang['options'], menu)

def to_create_e_f(update, context):
    global users
    menu = make_menu(update.message.chat_id)
    m_send(update, context, users[update.message.chat_id].lang['options_str'][1], menu)

def creating_e_f(update, context):
    global users, args_4_create, evs
    curr, u_id = update.message.text, update.message.chat_id
    menu = make_menu(u_id)

    if users[u_id].deep == 10:
        args_4_create['name'] = curr
        users[u_id].deep = 11
        m_send(update, context, users[u_id].lang['options_str'][2], menu)
    elif users[u_id].deep == 11:
        args_4_create['address'] = curr
        users[u_id].deep = 12
        m_send(update, context, users[u_id].lang['options_str'][3], menu)
    elif users[u_id].deep == 12:
        t = curr.split(',')
        try:
            if len(t) == 4:
                args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]), int(t[3]))
            else:
                args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]))
        except (IndexError, ValueError):
            m_send(update, context, users[u_id].lang['options_fail'])
        else:
            users[u_id].deep = 13
            m_send(update, context, users[u_id].lang['options_str'][4], menu)
    elif users[u_id].deep == 13:
        args_4_create['description'] = curr
        users[u_id].deep = 14
        menu = make_menu(u_id, buttons = [users[u_id].lang['button_opt'][1]])
        m_send(update, context, users[u_id].lang['options_almost'], menu)
    elif users[u_id].deep == 14 and \
            curr == users[u_id].lang['button_opt'][1]:
        new_ev_obj = Event(args_4_create['name'], args_4_create['address'],
                           args_4_create['date'], args_4_create['description'], u_id)
        evs[args_4_create['name']] = new_ev_obj
        evs = correct_order_ev(evs)
        users[u_id].deep = 0
        m_send(update, context, users[u_id].lang['options_succ'], menu)


# Functions for change existing events in bot
def to_to_edit_e_f(update, context):
    global users
    users[update.message.chat_id].to_default()
    users[update.message.chat_id].change = 1
    step_1(update, context)

def edit_e_f(update, context):
    global users, args_4_create, evs
    curr, u_id = update.message.text, update.message.chat_id
    menu = make_menu(u_id,
                     buttons=[users[u_id].lang['button_opt_edit'][0]])
    if users[u_id].change == 1:
        users[u_id].deep = 20
        users[u_id].change = 0
        users[u_id].previous = curr
        if evs[curr].host_id == u_id:
            text = users[u_id].lang['options_str'][1] + users[u_id].lang['old_option']+ \
                   users[u_id].previous
            m_send(update, context, text, menu)
        else:
            context.bot.send_message(u_id, users[u_id].lang['fail_right_4_edit_e'])
            users[u_id].to_default()
    elif users[u_id].deep == 20:
        if curr != users[u_id].lang['button_opt_edit'][0]:
            args_4_create['name'] = curr
        else:
            args_4_create['name'] = users[u_id].previous
        obj_ev = evs.pop(users[u_id].previous)
        obj_ev.name = args_4_create['name']
        evs[args_4_create['name']] = obj_ev
        users[u_id].deep = 21
        text = users[u_id].lang['options_str'][2] + users[u_id].lang['old_option'] + \
               evs[args_4_create['name']].address
        m_send(update, context, text, menu)
    elif users[u_id].deep == 21:
        if curr != users[u_id].lang['button_opt_edit'][0]:
            args_4_create['address'] = curr
        else:
            args_4_create['address'] = evs[args_4_create['name']].address
        users[u_id].deep = 22
        text = users[u_id].lang['options_str'][3]+ users[u_id].lang['old_option']\
               +str(evs[args_4_create['name']].date)
        m_send(update, context, text, menu)
    elif users[u_id].deep == 22:
        if curr != users[u_id].lang['button_opt_edit'][0]:
            t = curr.split(',')
            try:
                if len(t) == 4:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]), int(t[3]))
                else:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]))
            except (IndexError, ValueError):
                m_send(update, context, users[u_id].lang['options_fail'])
            else:
                users[u_id].deep = 23
                text = users[u_id].lang['options_str'][4] + users[u_id].lang['old_option'] +\
                       evs[args_4_create['name']].description
                m_send(update, context, text, menu)
        else:
            args_4_create['date'] = evs[args_4_create['name']].date
            users[u_id].deep = 23
            text = users[u_id].lang['options_str'][4] + users[u_id].lang['old_option'] +\
                   evs[args_4_create['name']].description
            m_send(update, context, text, menu)
    elif users[u_id].deep == 23:
        if curr != users[u_id].lang['button_opt_edit'][0]:
            args_4_create['description'] = curr
        else:
            args_4_create['description'] = evs[args_4_create['name']].description
        users[u_id].deep = 24
        menu = make_menu(u_id, buttons=[users[u_id].lang['button_opt_edit'][1]])
        m_send(update, context, users[u_id].lang['options_almost'], menu)
    elif users[u_id].deep == 24 and \
            curr == users[u_id].lang['button_opt_edit'][1]:
        evs[args_4_create['name']].address = args_4_create['address']
        if evs[args_4_create['name']].date != args_4_create['date']:
            evs[args_4_create['name']].date = args_4_create['date']
            evs[args_4_create['name']].correct_order_ev()
        evs[args_4_create['name']].description = args_4_create['description']
        users[u_id].to_default()
        menu = make_menu(u_id)
        m_send(update, context, users[u_id].lang['options_edit_succ'], menu)


# Functions for delete events in bot
def destroy_e_f(update, context):
    global users
    users[update.message.chat_id].change = -1
    step_1(update, context)

def succ_destroy_e_f(update, context):
    global users, evs
    users[update.message.chat_id].change = 0
    evs.pop(update.message.text)
    menu = make_menu(update.message.chat_id)
    m_send(update, context, users[update.message.chat_id].lang['destroy_succ'], menu)

def see_my_host(update, context):
    global users, evs
    text = ''
    for i in evs:
        if update.message.chat_id == evs[i].host_id:
            text += users[update.message.chat_id].lang['see_my_host_txt'](i, evs[i].nicknames, '@')
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
        for lang in languages:
            if lang in message.text:
                return False
        for def_butt in (en_texts['main'], en_texts['see_my_e'],
                  en_texts['show_org'], en_texts['button_opt'][0]):
            if def_butt in message.text:
                return False
        for def_butt in (ru_texts['main'], ru_texts['see_my_e'],
                  ru_texts['show_org'], ru_texts['button_opt'][0]):
            if def_butt in message.text:
                return False
        for passw in (en_texts['pass_create'], en_texts['pass_determine'],
                           en_texts['pass_edit']):
            if passw in message.text.lower():
                return False
        for passw in (ru_texts['pass_create'], ru_texts['pass_determine'],
                           ru_texts['pass_edit']):
            if passw in message.text.lower():
                return False
        if re.match(en_texts['begin']+r'|'+ru_texts['begin'], message.text.lower()):
            return False
        return True

class F_see_my_e(BaseFilter):
    def filter(self, message):
        return en_texts['see_my_e'] in message.text or ru_texts['see_my_e'] in message.text

class F_to_create_e(BaseFilter):
    def filter(self, message):
        return en_texts['button_opt'][0] in message.text or \
               ru_texts['button_opt'][0] in message.text


class F_to_to_create_e(BaseFilter):
    def filter(self, message):
        return en_texts['pass_create'] in message.text.lower() or \
               ru_texts['pass_create'] in message.text.lower()

class F_to_destroy_e(BaseFilter):
    def filter(self, message):
        return en_texts['pass_determine'] in message.text.lower() or \
               ru_texts['pass_determine'] in message.text.lower()

class F_to_to_edit_e(BaseFilter):
    def filter(self, message):
        return en_texts['pass_edit'] in message.text.lower() or \
               ru_texts['pass_edit'] in message.text.lower()

class F_to_see_my_host(BaseFilter):
    def filter(self, message):
        return en_texts['show_org'] in message.text or ru_texts['show_org'] in message.text

class F_re_for_start(BaseFilter):
    def filter(self, message):
        return re.match(en_texts['begin']+r'|'+ru_texts['begin'], message.text.lower()) or \
               message.text == en_texts['to_begin'] or message.text == ru_texts['to_begin']

class F_re_for_additional_ans(BaseFilter):
    def filter(self, message):
        return re.match(en_texts['welcom_re']+r'|'+ru_texts['welcom_re']+r'|'+ \
                        en_texts['a_che_tam']+r'|'+ru_texts['a_che_tam'],
                        message.text.lower())

ff_chosen_lang = F_chosen_lang()
ff_re_for_start = F_re_for_start()
ff_re_for_additional_ans = F_re_for_additional_ans()

ff_step1 = F_step1()
ff_step_e = F_step_e()
ff_see_my_e = F_see_my_e()
ff_to_to_edit_e = F_to_to_edit_e()


ff_to_create_e = F_to_create_e()
ff_to_to_create_e = F_to_to_create_e()
ff_to_destroy_e = F_to_destroy_e()

ff_to_see_my_host = F_to_see_my_host()

st_handler = CommandHandler('start', choose_lang)
lang_handler = MessageHandler(ff_chosen_lang, has_chosen_lang)
re_for_start_handler = MessageHandler(ff_re_for_start, start)

additional_ans_handler = MessageHandler(ff_re_for_additional_ans, additional_ans)
wrong_handler = MessageHandler(Filters.command, wrong_ans)

to_e_handler = MessageHandler(ff_step1, step_1)
in_e_handler = MessageHandler(ff_step_e, step_work_with_e)
see_my_e_handler = MessageHandler(ff_see_my_e, see_my_e_f)

begin_create_e_handler = MessageHandler(ff_to_to_create_e, begin_create_e_f)
to_create_e_handler = MessageHandler(ff_to_create_e, to_create_e_f)
to_destroy_e_handler = MessageHandler(ff_to_destroy_e, destroy_e_f)
to_to_edit_e_handler = MessageHandler(ff_to_to_edit_e, to_to_edit_e_f)

to_see_my_host_handler = MessageHandler(ff_to_see_my_host, see_my_host)




for i in (
        st_handler, lang_handler, re_for_start_handler,
        wrong_handler, additional_ans_handler,
        to_e_handler, in_e_handler, see_my_e_handler,
        begin_create_e_handler, to_create_e_handler, to_destroy_e_handler,
        to_see_my_host_handler, to_to_edit_e_handler,
    ):
    dispatcher.add_handler(i)

updater.start_polling()