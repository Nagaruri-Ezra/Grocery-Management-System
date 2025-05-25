import tkinter as tk
from tkinter import messagebox

# Dictionary to store carts for each user
cart = {}

# Predefined units for item quantity
UNITS = ["kg", "liter", "dozen", "pcs"]

# To keep track of the currently active user
current_user = None

# Function to add an item to the current user's cart
def add_item_to_cart(event=None):
    if not current_user:
        messagebox.showerror("Error", "Please enter a user name first.")
        return

    # Get user input from entry fields
    name = name_entry.get().strip()
    price_text = price_entry.get().strip()
    quantity_text = quantity_entry.get().strip()
    unit = unit_var.get()

    # Check if any field is empty
    if not name or not price_text or not quantity_text or unit == "":
        messagebox.showerror("Error", "All fields are required.")
        return

    # Try converting input to float and validating
    try:
        price = float(price_text)
        quantity = float(quantity_text)
        if price <= 0 or quantity <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter valid price and quantity.")
        return

    # Initialize user cart if new
    if current_user not in cart:
        cart[current_user] = {}

    # If item already exists, increase quantity; else add new
    if name in cart[current_user]:
        cart[current_user][name]["quantity"] += quantity
    else:
        cart[current_user][name] = {"quantity": quantity, "unit": unit, "price": price}

    # Refresh display and clear input fields
    update_cart_display()
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    name_entry.focus_set()

# Function to update the cart list display and total
def update_cart_display():
    if not current_user:
        return

    cart_list.delete(0, tk.END)  # Clear listbox
    total = 0.0
    for name, item in cart.get(current_user, {}).items():
        price = item['price']
        qty = item['quantity']
        unit = item['unit']
        subtotal = price * qty
        total += subtotal
        cart_list.insert(tk.END, f"{name} x {qty} {unit} = ₹{subtotal:.2f}")
    
    total_label.config(text=f"Total: ₹{total:.2f}")

# Function to clear the current user's cart and bill area
def clear_cart():
    if current_user:
        cart[current_user].clear()
        update_cart_display()
        bill_text.delete('1.0', tk.END)

# Function to generate and display the formatted bill
def generate_bill():
    if not current_user:
        messagebox.showerror("Error", "Please enter a user name first.")
        return

    if current_user not in cart or not cart[current_user]:
        messagebox.showinfo("Info", "Cart is empty.")
        return

    bill_text.delete('1.0', tk.END)
    bill_text.insert(tk.END, f"{'BILL FOR ' + current_user.upper():^50}\n")
    bill_text.insert(tk.END, "---- Grocery Items ----\n")
    bill_text.insert(tk.END, f"{'Name':<15}{'Qty':<12}{'Price':<10}{'Subtotal':<10}\n")
    bill_text.insert(tk.END, "-" * 50 + "\n")

    total = 0.0
    for name, item in cart[current_user].items():
        qty = item['quantity']
        unit = item['unit']
        price = item['price']
        subtotal = price * qty
        total += subtotal
        bill_text.insert(tk.END, f"{name:<15}{str(qty) + ' ' + unit:<12}{price:<10}{subtotal:<10.2f}\n")

    bill_text.insert(tk.END, "-" * 50 + "\n")
    bill_text.insert(tk.END, f"{'Total Bill:':<35} ₹{total:.2f}\n")

# Function to set the current user and update display
def set_user(event=None):
    global current_user
    user_name = user_name_entry.get().strip()
    if not user_name:
        messagebox.showerror("Error", "User name cannot be empty.")
        return

    current_user = user_name
    if current_user not in cart:
        cart[current_user] = {}

    user_label.config(text=f"Current User: {current_user}")
    user_name_entry.delete(0, tk.END)
    name_entry.focus_set()
    update_cart_display()

# Clears the bill and cart for the current user
def clear_user_bill():
    if not current_user:
        messagebox.showerror("Error", "Please enter a user name first.")
        return

    bill_text.delete('1.0', tk.END)
    cart[current_user].clear()
    update_cart_display()

