from tkinter import *
from ttkbootstrap.constants import *
import fdb
from pathlib import Path
import ttkbootstrap as ttkb
from datetime import datetime
import tkinter as tk
from tkinter import Toplevel, Label,  messagebox, filedialog

from tables.function.translate_colums import *
from tables.button_function.refresh_button import *

def open_edit_employer_window(conn, tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для редактирования")
        return

    item_values = tree.item(selected_item)['values']
    print("Полученные данные ", item_values ,"\n")
    columns = [
        "ID_EMPLOYER", "SMALL_DATA", "SURNAME", "NAME_EMP", "SURNAME_FATHER", "POL", "INN", "SNILS",
        "DATA_BIRTH", "DATE_CITY", "TYPE_DOC", "DOC_NUM", "DOC_DATE", "DOC_WERE", "ADRESS_REGIST",
        "ADRESS_PROPISKA", "MILITARY_NUM", "MILITARY_DATE", "EDUCATION"
    ]
    
    def edit_employer():
        new_data = {}
        for col, entry in entries.items():
            if isinstance(entry, ttkb.DateEntry):
                new_data[col] = entry.get_date().strftime('%Y-%m-%d')  
            else:
                new_data[col] = entry.get()


        try:
            cursor = conn.cursor()
            update_query = "UPDATE EMPLOYER SET "
            update_values = []
            for col in columns:
                if col != "ID_EMPLOYER":
                    update_query += f"{col} = ?, "
                    update_values.append(new_data[col])
            update_query = update_query.rstrip(', ')
            update_query += " WHERE ID_EMPLOYER = ?"
            update_values.append(item_values[columns.index("ID_EMPLOYER")])
            cursor.execute(update_query, update_values)
            conn.commit()
            messagebox.showinfo("Успех", "Изменения успешно сохранены в базу данных")
            edit_window.destroy()
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения изменений: {e}")

    edit_window = Toplevel()
    edit_window.title("Редактировать сотрудника")
    edit_window.geometry("400x1000")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    edit_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "SMALL_DATA": 255,
        "SURNAME": 50,
        "NAME_EMP": 50,
        "SURNAME_FATHER": 50,
        "POL": 10,
        "INN": 12,
        "SNILS": 14,
        "DATA_BIRTH": 10,
        "DATE_CITY": 200,
        "TYPE_DOC": 20,
        "DOC_NUM": 15,
        "DOC_DATE": 10,
        "DOC_WERE": 200,
        "ADRESS_REGIST": 200,
        "ADRESS_PROPISKA": 200,
        "MILITARY_NUM": 7,
        "MILITARY_DATE": 10,
        "EDUCATION": 20
    }

    for col in ["SMALL_DATA", "SURNAME", "NAME_EMP", "SURNAME_FATHER", "POL", "INN", "SNILS",
                "DATA_BIRTH", "DATE_CITY", "TYPE_DOC", "DOC_NUM", 
                "DOC_DATE", "DOC_WERE", "ADRESS_REGIST", "ADRESS_PROPISKA",
                "MILITARY_NUM", "MILITARY_DATE", "EDUCATION"]:

        frame = Frame(edit_window)
        frame.pack(anchor=W, padx=10, pady=5)

        label = ttkb.Label(frame, bootstyle="primary", text=translate_emp_columns([col])[0])
        label.pack(side=LEFT)

        if col in ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"]:
            date_entry = ttkb.DateEntry(frame, bootstyle="primary", width=12)
            date_entry.pack(side=LEFT)
            date_entry.entry.delete(0, END)
            date_entry.entry.insert(0, item_values[columns.index(col)])
            entries[col] = date_entry
        else:
            entry = ttkb.Entry(frame, bootstyle="primary")
            entry.pack(side=LEFT)
            entry.config(width=field_sizes[col])
            entry.insert(0, item_values[columns.index(col)])
            entries[col] = entry

    ttkb.Button(edit_window, bootstyle="primary", text="Сохранить изменения", command=edit_employer).pack(pady=10)

