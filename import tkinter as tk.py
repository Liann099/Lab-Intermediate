import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Membuat koneksi ke database SQLite
conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()

# Membuat tabel contacts jika belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Fungsi untuk menambahkan kontak baru
def add_contact():
    name = entry_name.get()
    address = entry_address.get()
    phone = entry_phone.get()
    email = entry_email.get()
    cursor.execute('''
    INSERT INTO contacts (name, address, phone, email)
    VALUES (?, ?, ?, ?)
    ''', (name, address, phone, email))
    conn.commit()
    messagebox.showinfo("Info", "Contact inserted successfully.")
    display_contacts()
    clear_entries()

# Fungsi untuk menampilkan semua kontak
def display_contacts():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM contacts')
    for contact in cursor.fetchall():
        tree.insert('', tk.END, values=contact)

# Fungsi untuk memperbarui kontak
def update_contact():
    selected_item = tree.selection()[0]
    contact_id = tree.item(selected_item)['values'][0]
    name = entry_name.get()
    address = entry_address.get()
    phone = entry_phone.get()
    email = entry_email.get()
    cursor.execute('''
    UPDATE contacts
    SET name = ?, address = ?, phone = ?, email = ?
    WHERE id = ?
    ''', (name, address, phone, email, contact_id))
    conn.commit()
    messagebox.showinfo("Info", "Contact updated successfully.")
    display_contacts()
    clear_entries()

# Fungsi untuk menghapus kontak
def delete_contact():
    selected_item = tree.selection()[0]
    contact_id = tree.item(selected_item)['values'][0]
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    messagebox.showinfo("Info", "Contact deleted successfully.")
    display_contacts()
    clear_entries()

# Fungsi untuk menghapus semua entri
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Fungsi untuk menampilkan data kontak yang dipilih di entri
def select_contact(event):
    selected_item = tree.selection()[0]
    contact = tree.item(selected_item)['values']
    entry_name.delete(0, tk.END)
    entry_name.insert(0, contact[1])
    entry_address.delete(0, tk.END)
    entry_address.insert(0, contact[2])
    entry_phone.delete(0, tk.END)
    entry_phone.insert(0, contact[3])
    entry_email.delete(0, tk.END)
    entry_email.insert(0, contact[4])

# Membuat jendela utama
root = tk.Tk()
root.title("Contact Manager")

# Membuat frame untuk entri kontak
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Name").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_form)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Address").grid(row=1, column=0, padx=5, pady=5)
entry_address = tk.Entry(frame_form)
entry_address.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Phone").grid(row=2, column=0, padx=5, pady=5)
entry_phone = tk.Entry(frame_form)
entry_phone.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Email").grid(row=3, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_form)
entry_email.grid(row=3, column=1, padx=5, pady=5)

# Membuat frame untuk tombol
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Add Contact", command=add_contact).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Update Contact", command=update_contact).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_buttons, text="Delete Contact", command=delete_contact).grid(row=0, column=2, padx=5, pady=5)
tk.Button(frame_buttons, text="Clear Entries", command=clear_entries).grid(row=0, column=3, padx=5, pady=5)

# Membuat Treeview untuk menampilkan kontak
columns = ('id', 'name', 'address', 'phone', 'email')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=100)

tree.pack(pady=10)
tree.bind('<<TreeviewSelect>>', select_contact)

# Menampilkan kontak yang ada pada saat aplikasi pertama kali dijalankan
display_contacts()

# Menjalankan aplikasi Tkinter
root.mainloop()

# Menutup koneksi ke database
conn.close()
