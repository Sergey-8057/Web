from abc import abstractmethod, ABC
from collections import UserDict
from dateutil import parser
from datetime import date
import re

class Field:

	def __init__(self):
		self._value = None

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		self._value = value.strip()

	def __str__(self):
		return f"{self.value}"

	def __repr__(self):
		return f"{self}"

class Name(Field):

	def __init__(self, name):
		self.value = name.strip().title()

class Phone(Field):

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, phone):
		phone = phone.strip()
		if len(phone) >= 10:
			self._value = phone
		else:
			print ('This phone format is unacceptable!')

class Birthday(Field):

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, birthday):
		birthday = birthday.strip()
		birthday = re.sub('[ ,:]', '-', birthday)
		try:
			self._value = parser.parse(birthday).date()
		except:
			print ('Check the date, please. Month must be in 1..12, Date 1...31')

class Email(Field):

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, email):
		email = email.strip()
		regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
		if re.fullmatch(regex, email):
			self._value = email
		else:
			print ('This email format is unacceptable!')


class Address(Field):
	pass


class BaseRecord(ABC):
	@abstractmethod
	def add_phone(self):
		pass

	@abstractmethod
	def add_birthday(self):
		pass

	@abstractmethod
	def add_email(self):
		pass

	@abstractmethod
	def add_address(self):
		pass

	@abstractmethod
	def remove_phone(self):
		pass

	@abstractmethod
	def edit_phone(self):
		pass

	@abstractmethod
	def remove_birthday(self):
		pass

	@abstractmethod
	def remove_address(self):
		pass

	@abstractmethod
	def remove_email(self):
		pass

	@abstractmethod
	def edit_birthday(self):
		pass

	@abstractmethod
	def edit_address(self):
		pass

	@abstractmethod
	def edit_email(self):
		pass

	@abstractmethod
	def days_birthday(self):
		pass


class Record(BaseRecord):
	def __init__(self, name):
		self.name = Name(name)
		self.phones = []
		self.birthday = None
		self.email = None
		self.address = None


	def add_phone(self, data):
		phone = Phone()
		phone.value = data
		if phone.value:
			self.phones.append(phone)

	def add_birthday(self, data):
		birthday = Birthday()
		birthday.value = data
		self.birthday = birthday

	def add_email(self, data):
		email = Email()
		email.value = data
		self.email = email

	def add_address(self, data):
		address = Address()
		address.value = data
		self.address = address

	def remove_phone(self, phone_to_remove):
		for phone in self.phones:
			if phone.value == phone_to_remove:
				self.phones.remove(phone)

	def edit_phone(self, phone_old, phone_new):
		for phone in range(len(self.phones)):
			if self.phones[phone].value == phone_old:
				edited_phone = Phone()
				edited_phone.value = phone_new
				self.phones[phone] = edited_phone


	def remove_birthday(self, name):
		if self.name.value == name:
			self.birthday = None

	def remove_address(self, name):
		if self.name.value == name:
			self.address = None

	def remove_email(self, name):
		if self.name.value == name:
			self.email = None

	def edit_birthday(self, name, birthday_new):
		if self.name.value == name:
			edited_birthday = Birthday()
			edited_birthday.value = birthday_new
			self.birthday = edited_birthday

	def edit_address(self, name, address_new):
		if self.name.value == name:
			edited_address = Address()
			edited_address.value = address_new
			self.address = edited_address

	def edit_email(self, name, email_new):
		if self.name.value == name:
			edited_email = Email()
			edited_email.value = email_new
			self.email = edited_email


	def days_birthday(self):
		birth_day = self.birthday.value
		birth_day = birth_day.replace(year = date.today().year)
		today = date.today()
		return (birth_day - today).days


	def __str__(self):
		return f'Name: {self.name}\nPhones: {self.phones}\nBirthday: {self.birthday}\nAddress: {self.address}\nEmail: {self.email}'


	def __repr__(self):
		return f"Name: {self.name}, Phones: {self.phones}, Birthday: {self.birthday}, Address: {self.address}, Email: {self.email}"


class AddressBook(UserDict):
	def add_record(self, record):
		self.data[record.name.value] = record


	def search_contacts(self, text):
		if self.data:
			result = [[repr(record)] for record in self.data.values() if text in repr(record)]
			if result:
				return result
			else:
				return f'The contact(s) with "{text}" such data is not found'
		else:
			return "Adress Book is empty"