def get_combobox_employer_values(column):
    if column == "POL":
        return ["М", "Ж"]
    elif column == "TYPE_DOC":
        return ["ПАСПОРТ РФ", "ВРНР", "ИДУЛ"]
    elif column == "EDUCATION":
        return ["СРЕДНЕЕ НЕПОЛНОЕ", "СРЕДНЕЕ ПОЛНОЕ", "СПЕЦИАЛИТЕТ", "ВЫСШЕЕ НЕ ПОЛНОЕ", "ВЫСШЕЕ ПОЛНОЕ", "УЧЕННАЯ СТЕПЕНЬ"]
    return []


def open_edit_employer_list_window(conn, tree, columns, v_scrollbar, h_scrollbar, username, password):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для редактирования")
        return

    item_values = tree.item(selected_item)['values']
    print(item_values)
    columns = [ "ID","EMPLOYER_NAME","DEPARTMENT_NAME","PROFESION_NAME","SOVM_NAME","BENEFITS_NAME","OKLAD","DATE_ADD","DATE_FIRED"]
    
    def edit_employer_list():
        new_data = {}
        new_data["DATE_ADD"] = date_entry_add.entry.get()
        new_data["DATE_FIRED"] = date_entry_fired.entry.get()

        for col, entry in entries.items():
            if col not in ["DATE_ADD", "DATE_FIRED"]: 
                if isinstance(entry, ttkb.DateEntry):
                    new_data[col] = entry.entry.get()
                else:
                    new_data[col] = entry.get()

        print("Новые данные : ", new_data, "\n")
        try:
            cursor = conn.cursor()
            update_query = "UPDATE EMPLOYER_LIST SET "
            update_values = []
            for col in columns:
                if col != "ID":
                    update_query += f"{col} = ?, "
                    update_values.append(new_data[col])
            update_query = update_query.rstrip(', ')
            update_query += " WHERE ID = ?"
            update_values.append(item_values[columns.index("ID")])
            print(update_query,update_values, "\n")
            cursor.execute(update_query, update_values)
            conn.commit()
            messagebox.showinfo("Успех", "Изменения успешно сохранены в базу данных")
            edit_window.destroy()
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения изменений: {e}")


    def open_employer_selection_window():
        def select_employer(event):
            selected_item = tree.selection()[0]
            employer_name = tree.item(selected_item, 'values')[0]
            entries["EMPLOYER_NAME"].delete(0, tk.END)
            entries["EMPLOYER_NAME"].insert(0, employer_name)
            employer_selection_window.destroy()

        employer_selection_window = Toplevel()
        employer_selection_window.title("Выбор сотрудника")
        employer_selection_window.geometry("400x300")

        tree = ttkb.Treeview(employer_selection_window, bootstyle="primary", columns=("SMALL_DATA",), show="headings")
        tree.heading("SMALL_DATA", text="Сотрудник")
        tree.column("SMALL_DATA", width=300)
        tree.pack(fill=tk.BOTH, expand=True)

        cursor = conn.cursor()
        cursor.execute("SELECT SMALL_DATA FROM EMPLOYER")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        tree.bind("<Double-1>", select_employer)

    def open_department_selection_window():
        def select_department(event):
            selected_item = tree.selection()[0]
            department_name = tree.item(selected_item, 'values')[0]
            entries["DEPARTMENT_NAME"].delete(0, tk.END)
            entries["DEPARTMENT_NAME"].insert(0, department_name)
            department_selection_window.destroy()

        department_selection_window = Toplevel()
        department_selection_window.title("Выбор отдела")
        department_selection_window.geometry("400x300")

        tree = ttkb.Treeview(department_selection_window, bootstyle="primary", columns=("DEPARTMENT_NAME",), show="headings")
        tree.heading("DEPARTMENT_NAME", text="Отдел")
        tree.column("DEPARTMENT_NAME", width=300)
        tree.pack(fill=tk.BOTH, expand=True)

        cursor = conn.cursor()
        cursor.execute("SELECT TAG FROM DEPARTMENT")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        tree.bind("<Double-1>", select_department)

    def open_profesion_selection_window():
        def select_profesion(event):
            selected_item = tree.selection()[0]
            profesion_name = tree.item(selected_item, 'values')[0]
            entries["PROFESION_NAME"].delete(0, tk.END)
            entries["PROFESION_NAME"].insert(0, profesion_name)
            profesion_selection_window.destroy()

        profesion_selection_window = Toplevel()
        profesion_selection_window.title("Выбор профессии")
        profesion_selection_window.geometry("400x300")

        tree = ttkb.Treeview(profesion_selection_window, bootstyle="primary", columns=("PROFESION_NAME",), show="headings")
        tree.heading("PROFESION_NAME", text="Профессия")
        tree.column("PROFESION_NAME", width=300)
        tree.pack(fill=tk.BOTH, expand=True)

        cursor = conn.cursor()
        cursor.execute("SELECT TAG FROM PROFESSION_NEW")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        tree.bind("<Double-1>", select_profesion)

    def open_sovm_selection_window():
        def select_sovm(event):
            selected_item = tree.selection()[0]
            sovm_name = tree.item(selected_item, 'values')[0]
            entries["SOVM_NAME"].delete(0, tk.END)
            entries["SOVM_NAME"].insert(0, sovm_name)
            sovm_selection_window.destroy()

        sovm_selection_window = Toplevel()
        sovm_selection_window.title("Выбор совмещения")
        sovm_selection_window.geometry("400x300")

        tree = ttkb.Treeview(sovm_selection_window, bootstyle="primary", columns=("SOVM_NAME",), show="headings")
        tree.heading("SOVM_NAME", text="Совмещение")
        tree.column("SOVM_NAME", width=300)
        tree.pack(fill=tk.BOTH, expand=True)

        cursor = conn.cursor()
        cursor.execute("SELECT TAG FROM SOVMEST")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        tree.bind("<Double-1>", select_sovm)

    def open_benefits_selection_window():
        def select_benefits(event):
            selected_item = tree.selection()[0]
            benefits_name = tree.item(selected_item, 'values')[0]
            entries["BENEFITS_NAME"].delete(0, tk.END)
            entries["BENEFITS_NAME"].insert(0, benefits_name)
            benefits_selection_window.destroy()

        benefits_selection_window = Toplevel()
        benefits_selection_window.title("Выбор льготы")
        benefits_selection_window.geometry("400x300")

        tree = ttkb.Treeview(benefits_selection_window, bootstyle="primary", columns=("BENEFITS_NAME",), show="headings")
        tree.heading("BENEFITS_NAME", text="Льгота")
        tree.column("BENEFITS_NAME", width=300)
        tree.pack(fill=tk.BOTH, expand=True)

        cursor = conn.cursor()
        cursor.execute("SELECT CATEGORY FROM BENEFITS")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        tree.bind("<Double-1>", select_benefits)

    edit_window = Toplevel()
    edit_window.title("Редактировать запись")
    edit_window.geometry("400x600")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    edit_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "EMPLOYER_NAME": 50,
        "DEPARTMENT_NAME": 50,
        "PROFESION_NAME": 50,
        "SOVM_NAME": 50,
        "OKLAD": 20,
        "BENEFITS_NAME": 50,
        "DATE_ADD": 10,
        "DATE_FIRED": 10
    }

    for col in ["EMPLOYER_NAME", "DEPARTMENT_NAME", "PROFESION_NAME", "SOVM_NAME", "OKLAD", "BENEFITS_NAME", "DATE_ADD", "DATE_FIRED"]:
        frame = Frame(edit_window)
        frame.pack(anchor=W, padx=10, pady=5)

        label = Label(frame, text=translate_emp_list_columns([col])[0])
        label.pack(side=LEFT)

        if col in ["DATE_ADD", "DATE_FIRED"]:
            if col == "DATE_ADD":
                date_entry_add = ttkb.DateEntry(frame, bootstyle="primary")
                date_entry_add.pack(side=tk.LEFT)
                date_entry_add.entry.delete(0, END)
                date_entry_add.entry.insert(0, item_values[columns.index(col)])
                print("Дата постулпления: ",date_entry_add.entry.get())
            else:
                date_entry_fired = ttkb.DateEntry(frame, bootstyle="primary")
                date_entry_fired.pack(side=tk.LEFT)
                date_entry_fired.entry.delete(0, END)
                date_entry_fired.entry.insert(0, item_values[columns.index(col)])
                print("Дата увольнения: ",date_entry_fired.entry.get())
        else:
            entry = ttkb.Entry(frame, bootstyle="primary")
            entry.pack(side=tk.LEFT)
            entry.config(width=field_sizes[col])
            entry.insert(0, item_values[columns.index(col)]) 

        entries[col] = entry

        if col == "EMPLOYER_NAME":
            select_button = ttkb.Button(frame, bootstyle="primary", text="Выбрать", command=open_employer_selection_window)
            select_button.pack(side=tk.LEFT, padx=(10, 0))
        elif col == "DEPARTMENT_NAME":
            select_button = ttkb.Button(frame, bootstyle="primary", text="Выбрать", command=open_department_selection_window)
            select_button.pack(side=tk.LEFT, padx=(10, 0))
        elif col == "PROFESION_NAME":
            select_button = ttkb.Button(frame, bootstyle="primary", text="Выбрать", command=open_profesion_selection_window)
            select_button.pack(side=tk.LEFT, padx=(10, 0))
        elif col == "SOVM_NAME":
            select_button = ttkb.Button(frame, bootstyle="primary", text="Выбрать", command=open_sovm_selection_window)
            select_button.pack(side=tk.LEFT, padx=(10, 0))
        elif col == "BENEFITS_NAME":
            select_button = ttkb.Button(frame, bootstyle="primary", text="Выбрать", command=open_benefits_selection_window)
            select_button.pack(side=tk.LEFT, padx=(10, 0))

    ttkb.Button(edit_window, bootstyle="primary", text="Сохранить изменения", command=edit_employer_list).pack(pady=10)

