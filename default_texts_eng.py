# Default buttons
to_begin = '⬅ Back to begin'
cancel = 'Отменить запись'
see_my_e = 'My registrations'
main = 'Upcoming events'
agree = "Go to this events"
button_opt = ['Create event', 'Add event']
button_opt_edit = ['All right - continue', 'Finish editing']
show_org = 'My visitors'
show_all = 'All visitors'


# Default messages from bot

hi_from_bot = ("Welcome! Let’s get to know uncoming events.\n"
"Sign up! - You always can see your registrations🙂"
"But if your plans changed - cancel it.\n"
"📌Look to icon near smile."
"Click - menu will open.\nKey words: create, edit, delete")

choice_e = 'Choose event: write a number or click a button.\n'
confirm = 'You registered on: '

wrong = ("😔I can’t understand you. Try again please\n"
"📌Open the icon near smile for navigation.\n📌Write “Hello” for starting conversation again"
cancel_all = "You canceled"

options = ('For adding event - fill in step by step:\n'
         '📌Short describe event. It will be on the button\n'
         '📌Address of event\n'
         '📌Data of event (mm,dd,hh) For example - 5, 25, 18\n'
         '📌Full describe event\n')

		 
mes_see = ('You can see you registrations💬.\n'
'For cancel - click event or write number. There will be button “cancel”\nYou registered on:\n')

choose_edit_e = 'Choose event for editing:\n'
old_option = '\nOld option:\n'
options_edit_succ = 'The event successful edited!'
fail_right_4_edit_e = 'The event successful edited.'

options_str = options.split('\n')
options_fail = 'Wrong data'
options_almost = 'Confirm adding'
options_succ = 'The event successful added!'

destroy_succ = 'The event successful deleted!'

mes_a_che_tam = "I'm fine.\nDo you want to go somewhere??"
welc = 'Welcome)\nMy pleasure😄'


# Regular Expressions
ok = r'(register)|(х[очуатю]{3})|(go)|(п[ао]й[дуеёмти])|(п[ао]?шли)|(да+)|((го)+у*)|(ид[ёемду])|(к[ао]не[чш]н[ао]*)|(ok[ay]*)'
nearest = r'(близ?жайш[ие]е!*)|([после]*завтр[ао])|([в ]*выходн[ыеой]*)'
begin = r'(menu)|(start[s]*)|(прив[етствую]*)|(добр[огоыйе]+( )?[утроадняденьвечера]*)|' \
        r'([вс]* ?нач[ниалоать]*)|(з?д[ао]+р[аоваствуйте]+)|(хай)|(hi)|(hello)|(ку)'
a_che_tam = r'([а ]*ч[еёо]{1} там\??)|(how[ are]* [yo]*u\??)'
welcom_re = r'(thanks?)|(thank [yo]*u)|(cool)|(к ?р ?а ?с ?[иа]? ?в ?[ао]?[чик]*)'


# Args for nice view of representation date
months = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
          7: 'july', 8: 'august', 9: 'september', 10: 'october',  11: 'november', 12: 'december'}
daysweek = {'Monday': 'monday', 'Tuesday': 'tuesday', 'Wednesday': 'wednesday',
'Thursday': 'thursday','Friday': 'friday', 'Saturday': 'saturday', 'Sunday': 'sunday'}


pass_create = 'create'
pass_determine = 'delete'
pass_edit = 'edit'

passwords = (pass_create, pass_determine, pass_edit)
