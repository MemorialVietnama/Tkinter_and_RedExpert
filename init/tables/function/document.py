from tkinter import *
from tkinter import messagebox, filedialog
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import fitz  # PyMuPDF
import tempfile
import textwrap
from datetime import datetime
from pathlib import Path
import sys
import os
from tkinter import ttk

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fdb

# Добавляем корневую директорию проекта в sys.path
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))

pdfmetrics.registerFont(TTFont('Times-New-Roman', 'times.ttf'))

def fetch_factor_information(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT SMALL_NAME, FULL_NAME FROM FACTOR_INFORMATION")
    factor_info = cursor.fetchone()
    cursor.close()
    return factor_info

def get_factor_information(conn):
    return fetch_factor_information(conn)

def create_pdf(output_filename, data, tree, user_data):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    image_path = current_dir.parents[2] / 'src' / 'r_app.png'
    img = ImageReader(str(image_path))
    c.drawImage(img, 1 * inch, height - 1 * inch, width=0.5 * inch, height=0.5 * inch)

    c.setFont("Times-New-Roman", 8)
    c.drawString(1.55 * inch, height - 0.65 * inch, "RUBY STAFF")
    c.drawString(3.5 * inch, height - 2 * inch, "Вывод данных")

    # Вывод данных из базы
    y_position = height - 0.9 * inch
    for row in data:
        row_text = ", ".join([str(item) for item in row])
        wrapped_text = textwrap.wrap(row_text, width=80)  
        for line in wrapped_text:
            c.drawString(1.55 * inch, y_position, line)
            y_position -= 0.2 * inch
        y_position -= 0.3 * inch  

    # Вывод данных из TreeView
    y_position = y_position - 0.5 * inch
    c.setFont("Times-New-Roman", 8)
    for item in tree.get_children():
        values = tree.item(item)['values']
        row_text = ", ".join([str(value) for value in values])
        wrapped_text = textwrap.wrap(row_text, width=80)  
        for line in wrapped_text:
            c.drawString(1.55 * inch, y_position, line)
            y_position -= 0.2 * inch
        y_position -= 0.3 * inch  

    c.setFont("Times-New-Roman", 10)
    c.drawString(1.55 * inch, y_position, f"Оформил: {user_data}")
    y_position -= 0.2 * inch
    current_time = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
    c.drawString(1.55 * inch, y_position, f"Время: {current_time}")

    c.showPage()
    c.save()

def create_pdf_for_selected_row(output_filename, selected_row, user_data, conn):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    image_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    img = ImageReader(str(image_path))
    c.drawImage(img, 1 * inch, height - 1 * inch, width=0.5 * inch, height=0.5 * inch)
    factor_info = get_factor_information(conn)
    if factor_info:
        factor_small_name, factor_full_name = factor_info
    else:
        factor_small_name = factor_full_name = "Неизвестно"

    c.setFont("Times-New-Roman", 8)
    c.drawString(1.55 * inch, height - 0.65 * inch, "RUBY STAFF")
    c.drawString(1.55 * inch, height - 0.8 * inch, factor_full_name)
    y_position = height - 2 * inch
    row_text = ", ".join([str(item) for item in selected_row])
    data_parts = row_text.split(", ")
    if len(data_parts) >= 19:
        small_name = data_parts[1]
        surname = data_parts[2]
        name = data_parts[3]
        surname_father = data_parts[4]
        pol = data_parts[5]
        inn = data_parts[6]
        snils = data_parts[7]
        data_birth = data_parts[8]
        date_city = data_parts[9]
        type_doc = data_parts[10]
        doc_num = data_parts[11]
        doc_date = data_parts[12]
        doc_were = data_parts[13]
        adress_regist = data_parts[14] + " " + data_parts[15]
        adress_propiska = data_parts[16] + " " + data_parts[17]
        military_num = data_parts[18]
        military_date = data_parts[19]
        education =data_parts[20]
    else:
        small_name = surname = name = surname_father = pol = inn = snils = data_birth = date_city = type_doc = doc_num = doc_date = doc_were = adress_regist = adress_propiska = military_num = military_date = education = "Неизвестно"

    # Вывод каждой переменной отдельной строкой
    variables = [
        ("Фамилия", surname),
        ("Имя", name),
        ("Отчество", surname_father),
        ("Пол", pol),
        ("ИНН", inn),
        ("СНИЛС", snils),
        ("Дата рождения", data_birth),
        ("Город рождения", date_city),
        ("Тип документа", type_doc),
        ("Номер документа", doc_num),
        ("Дата выдачи документа", doc_date),
        ("Место выдачи документа", doc_were),
        ("Адрес регистрации", adress_regist),
        ("Адрес прописки", adress_propiska),
        ("Военный билет", military_num),
        ("Дата выдачи военного билета", military_date),
        ("Образование", education),
    ]
    print(variables)
    c.setFont("Times-New-Roman", 14)
    c.drawString(2 * inch, height - 1.5 * inch, f"Вывод данных сотрудника {small_name}")
    c.setFont("Times-New-Roman", 10)
    for label, value in variables:
        line = f"{label}: {value}"
        wrapped_text = textwrap.wrap(line, width=80)  
        for wrapped_line in wrapped_text:
            c.drawString(1.55 * inch, y_position, wrapped_line)
            y_position -= 0.2 * inch
        y_position -= 0.01 * inch 

    c.setFont("Times-New-Roman", 14)
    c.drawString(1.55 * inch, y_position, f"Оформил: {user_data}")
    y_position -= 0.2 * inch
    current_time = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
    c.drawString(1.55 * inch, y_position, f"Время: {current_time}")

    c.showPage()
    c.save()

def connect_to_database(username, password):
    try:
        database_path = current_dir.parent.parent / 'kadrbase.fdb'
        database_path = database_path.resolve()
        
        conn = fdb.connect(
            host='localhost',
            database=str(database_path),
            user=username,
            password=password,
            port=3050,
            charset='utf8'
        )
        return conn
    except fdb.Error as e:
        print("Ошибка")
        return None


def generate_pdf(conn, user_data, output_filename="output.pdf"):
    factor_info = get_factor_information(conn)
    small_name, full_name = factor_info

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM FACTOR_INFORMATION")
    data = cursor.fetchall()
    cursor.close()

    create_pdf(output_filename, data, user_data)

def generate_pdf_for_selected_row(conn, user_data, selected_row, output_filename="output_selected.pdf"):
    create_pdf_for_selected_row(output_filename, selected_row, user_data, conn)

def full_output_form(conn, tree, user_data):
    def confirm_output():
        confirm_window.destroy()
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM FACTOR_INFORMATION")
        data = cursor.fetchall()
        cursor.close()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf_path = temp_pdf.name

        create_pdf(temp_pdf_path, data, tree, user_data)

        pdf_viewer = Toplevel()
        pdf_viewer.title("Просмотр PDF")
        pdf_viewer.geometry("800x600")
        icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
        pdf_viewer.iconbitmap(str(icon_path))

        button_frame = Frame(pdf_viewer)
        button_frame.pack(side="bottom", pady=10)

        def save_pdf():
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if save_path:
                try:
                    with open(temp_pdf_path, 'rb') as src, open(save_path, 'wb') as dst:
                        dst.write(src.read())
                    os.remove(temp_pdf_path)
                    pdf_viewer.destroy()
                    messagebox.showinfo("Успех!", "Файд был успешно создан и сохранен!")
                except PermissionError:
                    messagebox.showerror("Ошибка", "Не удалось сохранить файл из-за ошибки доступа. Попробуйте сохранить в другое место.")

        def exit_pdf():
            os.remove(temp_pdf_path)
            pdf_viewer.destroy()

        ttkb.Button(button_frame, bootstyle="primary", text="Сохранить", command=save_pdf).pack(side="left", padx=10)
        ttkb.Button(button_frame, bootstyle="primary", text="Выйти", command=exit_pdf).pack(side="right", padx=10)

        display_pdf(pdf_viewer, temp_pdf_path)

    confirm_window = Toplevel()
    confirm_window.title("Подтверждение")
    confirm_window.geometry("300x300")
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    confirm_window.iconbitmap(str(icon_path))

    ttk.Label(confirm_window, wraplength=200, foreground="#c61b14", font=("Times New Roman", 14), text="Вы уверены, что хотите вывести все данные?").pack(pady=10)
    ttkb.Button(confirm_window, bootstyle="primary", text="Да", command=confirm_output).pack(side=LEFT, padx=50)
    ttkb.Button(confirm_window, bootstyle="primary", text="Нет", command=confirm_window.destroy).pack(side=RIGHT, padx=50)

def confirm_output_selected_row(conn, tree, user_data, username, password):
    def confirm_output():
        confirm_window.destroy()
        
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите строку для вывода.")
            return

        selected_row = tree.item(selected_item)['values']

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf_path = temp_pdf.name

        generate_pdf_for_selected_row(conn, user_data, selected_row, temp_pdf_path)

        pdf_viewer = Toplevel()
        pdf_viewer.title("Просмотр PDF")
        pdf_viewer.geometry("800x600")
        icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
        pdf_viewer.iconbitmap(str(icon_path))

        button_frame = Frame(pdf_viewer)
        button_frame.pack(side="bottom", pady=10)

        def save_pdf():
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if save_path:
                try:
                    with open(temp_pdf_path, 'rb') as src, open(save_path, 'wb') as dst:
                        dst.write(src.read())
                    os.remove(temp_pdf_path)
                    pdf_viewer.destroy()
                    messagebox.showinfo("Успех!", "Файд был успешно создан и сохранен!")
                except PermissionError:
                    messagebox.showerror("Ошибка", "Не удалось сохранить файл из-за ошибки доступа. Попробуйте сохранить в другое место.")

        def exit_pdf():
            os.remove(temp_pdf_path)
            pdf_viewer.destroy()

        ttkb.Button(button_frame, bootstyle="primary", text="Сохранить", command=save_pdf).pack(side="left", padx=10)
        ttkb.Button(button_frame, bootstyle="primary", text="Выйти", command=exit_pdf).pack(side="right", padx=10)

        display_pdf(pdf_viewer, temp_pdf_path)

    confirm_window = Toplevel()
    confirm_window.title("Подтверждение")
    confirm_window.geometry("300x300")
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    confirm_window.iconbitmap(str(icon_path))

    ttk.Label(confirm_window, wraplength=200, foreground="#c61b14", font=("Times New Roman", 14), text="Вы уверены, что хотите вывести выбранную строку?").pack(pady=10)
    ttkb.Button(confirm_window, bootstyle="primary", text="Да", command=confirm_output).pack(side=LEFT, padx=50)
    ttkb.Button(confirm_window, bootstyle="primary", text="Нет", command=confirm_window.destroy).pack(side=RIGHT, padx=50)

def display_pdf(parent, pdf_path):
    canvas = Canvas(parent, width=800, height=600)
    canvas.pack(fill="both", expand=True)

    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = PhotoImage(data=pix.tobytes("ppm"))
        canvas.create_image(0, 0, image=img, anchor="nw")
        canvas.image = img
        canvas.update()