def open_edit_benefit_window(conn, tree, columns):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для редактирования")
        return

    item_values = tree.item(selected_item)['values']
    
    def edit_benefit():
        new_data = {col: entry.get() for col, entry in entries.items()}
        try:
            cursor = conn.cursor()
            update_query = "UPDATE BENEFITS SET "
            update_values = []
            for col in columns:
                if col != "ID":
                    update_query += f"{col} = ?, "
                    update_values.append(new_data[col])
            update_query = update_query.rstrip(', ')
            update_query += " WHERE ID = ?"
            update_values.append(item_values[columns.index("ID")])
            cursor.execute(update_query, update_values)
            conn.commit()
            messagebox.showinfo("Успех", "Изменения успешно сохранены в базу данных")
            refresh_bef_table(conn,tree)
            edit_window.destroy()
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения изменений: {e}")

    edit_window = Toplevel()
    edit_window.title("Редактировать льготу")
    edit_window.geometry("400x200")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    edit_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "CATEGORY": 50,
        "SUM_WITHOUT": 15
    }

    for col in ["CATEGORY", "SUM_WITHOUT"]:
        frame = Frame(edit_window)
        frame.pack(anchor=W, padx=10, pady=5)

        label = Label(frame, text=translate_bef_columns([col])[0])
        label.pack(side=LEFT)

        entry = ttkb.Entry(frame,bootstyle="primary",)
        entry.pack(side=LEFT)
        entry.config(width=field_sizes[col])
        entry.insert(0, item_values[columns.index(col)]) 
        entries[col] = entry

    ttkb.Button(edit_window,bootstyle="primary", text="Сохранить изменения", command=edit_benefit).pack(pady=10)

