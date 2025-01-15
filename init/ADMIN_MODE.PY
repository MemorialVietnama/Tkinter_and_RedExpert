import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import fdb
import sys
from pathlib import Path
from tkinter import ttk, messagebox
from fontTools.ttLib import TTFont
from tkinter import font as tkFont
from datetime import datetime



# Получаем текущую директорию скрипта
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(project_root.as_posix())


role = "Admin"
def load_custom_font(font_path, font_name):
    try:
        font_obj = TTFont(font_path)
        font_obj.save(font_path)
        tkFont.Font(font=font_name, family=font_path)
    except FileNotFoundError:
        pass  
    except Exception as e:
        print(f"Ошибка при загрузке шрифта: {e}")

def custom_font():

    current_dir = Path(__file__).resolve().parent
    app_dir = current_dir.parents[3] / 'App'
    font_path_header = app_dir / 'font' / 'gothampro_bold.ttf'
    font_path_text = app_dir / 'font' / 'TT Travels Next Trial Bold.ttf'
    if font_path_header.exists():
        load_custom_font(font_path_header, 'CustomHeaderFont')

    if font_path_text.exists():
        load_custom_font(font_path_text, 'CustomTextFont')

current_dir = Path.cwd()  # Устанавливаем текущий рабочий каталог

def display_employer():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", (current_dir / 'tables' / "EMPLOYER.py").as_posix(), username, password, role])

def display_employer_list():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", (current_dir / 'tables' / "EMPLOYER_LIST.py").as_posix(), username, password, role])

def display_department():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", (current_dir / 'tables' / "DEPARTMENT.py").as_posix(), username, password, role])

def display_proffesion():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", (current_dir / 'tables' / "PROFFESION.py").as_posix(), username, password, role])

def display_facator_information():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", (current_dir / 'tables' / "factor_information.py").as_posix(), username, password, role])

def display_benefit():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", (current_dir / 'tables' / "benefit.py").as_posix(), username, password, role])

def display_document():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", (current_dir / 'tables' / "DOCUMENTS.py").as_posix(), username, password, role])

def display_workshulder():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", (current_dir / 'tables' / "WORK_SHULDER.py").as_posix(), username, password, role])

def display_posts():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", (current_dir / 'tables' / "POSTS.py").as_posix(), username, password, role])

def display_sovmest():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", (current_dir / 'tables' / "sovmest.py").as_posix(), username, password, role])
current_table = None

def connect_to_database(username, password):
    try:
        current_dir = Path(__file__).resolve().parent
        database_path = current_dir.parents[0] / 'kadrbase.fdb'
        
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
    
def get_user_data(username, password, user_login):
    conn = connect_to_database(username, password)
    if conn:
        cursor = conn.cursor()
        cursor.execute("EXECUTE PROCEDURE GET_USER_DATA(?)", (user_login,))
        user_data = cursor.fetchone()
        conn.close()
        return user_data
    return None
def fetch_user_logs(username, password):
    conn = connect_to_database(username, password)
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USER_LOGS")  # Adjust the query as needed
        logs = cursor.fetchall()
        conn.close()
        return logs
    return []
def update_treeview(username, password, role):
    for row in treeview.get_children():
        treeview.delete(row)

    logs = fetch_user_logs(username, password)
    for log in logs:
        treeview.insert("", "end", values=log)

def sort_treeview(column, reverse):
    data = [(treeview.set(child, column), child) for child in treeview.get_children('')]
    data.sort(reverse=reverse)

    for index, (val, child) in enumerate(data):
        treeview.move(child, '', index)

    treeview.heading(column, command=lambda: sort_treeview(column, not reverse))

