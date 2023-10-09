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