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
    

def deleteMessage(userName):
    clearScreen()
    shundorHeader()
    print("Delete Message")
    print('='*40, end='\n')
    print('1. Delete All Messages')
    print('2. Delete Messages with a specific user')
    choice = input('Please enter your choice: ')
    
    if choice == '1':
        deleteChoice = input('You sure want to delete? (Y/N): ')  
        if deleteChoice.lower() == 'y':  
            chatHistory[userName] = [] #current user theke hisotry delete kortesi
            
            userDirectory = os.path.join(chatHistoryDir, userName) #text file delete kortesi
            if os.path.exists(userDirectory):
                for fileName in os.listdir(userDirectory):
                    filePath = os.path.join(userDirectory, fileName)
                    os.remove(filePath)
                    
            print('All messages deleted successfully.')
            
        elif deleteChoice.lower() == 'n':
            pass
        else: print('Invalid input. Please enter y or n only.')
    
    elif choice == '2': 
        targetUser = input('Enter the username of the user you want to delete the messages: ')
        
        deleteChoice = input('You sure want to delete? (Y/N): ')
        
        if deleteChoice.lower() == 'y':
            chatHistory[userName] = [message for message in chatHistory[userName] if targetUser not in message] #memory theke delete kortesi
            
            userDirectory = os.path.join(chatHistoryDir, userName) #text file theke delete
            if os.path.exists(userDirectory):
                for fileName in os.listdir(userDirectory):
                    if targetUser in fileName:
                        filePath = os.path.join(userDirectory, fileName)
                        os.remove(filePath)
                        
            print(f'Messages with {targetUser} deleted successfully.')
            
        elif deleteChoice.lower() == 'n':
            pass
        else:
            print('Invalid input. Please enter y or n only.')
    
    else: print('Invalid choice')

def searchUser(keyword, currentUser):
    matchingUsers = [user for user in userDatabase.keys() if keyword.lower() in user.lower()]
    return matchingUsers

def initiateChat(currentUser):
    clearScreen()
    shundorHeader()
    print('Search for user')
    print('='*40,end='\n')
    keyword = input("Search for user with name: ")
    
    matchingUsers = searchUser(keyword)
    
    if matchingUsers:
        print('Found users: ')
        for i, user in enumerate(matchingUsers, start = 1):
            print(f'{i}.{user}')
        
        try:
            choice = int(input('Choose an option: '))
            if choice == 0: return
            elif 1 <= choice <= len(matchingUsers):
                chatWith = matchingUsers[choice - 1]
                message = input(f'Chat with {chatWith}: ')
                sendMessage(currentUser,chatWith, message)
                writeMessage(currentUser, chatWith, message)
                print(f'You are now chatting with {chatWith}')
                input('Press enter to continue...')
            
            else: print('Invalid choice')
        
        except ValueError: print('Invalid input.')
    else: 
        print('No users found.')
        input('Press enter to continue...')               
    
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
            print("3. Search user to send message")
            print("4. Display messages")
            print("5. Delete messages")
            print("6. Update messages")
            print("8. Logout")

        print("9. Exit")

        choice = input("Please enter a choice: ")

        if choice == '1' and currentUser is None:
            register()
        elif choice == '2' and currentUser is None:
            currentUser = login()
            if currentUser:
                userSessions[currentUser] = True
                createUserDirectory(currentUser)
        elif choice == '3' and currentUser:
            initiateChat(currentUser)
            # receiver = input("Enter the recipient's username: ")
            # message = input('Enter your message: ')
            # if currentUser != receiver:
            #     sendMessage(currentUser, receiver, message)
            #     writeMessage(currentUser, receiver, message)
            # else:
            #     print("You cannot send message to yourself")
        elif choice == '4' and currentUser:
            chatHistory = readChat(currentUser)
            for message in chatHistory:
                print(message.strip())
            input('\nPress enter to continue...')
            # displayChat(currentUser)
        elif choice == '5' and currentUser:
            deleteMessage(currentUser)
        elif choice == '6' and currentUser:
            # updateMessage(currentUser)
            pass
        elif choice == '7' and currentUser:
            pass
        elif choice == '8' and currentUser:
            logout(currentUser)
            currentUser = None
        elif choice == '9':
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
