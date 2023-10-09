import getpass

userDatabase = {}
chatHistory = {}
userSessions = {}

def register():
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
    userName = input("Please enter your username: ")
    password = getpass.getpass("Enter your password: ")
    
    if userName in userDatabase and userDatabase[userName] == password:
        print("Congratulations! Login successful.")
        return userName
    else: print("Invalid username or password. Please try again.")
    return None

def logout(userName):
    if userName in userSessions:
        del userSessions[userName]
        print("Logout Successful")
    else:
        print("Not logged in") #eta shoray dite hobe pore
    
def sendMessage(sender, receiver, message):
    if receiver in chatHistory:
        chatHistory[receiver].append(f"{sender}: {message}") 
        chatHistory[sender].append(f"You to {receiver}: {message}")  
    else: print("Invalid recipient") 
    
def displayChat(userName):
    if userName in chatHistory:
        for message in chatHistory[userName]:
            print(message)
    else: print("You have no chat history to be shown")

if __name__ == "__main__":
    currentUser = None
    while True:
        print("\nOptions: ")
        if currentUser is None:
            print("1. Register")
            print("2. Login")
        else:
            print(f"Logged in as {currentUser}")
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
            sendMessage(currentUser, receiver, message)
        elif choice == '4' and currentUser:
            displayChat(currentUser)
        elif choice == '5' and currentUser:
            logout(currentUser)
            currentUser = None
        elif choice == '6':
            print("Goodbye tata Allah hafiz")
            break
        else: print("Invalid choice, please try again.")
        