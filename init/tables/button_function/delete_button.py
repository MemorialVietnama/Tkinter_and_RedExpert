from tkinter import *
from ttkbootstrap.constants import *
from tkinter import messagebox
import fdb
from tables.button_function.refresh_button import *

def delete_selected_employer(conn, tree, columns):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строки для удаления")
        return

    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранных сотрудников?"):
        try:
            cursor = conn.cursor()
            for item in selected_items:
                selected_employer_id = tree.item(item)['values'][columns.index("ID_EMPLOYER")]
                cursor.execute("DELETE FROM EMPLOYER WHERE ID_EMPLOYER = ?", [selected_employer_id])
            conn.commit()
            messagebox.showwarning("Успех", "Сотрудники успешно удалены")
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления сотрудников: {e}")

def delete_selected_employer_list(conn, tree, columns ):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строку для удаления")
        return

    selected_employer_list_id = tree.item(selected_item)['values'][columns.index("ID")]

    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранную запись?"):
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM EMPLOYER_LIST WHERE EMPLOYER_NAME = ?", [selected_employer_list_id])
            conn.commit()
            messagebox.showinfo("Успех", "Запись успешно удалена")
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления записи: {e}")

def delete_selected_benefits(conn, tree, columns):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строки для удаления")
        return

    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранных сотрудников?"):
        try:
            cursor = conn.cursor()
            for item in selected_items:
                selected_employer_id = str(tree.item(item)['values'][columns.index("ID")]) 
                # First, check and delete dependenci
                cursor.execute("DELETE FROM BENEFITS WHERE ID = ?", [selected_employer_id])
            conn.commit()
            messagebox.showinfo("Успех", "Льгота удалена!")
            refresh_bef_table(conn, tree)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления льготы: {e}")
            print(e)

def delete_selected_dep_employer(conn, tree, columns):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строки для удаления")
        return

    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранных сотрудников?"):
        try:
            cursor = conn.cursor()
            for item in selected_items:
                selected_employer_id = str(tree.item(item)['values'][columns.index("ID")]) 
                cursor.execute("DELETE FROM DEPARTMENT WHERE ID = ?", [selected_employer_id])
            conn.commit()
            messagebox.showinfo("Успех", "Отдел удален!!")
            refresh_dep_table(conn, tree)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления льготы: {e}")
            print(e)
def delete_selected_prof_post(conn, tree, columns):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строки для удаления")
        return

    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранные профессию?"):
        try:
            cursor = conn.cursor()
            for item in selected_items:
                selected_post_title = tree.item(item)['values'][columns.index("ID")]
                cursor.execute("DELETE FROM PROFESSION_NEW WHERE ID = ?", [selected_post_title])
            conn.commit()
            messagebox.showinfo("Успех", "Профессия успешно удалена")
            refresh_prof_table (conn,tree)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления профессии: {e}")
def delete_selected_sovm_post(conn, tree, columns):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строки для удаления")
        return

    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранную Категорию?"):
        try:
            cursor = conn.cursor()
            for item in selected_items:
                selected_post_title = tree.item(item)['values'][columns.index("ID")]
                cursor.execute("DELETE FROM SOVMEST WHERE ID = ?", [selected_post_title])
            conn.commit()
            messagebox.showinfo("Успех", "Категория успешно удалена")
            refresh_sovm_table (conn,tree)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления категории: {e}")

def delete_selected_document(conn, tree, columns):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строки для удаления")
        return

    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранные документы?"):
        try:
            cursor = conn.cursor()
            for item in selected_items:
                selected_document_id = tree.item(item)['values'][columns.index("ID")]
                cursor.execute("DELETE FROM DOCUMENTS WHERE ID = ?", [selected_document_id])
            conn.commit()
            messagebox.showinfo("Успех", "Документы успешно удалены")
            refresh_doc_table(conn, tree)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления документов: {e}")

def delete_selected_post(conn, tree, columns):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите строки для удаления")
        return

    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить Пост?"):
        try:
            cursor = conn.cursor()
            for item in selected_items:
                selected_document_id = tree.item(item)['values'][columns.index("ID")]
                cursor.execute("DELETE FROM POSTS WHERE ID = ?", [selected_document_id])
            conn.commit()
            messagebox.showinfo("Успех", "Пост успешно удален")
            refresh_doc_table(conn, tree)
        except fdb.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления поста: {e}")