def open_edit_dep_window(conn, tree, columns):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для редактирования")
        return

    item_values = tree.item(selected_item)['values']
    
    def edit_benefit():
        new_data = {col: entry.get() for col, entry in entries.items()}
        try:
            cursor = conn.cursor()
            update_query = "UPDATE DEPARTMENT SET "
            update_values = []
            for col in columns:
                if col != "ID":
                    update_query += f"{col} = ?, "
                    update_values.append(new_data[col])
            update_query = update_query.rstrip(', ')
            update_query += " WHERE ID = ?"
            update_values.append(item_values[columns.index("ID")])
            cursor.execute(update_query, update_values)
            conn.commit()
            messagebox.showinfo("Успех", "Изменения успешно сохранены в базу данных")
            edit_window.destroy()
            refresh_dep_table(conn, tree)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения изменений: {e}")

    edit_window = Toplevel()
    edit_window.title("Редактировать льготу")
    edit_window.geometry("400x200")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    edit_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "TAG": 30
    }

    for col in ["TAG"]:
        frame = Frame(edit_window)
        frame.pack(anchor=W, padx=10, pady=5)

        label = Label(frame, text=translate_dep_columns([col])[0])
        label.pack(side=LEFT)

        entry = ttkb.Entry(frame,bootstyle="primary",)
        entry.pack(side=LEFT)
        entry.config(width=field_sizes[col])
        entry.insert(0, item_values[columns.index(col)]) 
        entries[col] = entry

    ttkb.Button(edit_window,bootstyle="primary", text="Сохранить изменения", command=edit_benefit).pack(pady=10)

