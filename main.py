import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk

class UserApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("User Application")
        self.root.geometry("600x400")

        self.conn = sqlite3.connect("users.db")
        self.c = self.conn.cursor()
        self.create_table()

        self.id_label = tk.Label(self.root, text="ID:")
        self.id_label.pack()
        self.id_entry = tk.Entry(self.root)
        self.id_entry.pack()

        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.age_label = tk.Label(self.root, text="Age:")
        self.age_label.pack()
        self.age_entry = tk.Entry(self.root)
        self.age_entry.pack()

        self.add_button = tk.Button(self.root, text="Add User", command=self.add_user)
        self.add_button.pack()

        self.delete_button = tk.Button(self.root, text="Delete User", command=self.delete_user)
        self.delete_button.pack()

        self.find_button = tk.Button(self.root, text="Find Users", command=self.find_users)
        self.find_button.pack()

        self.update_button = tk.Button(self.root, text="Update User", command=self.update_user)
        self.update_button.pack()

        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Age"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.pack()

        self.view_records()

    def create_table(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")

    def add_user(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        if id and name and age:
            self.c.execute("INSERT INTO users (id, name, age) VALUES (?, ?, ?)", (id, name, age))
            self.conn.commit()
            messagebox.showinfo("Success", "User added successfully.")
            self.id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.view_records()
        else:
            messagebox.showerror("Error", "Please enter ID, name, and age.")

    def delete_user(self):
        id = self.id_entry.get()
        if id:
            self.c.execute("DELETE FROM users WHERE id=?", (id,))
            self.conn.commit()
            messagebox.showinfo("Success", "User deleted successfully.")
            self.id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.view_records()
        else:
            messagebox.showerror("Error", "Please enter an ID.")

    def find_users(self):
        age = self.age_entry.get()
        if age:
            self.c.execute("SELECT * FROM users WHERE age=?", (age,))
            users = self.c.fetchall()
            if users:
                messagebox.showinfo("Users Found", f"Users with age {age}:\n\n{users}")
            else:
                messagebox.showinfo("No Users", f"No users found with age {age}.")
        else:
            messagebox.showerror("Error", "Please enter an age.")

    def update_user(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        if id and name and age:
            self.c.execute("UPDATE users SET name=?, age=? WHERE id=?", (name, age, id))
            self.conn.commit()
            messagebox.showinfo("Success", "User updated successfully.")
            self.id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.view_records()
        else:
            messagebox.showerror("Error", "Please enter ID, name, and age.")

    def view_records(self):
        self.tree.delete(*self.tree.get_children())
        self.c.execute("SELECT * FROM users")
        rows = self.c.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = UserApp()
    app.run()
