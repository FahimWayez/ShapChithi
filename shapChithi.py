import getpass
import hashlib
import os
from time import sleep

userDatabase = {}
chatHistory = {}
userSessions = {}
credentials = 'credentials.txt'
chatHistoryDir = 'chatHistory'


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


def createUserDirectory(userName):
    userDirectory = os.path.join(chatHistoryDir, userName)
    os.makedirs(userDirectory, exist_ok=True)


def writeMessage(userName, receiver, message):
    senderFile = os.path.join(chatHistoryDir, userName, f'{receiver}.txt')
    receiverFile = os.path.join(chatHistoryDir, receiver, f'{userName}.txt')
    
    os.makedirs(os.path.dirname(senderFile), exist_ok=True)
    os.makedirs(os.path.dirname(receiverFile), exist_ok=True)
    
    with open(senderFile, 'a') as file:
        file.write(f'You to {receiver}:{message}\n')

    with open(receiverFile, 'a') as file:
        file.write(f'{userName}:{message}\n')


def readChat(userName):
    chatHistory = []
    userDirectory = os.path.join(chatHistoryDir, userName)
    if os.path.exists(userDirectory):
        chatFiles = os.listdir(userDirectory)
        for chatFile in chatFiles:
            filePath = os.path.join(userDirectory, chatFile)
            with open(filePath, 'r') as file:
                chatHistory.extend(file.readlines())
    return chatHistory

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

    os.makedirs(chatHistoryDir, exist_ok=True)

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
                createUserDirectory(currentUser)
        elif choice == '3' and currentUser:
            receiver = input("Enter the recipient's username: ")
            message = input('Enter your message: ')
            if currentUser != receiver:
                sendMessage(currentUser, receiver, message)
                writeMessage(currentUser, receiver, message)
            else:
                print("You cannot send message to yourself")
        elif choice == '4' and currentUser:
            chatHistory = readChat(currentUser)
            for message in chatHistory:
                print(message.strip())
            input('\nPress enter to continue...')
            # displayChat(currentUser)
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
        else:
            print("Invalid choice, please try again.")


# Rgistr kaj kortsna, amar kyboard o