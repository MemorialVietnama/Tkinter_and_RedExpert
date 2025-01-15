from tkinter import *
from ttkbootstrap.constants import *
from tkinter import messagebox
import fdb
from pathlib import Path
import ttkbootstrap as ttkb

from tables.function.translate_colums import *
from tables.button_function.refresh_button import *

def open_search_employer_window(conn, columns, tree):
    def search_employer():
        selected_column_translated = column_var.get()
        search_value = search_entry.get()

        if not search_value:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите значение для поиска")
            return

        column_mapping = {translated_columns[i]: columns[i] for i in range(len(columns))}
        selected_column = column_mapping[selected_column_translated]

        if selected_column == "POL":
            search_value = search_value[:1]

        try:
            cursor = conn.cursor()
            if selected_column in ["POL", "TYPE_DOC", "EDUCATION"]:
                search_query = f"SELECT * FROM EMPLOYER WHERE {selected_column} = ?"
                cursor.execute(search_query, (search_value,))
            else:
                search_query = f"SELECT * FROM EMPLOYER WHERE {selected_column} LIKE ?"
                cursor.execute(search_query, (f"%{search_value}%",))

            search_results = cursor.fetchall()
            cursor.close()

            if not search_results:
                messagebox.showinfo("Результаты поиска", "Ничего не найдено")
            else:
                refresh_emp_table( conn, tree, search_results,)

        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")
            print("Ошибка", f"Ошибка поиска: {e}")

    search_window = Toplevel()
    search_window.title("Поиск сотрудника")
    search_window.geometry("300x300")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    search_window.iconbitmap(icon_path)

    translated_columns = translate_emp_columns(columns)
    column_var = StringVar()
    column_var.set(translated_columns[0])

    column_label = ttkb.Label(search_window, bootstyle='primary', text="Выберите столбец:")
    column_label.pack(pady=5)

    column_combobox = ttkb.Combobox(search_window, textvariable=column_var, values=translated_columns, bootstyle='primary')
    column_combobox.pack(pady=5)

    search_label = ttkb.Label(search_window, bootstyle='primary', text="Введите значение:")
    search_label.pack(pady=5)

    search_entry = ttkb.Entry(search_window, bootstyle='primary')
    search_entry.pack(pady=5)

    date_fields = ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"]
    combobox_fields = ["POL", "TYPE_DOC", "EDUCATION"]

    for col in date_fields:
        if col in translated_columns:
            frame = Frame(search_window)
            frame.pack(anchor=W, padx=10, pady=5)
            label = ttkb.Label(frame, bootstyle='primary', text=translate_emp_columns([col])[0])
            label.pack(side=LEFT)
            date_entry = ttkb.DateEntry(frame, width=12, bootstyle="primary")
            date_entry.pack(side=LEFT)
            # Добавляем обработчик для поля даты
            date_entry.bind("<<DateEntrySelected>>", lambda event, entry=date_entry: search_entry.set(entry.get()))

    for col in combobox_fields:
        if col in translated_columns:
            frame = Frame(search_window)
            frame.pack(anchor=W, padx=10, pady=5)
            label = ttkb.Label(frame, bootstyle='primary', text=translate_emp_columns([col])[0])
            label.pack(side=LEFT)
            combobox_var = StringVar()
            combobox = ttkb.Combobox(frame, bootstyle="primary", textvariable=combobox_var, values=get_combobox_employer_values(col))
            combobox.pack(side=LEFT)
            # Добавляем обработчик для комбобокса
            combobox.bind("<<ComboboxSelected>>", lambda event, entry=combobox: search_entry.set(entry.get()))

    search_button = ttkb.Button(search_window, text="Поиск", command=search_employer, bootstyle='primary')
    search_button.pack(pady=10)

def get_combobox_employer_values(column):
    if column == "POL":
        return ["М", "Ж"]
    elif column == "TYPE_DOC":
        return ["ПАСПОРТ РФ", "ВРНР", "ИДУЛ"]
    elif column == "EDUCATION":
        return ["СРЕДНЕЕ НЕПОЛНОЕ", "СРЕДНЕЕ ПОЛНОЕ", "СПЕЦИАЛИТЕТ", "ВЫСШЕЕ НЕ ПОЛНОЕ", "ВЫСШЕЕ ПОЛНОЕ", "УЧЕННАЯ СТЕПЕНЬ"]
    return []


