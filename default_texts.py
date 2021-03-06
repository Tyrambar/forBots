# Default functions for repr
def format_event_repr_f(event, ev_prev, curr_lang):
    date_of_e = event.date
    text = f'{ev_prev}\n' \
       f'{int(date_of_e.strftime("%d"))} {curr_lang["months"][int(date_of_e.strftime("%m"))]}, ' \
       f'{curr_lang["daysweek"][date_of_e.strftime("%A")]}, ' \
	   f'в {date_of_e.strftime("%H:%M")}\nпо адресу: ' \
       f'{event.address}\n\n{event.description}'
    return text

def step_conf_txt_f(user_name, event_name):
	return f"Пользователь {user_name} записался на Ваше мероприятие '{event_name}'"
	
def step_canc_txt_f(user_name, event_name):
	return f"Пользователь {user_name} отменил запись на Ваше мероприятие '{event_name}'"

def see_my_e_f_txt_f(number, event_name, address):
	return f"{number+1}. {event_name} по адресу {address}\n"

def see_my_host_txt_f(event_name, nicknames, add = ''):
	return "На ваше мероприятие '" + event_name + \
			"' записались:\n" + ('\n'+add).join(nicknames) + '\n'

options = 'Чтобы добавить мероприятие, вам нужно заполнить поэтапно :\n' \
          '📌Краткое описание мероприятия, которое будет отображаться на кнопке\n' \
          '📌Адрес места проведения мероприятия. Пример: Маросейка 13с1\n' \
          '📌Дата проведения (месяц, дата, час - разделение через запятую). Пример: 5, 25, 18\n' \
          '📌Описание места проведения\n'

pass_add = 'создать'
pass_destroy = 'удалить'
pass_edit = 'правка'
passwords = (pass_add, pass_destroy, pass_edit)

months = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
          7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября',  11: 'ноября', 12: 'декабря'},
daysweek = {'Monday': 'понедельник', 'Tuesday': 'вторник', 'Wednesday': 'среда',
'Thursday': 'четверг','Friday': 'пятница', 'Saturday': 'суббота', 'Sunday': 'воскресенье'},

all_texts = dict(

# Default buttons
step_conf_txt = step_conf_txt_f,
step_canc_txt = step_canc_txt_f,
see_my_e_f_txt = see_my_e_f_txt_f,
see_my_host_txt = see_my_host_txt_f,
format_event_repr = format_event_repr_f,
to_begin = '⬅ Вернуться в начало',
cancel = 'Отменить запись',
see_my_e = 'Мои записи',
main = 'Ближайшие мероприятия',
agree = 'Пойду на это мероприятие',
button_opt = ['Создать мероприятие', 'Добавить мероприятие'],
button_opt_edit = ['Все правильно - дальше', 'Завершить редактирование'],
show_org = 'Мои посетители',
show_all = 'чо по чем?',


# Default messages from bot
hi_from_bot = ("Добро пожаловать! Ознакомьтесь с ближайшими мероприятиями.\n"
"Записывайтесь - Вы всегда можете посмотреть имеющиеся записи🙂."
"А если планы изменились, отменить их.\n"
"📌Обратите внимание на значки в поле сообщений, рядом со смайлом. "
"Нажмите - откроется меню или список команд."),
choice_e = 'Выберите мероприятие: напишите порядковый номер или нажмите на кнопку:\n',
confirm = 'Вы записались на ',
wrong = ('😔 Я не могу вас понять\nВы можете попробовать снова:\n'
'📌 Откройте рядом со смайликами квадратную иконку для удобной навигации\n📌 Напишите Привет, чтобы начать разговор заново'),
cancel_all = 'Ваша запись отменена.',
mes_see = 'Можете снова просмотреть те мероприятия💬, куда вы записались.\n' \
          'Чтобы отменить запись, нажмите на него или напиши номер ' \
          'там будет кнопка "отменить запись"\nРанее Вы записались на:\n',

options = options,

choose_edit_e = 'Выберете мероприятия, данные которого хотели бы изменить:\n',
old_option = '\nСтарое значение:\n',
options_edit_succ = 'Мероприятие успешно изменено!',
fail_right_4_edit_e = 'Вы не являетесь создателем этого мероприятия, поэтому Вы не можете его изменить',

options_str = options.split('\n'),
options_fail = 'Неправильно записаны данные',
options_almost = 'Подтвердите добавление мероприятия',
options_succ = 'Мероприятие успешно добавлено!',

destroy_succ = 'Мероприятие успешно испепелено!!!',

mes_a_che_tam = 'Нормас\nна движ-то какой-нибудь пойдешь?',
welc = 'Пожалуйста)\nЭто моя работа😄',

# Regular Expressions
ok = r'(записаться)|(х[очуатю]{3})|(д[ао]вай)|(п[ао]й[дуеёмти])|' \
	r'(п[ао]?шли)|(да+)|((го)+у*)|(ид[ёемду])|(к[ао]не[чш]н[ао]*)|(ок[ейи]*)',
nearest = r'(близ?жайш[ие]е!*)|([после]*завтр[ао])|([в ]*выходн[ыеой]*)',
begin = r'(меню)|(старт[уй]*)|(прив[етствую]*)|(добр[огоыйе]+( )?[утроадняденьвечера]*)|' \
        r'([вс]* ?нач[ниалоать]*)|(з?д[ао]+р[аоваствуйте]+)|(хай)|(hi)|(hello)|(ку)',
a_che_tam = r'([а ]*ч[еёо]{1} там\??)|(как [тыдела]\??)',
welcom_re = r'(с?пас[ие]б[ао]*)|(благодарю?[ствую]*[им]*)|(но?рм[ас]*)|(к ?р ?а ?с ?[иа]? ?в ?[ао]?[чик]*)',

# Args for nice view of representation date
months = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
          7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября',  11: 'ноября', 12: 'декабря'},
daysweek = {'Monday': 'понедельник', 'Tuesday': 'вторник', 'Wednesday': 'среда',
'Thursday': 'четверг','Friday': 'пятница', 'Saturday': 'суббота', 'Sunday': 'воскресенье'},

pass_add = pass_add,
pass_destroy = pass_destroy,
pass_edit = pass_edit,
passwords = passwords,)


#for VK
#options_str[1] = options_str[1] + ' - ДО 40 СИМВОЛОВ\n'








