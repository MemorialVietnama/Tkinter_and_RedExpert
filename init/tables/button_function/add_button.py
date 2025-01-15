
from tkinter import *
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from pathlib import Path
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import Toplevel, Label,  messagebox, filedialog
import fdb

from tables.function.translate_colums import *
from tables.button_function.refresh_button import *

def open_add_employer_window(conn):
    add_window = Toplevel()
    add_window.title("Добавить сотрудника")
    add_window.geometry("400x1000")
    add_window.configure(background="#fff")
    current_dir = Path(__file__).resolve().parent
    # Поднимаемся на две папки вверх и переходим в директорию src
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    print(icon_path)
    add_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "SMALL_DATA": 255,
        "SURNAME": 50,
        "NAME_EMP": 50,
        "SURNAME_FATHER": 50,
        "POL": 1,
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

    default_values = {
        "SMALL_DATA": "ФИО",
        "SURNAME": "Не указано",
        "NAME_EMP": "Не указано",
        "SURNAME_FATHER": "Не указано",
        "POL": "Н",
        "INN": "000",
        "SNILS": "000",
        "DATA_BIRTH": "01.01.2000",
        "DATE_CITY": "Не указано",
        "TYPE_DOC": "Не указано",
        "DOC_NUM": "Не указано",
        "DOC_DATE": "01.01.2000",
        "DOC_WERE": "Не указано",
        "ADRESS_REGIST": "Не указано",
        "ADRESS_PROPISKA": "Не указано",
        "MILITARY_NUM": "000000",
        "MILITARY_DATE": "01.01.2000",
        "EDUCATION": "Не указано"
    }

    def validate_input_length(entry, max_length):
        def validate(P):
            if len(P) <= max_length:
                return True
            else:
                return False
        vcmd = (entry.register(validate), '%P')
        entry.config(validate="key", validatecommand=vcmd)

    # SMALL_DATA
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["SMALL_DATA"])[0] + " Д:255", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT)  
    entry.config(width=field_sizes["SMALL_DATA"])
    validate_input_length(entry, field_sizes["SMALL_DATA"])
    entries["SMALL_DATA"] = entry

    # SURNAME
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["SURNAME"])[0] + " Д:50", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT) 
    entry.config(width=field_sizes["SURNAME"])
    validate_input_length(entry, field_sizes["SURNAME"])
    entries["SURNAME"] = entry

    # NAME
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5) 
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["NAME_EMP"])[0] + " Д:50", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT)  
    entry.config(width=field_sizes["NAME_EMP"])
    validate_input_length(entry, field_sizes["NAME_EMP"])
    entries["NAME_EMP"] = entry

    # SURNAME_FATHER
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["SURNAME_FATHER"])[0] + " Д:50", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT)  
    entry.config(width=field_sizes["SURNAME_FATHER"])
    validate_input_length(entry, field_sizes["SURNAME_FATHER"])
    entries["SURNAME_FATHER"] = entry

    # POL
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5) 
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["POL"])[0] + " Д:1", width=20)
    label.pack(side=tk.LEFT)  
    pol_var = StringVar()
    pol_combobox = ttkb.Combobox(frame, textvariable=pol_var, values=["М", "Ж"], bootstyle="primary", width=field_sizes["POL"])
    pol_combobox.pack(side=tk.LEFT)  
    entries["POL"] = pol_combobox

    # INN
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["INN"])[0] + " Д:12", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT)  
    entry.config(width=field_sizes["INN"])
    validate_input_length(entry, field_sizes["INN"])
    entries["INN"] = entry

    # SNILS
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5) 
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["SNILS"])[0] + " Д:14", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT)  
    entry.config(width=field_sizes["SNILS"])
    validate_input_length(entry, field_sizes["SNILS"])
    entries["SNILS"] = entry

    # DATA_BIRTH
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["DATA_BIRTH"])[0], width=20)
    label.pack(side=tk.LEFT) 
    data_birth_entry = ttkb.DateEntry(frame, bootstyle="primary", width=12)
    data_birth_entry.pack(side=tk.LEFT)  
    entries["DATA_BIRTH"] = data_birth_entry

    # DATE_CITY
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["DATE_CITY"])[0] + " Д:200", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT) 
    entry.config(width=field_sizes["DATE_CITY"])
    validate_input_length(entry, field_sizes["DATE_CITY"])
    entries["DATE_CITY"] = entry

    # TYPE_DOC
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["TYPE_DOC"])[0] + " Д:20", width=20)
    label.pack(side=tk.LEFT)  
    type_doc_var = StringVar()
    type_doc_combobox = ttkb.Combobox(frame, textvariable=type_doc_var, values=["ПАСПОРТ РФ", "ВРНР", "ИДУЛ"], bootstyle="primary", width=field_sizes["TYPE_DOC"])
    type_doc_combobox.pack(side=tk.LEFT)  
    entries["TYPE_DOC"] = type_doc_combobox

    # DOC_NUM
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["DOC_NUM"])[0] + " Д:15", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT)  
    entry.config(width=field_sizes["DOC_NUM"])
    validate_input_length(entry, field_sizes["DOC_NUM"])
    entries["DOC_NUM"] = entry

    # DOC_DATE
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5) 
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["DOC_DATE"])[0], width=20)
    label.pack(side=tk.LEFT) 
    doc_date_entry = ttkb.DateEntry(frame, width=12, bootstyle="primary")
    doc_date_entry.pack(side=tk.LEFT)  
    entries["DOC_DATE"] = doc_date_entry

    # DOC_WERE
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5) 
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["DOC_WERE"])[0] + " Д:200", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT)  
    entry.config(width=field_sizes["DOC_WERE"])
    validate_input_length(entry, field_sizes["DOC_WERE"])
    entries["DOC_WERE"] = entry

    # ADRESS_REGIST
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5) 
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["ADRESS_REGIST"])[0] + " Д:200", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT)  
    entry.config(width=field_sizes["ADRESS_REGIST"])
    validate_input_length(entry, field_sizes["ADRESS_REGIST"])
    entries["ADRESS_REGIST"] = entry

    # ADRESS_PROPISKA
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["ADRESS_PROPISKA"])[0] + " Д:200", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT)  
    entry.config(width=field_sizes["ADRESS_PROPISKA"])
    validate_input_length(entry, field_sizes["ADRESS_PROPISKA"])
    entries["ADRESS_PROPISKA"] = entry

    # MILITARY_NUM
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["MILITARY_NUM"])[0] + " Д:7", width=20)
    label.pack(side=tk.LEFT)  
    entry = ttkb.Entry(frame, bootstyle="primary")
    entry.pack(side=tk.LEFT)  
    entry.config(width=field_sizes["MILITARY_NUM"])
    validate_input_length(entry, field_sizes["MILITARY_NUM"])
    entries["MILITARY_NUM"] = entry

    # MILITARY_DATE
    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["MILITARY_DATE"])[0], width=20)
    label.pack(side=tk.LEFT)  
    military_date_entry = ttkb.DateEntry(frame, bootstyle="primary", width=12)
    military_date_entry.pack(side=tk.LEFT)  
    entries["MILITARY_DATE"] = military_date_entry

    # EDUCATION

    frame = ttk.Frame(add_window)
    frame.pack(anchor=tk.W, padx=10, pady=5)  
    label = ttkb.Label(frame, bootstyle="inverse-primary", text=translate_emp_columns(["EDUCATION"])[0], width=20)
    label.pack(side=tk.LEFT)  
    type_edu_var = StringVar()
    type_edu_combobox = ttkb.Combobox(frame, textvariable=type_edu_var, values=["Среднее","Среднее неполное","Специалитет","Высшее неполное","Высшее"], bootstyle="primary", width=field_sizes["EDUCATION"])
    type_edu_combobox.pack(side=tk.LEFT) 
    entries["EDUCATION"] = entry


    # Кнопка добавления сотрудника
    def add_employer():
        cursor = conn.cursor()
        # SQL-запрос
        insert_query = """
        INSERT INTO EMPLOYER (SMALL_DATA, SURNAME, NAME_EMP, SURNAME_FATHER, POL, INN, SNILS, DATA_BIRTH, DATE_CITY, TYPE_DOC, DOC_NUM, DOC_DATE, DOC_WERE, ADRESS_REGIST, ADRESS_PROPISKA, MILITARY_NUM, MILITARY_DATE, EDUCATION)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        insert_values = tuple(
            entry.entry.get() if isinstance(entry, ttkb.DateEntry) else entry.get() or "Н"
            for entry in entries.values()
        )

        try:
            print(insert_values)
            cursor.execute(insert_query, insert_values)
            conn.commit()
            messagebox.showwarning("Успех!", "Новый сотрудник добавлен!")
        except Exception as e:
            messagebox.showwarning("Предупреждение", "Ошибка при добавлении данных:")
            print(e)

    ttkb.Button(add_window, bootstyle="primary", text="Добавить", command=add_employer).pack(pady=10)



def open_add_employer_list_window(conn):
    def add_employer_list():
        cursor = conn.cursor()
        # SQL-запрос
        insert_query = """
                INSERT INTO EMPLOYER_LIST (EMPLOYER_NAME, DEPARTMENT_NAME, PROFESION_NAME, SOVM_NAME, OKLAD, BENEFITS_NAME, DATE_ADD, DATE_FIRED)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        insert_values = tuple(
            entry.entry.get() if isinstance(entry, ttkb.DateEntry) else entry.get() or ""
            for entry in entries.values()
        )

        print(insert_values)
        try:
            cursor.execute(insert_query, insert_values)
            conn.commit()
            messagebox.showinfo("Успех!", "Новый документ добавлен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении данных: {e}")
            print(e)
        add_window.destroy()

    def open_employer_selection_window():
        def select_employer(event):
            selected_item = tree.selection()[0]
            employer_name = tree.item(selected_item, 'values')[0]
            entries["EMPLOYER_NAME"].delete(0, tk.END)
            entries["EMPLOYER_NAME"].insert(0, employer_name)
            employer_selection_window.destroy()

        employer_selection_window = tk.Toplevel()
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

        department_selection_window = tk.Toplevel()
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

        profesion_selection_window = tk.Toplevel()
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

        sovm_selection_window = tk.Toplevel()
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

        benefits_selection_window = tk.Toplevel()
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

    add_window = tk.Toplevel()
    add_window.title("Добавить запись")
    add_window.geometry("400x600")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    add_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "EMPLOYER_NAME": 10,
        "DEPARTMENT_NAME": 10,
        "PROFESION_NAME": 10,
        "SOVM_NAME": 10,
        "OKLAD": 10,
        "BENEFITS_NAME": 10,
        "DATE_ADD": 10,
        "DATE_FIRED": 10
    }

    default_values = {
        "EMPLOYER_NAME": "0",
        "DEPARTMENT_NAME": "0",
        "PROFESION_NAME": "0",
        "SOVM_NAME": "0",
        "OKLAD": "0.00",
        "BENEFITS_NAME": "0",
        "DATE_ADD": "01.01.2000",
        "DATE_FIRED": ""
    }

    for col in ["EMPLOYER_NAME", "DEPARTMENT_NAME", "PROFESION_NAME", "SOVM_NAME", "OKLAD", "BENEFITS_NAME", "DATE_ADD", "DATE_FIRED"]:
        frame = ttk.Frame(add_window)
        frame.pack(anchor=tk.W, padx=10, pady=5)

        label = ttk.Label(frame, text=translate_emp_list_columns([col])[0])
        label.pack(side=tk.LEFT)

        if col in ["DATE_ADD", "DATE_FIRED"]:
            entry = ttkb.DateEntry(frame, bootstyle="primary")
            entry.pack(side=tk.LEFT)
        else:
            entry = ttkb.Entry(frame, bootstyle="primary")
            entry.pack(side=tk.LEFT)
            entry.config(width=field_sizes[col])

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

    ttkb.Button(add_window, bootstyle="primary", text="Добавить", command=add_employer_list).pack(pady=10)


