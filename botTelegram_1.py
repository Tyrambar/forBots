from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, RegexHandler, BaseFilter
from telegram import InlineQueryResultArticle, InputTextMessageContent, KeyboardButton, ReplyKeyboardMarkup
import re
import logging
from datetime import datetime
from default_texts import *
from examples_events import *

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
                    deep, previous, see_my_e_lst, change = 0):

        self.numb_see_my_e = numb_see_my_e
        self.deep = deep
        self.previous = previous
        self.see_my_e_lst = see_my_e_lst
        self.change = change

class Event:
    evs_names = []
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
        self.correct_order_ev()

    def correct_order_ev(self):
        if evs:
            for i in Event.evs_names:
                if self.date < evs[i].date:
                    self.ev_id = Event.evs_names.index(i)
                    Event.evs_names.insert(self.ev_id, self.name)
                    break
            else:
                Event.evs_names.append(self.name)
                self.ev_id = len(Event.evs_names)
            if Event.evs_names.count(self.name) > 1:
                Event.evs_names.pop(Event.evs_names.index(self.name))
        else:
            Event.evs_names.append(self.name)

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name + '__class_Event'

#ex_evs_objs = [make_date(1, 1, 1, 1) for _ in range(3)]
ex_evs_objs = {}
evs = {}
for i in range(3):
    ex_evs_objs[e[i]] = Event(e[i], e_adress[i], e_dates[e[i]], events_d[e[i]], 203292486)
evs = ex_evs_objs.copy()
print(evs)
#argss_ind[ind_id] = {'numb_see_my_e': pp, 'deep': deep, 'previous': prev, 'see_my_e_lst': see_my_e_lst}

#us = User(12345, 3, 2, 'some', ['aha', 'huh'])
#print(12345 in User.users, us.users[12345], User.users[12345].numb_see_my_e)

# Helping funcs
def make_date(month, date, hour, min = 0):
    return datetime(2019, month, date, hour, min)

def m_send(up, co, txt, keyboard = None,):
    return co.bot.send_message(chat_id=up.message.chat_id, text=txt, reply_markup=keyboard)

def make_menu(user_arg, buttons = [], n_cols=1, footer_buttons = [to_begin], seeing_my_e = 0, while_edit = 0):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    pre_footer_buttons = [see_my_e]
    print(footer_buttons, Event.confirmed_all)
    if not while_edit:
        if user_arg in Event.confirmed_all:
            if seeing_my_e:
                pre_footer_buttons.remove(see_my_e)
        if see_my_e in footer_buttons and not user_arg in Event.confirmed_all:
            pre_footer_buttons.remove(see_my_e)
        if user_arg in Event.host_all:
            pre_footer_buttons.append(show_org)
    if pre_footer_buttons:
        menu.append(pre_footer_buttons)
    if footer_buttons:
        menu.append(footer_buttons)

    return ReplyKeyboardMarkup(menu, resize_keyboard = True, one_time_keyboard = True)

def check_input_number(input_n_event, lst):
    if len(input_n_event) > 1:
        if re.match(r"\d", input_n_event[1]) and int(input_n_event[:2]) <= len(lst) - 1:
            return int(input_n_event[:2])
        elif int(input_n_event[0]) <= len(lst) - 1:
            return int(input_n_event[0])
        else:
            return
    else:
        if int(input_n_event[0]) <= len(lst):
            return int(input_n_event[0])
        else: return

def format_event_repr(update, event):
    date_of_e = event.date
    text = f'{users[update.message.chat_id].previous}\n' \
       f'{int(date_of_e.strftime("%d"))} {months[int(date_of_e.strftime("%m"))]}, ' \
       f'{daysweek[date_of_e.strftime("%A")]}, в {date_of_e.strftime("%H:%M")}\nпо адресу: ' \
       f'{event.address}\n\n{event.description}'
    return text


