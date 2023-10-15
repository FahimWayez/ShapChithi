import getpass
import hashlib
import os
import re
from time import sleep

userDatabase = {}
chatHistory = {}
userSessions = {}
credentials = "credentials.txt"
chatHistoryDir = "chatHistory"

def clearScreen():
    sleep(1.5)
    print("\033c")

def shundorHeader():
    print("="*40, end="\n")
    print("Shap Chithi")
    print("="*40, end="\n")

def writeCredentials(userName, password):
    with open(credentials, "a") as file:
        file.write(f"{userName}:{password}\n")

def updateCredentials():
    with open(credentials, 'w') as file:
        for userName, password in userDatabase.items():
            file.write(f"{userName}:{password}\n")
            
def readCredentials():
    try:
        with open(credentials, "r") as file:
            lines = file.readlines()
            for line in lines:
                userName, password = line.strip().split(":")
                userDatabase[userName] = password
    except FileNotFoundError:
        pass

def createUserDirectory(userName):
    userDirectory = os.path.join(chatHistoryDir, userName)
    os.makedirs(userDirectory, exist_ok=True)

def writeMessage(userName, receiver, message):
    senderFile = os.path.join(chatHistoryDir, userName, f"{receiver}.txt")
    receiverFile = os.path.join(chatHistoryDir, receiver, f"{userName}.txt")

    os.makedirs(os.path.dirname(senderFile), exist_ok=True)
    os.makedirs(os.path.dirname(receiverFile), exist_ok=True)

    with open(senderFile, "a") as file:
        file.write(f"You to {receiver}:{message}\n")

    with open(receiverFile, "a") as file:
        file.write(f"{userName}:{message}\n")

def register():
    clearScreen()
    shundorHeader()
    print("Registration Portal")
    print("="*40, end="\n")
    userName = input("Please enter your username: ")

    if userName in userDatabase:
        print("Username already exists. Registration failed.")
        return
    
    if re.search("^[0-9]", userName):
        print("Your username cannot start with a digit")
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
    
def login():
    clearScreen()
    shundorHeader()
    print("Login Portal")
    print("="*40, end="\n")
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
        print("Not logged in")  


def sendMessage(sender, receiver, message):
    if receiver in chatHistory:
        chatHistory[receiver].append(f"{sender}: {message}")
    else:
        chatHistory[receiver] = [f"{sender}: {message}"]
        
    if sender in chatHistory:
        chatHistory[sender].append(f"You to {receiver}: {message}")
    else:
        chatHistory[sender] = [f"{receiver}: {message}"]
        
        
    writeMessage(sender, receiver, message)
    print(f"Message sent to {receiver}")
    
def searchUser(keyword, currentUser):
    matchingUsers = [user for user in userDatabase.keys() if keyword.lower() in user.lower() and user != currentUser]
    return matchingUsers

def displayChatHistory(currentUser, targetUser):
    clearScreen()
    shundorHeader()
    print(f"Chat history with {targetUser}")
    print("="*40, end = "\n")
    
    if currentUser in chatHistory and targetUser in chatHistory:
        currentUserChat = chatHistory[currentUser]
        targetUserChat = chatHistory[targetUser]
        
        targetUserMessages = [msg for msg in currentUserChat if targetUser in msg or currentUser in msg]
        
        for message in targetUserMessages:
            print(message)
                    
    else: print(f"No chat history found between {currentUser} and {targetUser}")
    
    input("\nPress enter to continue...")
    
