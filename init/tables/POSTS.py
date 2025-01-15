from tkinter import *
from tkinter import ttk, messagebox
import pyperclip
from tkinter import Menu
import sys
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk

from function.document import *
from function.fetch_data import fetch_posts_data
from tables.function.conn_base import connect_to_database
from function.get_user_data import get_user_data
from function.custom_front import custom_font
from function.convert_date import convert_date_to_display_format
from function.copy_selected_row import copy_selected_row_to_clipboard
from function.translate_colums import translate_post_columns
from button_function.add_button import open_add_post_window
from button_function.refresh_button import refresh_post_table, color_rows,sort_column
from button_function.delete_button import delete_selected_post
from tables.button_function.edit_button import open_edit_post_window
from tables.button_function.search_button import open_search_post_window

font_header = ("Time New Roman", 14, "bold")
# Добавляем путь к директории function в sys.path
current_dir = Path(__file__).resolve().parent
function_dir = current_dir / 'function'
sys.path.append(str(function_dir))











def copy_selected_row_to_clipboard(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для копирования")
        return

    row_values = tree.item(selected_item)['values']
    clipboard_text = "\t".join(map(str, row_values))
    pyperclip.copy(clipboard_text)

def create_context_menu(tree, conn, columns):
    context_menu = Menu(tree, tearoff=0)
    context_menu.add_command(label="Скопировать строку", command=lambda: copy_selected_row_to_clipboard(tree))
    context_menu.add_command(label="Удалить", command=lambda: delete_selected_post(conn, tree, columns))
    context_menu.add_command(label="Изменить", command=lambda: open_edit_post_window(conn, tree, columns))

    def show_context_menu(event):
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)
            context_menu.post(event.x_root, event.y_root)

    tree.bind("<Button-3>", show_context_menu)


def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <username> <password> <login_user> <role> ")
        return

    username = sys.argv[1]
    password = sys.argv[2]
    user_login = username
    role = sys.argv[3]

    user_data = get_user_data(username, password, user_login)
    if user_data:
        user_name, first_name, middle_name, last_name = user_data
    else:
        messagebox.showerror("Ошибка", "Данные о пользователе не найдены")
        sys.exit(1)

    root = ttkb.Window(themename="simplex_4")
    root.title(f"Таблица Посты - Авторизованный пользователь: {user_name} {first_name} {middle_name} {last_name}")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.state('zoomed')
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[1] / 'src' / 'r_app.ico'
    root.iconbitmap(icon_path)
    custom_font()
    custom_font_entry = ('CustomTextFont', 11)
    custom_font_buttom = ("CustomTextFont", 15, "bold")


    conn = connect_to_database(username, password)
    if conn is None:
        return

    columns, data = fetch_posts_data(conn)
    translated_columns = translate_post_columns (columns)

    button_frame = Frame(root)
    button_frame.pack(pady=10, anchor='w')

    button_output_frame = Frame(root)
    button_output_frame.pack(pady=10, anchor='e')

    ttkb.Button(button_frame,bootstyle="primary", text="Добавить пост", command=lambda: open_add_post_window(conn,tree)).pack(side=LEFT, padx=5)
    ttkb.Button(button_frame,bootstyle="primary", text="Удалить пост", command=lambda: delete_selected_post(conn, tree, columns)).pack(side=LEFT, padx=5)
    ttkb.Button(button_frame,bootstyle="primary", text="Изменить пост", command=lambda: open_edit_post_window(conn, tree, columns)).pack(side=LEFT, padx=5)
    ttkb.Button(button_frame,bootstyle="primary",text="Найти пост", command=lambda: open_search_post_window (conn, tree, columns)).pack(side=LEFT, padx=5)
    ttkb.Button(button_frame,bootstyle="primary", text="Обновить Таблицу", command=lambda: refresh_post_table (conn, tree)).pack(side=LEFT, padx=5)

    tree_frame = tk.Frame(root)
    tree_frame.pack(fill=BOTH, expand=True)
    tree = ttkb.Treeview(tree_frame,  show="headings")
    tree["columns"] = translated_columns
    for col in translated_columns:
        tree.heading(col,  text=col, command=lambda c=col: sort_column(tree, c, False))
    # Вертикальный ползунок
    v_scrollbar = ttkb.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview, bootstyle='primary')
    v_scrollbar.pack(side=RIGHT, fill=Y)
    
    # Горизонтальный
    h_scrollbar = ttkb.Scrollbar(tree_frame, orient=HORIZONTAL, command=tree.xview, bootstyle='primary')
    h_scrollbar.pack(side=BOTTOM, fill=X)

    tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    for i, row in enumerate(data):
        data[i] = [convert_date_to_display_format(str(value)) if columns[j] in ["DATA_BIRTH", "DOC_DATE", "MILITARY_DATE"] else str(value) for j, value in enumerate(row)]

    for item in data:
        tree.insert("", "end", values=item)


    tree.pack(fill=BOTH, expand=True) 

    style = ttk.Style()
    style.configure("Treeview.Heading", background="#c61b14", foreground="white", font=('CustomTextFont', 11, "bold"))
    style.configure("Treeview", rowheight=40, background="white", foreground="black", font=custom_font_entry)
    style.configure('TButton', backgroundg="#fff", font=custom_font_buttom)
    color_rows(tree)

    root.protocol("WM_DELETE_WINDOW", lambda: conn.close() or root.destroy())
    root.mainloop()

if __name__ == "__main__":
    main()