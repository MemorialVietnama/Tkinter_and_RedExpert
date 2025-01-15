
from pathlib import Path
import fdb
def log_action(username, password, action, table_name, additional_info):
    current_dir = Path(__file__).resolve().parent
    database_path = current_dir.parents[2] / 'kadrbase.fdb'
    try:
        conn = fdb.connect(
            host='localhost',
            database=database_path,
            user=username,
            password=password,
            port=3050,
            charset='utf8'
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_logs (action, table_name, additional_info)
            VALUES (?, ?, ?)
        """, (action, table_name, additional_info))
        conn.commit()
        cursor.close()
        conn.close()
    except fdb.Error as e:
        print(f"Ошибка при логировании: {e}")