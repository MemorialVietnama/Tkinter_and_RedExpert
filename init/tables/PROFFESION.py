from tkinter import *
from tkinter import ttk, messagebox
from tkinter import Toplevel, Label, Button, messagebox, filedialog
from tkinter.ttk import Treeview, Scrollbar
import fdb
from datetime import datetime
import pyperclip
from tkinter import Menu
import sys
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import Frame, Text, INSERT
import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from pathlib import Path
from tkinter import ttk, messagebox
from fontTools.ttLib import TTFont
from tkinter import font as tkFont
import tkinter as tk
from tkinter import ttk
import datetime
import pyperclip
from function.document import *
from function.fetch_data import fetch_profesion_data
from tables.function.conn_base import connect_to_database
from function.get_user_data import get_user_data
from function.custom_front import custom_font
from function.copy_selected_row import copy_selected_row_to_clipboard
from function.translate_colums import translate_prof_columns
from button_function.add_button import open_add_profesion_window
from button_function.refresh_button import refresh_prof_table, color_rows,sort_column
from button_function.delete_button import delete_selected_prof_post
from tables.button_function.edit_button import open_edit_profesion_window
from tables.button_function.search_button import open_search_prof_window

current_dir = Path(__file__).resolve().parent
function_dir = current_dir / 'function'
sys.path.append(str(function_dir))

font_header = ('Time New Roman', 14, 'bold')


def create_context_menu(tree):
    context_menu = Menu(tree, tearoff=0)
    context_menu.add_command(label="Скопировать строку", command=lambda: copy_selected_row_to_clipboard(tree))

    def show_context_menu(event):
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)
            context_menu.post(event.x_root, event.y_root)

    tree.bind("<Button-3>", show_context_menu)

def wrap_text(text, width=30):
    """Обернуть текст по указанной ширине."""
    return '\n'.join(text[i:i+width] for i in range(0, len(text), width))



def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <username> <password> <role> ")
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
    root.title(f"Таблица Профессии - Авторизованный пользователь: {user_name} {first_name} {middle_name} {last_name}")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.state('zoomed') 
    current_dir = Path(__file__).resolve().parent
    icon_path = current_dir.parents[1] / 'src' / 'r_app.ico'
    root.iconbitmap(icon_path)
    custom_font()
    custom_font_header = ('CustomHeaderFont', 14, 'bold')
    custom_font_text =  ('CustomTextFont', 34, 'bold')
    custom_font_entry = ('CustomTextFont', 11)
    custom_font_buttom = ("CustomTextFont", 11, "bold")
    custom_font_status = ("CustomTextFont",20,"bold")
    conn = connect_to_database(username, password)
    if conn is None:
        return

    columns, data = fetch_profesion_data(conn)
    translated_columns = translate_prof_columns(columns)

    button_frame = Frame(root)
    button_frame.pack(pady=10, anchor='w')  

    button_output_frame = Frame(root)
    button_output_frame.pack(pady=10, anchor='e')

    if role == "Admin":
        ttkb.Button(button_frame, bootstyle="primary", text="Добавить профессию", command=lambda: open_add_profesion_window(conn, tree)).pack(side=LEFT, padx=5)
        ttkb.Button(button_frame, bootstyle="primary", text="Удалить профессию", command=lambda: delete_selected_prof_post(conn, tree, columns)).pack(side=LEFT, padx=5)
        ttkb.Button(button_frame, bootstyle="primary", text="Изменить профессию", command=lambda: open_edit_profesion_window(conn, tree, columns )).pack(side=LEFT, padx=5)
    ttkb.Button(button_frame, bootstyle="primary", text="Найти профессию", command=lambda: open_search_prof_window (conn, tree, columns )).pack(side=LEFT, padx=5)
    ttkb.Button(button_frame, bootstyle="primary", text="Обновить Таблицу", command=lambda: refresh_prof_table(conn, tree)).pack(side=LEFT, padx=5)

    def measure_text_width(text, font=None):
        """Измеряет ширину текста в пикселях."""
        if font is None:
            font = ("TkDefaultFont", 10)
        canvas = tk.Canvas(tree_frame)
        width = canvas.create_text(0, 0, text=text, font=font, anchor="nw")
        bbox = canvas.bbox(width)
        canvas.destroy()
        return bbox[2] - bbox[0]

    def set_column_widths(tree, columns):
        """Устанавливает ширину столбцов в зависимости от длины текста в ячейках."""
        for col in columns:
            max_width = measure_text_width(col) 
            for item in tree.get_children():
                cell_text = tree.set(item, col)
                cell_width = measure_text_width(cell_text)
                if cell_width > max_width:
                    max_width = cell_width
            tree.column(col, anchor='center', width=max_width)  

    tree_frame = tk.Frame(root)
    tree_frame.pack(fill=BOTH, expand=True)
    tree = ttkb.Treeview(tree_frame, show="headings")

    tree["columns"] = translated_columns
    for col in translated_columns:
        tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
    # Вертикальный ползунок
    v_scrollbar = ttkb.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview, bootstyle='primary')
    v_scrollbar.pack(side=RIGHT, fill=Y)
    
    # Горизонтальный
    h_scrollbar = ttkb.Scrollbar(tree_frame, orient=HORIZONTAL, command=tree.xview, bootstyle='primary')
    h_scrollbar.pack(side=BOTTOM, fill=X)

    tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    for i, row in enumerate(data):
        data[i] = [wrap_text(str(value)) if columns[j] in ["DESCRIPTION"] else str(value) for j, value in enumerate(row)]

    for item in data:
        tree.insert("", "end", values=item)

    set_column_widths(tree, translated_columns)
    tree.pack(fill=BOTH, expand=True) 

    style = ttk.Style()
    style.configure("Treeview.Heading", background="#c61b14", foreground="white", font=('CustomTextFont', 11, "bold"))
    style.configure("Treeview", rowheight=40, background="white", foreground="black", font=custom_font_entry)
    style.configure('TButton', backgroundg="#fff", font=custom_font_buttom)
    color_rows(tree)

    create_context_menu(tree)
    root.protocol("WM_DELETE_WINDOW", lambda: conn.close() or root.destroy())
    root.mainloop()

if __name__ == "__main__":
    main()