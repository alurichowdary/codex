import random
import string

def generate_password(length, use_letters=True, use_digits=True, use_symbols=True):
    character_pool = ""
    if use_letters:
        character_pool += string.ascii_letters
    if use_digits:
        character_pool += string.digits
    if use_symbols:
        character_pool += string.punctuation

    if not character_pool:
        return "Error: No character types selected."

    password = ''.join(random.choice(character_pool) for _ in range(length))
    return password

def get_boolean_input(prompt):
    while True:
        choice = input(prompt + " (yes/no): ").strip().lower()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")

def main():
    print("=== Simple Password Generator ===")

    try:
        length = int(input("Enter desired password length: "))
        if length <= 0:
            print("Password length must be greater than zero.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    use_letters = get_boolean_input("Include letters?")
    use_digits = get_boolean_input("Include digits?")
    use_symbols = get_boolean_input("Include symbols?")

    password = generate_password(length, use_letters, use_digits, use_symbols)
    print("\nGenerated Password:")
    print(password)

if __name__ == "__main__":
    main()