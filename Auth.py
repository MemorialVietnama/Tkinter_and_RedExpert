import tkinter as tk
from tkinter import messagebox
import fdb
import subprocess
import tkinter as tk
from PIL import Image, ImageTk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from fontTools.ttLib import TTFont
from tkinter import font as tkFont
from pathlib import Path

# путь к текущей директории
current_dir = Path(__file__).resolve().parent

# Путь к базе данных
database_path = current_dir / 'KADRBASE.FDB'
print(f"Database path: {database_path}")
ok_button_pressed = False

def login():
    username = entry_username.get()
    password = entry_password.get()

    try:
        database_path =  current_dir / 'KADRBASE.FDB'

        print(database_path)
        conn = fdb.connect(
            host='localhost',
            database=database_path,
            user=username,
            password=password,
            port=3050,
            charset='utf8'
        )

        cursor = conn.cursor()

        # проверка ролей
        cursor.execute("""
            SELECT DISTINCT RDB$RELATION_NAME 
            FROM RDB$USER_PRIVILEGES 
            WHERE RDB$USER = ? 
            AND RDB$PRIVILEGE = 'M'
            AND RDB$RELATION_NAME NOT LIKE 'RDB$%'
        """, (username.strip().upper(),))
        
        roles = [row[0].strip() for row in cursor.fetchall()]
        conn.close()
        if 'ADMINISTRATOR_APP' in roles:
            role = "Admin"
            messagebox.showinfo("Успех", f"Авторизация успешна! \n Вы авторизовались как {username} \n Вы авторизовались как Администратор")
            login_window.destroy()
            subprocess.Popen(["python", str(current_dir / "init" / 'ADMIN_MODE.py'), username, password, role])
        elif 'EMPLOYER_APP' in roles:
            role = "User"
            messagebox.showinfo("Успех", f"Авторизация успешна! \n Вы авторизовались как {username} \n Вы авторизовались как Пользователь")
            login_window.destroy()
            subprocess.Popen(["python", str(current_dir / "init" /'USER_MODE.py'), username, password, role])
        else:
            messagebox.showwarning("Ошибка", "Пользователь не имеет подходящей роли.")
    except fdb.Error as e:
        messagebox.showwarning("Ошибка", f"Неверное имя пользователя или пароль: {e}")

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

    app_dir = current_dir.parents[0] / 'App'
    print("APP_DIR", app_dir)


    font_path_header = app_dir / 'font' / 'gothampro_bold.ttf'
    font_path_text = app_dir / 'font' / 'TT Travels Next Trial Bold.ttf'

    if font_path_header.exists():
        load_custom_font(font_path_header, 'CustomHeaderFont')

    if font_path_text.exists():
        load_custom_font(font_path_text, 'CustomTextFont')

def auto_connect():
    try:
        database_path =  current_dir / 'KADRBASE.FDB'
        conn = fdb.connect(
            host='localhost',
            database=database_path,
            user='GUEST', #Отрублено все кроме проверки подключения
            password='010802',
            port=3050,
            charset='utf8'  
        )
        conn.close()
        status_label.config(text="Соединение установлено")
        status_label.config(font=custom_font_status)
    except fdb.Error as e:
        print(f"{e}")
        status_label.config(text=f"Ошибка подключения к базе данных: {e}")
        status_label.config(font=custom_font_status)


current_dir = Path(__file__).resolve().parent

icon_path = current_dir / 'src' / 'r_app.ico'

