import re
from collections import UserDict

# Field Class
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Name Class
class Name(Field):
    pass

# Phone Class
class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        self.value = value

    @staticmethod
    def validate(phone):
        return bool(re.fullmatch(r'\d{10}', phone))

# Record Class
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# AddressBook Class
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def all_records(self):
        return list(self.data.values())

    def find_by_phone(self, phone):
        for record in self.data.values():
            if any(p.value == phone for p in record.phones):
                return record
        return None

# Bot functions
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Incomplete command. Please check and try again."
    return inner

def parse_input(user_input):
    return user_input.split()

@input_error
def add_contact(args, book):
    if len(args) < 2:
        return "You need to provide both a name and a phone number to add a contact."
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return "Contact added."

@input_error
def change_contact(args, book):
    if len(args) != 3:
        return "Please provide a name, old phone, and new phone for changing contact details."
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def delete_contact(args, book):
    name = args[0]
    book.delete(name)
    return f"Deleted record for {name}."

@input_error
def find_by_name_or_phone(args, book):
    query = args[0]
    # Try to find by name first
    record = book.find(query)
    if not record:
        # If not found by name, try by phone
        record = book.find_by_phone(query)
    if not record:
        return "Contact not found."
    return str(record)

@input_error
def show_all(book):
    records = book.all_records()
    if not records:
        return "No contacts found."
    return "\n".join(str(record) for record in records)

# Main execution function
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "find":
            print(find_by_name_or_phone(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "all":
            print(show_all(book))
        else:
            print(f"'{command}' is an unrecognized command. Please provide a valid command.")

if __name__ == "__main__":
    main()
