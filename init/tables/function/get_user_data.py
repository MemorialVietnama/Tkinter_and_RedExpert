from tables.function.conn_base import connect_to_database
def get_user_data(username, password, user_login):
    conn = connect_to_database(username, password)
    if conn:
        cursor = conn.cursor()
        cursor.execute("EXECUTE PROCEDURE GET_USER_DATA(?)", (user_login,))
        user_data = cursor.fetchone()
        conn.close()
        return user_data
    return None