from mysql.connector import Error, pooling
from app.config import Config
import json


class MySQLClass:
    __instance = None

    @staticmethod
    def getInstance():
        if MySQLClass.__instance is None:
            MySQLClass()
        return MySQLClass.__instance

    def __init__(self):
        if MySQLClass.__instance is not None:
            print("Already set")
            return

        try:
            self.myConnectionPool = pooling.MySQLConnectionPool(
                pool_name="pynative_pool",
                pool_size=5,
                pool_reset_session=True,
                host=Config.DB_HOST,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
            )

            # Run once on startup
            self.update_query("SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''))")
            self.update_query("SET @@lc_time_names = 'he_IL'")

            MySQLClass.__instance = self
            print("Connection pool ready:", self.myConnectionPool.pool_name)

        except Error as e:
            print("Error while connecting to MySQL pool:", e)
            raise

    # ---------- internal helper ----------
    def _get_conn(self):
        return self.myConnectionPool.get_connection()

    # ---------- public API ----------
    def select_query(self, query, params=None):
        conn = None
        cursor = None
        try:
            conn = self._get_conn()
            cursor = conn.cursor(buffered=True)
            cursor.execute(query, params or ())
            return cursor.fetchall()

        except Error as e:
            print("select_query error:", e)
            return False

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_col_from_select_query(self, query, params=None):
        conn = None
        cursor = None
        try:
            conn = self._get_conn()
            cursor = conn.cursor(buffered=True)
            cursor.execute(query, params or ())
            cols = [col[0] for col in cursor.description]
            return json.dumps({"status": "ok", "cols": cols})

        except Error as e:
            print("get_col_from_select_query error:", e)
            return json.dumps({"status": "error", "errorCode": str(e)})

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def update_query(self, query, params=None):
        conn = None
        cursor = None
        try:
            conn = self._get_conn()
            cursor = conn.cursor(buffered=True)
            cursor.execute(query, params or ())
            conn.commit()
            return True

        except Error as e:
            print("update_query error:", e)
            if conn:
                conn.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def check(self, query, params=None):
        res = self.select_query(query, params)
        return bool(res)  # True if any rows

    def validate_query(self, query, params=None):
        # Just executes to see if valid
        conn = None
        cursor = None
        try:
            conn = self._get_conn()
            cursor = conn.cursor(buffered=True)
            cursor.execute(query, params or ())
            return json.dumps({"status": "ok"})

        except Error as e:
            print("validate_query error:", e)
            return json.dumps({"status": "error", "errorCode": str(e)})

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
