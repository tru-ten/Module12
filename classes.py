from collections import UserDict
from datetime import datetime
import re

class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

class Name(Field):
    @Field.value.setter
    def value(self, value):
        if value.isalpha():
            self._Field__value = value
        else:
            raise Exception('The name must consist of only letters')

class Phone(Field):
    @Field.value.setter
    def value(self, value):
        checking = re.findall(r'[0]{1}\d{9}',value)
        if checking and len(value) == 10:
            self._Field__value = value
        else:
            raise Exception('The length of the phone is not 10 or the phone does not consist of numbers. As it should be: 0661117733')

class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        checking = re.findall(r'\d{2}[.]\d{2}[.]\d{4}',value)
        if checking and len(value) == 10:
            self._Field__value = value
        else:
            raise Exception('The date should be written in full and with periods, for example: "09.08.1999"')

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            print(f'Phone {phone.value} is not listed')

    def change_phone(self, old_phone, new_phone):
        try:
            index_phone = self.phones.index(old_phone)
            self.phones[index_phone] = new_phone
        except ValueError:
            print(f'Phone {old_phone.value} is not listed')

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            parts_of_birth = self.birthday.split('.')
            birthday_this_year = datetime(year=today.year, month=int(parts_of_birth[1]), day=int(parts_of_birth[0]))
            if today > birthday_this_year:
                birthday_next_year = datetime(year=today.year+1, month=int(parts_of_birth[1]), day=int(parts_of_birth[0]))
                checking = birthday_next_year - today
                return checking.days 
            elif today <= birthday_this_year:
                checking = birthday_this_year - today
                return checking.days 

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record.phones
    
    def delete_record(self, record):
        try:
            self.data.pop(record.name.value)
        except KeyError:
            print(f'Record {record} not found')

    def search_record(self, record):
        if record.name.value in self.data.keys():
            return 'Record found'

    def iterator(self, number_of_records):
        counter = 0
        result = ''
        for name, phones in self.data.items():
            result += f'{name}: {phones}\n'
            counter += 1
            if counter >= number_of_records:
                yield result
                counter = 0
                result = ''
        if result:
            yield result