login_window = ttkb.Window(themename="simplex")
login_window.title("RUBY STAFF") 
login_window.geometry(f"{login_window.winfo_screenwidth()}x{login_window.winfo_screenheight()}")
login_window.state('zoomed') 
login_window.configure(bg="#f0f0f0")
login_window.iconbitmap(icon_path)
background_image = Image.open(current_dir / 'src' / 'header-bg-big.jpg')
background_image = background_image.resize((login_window.winfo_screenwidth(), login_window.winfo_screenheight()), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(login_window, image=background_photo)
background_label.place(relwidth=1, relheight=1)

custom_font()
custom_font_header = ('CustomHeaderFont', 14, 'bold')
custom_font_text =  ('CustomTextFont', 34, 'bold')
custom_font_entry = ('CustomTextFont', 14)
custom_font_buttom = ("CustomTextFont", 24, "bold")
custom_font_status = ("CustomTextFont",20,"bold")


canvas = tk.Canvas(login_window, bg="#f0f0f0", highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

# бэкраунд
canvas.create_image(0, 0, anchor="nw", image=background_photo)

text_id = canvas.create_text(login_window.winfo_screenwidth() // 1.97, login_window.winfo_screenheight() // 2.8, 
                   text="Авторизуйтесь", font=custom_font_text, fill="#c61b14", anchor="e")

canvas.create_text(login_window.winfo_screenwidth() // 2.65, login_window.winfo_screenheight() // 2.46, 
                   text="Отдел Кадров", font=custom_font_header, fill="#FFFFFF", anchor="e")


canvas.create_text(login_window.winfo_screenwidth() // 2, login_window.winfo_screenheight() // 2.46, 
                   text="НПО Примарис", font=custom_font_header, fill="#c61b14", anchor="e")

# Entry
style = ttkb.Style()
style.configure('Custom.TEntry', padding=10) 

place_text_user = "Имя пользователя"
place_text_password = "Пароль"

def add_placeholder_user(event=None):
    if entry_username.get() == "":
        entry_username.insert(0, place_text_user)
        entry_username.config(show="")
def remove_placeholder_user(event=None):
    if entry_username.get() == place_text_user:
        entry_username.delete(0,tk.END)
        entry_username.config(show="")

def add_placeholder(event=None):
    if entry_password.get() == "":
        entry_password.insert(0, place_text_password)
        entry_password.config(show="")
def remove_placeholder(event=None):
    if entry_password.get() == place_text_password:
        entry_password.delete(0, tk.END)
        entry_password.config(show="*")

entry_username = ttkb.Entry(login_window, width=32, font=custom_font_entry, bootstyle="primary", style='Custom.TEntry')
entry_username.insert(0, place_text_user)
entry_username.bind("<FocusIn>", remove_placeholder_user)
entry_username.bind("<FocusOut>", add_placeholder_user)

entry_password = ttkb.Entry(login_window, width=32, show="*", font=custom_font_entry, bootstyle="primary", style='Custom.TEntry')
entry_password.insert(0, place_text_password)
entry_password.bind("<FocusIn>", remove_placeholder)
entry_password.bind("<FocusOut>", add_placeholder)

# По середине
entry_username.place(x=login_window.winfo_screenwidth() // 2 - 400, y=login_window.winfo_screenheight() // 2  - 70)
entry_password.place(x=login_window.winfo_screenwidth() // 2 - 400, y=login_window.winfo_screenheight() // 2 )

# Получение ширины текста "Авторизуйтесь"
text_width = 230
button_login = ttkb.Button(login_window, text="Войти", command=login, bootstyle="primary",)
button_login.config(width=text_width // 12)  
button_login.place(relx=0.405, rely=0.65, anchor="center")

status_label = ttkb.Label(bootstyle="inverse-dark")
status_label.place(relx=0.4, rely=0.72, anchor="center")
auto_connect()

style = ttkb.Style()
style.configure('TButton', font=custom_font_buttom)


laptop_image = Image.open(current_dir / 'src' / 'laptops-icons.png')
laptop_image = laptop_image.resize((500, 500), Image.Resampling.LANCZOS)
laptop_photo = ImageTk.PhotoImage(laptop_image)


canvas.create_image(login_window.winfo_screenwidth() -250, login_window.winfo_screenheight() // 2, anchor="e", image=laptop_photo)


company_image = Image.open(current_dir / 'src' / 'company_logo.png')
company_image = company_image.resize((130, 50), Image.Resampling.LANCZOS)
company_photo = ImageTk.PhotoImage(company_image)


canvas.create_image(login_window.winfo_screenwidth() - 1200, login_window.winfo_screenheight() - 750, anchor="e", image=company_photo)


app_image = Image.open(current_dir  / 'src' / 'app_logo.png')
app_image = app_image.resize((130, 50), Image.Resampling.LANCZOS)
app_photo = ImageTk.PhotoImage(app_image)


canvas.create_image(login_window.winfo_screenwidth() - 1000, login_window.winfo_screenheight() - 750, anchor="e", image=app_photo)

login_window.mainloop()