# Main with data
ac_token = '909606708:AAENJ02T_jOjbShWb5ETckHDKHekV6X58QM'
updater = Updater(token= ac_token, base_url = TG_URL, use_context= True)
dispatcher = updater.dispatcher


users = {}
args_4_create = {}
password = 'праотцы'
pass_determine = 'кара'
pass_edit = 'правка'

# Additional funcs-handlers
def welc_ans(update, context):
    m_send(update, context, welc)

def how_a_u(update, context):
    m_send(update, context, mes_a_che_tam)

def wrong_ans(update, context):
    print(update.message.text)
    m_send(update, context, wrong)


# argss_ind[ind_id] = {'numb_see_my_e': pp, 'deep': deep, 'previous': prev, 'see_my_e_lst': see_my_e_lst}
# Main funcs-handlers
def start(update, context):
    global users
    menu = make_menu(update.message.chat_id, buttons = [main], footer_buttons = [])
    m_send(update, context, hi_from_bot, menu)
    users[update.message.chat_id] = Arg(0, 0, '', [])

    print(update.effective_user.username)

def step_1(update, context):
    global users
    menu = make_menu(update.message.chat_id, Event.evs_names)
    text = ''
    if update.message.chat_id not in users:
        users[update.message.chat_id] = Arg(0, 0, '', [])
    if users[update.message.chat_id].change == 1:
        text = choose_edit_e
    print(Event.evs_names)
    for kk, i in enumerate(Event.evs_names):
        text += f"{kk+1}. {i}\n"
    m_send(update, context, text, menu)
    if not users[update.message.chat_id].change:
        users[update.message.chat_id].deep = 1

