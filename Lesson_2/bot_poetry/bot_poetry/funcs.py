from classes import AddressBook, Record
import pickle
import os
from ordered_folders import sorting_dir_files
from notebook import call_notebook
from textmatch import fuzzy_match


def creation_adressbook():
	global CONTACTS
	if os.path.exists('AdressBook.pickle'):
		with open('AdressBook.pickle', 'rb') as f:
			CONTACTS = pickle.load(f)
	else:
		CONTACTS = AddressBook()


def input_error(handler):
	def wrapper(*args, **kargs):
		try:
			return handler(*args, **kargs)
		except KeyError:
			return 'Mistyping. Try again!'
		except ValueError:
			return 'Mistyping. Try again!'
		except IndexError:
			return 'Mistyping. Try again!'
		except TypeError:
			return 'Mistyping. Try again!'
		except OSError:
			return 'Paste link in correct format e.g.: C:\\foo\\bar without "quotes"'
	return wrapper


@input_error
def quit_func():
	if CONTACTS:
		with open('AdressBook.pickle', 'wb') as f:
			pickle.dump(CONTACTS, f)
	return 'Good bye!'


@input_error
def create_contact_func():
	name = input("Text Name: ")
	if name in CONTACTS:
		return f'{name} - this contact already axist in the AdressBook'
	phone = input("Text phone / ('enter' to skip): ")
	birthday = input("Text birthday / ('enter' to skip): ")
	address = input("Text address / ('enter' to skip): ")
	email = input("Text email / ('enter' to skip): ")
	record =  Record(name)
	if phone:
		record.add_phone(phone)
	if birthday:
		record.add_birthday(birthday)
	if address:
		record.add_address(address)
	if email:
		record.add_email(email)
	CONTACTS.add_record(record)
	return repr(record)


@input_error
def show_all_func():
	if CONTACTS:
		contact_book = []
		for record in CONTACTS.values():
			contact_book.append([repr(record)])
		return contact_book
	else:
		return "The AdressBook is empty!"


@input_error
def add_phone_func(name, phone):
	CONTACTS[name].add_phone(phone)


@input_error
def add_birthday_func(name, record, birthday):
		record.add_birthday(birthday)
		CONTACTS[name] = record
		return f"Birthday: {birthday} added for the {name}"

@input_error
def add_address_func(name, record, address):
		record.add_address(address)
		CONTACTS[name] = record
		return f"Address: {address} added for the {name}"

@input_error
def add_email_func(name, record, email):
		record.add_email(email)
		CONTACTS[name] = record
		return f"Email: {email} added for the {name}"


@input_error
def edit_phone(name, record ,phone_old, phone_new):
	for phone in record.phones:
		if phone_old == phone.value:
			record.edit_phone(phone_old, phone_new)
			CONTACTS[name] = record
			return f"{phone_old} --> {phone_new}: Changed!"

	return f'{phone_old} was not found in the {name} contact'


@input_error
def edit_birthday(name, record, birthday_new):
	record.edit_birthday(name, birthday_new)
	CONTACTS[name] = record
	return f"{name}: new date --> {birthday_new}: birthday Changed!"


@input_error
def edit_address(name, record, address_new):
	record.edit_birthday(name, address_new)
	CONTACTS[name] = record
	return f"{name}: new address --> {address_new}: Changed!"


@input_error
def edit_email(name, record, email_new):
	record.edit_email(name, email_new)
	CONTACTS[name] = record
	return f"{name}: new email --> {email_new}: Changed!"


@input_error
def remove_phone(name, record, phone_to_delete):
	phone_to_delete = phone_to_delete.strip()
	for phone in record.phones:
		if phone_to_delete == phone.value:
			record.remove_phone(phone.value)
			CONTACTS[name] = record
			return f"{phone_to_delete}: Deleted!"
	return f'{phone_to_delete} was not found in the {name} contact'


@input_error
def remove_birthday(name, record):
	record.remove_birthday(name)
	return f"{name}: birthday Deleted!"


@input_error
def remove_address(name, record):
	record.remove_address(name)
	return f"{name}: address Deleted!"


@input_error
def remove_email(name, record):
	record.remove_email(name)
	return f"{name}: email Deleted!"


@input_error
def search_contacts_func():
	data = input('Please type any "text" and I will find all relevant Contacts with this text: ')
	return CONTACTS.search_contacts(data.strip())