def open_add_benefit_window(conn,tree):
    def add_benefit():
        cursor = conn.cursor()
        # SQL-запрос
        insert_query = """
        INSERT INTO BENEFITS (CATEGORY, SUM_WITHOUT)
        VALUES (?, ?)
        """

        insert_values = tuple(
            entry.entry.get() if isinstance(entry, ttkb.DateEntry) else entry.get() or "Н"
            for entry in entries.values()
        )

        try:
            cursor.execute(insert_query, insert_values)
            conn.commit()
            messagebox.showwarning("Успех!", "Новая категория добавлена!")
            refresh_bef_table(conn, tree)
        except Exception as e:
            messagebox.showwarning("Предупреждение","Ошибка при добавлении данных:")

    add_window = Toplevel()
    add_window.title("Добавить льготу")
    add_window.geometry("400x200")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    add_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "CATEGORY": 50,
        "SUM_WITHOUT": 15
    }


    for col in ["CATEGORY", "SUM_WITHOUT"]:
        frame = Frame(add_window)
        frame.pack(anchor=W, padx=10, pady=5)

        label = Label(frame, text=translate_bef_columns([col])[0])
        label.pack(side=LEFT)

        entry = ttkb.Entry(frame,bootstyle="primary",)
        entry.pack(side=LEFT)
        entry.config(width=field_sizes[col])
        entries[col] = entry

    ttkb.Button(add_window, bootstyle="primary",text="Добавить", command=add_benefit).pack(pady=10)