# Most popular function-handler for processing events, depending from what do you want
def step_work_with_e(update, context):
    global users, evs
    if update.message.chat_id not in users:
        users[update.message.chat_id] = Arg(0, 0, '', [])
    print('in step_in_e')
    print(users[update.message.chat_id].see_my_e_lst)
    # Function-handler for see some event
    def step_e(numb = None):
        global users, evs
        if update.message.text in Event.evs_names:
            users[update.message.chat_id].previous = update.message.text
            if update.message.chat_id in evs[update.message.text].confirmed:
                menu = make_menu(update.message.chat_id, [cancel])
            else:
                menu = make_menu(update.message.chat_id, [agree])
            text = format_event_repr(update, evs[update.message.text])
            m_send(update, context, text, menu)

        elif numb:
            if users[update.message.chat_id].see_my_e_lst:
                users[update.message.chat_id].previous = users[update.message.chat_id].see_my_e_lst[numb-1]

                if update.message.chat_id in evs[users[update.message.chat_id].previous].confirmed:
                    menu = make_menu(update.message.chat_id, [cancel])
                else:
                    menu = make_menu(update.message.chat_id, [agree])
                text = format_event_repr(update, evs[users[update.message.chat_id].previous])
                m_send(update, context, text, menu)
            else:
                users[update.message.chat_id].previous = Event.evs_names[numb-1]
                if update.message.chat_id in evs[Event.evs_names[numb-1]].confirmed:
                    menu = make_menu(update.message.chat_id)
                else:
                    menu = make_menu(update.message.chat_id, [agree])
                text = format_event_repr(update, evs[Event.evs_names[numb-1]])
                m_send(update, context, text, menu)
        else:
            return wrong_ans(update, context)

        if users[update.message.chat_id].numb_see_my_e:
            users[update.message.chat_id].numb_see_my_e = 0
        users[update.message.chat_id].see_my_e_lst = []
        users[update.message.chat_id].deep = 2
    # Function-handler for confirm to event
    def step_confirm():
        global users, evs
        menu = make_menu(update.message.chat_id)
        m_send(update, context, f'{confirm} `{users[update.message.chat_id].previous}`', menu)
        if update.message.chat_id not in evs[users[update.message.chat_id].previous].confirmed:
            evs[users[update.message.chat_id].previous].confirmed.append(update.message.chat_id)
            Event.confirmed_all.append(update.message.chat_id)
            context.bot.send_message(
                chat_id=evs[users[update.message.chat_id].previous].host_id,
                text=f'Пользователь @{update.effective_user.username} записался на Ваше мероприятие')
            print(evs[users[update.message.chat_id].previous])
            evs[users[update.message.chat_id].previous].nicknames.append(f'@{update.effective_user.username}')
            print(evs[users[update.message.chat_id].previous].nicknames)

    # Function-handler for cancel confirm to event
    def step_canc():
        global users, evs
        menu = make_menu(update.message.chat_id)
        m_send(update, context, cancel_all, menu)
        evs[users[update.message.chat_id].previous].confirmed.remove(update.message.chat_id)
        Event.confirmed_all.remove(update.message.chat_id)
        context.bot.send_message(
            chat_id=evs[users[update.message.chat_id].previous].host_id,
            text=f'Пользователь @{update.effective_user.username} отменил запись на Ваше мероприятие')
        evs[users[update.message.chat_id].previous].nicknames.remove(
            f'@{update.effective_user.username}')

    # Conditions returns needed function
    if users[update.message.chat_id].change == -1:
        return succ_destroy_e_f(update, context)
    elif (update.message.text in Event.evs_names or re.match(r"[1-9]\d?", update.message.text[:2]))\
            and users[update.message.chat_id].deep < 10 and users[update.message.chat_id].change == 0:
        if update.message.text in Event.evs_names:
            return step_e()
        elif users[update.message.chat_id].numb_see_my_e:
            numb_for_see_my = check_input_number(update.message.text, users[update.message.chat_id].see_my_e_lst)
            print(users[update.message.chat_id].numb_see_my_e, [j for j in range(1,users[update.message.chat_id].numb_see_my_e+1)], numb_for_see_my)
            return step_e(numb_for_see_my) if numb_for_see_my else wrong_ans(update, context)
        elif users[update.message.chat_id].deep == 1 and check_input_number(update.message.text, Event.evs_names):
            return step_e(check_input_number(update.message.text, Event.evs_names))
        else:
            return wrong_ans(update, context)
    elif update.message.text == agree or re.match(ok, update.message.text.lower()):
        return step_confirm()
    elif 'отмен' in update.message.text.lower() and \
            update.message.chat_id in evs[users[update.message.chat_id].previous].confirmed:
        return step_canc()
    elif 10 <= users[update.message.chat_id].deep < 20:
        return creating_e_f(update, context)
    elif users[update.message.chat_id].change == 1 or users[update.message.chat_id].deep >= 20:
        return edit_e_f(update, context)
    else:
        return wrong_ans(update, context)

# Seeing yours confirmed
def see_my_e_f(update, context):
    global users, evs
    if update.message.chat_id not in users:
        users[update.message.chat_id] = Arg(0, 0, '', [])
        return wrong_ans(update, context)
    see_my = mes_see
    for i in Event.evs_names:
        if update.message.chat_id in evs[i].confirmed:
            users[update.message.chat_id].see_my_e_lst.append(i)
            see_my += f"{users[update.message.chat_id].numb_see_my_e+1}. {i} по адресу {evs[i].address}\n"
            users[update.message.chat_id].numb_see_my_e += 1
    print(users[update.message.chat_id].see_my_e_lst, users[update.message.chat_id].numb_see_my_e)
    menu = make_menu(update.message.chat_id, users[update.message.chat_id].see_my_e_lst, seeing_my_e=1)
    m_send(update, context, see_my, menu)
    users[update.message.chat_id].deep = 3


# Functions for creating events in bot
def begin_create_e_f(update, context):
    global users
    users[update.message.chat_id] = Arg(0, 0, '', [])
    menu = make_menu(update.message.chat_id, buttons= [button_opt[0]], while_edit = 1)
    m_send(update, context, options, menu)