def open_search_window():
    search_window = tk.Toplevel(admin_window)
    search_window.title("Поиск данных")
    search_window.geometry("350x250")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[0] / 'src' / 'r_app.ico'
    search_window.iconbitmap(icon_path)
    
    ttkb.Label(search_window, text="Выберите столбец:", bootstyle="light").pack(pady=5)

    column_combobox = ttkb.Combobox(search_window, bootstyle="primary", values=["ID", "Время", "Действия", "Таблица", "Информация"])
    column_combobox.pack(pady=5)

    ttkb.Label(search_window, text="Введите значение для поиска:", bootstyle="light").pack(pady=5)
    

    search_entry = ttkb.Entry(search_window, bootstyle="primary")
    search_entry.pack(pady=5)

    date_entry = ttkb.DateEntry(search_window, bootstyle="primary", width=12)
    date_entry.pack(pady=5)
    date_entry.pack_forget()  


    def perform_search():
        column = column_combobox.get()
        for row in treeview.get_children():
            treeview.delete(row)

        conn = connect_to_database(username, password)
        if conn:
            cursor = conn.cursor()
            if column == "Время":
                search_value = date_entry.entry.get()  #
                print("Search value: ", search_value)
                search_value = datetime.strptime(search_value, "%d.%m.%Y")
                print("Измененная строка:", search_value)
                start_of_day = datetime.combine(search_value, datetime.min.time())
                end_of_day = datetime.combine(search_value, datetime.max.time())
                print("Start: ", start_of_day, " ", "End: ", end_of_day )
                query = "SELECT * FROM USER_LOGS WHERE LOG_TIME >= ? AND LOG_TIME <= ?"
                cursor.execute(query, (start_of_day, end_of_day))
            elif column == "ID":
                search_value = search_entry.get()
                try:
                    search_value = int(search_value) 
                    query = "SELECT * FROM USER_LOGS WHERE ID = ?"
                    cursor.execute(query, (search_value,))
                except ValueError:
                    messagebox.showerror("Ошибка", "ID должен быть числом")
                    return
            elif column == "Информация":
                query = "SELECT * FROM USER_LOGS WHERE ADDITIONAL_INFO LIKE ?"
                search_value = search_entry.get()
                cursor.execute(query, (f'%{search_value}%',))
            else:
                search_value = search_entry.get()
                if column == "Действия":
                    query = "SELECT * FROM USER_LOGS WHERE ACTION LIKE ?"
                elif column == "Таблица":
                    query = "SELECT * FROM USER_LOGS WHERE TABLE_NAME LIKE ?"
                else:
                    search_window.destroy()
                    return
                
                cursor.execute(query, (f'%{search_value}%',))

            results = cursor.fetchall()
            conn.close()

            for result in results:
                treeview.insert("", "end", values=result)
            
        search_window.destroy()
    def update_entry_visibility(event):
        if column_combobox.get() == "Время":
            search_entry.pack_forget()  
            date_entry.pack(pady=5)  
        else:
            date_entry.pack_forget()  
            search_entry.pack(pady=5)  

    column_combobox.bind("<<ComboboxSelected>>", update_entry_visibility)
    search_button = ttkb.Button(search_window, bootstyle="primary", text="Поиск", command=perform_search)
    search_button.pack(pady=10)
    search_window.focus_set()
    search_window.update_idletasks()
    width = search_window.winfo_width()
    height = search_window.winfo_height()
    x = (search_window.winfo_screenwidth() // 2) - (width // 2)
    y = (search_window.winfo_screenheight() // 2) - (height // 2)
    search_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

if len(sys.argv) != 4:
    messagebox.showinfo("Ошибка", "Неверное количество аргументов")
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]
user_login = sys.argv[1]

user_data = get_user_data(username, password, user_login)

if user_data:
    user_name, first_name, middle_name, last_name = user_data
else:
    messagebox.showinfo("Ошибка", "Данные о пользователе не найдены")
    sys.exit(1)



admin_window = ttkb.Window(themename="simplex_2")
admin_window.title(f"RUBY STAFF - Сотрудник: {first_name} {middle_name} {last_name}             Авторизован как: {user_name}")
admin_window.state('zoomed') 
admin_window.geometry(f"{admin_window.winfo_screenwidth()}x{admin_window.winfo_screenheight()}")
current_dir = Path(__file__).resolve().parent
    # Поднимаемся на две папки вверх и переходим в директорию src
icon_path = current_dir.parents[0] / 'src' / 'r_app.ico'
admin_window.iconbitmap(icon_path)

background_image = Image.open(current_dir.parents[0] / 'src' / 'header-bg-big.jpg')
background_image = background_image.resize((admin_window.winfo_screenwidth(), admin_window.winfo_screenheight()), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(admin_window, image=background_photo)
background_label.place(relwidth=1, relheight=1)

custom_font()
custom_font_header = ('CustomHeaderFont', 14, 'bold')
custom_font_text =  ('CustomTextFont', 34, 'bold')
custom_font_entry = ('CustomTextFont', 14)
custom_font_buttom = ("CustomTextFont", 24, "bold")
custom_font_status = ("CustomTextFont", 20, "bold")

center_frame = ttk.Frame(admin_window, width=600)
center_frame.pack(side="right", fill="both", expand=True, padx=(10,50))

left_frame = tk.Frame(admin_window, width=600)
left_frame.pack(side="left",  fill="y", pady=(160, 250), padx=40)

ad_label_image = Image.open(current_dir.parents[0] / 'src' / 'admin_label.png')
ad_label_image = ad_label_image.resize((200, 60), Image.Resampling.LANCZOS)
ad_label_photo = ImageTk.PhotoImage(ad_label_image)
ad_label_label = tk.Label(admin_window, image=ad_label_photo)
ad_label_label.place(x=200, y=50)  

tables = [
    ("Список Сотрудников", display_employer_list),
    ("Сотрудник", display_employer),
    ("Отделы", display_department),
    ("Професcии", display_proffesion),
    ("Информация о Предприятии", display_facator_information),
    ("Льготы", display_benefit),
    ("Совместительство", display_sovmest),
    ("Документация", display_document),
    ("Посты обновлений", display_posts),
]


for table_name, command in tables:
    tk.Button(left_frame, bg="#c61b14", fg="#ffffff", font=("CustomTextFont", 20, "bold"), text=table_name, command=command).pack(pady=1, fill="x")

center_label = ttk.Label(center_frame, font=custom_font_text, text="Журнал Аудита", bootstyle="light")
center_label.pack(pady=10, anchor="center")

button_table = tk.Frame(center_frame, width=600)
button_table.pack(pady=10, anchor='n')  

refresh_button = ttkb.Button(button_table, bootstyle="primary", text="Обновить Журнал", command=lambda: update_treeview(username, password, role))
refresh_button.pack(side="left", padx=5)

find_button = ttkb.Button(button_table, bootstyle="primary", text="Найти", command=open_search_window)
find_button.pack(side="left", padx=5)


treeview = ttk.Treeview(center_frame, bootstyle="primary", selectmode="extended", columns=("ID", "Время", "Действия", "Таблица", "Информация"), show='headings')


column_widths = [50, 200, 300, 150, 550]  
for col, width in zip(("ID", "Время", "Действия", "Таблица", "Информация"), column_widths):
    treeview.heading(col, text=col, command=lambda c=col: sort_treeview(c, False))
    treeview.column(col, width=width, stretch=False)  


scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=treeview.yview)
scrollbar.pack(side="right", fill="y", padx=10)

treeview.configure(yscrollcommand=scrollbar.set)

treeview.pack(fill="both", expand=True)


update_treeview(username, password, role)

style = ttk.Style()
style.configure('TButton', font=('CustomTextFont', 20, 'bold'))

admin_window.mainloop()