def open_search_emplist_window(conn, tree, columns, v_scrollbar, h_scrollbar, username, password,):
    def search_employer_list():
        selected_column_translated = column_var.get()
        search_value = search_entry.get()

        if not search_value:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите значение для поиска")
            return

        column_mapping = {translated_columns[i]: columns[i] for i in range(len(columns))}
        selected_column = column_mapping[selected_column_translated]

        try:
            cursor = conn.cursor()
            search_query = f"SELECT * FROM EMPLOYER_LIST WHERE {selected_column} LIKE ?"
            cursor.execute(search_query, (f"%{search_value}%",))
            search_results = cursor.fetchall()
            cursor.close()

            if not search_results:
                messagebox.showinfo("Результаты поиска", "Ничего не найдено")
            else:
                refresh_emp_list_table(conn, tree, search_results)

        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")
            print("Ошибка", f"Ошибка поиска: {e}")

    search_window = Toplevel()
    search_window.title("Поиск записи")
    search_window.geometry("300x250")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    search_window.iconbitmap(icon_path)

    translated_columns = translate_emp_list_columns(columns)
    column_var = StringVar()
    column_var.set(translated_columns[0])  

    column_label = Label(search_window, text="Выберите столбец:")
    column_label.pack(pady=5)

    column_combobox = ttkb.Combobox(search_window,bootstyle="primary", textvariable=column_var, values=translated_columns)
    column_combobox.pack(pady=5)

    search_label = Label(search_window, text="Введите значение:")
    search_label.pack(pady=5)

    search_entry = ttkb.Entry(search_window, bootstyle="primary")
    search_entry.pack(pady=5)

    search_button = ttkb.Button(search_window,bootstyle="primary", text="Поиск", command=search_employer_list)
    search_button.pack(pady=10)

def open_search_bef_window(conn, columns,tree):
    def search_document():
        selected_column_translated = column_var.get()
        search_value = search_entry.get()

        if not search_value:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите значение для поиска")
            return

        column_mapping = {translated_columns[i]: columns[i] for i in range(len(columns))}
        selected_column = column_mapping[selected_column_translated]

        try:
            cursor = conn.cursor()
            search_query = f"SELECT * FROM BENEFITS WHERE {selected_column} LIKE ?"
            cursor.execute(search_query, (f"%{search_value}%",))
            search_results = cursor.fetchall()
            cursor.close()

            if not search_results:
                messagebox.showinfo("Результаты поиска", "Ничего не найдено")
            else:
                refresh_bef_table(conn,tree,search_results)

        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")
            print("Ошибка", f"Ошибка поиска: {e}")

    search_window = Toplevel()
    search_window.title("Поиск льготы")
    search_window.geometry("300x250")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    search_window.iconbitmap(icon_path)


    translated_columns = translate_bef_columns(columns)
    column_var = StringVar()
    column_var.set(translated_columns[0])

    column_label = Label(search_window, text="Выберите столбец:")
    column_label.pack(pady=5)

    column_combobox = ttkb.Combobox(search_window, textvariable=column_var, values=translated_columns, bootstyle='primary')
    column_combobox.pack(pady=5)

    search_label = Label(search_window, text="Введите значение:")
    search_label.pack(pady=5)

    search_entry = ttkb.Entry(search_window, bootstyle='primary')
    search_entry.pack(pady=5)

    search_button = ttkb.Button(search_window, text="Поиск", command=search_document, bootstyle='primary')
    search_button.pack(pady=10)

def open_search_dep_window(conn, tree, columns):
    def search_department():
        selected_column_translated = column_var.get()
        search_value = search_entry.get()

        if not search_value:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите значение для поиска")
            return

        # Не забыть, collum - переведеное , mapping - сам процесс смены
        column_mapping = {translated_columns[i]: columns[i] for i in range(len(columns))}
        selected_column = column_mapping[selected_column_translated]

        try:
            cursor = conn.cursor()
            search_query = f"SELECT * FROM DEPARTMENT WHERE {selected_column} LIKE ?"
            cursor.execute(search_query, (f"%{search_value}%",))
            search_results = cursor.fetchall()
            cursor.close()

            if not search_results:
                messagebox.showwarning("Результаты поиска", "Ничего не найдено")
            else:
                refresh_dep_table(conn, tree, search_results)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")
            print("Ошибка", f"Ошибка поиска: {e}")

    search_window = Toplevel()
    search_window.title("Поиск отдела")
    search_window.geometry("300x250")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    search_window.iconbitmap(icon_path)

    translated_columns = translate_dep_columns(columns)
    column_var = StringVar()
    column_var.set(translated_columns[0])  

    column_label = Label(search_window, text="Выберите столбец:")
    column_label.pack(pady=5)

    column_combobox = ttkb.Combobox(search_window,bootstyle="primary", textvariable=column_var, values=translated_columns)
    column_combobox.pack(pady=5)

    search_label = Label(search_window, text="Введите значение:")
    search_label.pack(pady=5)

    search_entry = ttkb.Entry(search_window, bootstyle="primary")
    search_entry.pack(pady=5)

    search_button = ttkb.Button(search_window, text="Поиск",bootstyle="primary", command=search_department)
    search_button.pack(pady=10)