def open_add_dep_window(conn,tree):
    def add_dep():
        cursor = conn.cursor()
        # SQL-запрос
        insert_query = """
        INSERT INTO DEPARTMENT (TAG)
        VALUES (?)
        """

        insert_values = tuple(
            entry.entry.get() if isinstance(entry, ttkb.DateEntry) else entry.get() or "Н"
            for entry in entries.values()
        )

        try:
            cursor.execute(insert_query, insert_values)
            conn.commit()
            messagebox.showwarning("Успех!", "Новая категория добавлена!")
            refresh_dep_table(conn, tree)
        except Exception as e:
            messagebox.showwarning("Предупреждение","Ошибка при добавлении данных:")

    add_window = Toplevel()
    add_window.title("Добавить отдел")
    add_window.geometry("400x200")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    add_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "TAG": 255,
    }


    for col in ["TAG"]:
        frame = Frame(add_window)
        frame.pack(anchor=W, padx=10, pady=5)

        label = Label(frame, text=translate_dep_columns ([col])[0])
        label.pack(side=LEFT)

        entry = ttkb.Entry(frame,bootstyle="primary",)
        entry.pack(side=LEFT)
        entry.config(width=field_sizes[col])
        entries[col] = entry

    ttkb.Button(add_window, bootstyle="primary",text="Добавить", command=add_dep).pack(pady=10)


