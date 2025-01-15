import fdb
from pathlib import Path
from tkinter import messagebox
def connect_to_database(username, password):
    try:
        current_dir = Path(__file__).resolve().parent
        database_path = current_dir.parents[2] / 'kadrbase.fdb'
        
        conn = fdb.connect(
            host='localhost',
            database=database_path,
            user=username,
            password=password,
            port=3050,
            charset='utf8'
        )
        return conn
    except fdb.Error as e:
        messagebox.showinfo("Ошибка", "Подключение не доступно")
        return None