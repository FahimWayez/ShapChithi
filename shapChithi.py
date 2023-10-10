import getpass
import hashlib
from time import sleep

userDatabase = {}
chatHistory = {}
userSessions = {}
credentials = 'credentials.txt'

def clearScreen():
    sleep(1.5)
    print('\033c')

def shundorHeader():
    print('='*40, end="\n")
    print('Shap Chithi')
    print('='*40, end="\n")

def writeCredentials(userName, password):
    with open(credentials, 'a') as file:
        file.write(f'{userName}:{password}\n')

def readCredentials():
    try:
        with open(credentials, 'r') as file:
            lines = file.readlines()
            for line in lines:
                userName, password = line.strip().split(':')
                userDatabase[userName] = password
    except FileNotFoundError:
        pass          
        
def register():
    clearScreen()
    shundorHeader()
    print("Registration Portal")
    print('='*40, end="\n")
    userName = input("Please enter your username: ")
    
    if userName in userDatabase:
        print("Username already exists. Registration failed.")
        return
    
    password = getpass.getpass("Please enter a password: ")
    cPassword = getpass.getpass("Confirm your password: ")

    if password != cPassword:
        print("Passwords do not match, please try again.")
        return
    
    hashedPassword = hashlib.sha256(password.encode()).hexdigest()
    userDatabase[userName] = hashedPassword
    
    writeCredentials(userName, hashedPassword)
    
    chatHistory[userName] = []
    print("Registration is successful. You have become a python.")
    
    # userDatabase[userName] = password
    # chatHistory[userName] = []

def login():
    clearScreen()
    shundorHeader()
    print("Login Portal")
    print('='*40, end="\n")
    userName = input("Please enter your username: ")
    password = getpass.getpass("Enter your password: ")

    if userName in userDatabase and userDatabase[userName] == hashlib.sha256(password.encode()).hexdigest():
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
    readCredentials()
    
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
        