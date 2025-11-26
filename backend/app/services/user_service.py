from app.services.mysql_service import MySQLClass

db = MySQLClass.getInstance()


def get_user_by_id(user_id):
    query = "SELECT * FROM user WHERE id = %s"
    result = db.select_query(query, (user_id,))
    return result


def get_user_by_email(email):
    query = "SELECT * FROM user WHERE user_email = %s"
    result = db.select_query(query, (email,))
    return result


def get_user_by_username(username):
    query = "SELECT * FROM user WHERE user_name = %s"
    result = db.select_query(query, (username,))
    return result


def create_user(user_name, user_email, hashed_password, account_type):
    query = """
        INSERT INTO user (user_name, user_email, user_password, user_account_type)
        VALUES (%s, %s, %s, %s)
    """
    result = db.update_query(query, (user_name, user_email, hashed_password, account_type))
    return result
