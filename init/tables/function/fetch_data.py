
def fetch_employer_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EMPLOYER")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return columns, data
def fetch_employer_list_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EMPLOYER_LIST")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return columns, data
def fetch_benefits_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BENEFITS")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return columns, data

def fetch_department_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DEPARTMENT")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return columns, data

def fetch_factor_information_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM FACTOR_INFORMATION")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return columns, data
def fetch_posts_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM POSTS")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return columns, data
def fetch_profesion_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PROFESSION_NEW")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return columns, data
def fetch_sovmest_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SOVMEST")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return columns, data
def fetch_document_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DOCUMENTS")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return columns, data