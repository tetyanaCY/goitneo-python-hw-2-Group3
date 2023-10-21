def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
    return inner

@input_error
def add_contact(args, contacts):
    name, phone = args
    if not name or not phone:
        raise ValueError("Both name and phone are required")
    
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    if not name or not phone:
        raise ValueError("Both name and phone are required")
    
    if name not in contacts:
        raise KeyError("Contact not found.")
    
    contacts[name] = phone
    return "Contact updated."

@input_error
def get_phone(args, contacts):
    name = args[0]
    if not name:
        raise ValueError("Name is required")
    
    return contacts[name]

@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts available."

    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(get_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