# Clears all data from the system
def clear_all_bills():
    global cart
    cart = {}
    bill_text.delete('1.0', tk.END)
    update_cart_display()

# Removes the selected item from the current user's cart
def remove_selected_item():
    if not current_user:
        messagebox.showerror("Error", "Please enter a user name first.")
        return

    selected = cart_list.curselection()
    if not selected:
        messagebox.showinfo("Info", "Please select an item to remove.")
        return

    item_text = cart_list.get(selected[0])
    item_name = item_text.split(' x ')[0]

    if item_name in cart[current_user]:
        del cart[current_user][item_name]
        update_cart_display()

# ---------- GUI Layout ----------

root = tk.Tk()
root.title("Grocery Management System")
root.geometry("1000x600")

# Top Input Frame
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

# Input Widgets
tk.Label(top_frame, text="Enter Your Name:").grid(row=0, column=0, padx=5, sticky="e")
user_name_entry = tk.Entry(top_frame)
user_name_entry.grid(row=0, column=1)
user_name_entry.bind("<Return>", set_user)
tk.Button(top_frame, text="Set User", command=set_user).grid(row=0, column=2, padx=10)

# Product Input Section
tk.Label(top_frame, text="Product Name:").grid(row=1, column=0, padx=5, sticky="e")
name_entry = tk.Entry(top_frame)
name_entry.grid(row=1, column=1)
name_entry.bind("<Return>", lambda event: price_entry.focus_set())

tk.Label(top_frame, text="Price (₹):").grid(row=1, column=2, padx=5, sticky="e")
price_entry = tk.Entry(top_frame)
price_entry.grid(row=1, column=3)
price_entry.bind("<Return>", lambda event: quantity_entry.focus_set())

tk.Label(top_frame, text="Quantity:").grid(row=1, column=4, padx=5, sticky="e")
quantity_entry = tk.Entry(top_frame)
quantity_entry.grid(row=1, column=5)
quantity_entry.bind("<Return>", lambda event: unit_menu.focus_set())

tk.Label(top_frame, text="Unit:").grid(row=1, column=6, padx=5, sticky="e")
unit_var = tk.StringVar()
unit_var.set("kg")
unit_menu = tk.OptionMenu(top_frame, unit_var, *UNITS)
unit_menu.grid(row=1, column=7)
unit_menu.bind("<Return>", add_item_to_cart)

tk.Button(top_frame, text="Add Item to Cart", command=add_item_to_cart).grid(row=1, column=8, padx=10)

# Middle Frame: Cart and Bill
middle_frame = tk.Frame(root)
middle_frame.pack(fill="both", expand=True, padx=10)

# Left Frame - Cart and Controls
left_frame = tk.Frame(middle_frame)
left_frame.pack(side="left", fill="both", expand=True)

user_label = tk.Label(left_frame, text="Current User: None", font=("Arial", 12))
user_label.pack(pady=5)

tk.Label(left_frame, text="Cart:", font=("Arial", 12)).pack()
cart_list = tk.Listbox(left_frame, width=45)
cart_list.pack(pady=5)

total_label = tk.Label(left_frame, text="Total: ₹0.00", font=("Arial", 14))
total_label.pack(pady=5)

# Action Buttons
tk.Button(left_frame, text="Clear Cart", command=clear_cart).pack(pady=5)
tk.Button(left_frame, text="Generate Bill", command=generate_bill).pack(pady=5)
tk.Button(left_frame, text="Remove Selected Item", command=remove_selected_item).pack(pady=5)
tk.Button(left_frame, text="Clear User Bill", command=clear_user_bill).pack(pady=5)
tk.Button(left_frame, text="Clear All Bills", command=clear_all_bills).pack(pady=5)

# Right Frame - Bill Display
right_frame = tk.Frame(middle_frame)
right_frame.pack(side="right", fill="both", expand=True)

tk.Label(right_frame, text="Generated Bill:", font=("Arial", 12)).pack()
bill_text = tk.Text(right_frame, height=25, width=60)
bill_text.pack(pady=5)

# Focus cursor on user name entry on startup
user_name_entry.focus_set()
root.mainloop()