def open_add_post_window(conn, tree):
    def add_post():
        try:
            cursor = conn.cursor()
            # SQL-запрос для вставки данных
            insert_query = """
                INSERT INTO POSTS (TITLE, DESCRIPTION, AUTHOR, DATE_POSTS)
                VALUES (?, ?, ?, ?)
            """

            # Извлекаем значения из полей
            insert_values = tuple(
                entry.entry.get() if isinstance(entry, ttkb.DateEntry) else
                entry.get("1.0", "end-1c") if isinstance(entry, tk.Text) else
                entry.get() or "Н"
                for entry in entries.values()
            )

            # Добавляем данные post и даты
            insert_values = (
                insert_values[0],  # TITLE
                insert_values[1],  # DESCRIPTION
                insert_values[2],  # AUTHOR
                date_entry.entry.get()  # DATE_POSTS
            )

            cursor.execute(insert_query, insert_values)
            conn.commit()
            messagebox.showinfo("Успех", "Пост успешно добавлен")
            add_window.destroy()
            refresh_post_table(conn, tree)

        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка добавления поста: {e}")


    add_window = Toplevel()
    add_window.title("Добавить пост")
    add_window.geometry("400x600")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    add_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "TITLE": 255,
        "DESCRIPTION": 8000,
        "AUTHOR": 255,
        "DATE_POST": 15
    }

    default_values = {
        "TITLE": "Задайте Заголовок!",
        "DESCRIPTION": "Задайте Описание",
        "AUTHOR": "Автор Статьи",
        "DATE_POSTS": "2024-10-01"
    }

    for col in ["TITLE", "DESCRIPTION", "AUTHOR", "DATE_POSTS"]:
        frame = Frame(add_window)
        frame.pack(anchor=W, padx=10, pady=5)
        label = Label(frame, text=translate_post_columns ([col])[0])
        label.pack(side=LEFT)

        if col == "DESCRIPTION":
            entry = tk.Text(frame, wrap="word", width=40, height=15)
            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            entry.insert(END, default_values[col])
        elif col == "DATE_POSTS":
            date_frame = Frame(add_window)
            date_frame.pack(anchor=W, padx=10, pady=5)
            date_label = Label(date_frame, text="Дата:")
            date_label.pack(side=LEFT)
            date_entry = ttkb.DateEntry(date_frame, bootstyle="primary")
            date_entry.pack(side=LEFT)
        else:
            entry = ttkb.Entry(frame, bootstyle="primary")
            entry.pack(side=tk.LEFT)
            entry.insert(0, default_values[col])
            entry.config(width=field_sizes[col])

        entries[col] = entry

    ttkb.Button(add_window, bootstyle="primary", text="Добавить", command=add_post).pack(pady=10)

