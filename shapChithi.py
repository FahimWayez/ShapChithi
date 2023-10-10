import getpass
from time import sleep

userDatabase = {}
chatHistory = {}
userSessions = {}

def clearScreen():
    sleep(1.5)
    print('\033c')

def shundorHeader():
    print('='*40, end="\n")
    print('Shap Chithi')
    print('='*40, end="\n")

def register():
    clearScreen()
    shundorHeader()
    print("Registration Portal")
    print('='*40, end="\n")
    userName = input("Please enter your username: ")
    password = getpass.getpass("Please enter a password: ")
    cPassword = getpass.getpass("Confirm your password: ")

    if password != cPassword:
        print("Passwords do not match, please try again.")
        return
    userDatabase[userName] = password
    chatHistory[userName] = []
    print("Registration is successful. You have become a python.")

def login():
    clearScreen()
    shundorHeader()
    print("Login Portal")
    print('='*40, end="\n")
    userName = input("Please enter your username: ")
    password = getpass.getpass("Enter your password: ")

    if userName in userDatabase and userDatabase[userName] == password:
        print("Congratulations! Login successful.")
        return userName
    else:
        print("Invalid username or password. Please try again.")
    return None

def logout(userName):
    clearScreen()
    shundorHeader()
    if userName in userSessions:
        del userSessions[userName]
        print("Logout Successful")
    else:
        print("Not logged in")  # eta shoray dite hobe pore


def sendMessage(sender, receiver, message):
    if receiver in chatHistory:
        chatHistory[receiver].append(f"{sender}: {message}")
        chatHistory[sender].append(f"You to {receiver}: {message}")
    else:
        print("Invalid recipient")


def displayChat(userName):
    clearScreen()
    shundorHeader()
    if userName in chatHistory:
        for message in chatHistory[userName]:
            print(message)
    else:
        print("You have no chat history to be shown")
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    currentUser = None
    while True:
        clearScreen()
        shundorHeader()
        if currentUser is None:
            print("\nOptions: ")
            print("1. Register")
            print("2. Login")
        else:
            print(f"Logged in as {currentUser}")
            print("\nOptions: ")
            print("3. Send message")
            print("4. Display messages")
            print("5. Logout")

        print("6. Exit")

        choice = input("Please enter a choice: ")

        if choice == '1' and currentUser is None:
            register()
        elif choice == '2' and currentUser is None:
            currentUser = login()
            if currentUser:
                userSessions[currentUser] = True
        elif choice == '3' and currentUser:
            receiver = input("Enter the recipient's username: ")
            message = input('Enter your message: ')
            if currentUser != receiver:
                sendMessage(currentUser, receiver, message)
            else:
                print("You cannot send message to yourself")
        elif choice == '4' and currentUser:
            displayChat(currentUser)
        elif choice == '5' and currentUser:
            logout(currentUser)
            currentUser = None
        elif choice == '6':
            exitChoice = input("You sure want to exit? (Y/N): ")
            if exitChoice.lower() == 'y':
                print("Goodbye tata Allah Hafiz")
                break
            elif exitChoice.lower() == 'n':
                pass
            else:
                print("Invalid input. Please enter y or n only.")
        else: print("Invalid choice, please try again.")