def to_create_e_f(update, context):
    global users
    users[update.message.chat_id].deep = 10
    menu = make_menu(update.message.chat_id, while_edit = 1)
    m_send(update, context, options_str[1], menu)

def creating_e_f(update, context):
    global users, args_4_create, evs
    menu = make_menu(update.message.chat_id, while_edit=1)

    if users[update.message.chat_id].deep == 10:
        args_4_create['name'] = update.message.text
        users[update.message.chat_id].deep = 11
        m_send(update, context, options_str[2], menu)
    elif users[update.message.chat_id].deep == 11:
        args_4_create['address'] = update.message.text
        users[update.message.chat_id].deep = 12
        m_send(update, context, options_str[3], menu)
    elif users[update.message.chat_id].deep == 12:
        t = update.message.text.split(',')
        try:
            if len(t) == 4:
                args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]), int(t[3]))
            else:
                args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]))
        except (IndexError, ValueError):
            m_send(update, context, options_fail)
        else:
            users[update.message.chat_id].deep = 13
            m_send(update, context, options_str[4], menu)
    elif users[update.message.chat_id].deep == 13:
        args_4_create['description'] = update.message.text
        users[update.message.chat_id].deep = 14
        menu = make_menu(update.message.chat_id, buttons = [button_opt[1]], while_edit=1)
        m_send(update, context, options_almost, menu)
    elif users[update.message.chat_id].deep == 14 and update.message.text == button_opt[1]:
        new_ev_obj = Event(args_4_create['name'], args_4_create['address'],
                           args_4_create['date'], args_4_create['description'], update.message.chat_id)
        evs[args_4_create['name']] = new_ev_obj
        users[update.message.chat_id].deep = 0
        m_send(update, context, options_succ, menu)


# Functions for change existing events in bot
def to_to_edit_e_f(update, context):
    global users
    users[update.message.chat_id] = Arg(0, 0, '', [])
    users[update.message.chat_id].change = 1
    step_1(update, context)

def edit_e_f(update, context):
    global users, args_4_create, evs
    menu = make_menu(update.message.chat_id, buttons=[button_opt_edit[0]], while_edit=1)
    if users[update.message.chat_id].change == 1:
        users[update.message.chat_id].deep = 20
        users[update.message.chat_id].change = 0
        users[update.message.chat_id].previous = update.message.text
        if evs[update.message.text].host_id == update.message.chat_id:
            text = options_str[1]+old_option+users[update.message.chat_id].previous
            m_send(update, context, text, menu)
        else:
            context.bot.send_message(update.message.chat_id, fail_right_4_edit_e)
            users[update.message.chat_id] = Arg(0, 0, '', [])
    elif users[update.message.chat_id].deep == 20:
        if update.message.text != button_opt_edit[0]:
            args_4_create['name'] = update.message.text
        else:
            args_4_create['name'] = users[update.message.chat_id].previous
        obj_ev = evs.pop(users[update.message.chat_id].previous)
        obj_ev.name = args_4_create['name']
        evs[args_4_create['name']] = obj_ev
        curr_index = Event.evs_names.index(users[update.message.chat_id].previous)
        del Event.evs_names[curr_index]
        Event.evs_names.insert(curr_index, args_4_create['name'])
        users[update.message.chat_id].deep = 21
        text = options_str[2] + old_option + evs[args_4_create['name']].address
        print(evs)
        m_send(update, context, text, menu)
    elif users[update.message.chat_id].deep == 21:
        if update.message.text != button_opt_edit[0]:
            args_4_create['address'] = update.message.text
        else:
            args_4_create['address'] = evs[args_4_create['name']].address
        users[update.message.chat_id].deep = 22
        text = options_str[3]+old_option+str(evs[args_4_create['name']].date)
        m_send(update, context, text, menu)
    elif users[update.message.chat_id].deep == 22:
        if update.message.text != button_opt_edit[0]:
            t = update.message.text.split(',')
            try:
                if len(t) == 4:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]), int(t[3]))
                else:
                    args_4_create['date'] = make_date(int(t[0]), int(t[1]), int(t[2]))
            except (IndexError, ValueError):
                m_send(update, context, options_fail)
            else:
                users[update.message.chat_id].deep = 23
                text = options_str[4] + old_option + evs[args_4_create['name']].description
                m_send(update, context, text, menu)
        else:
            args_4_create['date'] = evs[args_4_create['name']].date
            users[update.message.chat_id].deep = 23
            text = options_str[4] + old_option + evs[args_4_create['name']].description
            m_send(update, context, text, menu)
    elif users[update.message.chat_id].deep == 23:
        if update.message.text != button_opt_edit[0]:
            args_4_create['description'] = update.message.text
        else:
            args_4_create['description'] = evs[args_4_create['name']].description
        users[update.message.chat_id].deep = 24
        menu = make_menu(update.message.chat_id, buttons=[button_opt_edit[1]], while_edit=1)
        m_send(update, context, options_almost, menu)
    elif users[update.message.chat_id].deep == 24 and update.message.text == button_opt_edit[1]:
        evs[args_4_create['name']].address = args_4_create['address']
        if evs[args_4_create['name']].date != args_4_create['date']:
            evs[args_4_create['name']].date = args_4_create['date']
            evs[args_4_create['name']].correct_order_ev()
        evs[args_4_create['name']].description = args_4_create['description']
        users[update.message.chat_id] = Arg(0, 0, '', [])
        menu = make_menu(update.message.chat_id, while_edit=1)
        m_send(update, context, options_edit_succ, menu)


