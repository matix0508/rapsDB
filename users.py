from user import User, try_connecting
from getpass import getpass
class Auth:
    def __init__(self):
        self.users = []
        self.user = None
        self.login = None
        self.password = None
        self.authenticated = False

    def get_users(self):
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

print("Hello!")
auth = Auth()
auth.get_users()
i = 0
while i!= 3 and not auth.authenticated:
    auth.authenticate()
    if not auth.authenticated:
        i += 1
        print(f"You have {3-i} attempts left...")

if auth.authenticated:
    print(f"Hello {auth.user}")
    
