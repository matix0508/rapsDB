from user import User, try_connecting, DEBUG
from getpass import getpass

def menu(auth):
    if auth.authenticated:
        print(f"[INFO]::Hello {auth.login}")
        print("[MENU]::Choose what you want to do (press Enter to quit):")
        print("\t[OPTION 1]::Change your data")
        print("\t[OPTION 2]::Add user")
        print("\t[OPTION 3]::Remove user")
        return input("\n\t[INPUT]::")
    else:
        print("[MENU]::You are not logged in")

def change_data(auth):
    print("[INFO]::Your data:")
    us = auth.user
    us.display()
    print("[INFO]::Type to change your date, press enter to skip")
    name = input("First Name: ")
    lname = input("Second Name: ")
    password = getpass("Password: ")
    if password:
        cpassword = getpass("Confirm password: ")
        if password != cpassword:
            print("[ERROR]::Passwords don't match!")
            password = None
    if name:
        us.firstName = name
    if lname:
        us.lastName = lname
    if password:
        us.password = password
    us.save()


def add_user(auth):
    print("[INFO]::Adding new user")
    login = input("[NEW]::Login: ")
    password = getpass("[NEW]::Password: ")
    admin = input("[NEW]::Admin?(y/n): ")
    try:
        new = User(login)
        new.password = password
        if admin.lower() == 'y':
            new.privileges = 1
        new.save()
        auth.get_users()
    except:
        print("[ERROR]::Something went wrong")


def log_in():
    auth = Auth()
    auth.get_users()
    i = 0
    while i!= 3 and not auth.authenticated:
        auth.authenticate()
        if not auth.authenticated:
            i += 1
            print(f"You have {3-i} attempts left...")
    return auth

def remove_user(auth):
    print("[INFO]::removing user")
    print("[INFO]::Choose user to be removed (press Enter to cancel)")
    for i, u in enumerate(auth.users):
        print(f"[{i}]::{u}")
    opt = input("[INPUT]::")
    if not opt:
        return
    opt = int(opt)
    if opt >= 0 and opt < len(auth.users):
        u = auth.users[opt]
        ans = input(f"Are you sure you want to remove {u}?(y/n)")
        if ans.lower() == "y":
            u.remove()
            auth.get_users()


class Auth:
    def __init__(self):
        self.users = []
        self.user = None
        self.login = None
        self.password = None
        self.authenticated = False

    def get_users(self):
        self.users = []
        budget = try_connecting()
        if not budget:
            raise Exception("Can't connect to database")
        budget.db_connect()
        budget.sql("SELECT * FROM users")
        for user in budget.cursor.fetchall():
            id, first, last, login, password, priv = user
            new = User(login)
            new.id = id
            new.firstName = first
            new.lastName = last
            new.password = password
            new.privileges = priv
            self.users.append(new)
        if DEBUG:
            print(self.users)

    def authenticate(self):
        self.login = input("Login: ")
        self.password = getpass("Password: ")
        for user in self.users:
            if user.login == self.login and user.password == self.password:
                self.authenticated = True
                self.user = user
                print("Succes! ")
                return
        print("Wrong credentials")

# print("Hello!")

auth = log_in()
opt = 1
while opt:
    opt = menu(auth)
    if opt:
        if int(opt) == 1:
            change_data(auth)
        elif int(opt) == 2:
            add_user(auth)
        elif int(opt) == 3:
            remove_user(auth)
        else:
            break