# Functions for delete events in bot
def destroy_e_f(update, context):
    global users
    users[update.message.chat_id].change = -1
    step_1(update, context)

def succ_destroy_e_f(update, context):
    global users, evs
    users[update.message.chat_id].change = 0
    evs.pop(update.message.text)
    Event.evs_names.remove(update.message.text)
    menu = make_menu(update.message.chat_id, while_edit=1)
    m_send(update, context, destroy_succ, menu)

def see_my_host(update, context):
    global users, evs
    text = ''
    for i in evs:
        if update.message.chat_id == evs[i].host_id:
            print(evs[i].nicknames)
            text += "На ваше мероприятие`" + i + "`записались:\n" + '\n@'.join(evs[i].nicknames) + '\n'
    m_send(update, context, text)


# Filters for handlers
class F_step1(BaseFilter):
    def filter(self, message):
        return main in message.text

class F_step_e(BaseFilter):
    def filter(self, message):
        for j in (main, see_my_e, show_org, button_opt[0]):
            if j in message.text:
                return False
        for i in (password, pass_determine, pass_edit):
            if i in message.text.lower():
                return False
        if re.match(begin, message.text.lower()):
            return False
        return True

class F_see_my_e(BaseFilter):
    def filter(self, message):
        return see_my_e in message.text

class F_to_create_e(BaseFilter):
    def filter(self, message):
        return button_opt[0] in message.text

class F_to_to_create_e(BaseFilter):
    def filter(self, message):
        print(password in message.text.lower())
        return password in message.text.lower()

class F_to_destroy_e(BaseFilter):
    def filter(self, message):
        print(pass_determine in message.text.lower())
        return pass_determine in message.text.lower()

class F_to_to_edit_e(BaseFilter):
    def filter(self, message):
        print(pass_edit in message.text.lower())
        return pass_edit in message.text.lower()

class F_to_see_my_host(BaseFilter):
    def filter(self, message):
        return show_org in message.text

class F_re_for_start(BaseFilter):
    def filter(self, message):
        return re.match(begin, message.text.lower()) or message.text == to_begin

class F_re_for_welcom(BaseFilter):
    def filter(self, message):
        return re.match(welcom_re, message.text.lower())

ff_re_for_start = F_re_for_start()
ff_re_for_welcom = F_re_for_welcom()