@input_error
def birthday_exact_date():
	days = int(input('Input the number of days from today and I will show you the list of contacts with the Birthday through this number of days: '))
	birthday_list = []
	for record in CONTACTS.values():
		if record.birthday:
			if record.days_birthday() == days:
				birthday_list.append([record])
	if birthday_list:
		return birthday_list
	else:
		return f'No any birthdays through {days} days'


@input_error
def remove_contact_func():
	name = input('Please type the "Name" of the contact which should be removed: ')
	if name in CONTACTS:
		CONTACTS.pop(name)
		return f'{name} contact was removed from AddressBook'
	else:
		return f'The contact with the name "{name}" is not in the AdressBook yet'


@input_error
def edit_contact_func():
	name = input('Please type the "Name" of the contact which should be edited: ')
	if name in CONTACTS:
		command = input('Type the command from this list:\nadd/edit/remove phone\n\
add/edit/remove birthday\nadd/edit/remove email\nadd/edit/remove address: \n')
		if command == 'add phone':
			new_phone = input(f"Type the additional phone for | {name} |: ")
			add_phone_func(name, new_phone)
			return f"{name} has a list of phones {CONTACTS[name].phones}!"
		if command == 'edit phone':
			old_phone = input(f"Type the old phone for | {name} |: ")
			new_phone = input(f"Type the new phone for | {name} |: ")
			return edit_phone(name, CONTACTS[name], old_phone, new_phone)
		if command == 'remove phone':
			phone_to_delete = input(f"Type the phone for | {name} | which require to be removed: ")
			return remove_phone(name, CONTACTS[name], phone_to_delete)

		if command == 'add birthday':
			if CONTACTS[name].birthday:
				return f'For contact: {name} the Birthday already exist: {CONTACTS[name].birthday.value}'
			birthday = input(f"Type the Birthday for | {name} |: ")
			return add_birthday_func(name, CONTACTS[name], birthday)
		if command == 'edit birthday':
			birthday_new = input(f"Type to change Birthday for | {name} |: ")
			return edit_birthday(name, CONTACTS[name], birthday_new)
		if command == 'remove birthday':
			return remove_birthday(name, CONTACTS[name])

		if command == 'add address':
			if CONTACTS[name].address:
				return f'For contact: {name} the Address already exist: {CONTACTS[name].address.value}'
			address = input(f"Type the Address for | {name} |: ")
			return add_address_func(name, CONTACTS[name], address)
		if command == 'edit address':
			address_new = input(f"Type new address to change Address for | {name} |: ")
			return edit_address(name, CONTACTS[name], address_new)
		if command == 'remove address':
			return remove_address(name, CONTACTS[name])

		if command == 'add email':
			if CONTACTS[name].email:
				return f'For contact: {name} the Email already exist: {CONTACTS[name].email.value}'
			email = input(f"Type the Email for | {name} |: ")
			return add_email_func(name, CONTACTS[name], email)
		if command == 'edit email':
			email_new = input(f"Type new email to change the Email for | {name} |: ")
			return edit_email(name, CONTACTS[name], email_new)
		if command == 'remove email':
			return remove_email(name, CONTACTS[name])


@input_error
def sort_dir_func():
	path = input('Please paste the "path" to the folder to sort it: ')
	sorting_dir_files(path)
	return '\nFolder ordered'


def change_input(user_input):
	new_input = user_input
	data = ''
	for key in COMMANDS:
		if user_input.lower().startswith(key):
			new_input = key
			data = user_input[len(new_input):]
			break
	if data:
		return reaction_func(new_input)(data)
	return reaction_func(new_input)()


def reaction_func(reaction):
	return COMMANDS.get(reaction, break_func)


def break_func():
	return 'Wrong enter.'


def create_data(data):
	new_data = data.split()
	name = new_data[0]
	phones = []
	birthday = ''
	for value in new_data[1:]:
		if value.isnumeric():
			phones.append(value)
		else:
			birthday += value
	return name, phones, birthday


def check_input_data(user_input):
	if user_input in COMMANDS:
		return change_input(user_input)
	else:
		return fuzzy_match(user_input, COMMANDS.keys())



COMMANDS = {
'create contact' : create_contact_func,
'edit contact' : edit_contact_func,
'remove contact' : remove_contact_func,
'show all': show_all_func,
'find contact': search_contacts_func,
'birthday' : birthday_exact_date,
'sort by path' : sort_dir_func,
'call notebook' : call_notebook,
'exit': quit_func,
}

@input_error
def choose_command():
	while True:
		user_input = input(f'Enter command from list: {[key for key in COMMANDS.keys()]}: ')
		result = check_input_data(user_input)
		print(result)
		if result == 'Good bye!':
			break