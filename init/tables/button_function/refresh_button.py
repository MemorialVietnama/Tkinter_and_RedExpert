import ttkbootstrap as ttkb
from tables.function.fetch_data import *
from tables.function.translate_colums import *
from tables.function.convert_date import convert_date_to_display_format

# Функция для обновления таблицы сотрудников
def refresh_emp_table(conn, tree, data=None):
    # Очищаем таблицу
    for item in tree.get_children():
        tree.delete(item)

    if data is None:
        columns, data = fetch_employer_data(conn)
    else:
        columns = tree["columns"]

    translated_columns = translate_emp_columns(columns)

    tree["columns"] = translated_columns
    for col in translated_columns:
        # Устанавливаем ширину 300 для столбцов с именем "Адрес"
        if col in ["ФИО"]:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=300, anchor='center', stretch=False)
        elif col in ["Адрес", "Адрес регистрации", "Адрес прописки"]:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=450, anchor='center', stretch=False)
        elif col in ["Образование"]:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=200, anchor='center', stretch=False)
        else:
            # Для остальных столбцов устанавливаем ширину 200
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=150, anchor='center', stretch=False)

    for row in data:
        display_row = [convert_date_to_display_format(str(value)) if columns[i] in ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"] else str(value) for i, value in enumerate(row)]
        tree.insert("", "end", values=display_row)

    color_rows(tree)
    tree.update_idletasks()

def refresh_emp_list_table(conn, tree, data=None):
    for item in tree.get_children():
        tree.delete(item)

    if data is None:
        columns, data = fetch_employer_list_data(conn)
    else:
        columns = tree["columns"]

    translated_columns = translate_emp_list_columns(columns)

    tree["columns"] = translated_columns
    for col in translated_columns:
        # Устанавливаем ширину 300 для столбцов с именем "Адрес"
        if col in ["Сотрудник"]:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=300, anchor='center', stretch=False)
        elif col in ["ID"]:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=100, anchor='center', stretch=False)
        else:
            # Для остальных столбцов устанавливаем ширину 250
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=250, anchor='center', stretch=False)

    for row in data:
        display_row = [convert_date_to_display_format(str(value)) if columns[i] in ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"] else str(value) for i, value in enumerate(row)]
        tree.insert("", "end", values=display_row)

    color_rows(tree)
    tree.update_idletasks()

def refresh_bef_table(conn, tree, data=None):
    for item in tree.get_children():
        tree.delete(item)

    if data is None:
        columns, data = fetch_benefits_data(conn)
    else:
        columns = tree["columns"]

    translated_columns = translate_bef_columns(columns)
    tree["columns"] = translated_columns
    for col in translated_columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=650, anchor='center', stretch=False)

    for row in data:
        display_row = [convert_date_to_display_format(str(value)) if columns[i] in ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"] else str(value) for i, value in enumerate(row)]
        tree.insert("", "end", values=display_row)

    color_rows(tree)
    tree.update_idletasks()
def refresh_dep_table(conn, tree, data=None):
    for item in tree.get_children():
        tree.delete(item)

    if data is None:
        columns, data = fetch_department_data (conn)
    else:
        columns = tree["columns"]

    translated_columns = translate_dep_columns (columns)
    tree["columns"] = translated_columns
    for col in translated_columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=650, anchor='center', stretch=False)

    for row in data:
        display_row = [convert_date_to_display_format(str(value)) if columns[i] in ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"] else str(value) for i, value in enumerate(row)]
        tree.insert("", "end", values=display_row)

    color_rows(tree)
    tree.update_idletasks()
def refresh_fact_table(conn, tree, data=None):
    for item in tree.get_children():
        tree.delete(item)

    if data is None:
        columns, data = fetch_factor_information_data (conn)
    else:
        columns = tree["columns"]

    translated_columns = translate_fact_columns (columns)
    tree["columns"] = translated_columns
    for col in translated_columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=650, anchor='center', stretch=False)

    for row in data:
        display_row = [convert_date_to_display_format(str(value)) if columns[i] in ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"] else str(value) for i, value in enumerate(row)]
        tree.insert("", "end", values=display_row)

    color_rows(tree)
    tree.update_idletasks()

def refresh_post_table(conn, tree, data=None):
    for item in tree.get_children():
        tree.delete(item)

    if data is None:
        columns, data = fetch_posts_data (conn)
    else:
        columns = tree["columns"]

    translated_columns = translate_post_columns (columns)
    tree["columns"] = translated_columns
    for col in translated_columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=650, anchor='center', stretch=False)

    for row in data:
        display_row = [convert_date_to_display_format(str(value)) if columns[i] in ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"] else str(value) for i, value in enumerate(row)]
        tree.insert("", "end", values=display_row)

    color_rows(tree)
    tree.update_idletasks()
def refresh_prof_table(conn, tree, data=None):
    for item in tree.get_children():
        tree.delete(item)

    if data is None:
        columns, data = fetch_profesion_data (conn)
    else:
        columns = tree["columns"]

    translated_columns = translate_prof_columns (columns)
    tree["columns"] = translated_columns
    for col in translated_columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=650, anchor='center', stretch=False)

    for row in data:
        display_row = [convert_date_to_display_format(str(value)) if columns[i] in ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"] else str(value) for i, value in enumerate(row)]
        tree.insert("", "end", values=display_row)

    color_rows(tree)
    tree.update_idletasks()

def refresh_sovm_table(conn, tree, data=None):
    for item in tree.get_children():
        tree.delete(item)

    if data is None:
        columns, data = fetch_sovmest_data (conn)
    else:
        columns = tree["columns"]

    translated_columns = translate_sovm_columns (columns)
    tree["columns"] = translated_columns
    for col in translated_columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=650, anchor='center', stretch=False)

    for row in data:
        display_row = [convert_date_to_display_format(str(value)) if columns[i] in ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"] else str(value) for i, value in enumerate(row)]
        tree.insert("", "end", values=display_row)

    color_rows(tree)
    tree.update_idletasks()

def refresh_doc_table(conn, tree, data=None):
    for item in tree.get_children():
        tree.delete(item)

    if data is None:
        columns, data = fetch_document_data(conn)
    else:
        columns = tree["columns"]

    translated_columns = translate_doc_columns (columns)
    tree["columns"] = translated_columns
    for col in translated_columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
            tree.column(col, width=650, anchor='center', stretch=False)

    for row in data:
        display_row = [convert_date_to_display_format(str(value)) if columns[i] in ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"] else str(value) for i, value in enumerate(row)]
        tree.insert("", "end", values=display_row)

    color_rows(tree)

    tree.update_idletasks()
    
# Функция для раскраски строк
def color_rows(tree):
    for index, item in enumerate(tree.get_children()):
        if index % 2 != 0:
            tree.item(item, tags='even')
        else:
            tree.item(item, tags='odd')

    tree.tag_configure('even', background='white')
    tree.tag_configure('odd', background='lightgrey')

# Функция для сортировки столбцов
def sort_column(tree, col, reverse):
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    data.sort(reverse=reverse)
    for index, (val, child) in enumerate(data):
        tree.move(child, '', index)

    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))
    style = ttkb.Style()
    style.configure("Treeview", rowheight=40)
    tree.configure(style="Treeview")