def initiateChat(currentUser):
    clearScreen()
    shundorHeader()
    print("Search for user")
    print("="*40, end="\n")
    
    while True:
        keyword = input("Search for user with name (or type 'quit' to exit): ")
        
        if keyword.lower() == "quit": break

        matchingUsers = searchUser(keyword, currentUser)

        if matchingUsers:
            print("Found users: ")
            for i, user in enumerate(matchingUsers, start=1):
                print(f"{i}.{user}")

            try:
                choice = int(input("Choose an option (or type '0' to go back): "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(matchingUsers):
                    receiver = matchingUsers[choice - 1]                            
                    while True:
                        message = input(f"Chat with {receiver} (type 'quit' to exit): ")
                        if message.lower() == "quit": break
                        
                        sendMessage(currentUser, receiver, message)
                        writeMessage(currentUser, receiver, message)
                        print("")

                else:
                    print("Invalid choice")

            except ValueError:
                print("Invalid input.")
        else:
            print("No users found.")
            input("Press enter to continue...")

def displayChat(currentUser):
    clearScreen()
    shundorHeader()
    print("Search for user")
    print("="*40, end="\n")

    while True:
        keyword = input("Search for user with name (or type 'quit' to exit): ")

        if keyword.lower() == "quit":
            break

        matchingUsers = searchUser(keyword, currentUser)

        if matchingUsers:
            print("Found users: ")
            for i, user in enumerate(matchingUsers, start=1):
                print(f"{i}.{user}")

            try:
                choice = int(
                    input("Choose an option (or type '0' to go back): "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(matchingUsers):
                    receiver = matchingUsers[choice - 1]
                    displayChatHistory(currentUser, receiver)

                else:
                    print("Invalid choice")

            except ValueError:
                print("Invalid input.")
        else:
            print("No users found.")
            input("Press enter to continue...")
            

def deleteMessage(userName):
    clearScreen()
    shundorHeader()
    print("Delete Message")
    print("="*40, end="\n")
    print("1. Delete All Messages")
    print("2. Delete Messages with a specific user")
    choice = input("Please enter your choice: ")

    if choice == "1":
        deleteChoice = input("You sure want to delete? (Y/N): ")
        if deleteChoice.lower() == "y":
            chatHistory[userName] = []

            userDirectory = os.path.join(chatHistoryDir, userName)
            if os.path.exists(userDirectory):
                for fileName in os.listdir(userDirectory):
                    filePath = os.path.join(userDirectory, fileName)
                    os.remove(filePath)

            print("All messages deleted successfully.")

        elif deleteChoice.lower() == "n":
            pass
        else:
            print("Invalid input. Please enter y or n only.")

    elif choice == "2":
        receiver = input("Enter the username of the user you want to delete the messages: ")

        deleteChoice = input("You sure want to delete? (Y/N): ")

        if deleteChoice.lower() == "y":
            chatHistory[userName] = [message for message in chatHistory[userName] if receiver not in message]  # memory theke delete kortesi

            userDirectory = os.path.join(
                chatHistoryDir, userName)  # text file theke delete
            if os.path.exists(userDirectory):
                for fileName in os.listdir(userDirectory):
                    if receiver in fileName:
                        filePath = os.path.join(userDirectory, fileName)
                        os.remove(filePath)

            print(f"Messages with {receiver} deleted successfully.")

        elif deleteChoice.lower() == "n":
            pass
        else:
            print("Invalid input. Please enter y or n only.")

    else:
        print("Invalid choice")


def updateProfile(userName):
    clearScreen()
    shundorHeader()
    print("Update Profile")
    print("="*40, end = "\n")
    print("1. Update username")
    print("2. Update password")
    choice = input("Please enter your choice: ")
    
    if choice == "1":
        newUserName = input("Please enter your new username: ")
        
        if newUserName in userDatabase:
            print("This username is already in use.")
        else:
            userDatabase[newUserName] = userDatabase.pop(userName)
            
            oldUserDir = os.path.join(chatHistoryDir, userName)
            newUserDir = os.path.join(chatHistoryDir, newUserName)
            os.rename(oldUserDir,newUserDir)
            
            userName = newUserName
            print("Username updated successfully.")
            
        updateCredentials()
            
    elif choice == "2":
        newPassword = getpass.getpass("Enter your new password: ")
        cNewPassword = getpass.getpass("Confirm your new password: ")
        
        if newPassword != cNewPassword:
            print("Passwords do not match.")
        else:
            hashedPassword = hashlib.sha256(newPassword.encode()).hexdigest()
            userDatabase[userName] = hashedPassword
            writeCredentials(userName, hashedPassword)
            
            print("Password updated successfully.")
            
        updateCredentials()
        
    else: print("Invalid choice")
    
    return userName


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
            print("4. Search user to display messages")
            print("5. Delete messages")
            print("6. Update profile")
            print("7. Logout")

        print("8. Exit")

        choice = input("Please enter a choice: ")

        if choice == "1" and currentUser is None:
            register()
        elif choice == "2" and currentUser is None:
            currentUser = login()
            if currentUser:
                userSessions[currentUser] = True
                createUserDirectory(currentUser)
        elif choice == "3" and currentUser:
            initiateChat(currentUser)
        elif choice == "4" and currentUser:
            displayChat(currentUser)
        elif choice == "5" and currentUser:
            deleteMessage(currentUser)
        elif choice == "6" and currentUser:
            currentUser = updateProfile(currentUser)
        elif choice == "7" and currentUser:
            logout(currentUser)
            currentUser = None
        elif choice == "8":
            exitChoice = input("You sure want to exit? (Y/N): ")
            if exitChoice.lower() == "y":
                print("Goodbye tata Allah Hafiz")
                break
            elif exitChoice.lower() == "n":
                pass
            else:
                print("Invalid input. Please enter y or n only.")
        else:
            print("Invalid choice, please try again.")
