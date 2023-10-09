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
    