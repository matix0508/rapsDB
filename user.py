from DB import DataBase, Table

def try_connecting():
    i = 0
    db = DataBase("budget", "192.168.1.100", "Budget", "matix0508", "G@d#ryp0luk!")
    while not (db.connected or i == 10):
        try:
            db.db_connect()
        except:
            i+=1
            db = DataBase("budget", "192.168.1.10{i}", "Budget", "matix0508", "G@d#ryp0luk!")
    if db.connected:
        db.close()
        return db



def create_users(db):
    db.create_table("users", """CREATE TABLE users
                (id INT AUTO_INCREMENT PRIMARY KEY,
                    firstname VARCHAR(255),
                    lastname VARCHAR(255),
                    login VARCHAR(255),
                    password VARCHAR(255),
                    privileges INT)""")


class User:
    def __init__(self, login):
        self.id = None
        self.firstName = None
        self.lastName = None
        self.login = login
        self.password = None
        self.privileges = 0

    def __repr__(self):
        title = "User"
        if self.privileges == 1:
            title = "Admin"
        return f"{title}: {self.login}"

    def __eq__(self, other):
        if self.login == other.login:
            return True
        else:
            return False

    def save(self):
        budget = try_connecting()
        budget.db_connect()
        create_users(budget)
        print(budget.tables)
        # budget.close()
        #
        budget.sql("SELECT login FROM users")
        try:
            if self.login not in budget.cursor.fetchall()[0]:
                 budget.sql_insert(
                    "users",
                    (self.firstName, self.lastName, self.login, self.password, self.privileges),
                    ("firstname", "lastname", "login", "password", "privileges")
                )
                 print("sth")
            else:
                budget.sql(f"""UPDATE users
                                SET
                                firstname = '{self.firstName}',
                                lastName = '{self.lastName}',
                                password = '{self.password}',
                                privileges = '{self.privileges}'
                                WHERE
                                login = '{self.login}';""")
                budget.connection.commit()
        except Exception as ex:
            try:
                budget.sql_insert(
                   "users",
                   (self.firstName, self.lastName, self.login, self.password, self.privileges),
                   ("firstname", "lastname", "login", "password", "privileges")
               )
            except:
                pass

        budget.close()