def open_search_factor_window(conn, tree, columns):
    def search_factor_information():
        selected_column_translated = column_var.get()
        search_value = search_entry.get()

        if not search_value:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите значение для поиска")
            return

        # Не забыть, collum - переведеное , mapping - сам процесс смены
        column_mapping = {translated_columns[i]: columns[i] for i in range(len(columns))}
        selected_column = column_mapping[selected_column_translated]

        try:
            cursor = conn.cursor()
            search_query = f"SELECT * FROM FACTOR_INFORMATION WHERE {selected_column} LIKE ?"
            cursor.execute(search_query, (f"%{search_value}%",))
            search_results = cursor.fetchall()
            cursor.close()

            if not search_results:
                messagebox.showinfo("Результаты поиска", "Ничего не найдено")
            else:
                refresh_fact_table (conn, tree, search_results)

        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")
            print("Ошибка", f"Ошибка поиска: {e}")

    search_window = Toplevel()
    search_window.title("Поиск информации о предприятии")
    search_window.geometry("300x200")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[1] / 'src' / 'r_app.ico'
    search_window.iconbitmap(icon_path)

    translated_columns = translate_fact_columns (columns)
    column_var = StringVar()
    column_var.set(translated_columns[0])  

    column_label = Label(search_window, text="Выберите столбец:")
    column_label.pack(pady=5)

    column_combobox = ttkb.Combobox(search_window, bootstyle="primary",textvariable=column_var, values=translated_columns)
    column_combobox.pack(pady=5)

    search_label = Label(search_window, text="Введите значение:")
    search_label.pack(pady=5)

    search_entry = ttkb.Entry(search_window,bootstyle="primary",)
    search_entry.pack(pady=5)

    search_button = ttkb.Button(search_window, bootstyle="primary",text="Поиск", command=search_factor_information)
    search_button.pack(pady=10)


def open_search_post_window(conn, tree, columns):
    def search_post():
        selected_column_translated = column_var.get()
        search_value = search_entry.get()

        if not search_value:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите значение для поиска")
            return

        column_mapping = {translated_columns[i]: columns[i] for i in range(len(columns))}
        selected_column = column_mapping[selected_column_translated]

        try:
            cursor = conn.cursor()
            search_query = f"SELECT * FROM POSTS WHERE {selected_column} LIKE ?"
            cursor.execute(search_query, (f"%{search_value}%",))
            search_results = cursor.fetchall()
            cursor.close()

            if not search_results:
                messagebox.showinfo("Результаты поиска", "Ничего не найдено")
            else:
                refresh_post_table(conn,tree,search_results)

        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")
            print("Ошибка", f"Ошибка поиска: {e}")

    search_window = Toplevel()
    search_window.title("Поиск поста")
    search_window.geometry("300x300")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    search_window.iconbitmap(icon_path)

    translated_columns = translate_post_columns(columns)
    column_var = StringVar()
    column_var.set(translated_columns[0])

    column_label = Label(search_window, text="Выберите столбец:")
    column_label.pack(pady=5)

    column_combobox = ttkb.Combobox(search_window, bootstyle="primary", textvariable=column_var, values=translated_columns)
    column_combobox.pack(pady=5)

    search_label = Label(search_window, text="Введите значение:")
    search_label.pack(pady=5)

    search_entry = ttkb.Entry(search_window, bootstyle="primary")
    search_entry.pack(pady=5)

    search_button = ttkb.Button(search_window, bootstyle="primary", text="Поиск", command=search_post)
    search_button.pack(pady=10)

def open_search_prof_window(conn, tree, columns):
    def search_department():
        selected_column_translated = column_var.get()
        search_value = search_entry.get()

        if not search_value:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите значение для поиска")
            return

        # Не забыть, collum - переведеное , mapping - сам процесс смены
        column_mapping = {translated_columns[i]: columns[i] for i in range(len(columns))}
        selected_column = column_mapping[selected_column_translated]

        try:
            cursor = conn.cursor()
            search_query = f"SELECT * FROM DEPARTMENT WHERE {selected_column} LIKE ?"
            cursor.execute(search_query, (f"%{search_value}%",))
            search_results = cursor.fetchall()
            cursor.close()

            if not search_results:
                messagebox.showwarning("Результаты поиска", "Ничего не найдено")
            else:
                refresh_prof_table(conn, tree, search_results)

        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")
            print("Ошибка", f"Ошибка поиска: {e}")

    search_window = Toplevel()
    search_window.title("Поиск отдела")
    search_window.geometry("300x250")
            # Получаем путь к текущей директории
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    search_window.iconbitmap(icon_path)

    translated_columns = translate_prof_columns(columns)
    column_var = StringVar()
    column_var.set(translated_columns[0])  

    column_label = Label(search_window, text="Выберите столбец:")
    column_label.pack(pady=5)

    column_combobox = ttkb.Combobox(search_window,bootstyle="primary", textvariable=column_var, values=translated_columns)
    column_combobox.pack(pady=5)

    search_label = Label(search_window, text="Введите значение:")
    search_label.pack(pady=5)

    search_entry = ttkb.Entry(search_window, bootstyle="primary")
    search_entry.pack(pady=5)

    search_button = ttkb.Button(search_window, text="Поиск",bootstyle="primary", command=search_department)
    search_button.pack(pady=10)