def open_edit_factor_information_window(conn, tree, columns):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для редактирования")
        return

    item_values = tree.item(selected_item)['values']
    
    def edit_factor_information():
        new_data = {col: entry.get() for col, entry in entries.items()}
        try:
            cursor = conn.cursor()
            update_query = "UPDATE FACTOR_INFORMATION SET "
            update_values = []
            for col in columns:
                if col != "SMALL_NAME":
                    update_query += f"{col} = ?, "
                    update_values.append(new_data[col])
            update_query = update_query.rstrip(', ') + " WHERE SMALL_NAME = ?"
            update_values.append(item_values[columns.index("SMALL_NAME")])
            cursor.execute(update_query, update_values)
            conn.commit()
            messagebox.showinfo("Успех", "Изменения успешно сохранены в базу данных")
            edit_window.destroy()
            refresh_fact_table(conn,tree)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения изменений: {e}")

    edit_window = Toplevel()
    edit_window.title("Редактировать информацию о предприятии")
    edit_window.geometry("400x600")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    edit_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "SMALL_NAME": 100,
        "FULL_NAME": 100,
        "INN": 20,
        "KPP": 20,
        "OKPO": 20,
        "KOD_GNI": 20,
        "KOD_SNIILS": 50,
        "ADRES": 100,
        "RUK_DOLG": 100,
        "RUK_FIO": 100,
        "GL_BUX": 100
    }

    for col in ["SMALL_NAME", "FULL_NAME", "INN", "KPP", "OKPO", "KOD_GNI", "KOD_SNIILS", "ADRES", "RUK_DOLG", "RUK_FIO", "GL_BUX"]:
        frame = Frame(edit_window)
        frame.pack(anchor=W, padx=10, pady=5)

        label = Label(frame, text=translate_fact_columns([col])[0])
        label.pack(side=LEFT)

        entry = ttkb.Entry(frame, bootstyle="primary")
        entry.pack(side=LEFT)
        entry.config(width=field_sizes[col])
        entry.insert(0, item_values[columns.index(col)]) 
        entries[col] = entry

    ttkb.Button(edit_window, bootstyle="primary", text="Сохранить изменения", command=edit_factor_information).pack(pady=10)