def open_add_profesion_window(conn, tree):
        def add_profesion():
            new_data = {col: entry.get() if entry.get() != "" else default_values[col] for col, entry in entries.items()}

            try:
                cursor = conn.cursor()
                insert_query = """
                    INSERT INTO PROFESSION_NEW (TAG)
                    VALUES (?)
                """
                insert_values = [new_data[col] for col in ["TAG"]]
                cursor.execute(insert_query, insert_values)
                conn.commit()
                messagebox.showinfo("Успех", "Профессия успешно добавлена")
                add_window.destroy()
                refresh_prof_table(conn, tree)

            except fdb.Error as e:
                messagebox.showerror("Ошибка", f"Ошибка добавления профессии: {e}")

        add_window = Toplevel()
        add_window.title("Добавить профессию")
        add_window.geometry("400x200")
        current_dir = Path(__file__).resolve().parent
        icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
        add_window.iconbitmap(icon_path)

        entries = {}
        field_sizes = {
            "TAG": 50
        }

        default_values = {
            "TAG": "Новая профессия"
        }

        for col in ["TAG"]:
            frame = Frame(add_window)
            frame.pack(anchor=W, padx=10, pady=5)
            label = Label(frame, text=translate_prof_columns([col])[0])
            label.pack(side=LEFT)
            entry = ttkb.Entry(frame, bootstyle="primary")
            entry.pack(side=LEFT)
            entry.config(width=field_sizes[col])
            entries[col] = entry

        ttkb.Button(add_window, bootstyle="primary", text="Добавить", command=add_profesion).pack(pady=10)

