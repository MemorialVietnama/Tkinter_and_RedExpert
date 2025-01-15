import tkinter as tk
from tkinter import ttk, messagebox
import fdb
import sys
import subprocess
from pathlib import Path
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from fontTools.ttLib import TTFont
from tkinter import font as tkFont
import tkinter as tk
from tkinter import ttk

role = "User"

# Добавляем корневую директорию проекта в sys.path
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))

def translate_post_columns(columns):
    translation_dict = {
        "TITLE": "Заголовок",
        "DESCRIPTION": "Описание",
        "AUTHOR": "Автор",
        "DATE_POSTS": "Дата публикации"
    }
    return [translation_dict.get(col, col) for col in columns]
def connect_to_database(username, password):
    try:
        # Получаем путь к текущей директории
        current_dir = Path(__file__).resolve().parent
        
        # Создаем относительный путь к базе данных
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
        messagebox.showinfo("Ошибка", f"Ошибка подключения к базе данных: {e}")
        return None
    
def fetch_posts(username, password):
    conn = connect_to_database(username, password)
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT TITLE, DESCRIPTION, AUTHOR, DATE_POSTS FROM POSTS ORDER BY DATE_POSTS DESC")
        posts = cursor.fetchall()
        conn.close()
        return posts
    return []
def get_user_data(username, password, user_login):
    conn = connect_to_database(username, password)
    if conn:
        cursor = conn.cursor()
        cursor.execute("EXECUTE PROCEDURE GET_USER_DATA(?)", (user_login,))
        user_data = cursor.fetchone()
        conn.close()
        return user_data
    return None

def display_employer():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", str(current_dir / 'tables' / "EMPLOYER.py"), username, password, role])

def display_employer_list():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", str(current_dir / 'tables' / "EMPLOYER_LIST.py"), username, password, role])

def display_department():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", str(current_dir / 'tables' / "DEPARTMENT.py"), username, password, role])

def display_proffesion():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", str(current_dir / 'tables' / "PROFFESION.py"), username, password, role])

def display_facator_information():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", str(current_dir / 'tables' / "factor_information.py"), username, password, role])

def display_benefit():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", str(current_dir / 'tables' / "benefit.py"), username, password, role])

def display_document():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", str(current_dir / 'tables' / "DOCUMENTS.py"), username, password, role])

def display_sovmest():
    global current_table
    if current_table:
        current_table.terminate()
    current_table = subprocess.Popen(["python", str(current_dir / 'tables' / "sovmest.py"), username, password, role])



def display_posts(username, password):
    posts = fetch_posts(username, password)
    print(posts)
    for post in posts:
        post_frame = tk.Frame(canvas_frame)
        post_frame.pack(fill="x", padx=(0,20), pady=(0,10))

        title_label = ttk.Button(post_frame, style='Custom.TButton', text=post[0])
        title_label.pack(anchor="center", pady=0, fill="x")

        desk_font = custom_font_entry
        description_text = tk.Text(post_frame, font=desk_font, wrap="word", height=10, relief="flat")
        description_text.insert("1.0", post[1])
        description_text.config(state="disabled", bg='#131313', fg='#e5e5e5', borderwidth=0, font=desk_font)  # Запрещаем редактирование
        description_text.pack(anchor="w", fill="x")

        date_font = custom_font_status
        # Форматируем объект datetime.date
        formatted_date = post[3].strftime("%d %B %Y года")
        date_author_label = ttk.Button(post_frame, style='Custom.TButton', text=f"Автор: {post[2]} | Дата: {formatted_date}")
        date_author_label.pack(anchor="w")


    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

current_table = None
button_frame = None

if len(sys.argv) != 4:
    messagebox.showerror("Ошибка", "Неверное количество аргументов")
    sys.exit(1)

username = sys.argv[1]  # username должен быть вторым аргументом
password = sys.argv[2]  # password должен быть третьим аргументом
user_login = username    # user_login может оставаться username
role = sys.argv[3]      # role должен быть четвёртым аргументом

user_data = get_user_data(username, password, user_login)

if user_data:
    user_name, first_name, middle_name, last_name = user_data
else:
    messagebox.showerror("Ошибка", "Данные о пользователе не найдены")
    sys.exit(1)

# Получаем путь к текущей директории
current_dir = Path(__file__).resolve().parent

# Устанавливаем соединение с базой данных
conn = connect_to_database(username, password)
if not conn:
    messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных")
    sys.exit(1)

admin_window = ttkb.Window(themename="simplex_3")
admin_window.title(f"RUBY STAFF - Сотрудник: {first_name} {middle_name} {last_name}             Авторизован как: {user_name}")
admin_window.state('zoomed') 
admin_window.configure(bg="black")
admin_window.geometry(f"{admin_window.winfo_screenwidth()}x{admin_window.winfo_screenheight()}")
icon_path = current_dir.parent / 'src' / 'r_app.ico'
admin_window.iconbitmap(icon_path)

background_image = Image.open(current_dir.parent / 'src' / 'header-bg-big.jpg')
background_image = background_image.resize((admin_window.winfo_screenwidth(), admin_window.winfo_screenheight()), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(admin_window, image=background_photo)
background_label.place(relwidth=1, relheight=1)

def load_custom_font(font_path, font_name):
    try:
        font_obj = TTFont(font_path)
        font_obj.save(font_path)
        tkFont.Font(font=font_name, family=font_path)
        print(f"Шрифт {font_name} успешно загружен.")
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
custom_font()
custom_font_header = ('CustomHeaderFont', 14, 'bold')
custom_font_text =  ('CustomTextFont', 34, 'bold')
custom_font_entry = ('CustomTextFont', 14)
custom_font_buttom = ("CustomTextFont", 24, "bold")
custom_font_status = ("CustomTextFont",20,"bold")

left_frame = tk.Frame(admin_window, width=600)
left_frame.pack(side="left",  fill="y", pady=(160,440), padx=40)

ad_label_image = Image.open(current_dir.parent / 'src' / 'admin_label.png')
ad_label_image = ad_label_image.resize((200, 60), Image.Resampling.LANCZOS)
ad_label_photo = ImageTk.PhotoImage(ad_label_image)
ad_label_label = tk.Label(admin_window, image=ad_label_photo)
ad_label_label.place(x=200, y=50)  
tables = [
    ("Список Сотрудников", display_employer_list),
    ("Сотрудник", display_employer),
    ("Отделы", display_department),
    ("Профеcсии", display_proffesion),
    ("Льготы", display_benefit),
    ("Совместительство", display_sovmest),
    ("Документация", display_document),
]


for table_name, command in tables:
    tk.Button(left_frame, bg="#c61b14", width=30, fg="#ffffff", font=("CustomTextFont", 20, "bold"), text=table_name, command=command).pack(pady=1, fill="x")

center_label = ttk.Label(admin_window, font=custom_font_text, text="НОВОСТИ И ОБНОВЛЕНИЯ", bootstyle="light")
center_label.pack(pady=(20,0), anchor="center")

center_frame = tk.Frame(admin_window)
center_frame.pack(side="right", fill="both", expand=True, padx=(150,40), pady=(50,0))

custom_style = ttkb.Style(theme="simplex_3")
custom_style.configure('Custom.TButton', font=('CustomTextFont', 18, 'bold'))


canvas = tk.Canvas(center_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(center_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y", padx=(50,0))

canvas.configure(yscrollcommand=scrollbar.set)

canvas_frame = tk.Frame(canvas)
canvas.create_window((0, 0), width=1000, window=canvas_frame, anchor="nw")


display_posts(username, password)

admin_window.mainloop()

conn.close()