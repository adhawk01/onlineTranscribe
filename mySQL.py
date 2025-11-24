import sys
sys.path.append("venv/Lib/site-packages/")
from mysql.connector import Error
from mysql.connector import pooling
import random
import json
from config import serverName



class MySQLClass:
    __instance = None

    def getInstance():
        """ Static access method. """
        if MySQLClass.__instance == None:
            MySQLClass()
        return MySQLClass.__instance

    def __init__(self):
        if MySQLClass.__instance != None:
            print("Already set ")
        else:
            try:
                self.myConnectionPool = pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                                    pool_size=5,
                                                                    pool_reset_session=True,
                                                                    host='localhost',
                                                                    database='alberto',
                                                                    user='root',
                                                                    password='adHawk01')

                print("Printing connection pool properties ")
                print("Connection Pool Name - ", self.myConnectionPool.pool_name)
                print("Connection Pool Size - ",  self.myConnectionPool.pool_size)
                self.update_query("SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''))", "dummy")
                self.update_query("SET @@lc_time_names = 'he_IL'", "dummy")
                MySQLClass.__instance = self

            except Error as e:
                print("Error while connecting to MySQL using Connection pool ", e)

    def select_query(self, query, user):
        user = str(random.randint(1, 900))
        print(f"getting connection for {user}")
        globals()[f"Connect_object_{user}"] = self.myConnectionPool.get_connection()
        print(query)
        if globals()[f"Connect_object_{user}"].is_connected():
            try:
                print("getting cursor for user " + user)
                myCursor = globals()[f"Connect_object_{user}"].cursor(buffered=True)
                # myCursor.execute("SET @@lc_time_names = 'he_IL'")
                myCursor.execute(query)
            except Error as e:
                print("Error while creating cursor and executing ", e)
                if globals()[f"Connect_object_{user}"].is_connected():
                    print("releasing the cursor")
                    globals()[f"Connect_object_{user}"].close()
                return False
        resultsList = []
        for row in myCursor:
            resultsList.append(row)
        if globals()[f"Connect_object_{user}"].is_connected():
            print("releasing the cursor")
            globals()[f"Connect_object_{user}"].close()
            print("returning " + str(type(resultsList)))
        else:
            print("Cursor not connected")
        return resultsList

    def get_col_from_select_query(self, query, user):
        user = str(random.randint(1, 900))
        globals()[f"Connect_object_{user}"] = self.myConnectionPool.get_connection()
        print(query)
        if globals()[f"Connect_object_{user}"].is_connected():
            try:
                print("getting cursor for user " + user)
                myCursor = globals()[f"Connect_object_{user}"].cursor(buffered=True)
                myCursor.execute(query)
                colList = []
                for col in myCursor.description:
                    colList.append(col[0])
                if globals()[f"Connect_object_{user}"].is_connected():
                    globals()[f"Connect_object_{user}"].close()
                return json.dumps({"status": "ok", "cols": colList})
            except Error as e:
                print("Error while creating cursor and executing ", e)
                if globals()[f"Connect_object_{user}"].is_connected():
                    globals()[f"Connect_object_{user}"].close()
                return json.dumps({"status": "error", "errorCode": str(e)})

    def update_query(self, query, user):
        user = str(random.randint(1, 900))
        globals()[f"Connect_object_{user}"] = self.myConnectionPool.get_connection()
        print(query)
        if globals()[f"Connect_object_{user}"].is_connected():
            try:
                my_cursor = globals()[f"Connect_object_{user}"].cursor(buffered=True)
                my_cursor.execute(query)
            except Error as e:
                print("Error while creating cursor and executing ", e)
                if globals()[f"Connect_object_{user}"].is_connected():
                    globals()[f"Connect_object_{user}"].close()
                return False

        globals()[f"Connect_object_{user}"].commit()
        if globals()[f"Connect_object_{user}"].is_connected():
            globals()[f"Connect_object_{user}"].close()
        return True

    def check(self, query, user):
        user = str(random.randint(1, 900))
        globals()[f"Connect_object_{user}"] = self.myConnectionPool.get_connection()
        print(query)
        try:
            my_cursor = globals()[f"Connect_object_{user}"].cursor(buffered=True)
            my_cursor.execute(query)
        except Error as e:
            print("Error while creating cursor and executing ", e)
            if globals()[f"Connect_object_{user}"].is_connected():
                globals()[f"Connect_object_{user}"].close()

        num_of_records = 0
        for row in my_cursor:
            num_of_records = num_of_records + 1

        if globals()[f"Connect_object_{user}"].is_connected():
            globals()[f"Connect_object_{user}"].close()

        if num_of_records > 0:
            return True
        else:
            return False

    def validate_query(self, query, user):
        user = str(random.randint(1, 900))
        globals()[f"Connect_object_{user}"] = self.myConnectionPool.get_connection()
        print("got connection in validate query")
        print(query)
        if globals()[f"Connect_object_{user}"].is_connected():
            try:
                print("getting cursor for user " + user)
                myCursor = globals()[f"Connect_object_{user}"].cursor(buffered=True)
                print("got cursor in validate query")
                myCursor.execute(query)
                print("query was executed in validate query")
                if globals()[f"Connect_object_{user}"].is_connected():
                    globals()[f"Connect_object_{user}"].close()
                print("released connection in validate query")
                return json.dumps({"status": "ok"})
            except Error as e:
                print("Error while creating cursor and executing ", e)
                if globals()[f"Connect_object_{user}"].is_connected():
                    globals()[f"Connect_object_{user}"].close()
                print("released connection in validate query 2")
                return json.dumps({"status": "error", "errorCode": str(e)})