def open_add_sovm_window(conn, tree,):
    def add_profesion():
        new_data = {col: entry.get() if entry.get() != "" else default_values[col] for col, entry in entries.items()}

        try:
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO SOVMEST (TAG)
                VALUES (?)
            """
            insert_values = [new_data[col] for col in ["TAG"]]
            cursor.execute(insert_query, insert_values)
            conn.commit()
            messagebox.showinfo("Успех", "Совместительство добавлено!")
            add_window.destroy()
            refresh_sovm_table(conn,tree)

        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка добавления профессии: {e}")

    add_window = Toplevel()
    add_window.title("Добавить совместительство")
    add_window.geometry("400x200")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    add_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "TAG": 255
    }

    default_values = {
        "TAG": "Совместительсто"
    }

    for col in ["TAG"]:
        frame = Frame(add_window)
        frame.pack(anchor=W, padx=10, pady=5)
        label = Label(frame, text=translate_prof_columns([col])[0])
        label.pack(side=LEFT)
        entry = ttkb.Entry(frame, bootstyle="primary")
        entry.pack(side=LEFT)
        entry.config(width=field_sizes[col])
        entries[col] = entry

    ttkb.Button(add_window, bootstyle="primary", text="Добавить", command=add_profesion).pack(pady=10)

def open_add_document_window(conn,tree):
    def add_document():
        cursor = conn.cursor()
        # SQL-запрос
        insert_query = """
                INSERT INTO DOCUMENTS (TAG, DOCUMENT_TYPE, FILE_DATA, INNER_DATE)
                VALUES (?, ?, ?, ?)
        """

        # Сбор данных из виджетов `entries`
        insert_values = tuple(
            entry.entry.get() if isinstance(entry, ttkb.DateEntry) else entry.get() or "Н"
            for entry in entries.values()
        )

        # Добавляем данные файла и даты
        insert_values = (
            insert_values[0],  # TAG
            insert_values[1],  # DOCUMENT_TYPE
            file_data,         # FILE_DATA
            date_entry.entry.get()  # INNER_DATE
        )

        try:
            cursor.execute(insert_query, insert_values)
            conn.commit()
            messagebox.showinfo("Успех!", "Новый документ добавлен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении данных: {e}")
        add_window.destroy()
        refresh_doc_table(conn, tree)

    def select_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                nonlocal file_data
                file_data = file.read()
            file_label.config(text=f"Выбран файл: {file_path}")

    add_window = Toplevel()
    add_window.title("Добавить документ")
    add_window.geometry("400x400")
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[2] / 'src' / 'r_app.ico'
    add_window.iconbitmap(icon_path)

    entries = {}
    field_sizes = {
        "TAG": 255,
        "DOCUMENT_TYPE": 50,
        "FILE_DATA": 1000,
        "INNER_DATE": 10
    }

    file_data = None

    for col in ["TAG", "DOCUMENT_TYPE"]:
        frame = Frame(add_window)
        frame.pack(anchor=W, padx=10, pady=5)
        label = Label(frame, text=translate_doc_columns([col])[0])
        label.pack(side=LEFT)
        entry = ttkb.Entry(frame, bootstyle="primary")
        entry.pack(side=LEFT)
        entry.config(width=field_sizes[col])
        entries[col] = entry

    file_frame = Frame(add_window)
    file_frame.pack(anchor=W, padx=10, pady=5)
    file_label = Label(file_frame, text="Выберите файл:")
    file_label.pack(side=LEFT)
    file_button = ttkb.Button(file_frame, bootstyle="primary", text="Выбрать файл", command=select_file)
    file_button.pack(side=LEFT)

    date_frame = Frame(add_window)
    date_frame.pack(anchor=W, padx=10, pady=5)
    date_label = Label(date_frame, text="Дата:")
    date_label.pack(side=LEFT)
    date_entry = ttkb.DateEntry(date_frame, bootstyle="primary")
    date_entry.pack(side=LEFT)

    ttkb.Button(add_window, bootstyle="primary", text="Добавить", command=add_document).pack(pady=10)