def open_edit_post_window(conn, tree, columns):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для редактирования")
        return

    item_values = tree.item(selected_item)['values']
    
    def edit_post():
        new_data = {}
        for col, entry in entries.items():
            if isinstance(entry, ttkb.DateEntry):
                new_data[col] = entry.entry.get()  # Получаем строку даты
            elif isinstance(entry, tk.Text):
                new_data[col] = entry.get("1.0", "end-1c")  # Извлекаем текст из tk.Text
            else:
                new_data[col] = entry.get()
        try:
            cursor = conn.cursor()
            update_query = "UPDATE POSTS SET "
            update_values = []
            for col in columns:
                if col != "ID":
                    update_query += f"{col} = ?, "
                    update_values.append(new_data[col])
            update_query = update_query.rstrip(', ')
            update_query += " WHERE ID = ?"
            update_values.append(item_values[columns.index("ID")])
            cursor.execute(update_query, update_values)
            conn.commit()
            messagebox.showinfo("Успех", "Изменения успешно сохранены в базу данных")
            edit_window.destroy()
            refresh_post_table(conn, tree)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения изменений: {e}")

    edit_window = Toplevel()
    edit_window.title("Редактировать пост")
    edit_window.geometry("400x600")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    edit_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "TITLE": 255,
        "DESCRIPTION": 8000,
        "AUTHOR": 255,
        "DATE_POSTS": 15
    }

    for col in ["TITLE", "DESCRIPTION", "AUTHOR", "DATE_POSTS"]:
        frame = Frame(edit_window)
        frame.pack(anchor=W, padx=10, pady=5)
        if col == "DESCRIPTION":
            # Создаем Text для описания
            entry = tk.Text(frame, wrap="word", width=40, height=15)
            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            entry.insert(END, item_values[columns.index(col)])
            entries[col] = entry  
        elif col == "DATE_POSTS":
            date_frame = Frame(edit_window)
            date_frame.pack(anchor=W, padx=10, pady=5)
            date_label = Label(date_frame, text="Дата:")
            date_label.pack(side=LEFT)
            date_entry = ttkb.DateEntry(date_frame, bootstyle="primary")
            date_entry.pack(side=LEFT)
            date_entry.entry.delete(0, END)
            date_entry.entry.insert(0, item_values[columns.index(col)])
            entries[col] = date_entry  
        else:
            entry = ttkb.Entry(frame, bootstyle="primary")
            entry.pack(side=tk.LEFT)
            entry.insert(0, item_values[columns.index(col)])
            entry.config(width=field_sizes[col])
            entries[col] = entry  #

    ttkb.Button(edit_window, bootstyle="primary", text="Сохранить изменения", command=edit_post).pack(pady=10)

def open_edit_profesion_window(conn, tree, columns):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для редактирования")
        return

    item_values = tree.item(selected_item)['values']
    
    def edit_profesion():
        new_data = {col: entry.get() for col, entry in entries.items()}
        try:
            cursor = conn.cursor()
            update_query = "UPDATE PROFESSION_NEW SET "
            update_values = []
            for col in columns:
                if col != "ID":
                    update_query += f"{col} = ?, "
                    update_values.append(new_data[col])
            update_query = update_query.rstrip(', ')
            update_query += " WHERE TAG = ?"
            update_values.append(item_values[columns.index("TAG")])
            cursor.execute(update_query, update_values)
            conn.commit()
            messagebox.showinfo("Успех", "Изменения успешно сохранены в базу данных")
            edit_window.destroy()
            refresh_prof_table(conn, tree)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения изменений: {e}")

    edit_window = Toplevel()
    edit_window.title("Редактировать профессию")
    edit_window.geometry("400x200")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    edit_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "TAG": 50
    }

    for col in ["TAG"]:
        frame = Frame(edit_window)
        frame.pack(anchor=W, padx=10, pady=5)

        label = Label(frame, text=translate_prof_columns([col])[0])
        label.pack(side=LEFT)

        entry = ttkb.Entry(frame, bootstyle="primary")
        entry.pack(side=LEFT)
        entry.config(width=field_sizes[col])
        entry.insert(0, item_values[columns.index(col)])  
        entries[col] = entry

    ttkb.Button(edit_window,bootstyle="primary-outline", text="Сохранить изменения", command=edit_profesion).pack(pady=10)

