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