ff_step1 = F_step1()
ff_step_e = F_step_e()
ff_see_my_e = F_see_my_e()
ff_to_to_edit_e = F_to_to_edit_e()


ff_to_create_e = F_to_create_e()
ff_to_to_create_e = F_to_to_create_e()
ff_to_destroy_e = F_to_destroy_e()

ff_to_see_my_host = F_to_see_my_host()



st_handler = CommandHandler('start', start)
re_for_start_handler = MessageHandler(ff_re_for_start, start)
#st_handler2 = MessageHandler(Filters.regex(begin), start)

to_e_handler = MessageHandler(ff_step1, step_1)
in_e_handler = MessageHandler(ff_step_e, step_work_with_e)
see_my_e_handler = MessageHandler(ff_see_my_e, see_my_e_f)

begin_create_e_handler = MessageHandler(ff_to_to_create_e, begin_create_e_f)
to_create_e_handler = MessageHandler(ff_to_create_e, to_create_e_f)
to_destroy_e_handler = MessageHandler(ff_to_destroy_e, destroy_e_f)
to_to_edit_e_handler = MessageHandler(ff_to_to_edit_e, to_to_edit_e_f)

to_see_my_host_handler = MessageHandler(ff_to_see_my_host, see_my_host)

welc_handler = MessageHandler(ff_re_for_welcom, welc_ans)
how_a_u_handler = MessageHandler(Filters.regex(a_che_tam), how_a_u)
wrong_handler = MessageHandler(Filters.command, wrong_ans)


for i in (
        st_handler, re_for_start_handler, wrong_handler, welc_handler, how_a_u_handler,
        to_e_handler, in_e_handler, see_my_e_handler,
        begin_create_e_handler, to_create_e_handler, to_destroy_e_handler,
        to_see_my_host_handler, to_to_edit_e_handler
    ):
    dispatcher.add_handler(i)

updater.start_polling()


"""


class Some():
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)

        return cls.instance



def format_event_repr(update, event):
    date_of_e = event.date
    text = f'{users[update.message.chat_id].previous}\n' \
       f'{int(date_of_e.strftime("%d"))} {months[int(date_of_e.strftime("%m"))]}, ' \
       f'{daysweek[date_of_e.strftime("%A")]}, в {date_of_e.strftime("%H:%M")}\nпо адресу: ' \
       f'{event.address}\n\n{event.description}'
    return text

date_of_e = evs[update.message.text].date
text = f'{users[update.message.chat_id].previous}\n' \
       f'{int(date_of_e.strftime("%d"))} {months[int(date_of_e.strftime("%m"))]}, ' \
       f'{daysweek[date_of_e.strftime("%A")]}, в {date_of_e.strftime("%H:%M")}\nпо адресу: ' \
       f'{evs[update.message.text].address}\n\n' \
       f'{evs[update.message.text].description}'

date_of_e = evs[users[update.message.chat_id].previous].date
text = f'{users[update.message.chat_id].previous}\n' \
       f'{int(date_of_e.strftime("%d"))} {months[int(date_of_e.strftime("%m"))]}, ' \
       f'{daysweek[date_of_e.strftime("%A")]}, в {date_of_e.strftime("%H:%M")}\nпо адресу: ' \
       f'{evs[users[update.message.chat_id].previous].address}\n\n' \
       f'{evs[users[update.message.chat_id].previous].description}'

date_of_e = evs[Event.evs_names[numb-1]].date
text = f'{users[update.message.chat_id].previous}\n' \
       f'{int(date_of_e.strftime("%d"))} {months[int(date_of_e.strftime("%m"))]}, ' \
       f'{daysweek[date_of_e.strftime("%A")]}, в {date_of_e.strftime("%H:%M")}\nпо адресу: ' \
       f'{evs[Event.evs_names[numb-1]].address}\n\n' \
       f'{evs[Event.evs_names[numb-1]].description}'


"""