def open_edit_sovmest_window(conn, tree, columns):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для редактирования")
        return

    item_values = tree.item(selected_item)['values']
    
    def edit_profesion():
        new_data = {col: entry.get() for col, entry in entries.items()}
        try:
            cursor = conn.cursor()
            update_query = "UPDATE SOVMEST SET "
            update_values = []
            for col in columns:
                if col != "ID":
                    update_query += f"{col} = ?, "
                    update_values.append(new_data[col])
            update_query = update_query.rstrip(', ')
            update_query += " WHERE TAG = ?"
            update_values.append(item_values[columns.index("TAG")])
            cursor.execute(update_query, update_values)
            conn.commit()
            messagebox.showinfo("Успех", "Изменения успешно сохранены в базу данных")
            edit_window.destroy()
            refresh_sovm_table(conn,tree)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения изменений: {e}")

    edit_window = Toplevel()
    edit_window.title("Редактировать профессию")
    edit_window.geometry("400x200")
    current_dir = Path(__file__).resolve().parent
    # Поднимаемся на две папки вверх и переходим в директорию src
    icon_path = current_dir.parents[1] / 'src' / 'r_app.ico'
    edit_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "TAG": 255
    }

    for col in ["TAG"]:
        frame = Frame(edit_window)
        frame.pack(anchor=W, padx=10, pady=5)

        label = Label(frame, text=translate_prof_columns([col])[0])
        label.pack(side=LEFT)

        entry = ttkb.Entry(frame, bootstyle="primary")
        entry.pack(side=LEFT)
        entry.config(width=field_sizes[col])
        entry.insert(0, item_values[columns.index(col)])  
        entries[col] = entry

    ttkb.Button(edit_window,bootstyle="primary", text="Сохранить изменения", command=edit_profesion).pack(pady=10)

def open_edit_document_window(conn, tree, columns):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для редактирования")
        return

    item_values = tree.item(selected_item)['values']
    
    def edit_document(conn, tree):
        new_data = {col: entry.get() for col, entry in entries.items()}
        new_data["FILE_DATA"] = file_data  # Добавляем данные файла
        new_data["INNER_DATE"] = date_entry.entry.get()  # Добавляем дату

        try:
            cursor = conn.cursor()
            update_query = "UPDATE DOCUMENTS SET "
            update_values = []
            for col in columns:
                if col != "ID":
                    update_query += f"{col} = ?, "
                    update_values.append(new_data[col])
            update_query = update_query.rstrip(', ')
            update_query += " WHERE ID = ?"
            update_values.append(item_values[columns.index("ID")])
            cursor.execute(update_query, update_values)
            conn.commit()
            messagebox.showinfo("Успех", "Изменения успешно сохранены в базу данных")
            edit_window.destroy()
            refresh_doc_table(conn, tree)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения изменений: {e}")

    def select_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                nonlocal file_data
                file_data = file.read()
            file_label.config(text=f"Выбран файл: {file_path}")

    edit_window = Toplevel()
    edit_window.title("Редактировать документ")
    edit_window.geometry("400x400")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    edit_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "TAG": 255,
        "DOCUMENT_TYPE": 50,
        "FILE_DATA": 1000,
        "INNER_DATE": 10
    }

    file_data = None

    for col in ["TAG", "DOCUMENT_TYPE"]:
        frame = Frame(edit_window)
        frame.pack(anchor=W, padx=10, pady=5)
        label = Label(frame, text=translate_doc_columns([col])[0])
        label.pack(side=LEFT)
        entry = ttkb.Entry(frame, bootstyle="primary")
        entry.pack(side=LEFT)
        entry.config(width=field_sizes[col])
        entry.insert(0, item_values[columns.index(col)])
        entries[col] = entry

    file_frame = Frame(edit_window)
    file_frame.pack(anchor=W, padx=10, pady=5)
    file_label = Label(file_frame, text="Выберите файл:")
    file_label.pack(side=LEFT)
    file_button = ttkb.Button(file_frame, bootstyle="primary", text="Выбрать файл", command=select_file)
    file_button.pack(side=LEFT)

    date_frame = Frame(edit_window)
    date_frame.pack(anchor=W, padx=10, pady=5)
    date_label = Label(date_frame, text="Дата:")
    date_label.pack(side=LEFT)
    date_entry = ttkb.DateEntry(date_frame, bootstyle="primary")
    date_entry.pack(side=LEFT)

    ttkb.Button(edit_window, bootstyle="primary", text="Сохранить изменения", command=lambda: edit_document(conn, tree)).pack(pady=10)