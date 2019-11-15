# Default buttons
to_begin = '⬅ Вернуться в начало'
cancel = 'Отменить запись'
see_my_e = 'Мои записи'
main = 'Ближайшие мероприятия'
agree = 'Пойду на это мероприятие'
button_opt = ['Создать мероприятие', 'Добавить мероприятие']
button_opt_edit = ['Все правильно - дальше', 'Завершить редактирование']
show_org = 'Мои посетители'
show_all = 'чо по чем?'


# Default messages from bot
hi_from_bot = ("Добро пожаловать! Ознакомьтесь с ближайшими мероприятиями.\n"
"Записывайтесь - Вы всегда можете посмотреть имеющиеся записи🙂."
"А если планы изменились, отменить их.\n"
"📌Обратите внимание на значок в поле сообщений, рядом со смайлом. "
"Нажмите - откроется меню.\nКлючевые слова: создать, правка, удалить")
choice_e = 'Выберите мероприятие: напишите порядковый номер или нажмите на кнопку:\n'
confirm = 'Вы записались на '
wrong = ('😔 Я не могу вас понять\nВы можете попробовать снова:\n'
'📌 Откройте рядом со смайликами квадратную иконку для удобной навигации\n📌 Напишите Привет, чтобы начать разговор заново')
cancel_all = 'Ваша запись отменена.'
mes_see = 'Можете снова просмотреть те мероприятия💬, куда вы записались.\n' \
          'Чтобы отменить запись, нажмите на него или напиши номер ' \
          'там будет кнопка "отменить запись"\nРанее Вы записались на:\n'

options = 'Чтобы добавить мероприятие, вам нужно заполнить поэтапно :\n' \
          '📌Краткое описание мероприятия, которое будет отображаться на кнопке\n' \
          '📌Адрес места проведения мероприятия. Пример: Маросейка 13с1\n' \
          '📌Дата проведения (месяц, дата, час - разделение через запятую). Пример: 5, 25, 18\n' \
          '📌Описание места проведения\n'

choose_edit_e = 'Выберете мероприятия, данные которого хотели бы изменить:\n'
old_option = '\nСтарое значение:\n'
options_edit_succ = 'Мероприятие успешно изменено!'
fail_right_4_edit_e = 'Вы не являетесь создателем этого мероприятия, поэтому Вы не можете его изменить'

options_str = options.split('\n')
options_fail = 'Неправильно записаны данные'
options_almost = 'Подтвердите добавление мероприятия'
options_succ = 'Мероприятие успешно добавлено!'

destroy_succ = 'Мероприятие успешно испепелено!!!'

mes_a_che_tam = 'Нормас\nна движ-то какой-нибудь пойдешь?'
welc = 'Пожалуйста)\nЭто моя работа😄'


# Regular Expressions
ok = r'(записаться)|(х[очуатю]{3})|(д[ао]вай)|(п[ао]й[дуеёмти])|(п[ао]?шли)|(да+)|((го)+у*)|(ид[ёемду])|(к[ао]не[чш]н[ао]*)|(ок[ейи]*)'
nearest = r'(близ?жайш[ие]е!*)|([после]*завтр[ао])|([в ]*выходн[ыеой]*)'
begin = r'(меню)|(старт[уй]*)|(прив[етствую]*)|(добр[огоыйе]+( )?[утроадняденьвечера]*)|' \
        r'([вс]* ?нач[ниалоать]*)|(з?д[ао]+р[аоваствуйте]+)|(хай)|(hi)|(hello)|(ку)'
a_che_tam = r'([а ]*ч[еёо]{1} там\??)|(как [тыдела]\??)'
welcom_re = r'(с?пас[ие]б[ао]*)|(благодарю?[ствую]*[им]*)|(но?рм[ас]*)|(к ?р ?а ?с ?[иа]? ?в ?[ао]?[чик]*)'


# Args for nice view of representation date
months = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
          7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября',  11: 'ноября', 12: 'декабря'}
daysweek = {'Monday': 'понедельник', 'Tuesday': 'вторник', 'Wednesday': 'среда',
'Thursday': 'четверг','Friday': 'пятница', 'Saturday': 'суббота', 'Sunday': 'воскресенье'}


pass_create = 'создать'
pass_determine = 'удалить'
pass_edit = 'правка'

passwords = (pass_create, pass_determine, pass_edit)
