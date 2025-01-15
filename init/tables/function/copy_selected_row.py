import pyperclip
from tkinter import messagebox
def copy_selected_row_to_clipboard(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для копирования")
        return

    row_values = tree.item(selected_item)['values']
    clipboard_text = "\t".join(map(str, row_values))
    pyperclip.copy(clipboard_text)