def open_search_sovm_window(conn, tree, columns):
    def search_department():
        selected_column_translated = column_var.get()
        search_value = search_entry.get()

        if not search_value:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите значение для поиска")
            return

        # Не забыть, collum - переведеное , mapping - сам процесс смены
        column_mapping = {translated_columns[i]: columns[i] for i in range(len(columns))}
        selected_column = column_mapping[selected_column_translated]

        try:
            cursor = conn.cursor()
            search_query = f"SELECT * FROM SOVMEST WHERE {selected_column} LIKE ?"
            cursor.execute(search_query, (f"%{search_value}%",))
            search_results = cursor.fetchall()
            cursor.close()

            if not search_results:
                messagebox.showwarning("Результаты поиска", "Ничего не найдено")
            else:
                refresh_sovm_table(conn,tree, search_results)

        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")
            print("Ошибка", f"Ошибка поиска: {e}")

    search_window = Toplevel()
    search_window.title("Поиск совместительства")
    search_window.geometry("300x250")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    search_window.iconbitmap(icon_path)

    translated_columns = translate_prof_columns(columns)
    column_var = StringVar()
    column_var.set(translated_columns[0])  

    column_label = Label(search_window, text="Выберите столбец:")
    column_label.pack(pady=5)

    column_combobox = ttkb.Combobox(search_window,bootstyle="primary", textvariable=column_var, values=translated_columns)
    column_combobox.pack(pady=5)

    search_label = Label(search_window, text="Введите значение:")
    search_label.pack(pady=5)

    search_entry = ttkb.Entry(search_window, bootstyle="primary")
    search_entry.pack(pady=5)

    search_button = ttkb.Button(search_window, text="Поиск",bootstyle="primary", command=search_department)
    search_button.pack(pady=10)

def open_search_doc_window(conn, tree, columns):
    def search_department():
        selected_column_translated = column_var.get()
        search_value = search_entry.get()

        if not search_value:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите значение для поиска")
            return

        column_mapping = {translated_columns[i]: columns[i] for i in range(len(columns))}
        selected_column = column_mapping[selected_column_translated]

        try:
            cursor = conn.cursor()
            if selected_column in ["DOCUMENT_TYPE"]:
                search_query = f"SELECT * FROM DOCUMENTS WHERE {selected_column} = ?"
                cursor.execute(search_query, (search_value,))
            else:
                search_query = f"SELECT * FROM DOCUMENTS WHERE {selected_column} LIKE ?"
                cursor.execute(search_query, (f"%{search_value}%",))

            search_results = cursor.fetchall()
            cursor.close()

            if not search_results:
               messagebox.showwarning("Результаты поиска", "Ничего не найдено","info")
            else:
                refresh_doc_table (conn, tree, search_results)

        except fdb.Error as e:
            messagebox.showwarning("Ошибка", f"Ошибка поиска: {e}")
            print("Ошибка", f"Ошибка поиска: {e}")

    search_window = Toplevel()
    search_window.title("Поиск отдела")
    search_window.geometry("300x250")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    search_window.iconbitmap(icon_path)

    translated_columns = translate_doc_columns(columns)
    column_var = StringVar()
    column_var.set(translated_columns[0])  

    column_label = Label(search_window, text="Выберите столбец:")
    column_label.pack(pady=5)

    column_combobox = ttkb.Combobox(search_window, bootstyle="primary", textvariable=column_var, values=translated_columns)
    column_combobox.pack(pady=5)

    search_label = Label(search_window, text="Введите значение:")
    search_label.pack(pady=5)

    search_entry = ttkb.Entry(search_window, bootstyle="primary")
    search_entry.pack(pady=5)

    search_button = ttkb.Button(search_window, text="Поиск", bootstyle="primary", command=search_department)
    search_button.pack(pady=10)