# Default functions for repr
def format_event_repr_f(event, ev_prev, curr_lang):
    date_of_e = event.date
    text = f'{ev_prev}\n' \
       f'{int(date_of_e.strftime("%d"))} {curr_lang["months"][int(date_of_e.strftime("%m"))]}, ' \
       f'{curr_lang["daysweek"][date_of_e.strftime("%A")]}, ' \
	   f'at {date_of_e.strftime("%H:%M")}\nis located at: ' \
       f'{event.address}\n\n{event.description}'
    return text

def step_conf_txt_f(user_name, event_name):
	return f"User {user_name} has registered for your event '{event_name}'"
	
def step_canc_txt_f(user_name, event_name):
	return f"User {user_name} has canceled his registration for your event '{event_name}'"
		
def see_my_e_f_txt_f(number, event_name, address):
	return f"{number+1}. {event_name} is located at {address}\n"

def see_my_host_txt_f(event_name, nicknames, add = ''):
	return "On your event '" + event_name + \
			"' registered:\n" + ('\n'+add).join(nicknames) + '\n'
	
	
options = ('For adding event - fill in step by step:\n'
'📌Short describe event. It will be on the button\n'
'📌Address of event\n'
'📌Data of event (mm,dd,hh) For example - 5, 25, 18\n'
'📌Full describe event\n')

all_texts = dict(
# Default buttons
step_conf_txt=step_conf_txt_f,
step_canc_txt=step_canc_txt_f,
see_my_e_f_txt=see_my_e_f_txt_f,
see_my_host_txt=see_my_host_txt_f,
format_event_repr = format_event_repr_f,
to_begin='⬅ Back to begin',
cancel = 'Cancel registration',
see_my_e = 'My registrations',
main = 'Upcoming events',
agree = "Go to this events",
button_opt = ['Create event', 'Add event'],
button_opt_edit = ['All right - continue', 'Finish editing'],
show_org = 'My visitors',
show_all = 'All visitors',

# Default messages from bot
hi_from_bot = ("Welcome! Let’s get to know upcoming events.\n"
               "Sign up! - You always can see your registrations🙂"
               "But if your plans changed - cancel it.\n"
               "📌Look to icons near smile. "
               "Click - menu or list of commands will open."),

choice_e = 'Choose event: write a number or click a button.\n',
confirm = 'You registered on: ',

wrong = ("😔I can’t understand you. Try again please\n"
         "📌Open the icon near smile for navigation.\n📌Write “Hi” for starting conversation again"),
cancel_all = "You canceled",

options = options,

mes_see = ('You can see you registrations💬.\n'
           'For cancel - click event or write number. There will be button “cancel”\nYou registered on:\n'),

choose_edit_e = 'Choose event for editing:\n',
old_option = '\nOld option:\n',
options_edit_succ = 'The event successful edited!',
fail_right_4_edit_e = "You can't edit this event, because it's not your event.",

options_str = options.split('\n'),
options_fail = 'Wrong data',
options_almost = 'Confirm adding',
options_succ = 'The event successful added!',

destroy_succ = 'The event successful deleted!',

mes_a_che_tam = "I'm fine.\nDo you want to go somewhere??",
welc = 'Welcome)\nMy pleasure😄',


#for VK
#options_str[1] = options_str[1] + ' - UP TO 40 SYMBOLS\n'


# Regular Expressions
ok = r'(register)|(go)|(yep)|(yes)|(ok[ay]*)',
nearest = r'(near[est]*)|(tomorrow)',
begin = r'(menu)|(start[s]*)|(hi)|(hey)|(hello)|(gr[ee]+tings)',
a_che_tam = r'(how ?[are]* [yo]*u\??)',
welcom_re = r'(thanks?)|(thank [yo]*u)|(cool)|(thx)',


# Args for nice view of representation date
months = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
          7: 'july', 8: 'august', 9: 'september', 10: 'october',  11: 'november', 12: 'december'},
daysweek = {'Monday': 'monday', 'Tuesday': 'tuesday', 'Wednesday': 'wednesday',
'Thursday': 'thursday','Friday': 'friday', 'Saturday': 'saturday', 'Sunday': 'sunday'})



