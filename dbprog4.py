# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 08:43:19 2021

@author: 207199
"""
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def run_query(query, parameters = ()):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result

def get_products():
    records = t1.get_children()
    for element in records:
        t1.delete(element)
    query = 'SELECT * FROM product ORDER BY name DESC'
    db_rows = run_query(query)
    
    for row in db_rows:
        t1.insert('', 0, text = row[1], values = row[2])
        
def validation():
    return len(e1.get()) != 0 and len(e1.get()) != 0

def add_product():
    if validation():
        query = 'INSERT INTO product VALUES(NULL, ?, ?)'
        parameters = (e1.get(), e2.get())
        run_query(query, parameters)
        message['text'] = 'Product {} added successfully.'.format(e1.get())
        e1.delete(0, END)
        e2.delete(0, END)
    else:
        message['text'] = 'Name and Price is required.'
    get_products()

def delete_product():
    message['text'] = ''
    try:
        t1.item(t1.selection())['text'][0]
    except IndexError as e:
        message['text'] = 'Please select a record.'
        return
    message['text'] = ''
    sss = t1.item(t1.selection())['text']
    query = 'DELETE from product where name = ?'
    run_query(query, (sss, ))
    message['text'] = 'Record {} deleted successfully.'.format(sss)
    get_products()
    
def edit_product():
    message['text'] = ''
    try:
        t1.item(t1.selection())['values'][0]
    except IndexError as e:
        message['text'] = 'Please, select Record'
        return
    old_name = t1.item(t1.selection())['text']
    old_price = t1.item(t1.selection())['values'][0]
    edit_wind = Toplevel()
    edit_wind.title = 'Edit Product'
        # Old Name
    Label(edit_wind, text = 'Old Name:').grid(row = 0, column = 1)
    Entry(edit_wind, textvariable = StringVar(edit_wind, value = old_name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
    Label(edit_wind, text = 'New Name:').grid(row = 1, column = 1)
    new_name = Entry(edit_wind)
    new_name.grid(row = 1, column = 2)

        # Old Price 
    Label(edit_wind, text = 'Old Price:').grid(row = 2, column = 1)
    Entry(edit_wind, textvariable = StringVar(edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # New Price
    Label(edit_wind, text = 'New Price:').grid(row = 3, column = 1)
    new_price= Entry(edit_wind)
    new_price.grid(row = 3, column = 2)

    Button(edit_wind, text = 'Update', command = lambda: edit_records(new_name.get(), old_name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
    edit_wind.mainloop()

def edit_records(new_name, old_name, new_price, old_price):
    query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
    parameters = (new_name, new_price, old_name, old_price)
    run_query(query, parameters)
#    edit_wind.destroy()
    message['text'] = 'Record {} updated successfylly'.format(new_name)
    get_products()
    
root = tk.Tk()
root.geometry("400x420")
root.title("Products")

l1 = Label(root, text = "Register new Product").place(x = 100, y = 18)
l2 = Label(root, text = "Name").place(x = 100, y = 40)
l3 = Label(root, text = "Price").place(x = 100, y = 60)
e1 = Entry(root)
e1.place(x = 152, y = 40)
e2 = Entry(root)
e2.place(x = 152, y = 60)
b1 = Button(root, text = "Save Product", width = 24, command = add_product).place(x = 100, y = 80)

t1 = ttk.Treeview(height =10, columns =2)
t1.place(x = 0, y = 120)
t1.heading('#0', text = 'NAME', anchor = CENTER)
t1.heading('#1', text = 'PRICE', anchor = CENTER)
           
b2 = Button(root, text = "DELETE", width = 25, command = delete_product).place(x = 0, y = 360)
b3 = Button(root, text = "EDIT", width = 25, command = edit_product).place(x = 200, y = 360)

message = Label(text='', fg = 'red')
message.place(x = 10, y = 390)
        
get_products()
root.mainloop()