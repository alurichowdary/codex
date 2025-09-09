import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

DATA_FILE = "bmi_data.json"

# -------------------- Core Logic --------------------
def calculate_bmi(weight, height):
    try:
        bmi = float(weight) / (float(height) ** 2)
        return round(bmi, 2)
    except:
        return None

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def save_to_file(entry):
    history = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            history = json.load(f)
    history.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=4)

def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# -------------------- Event Handlers --------------------
def calculate_and_store():
    name = name_entry.get()
    weight = weight_entry.get()
    height = height_entry.get()

    if not name or not weight or not height:
        messagebox.showwarning("Missing info", "Please fill in all fields.")
        return

    bmi = calculate_bmi(weight, height)
    if bmi is None or bmi <= 0:
        messagebox.showerror("Invalid Input", "Enter valid positive numbers for weight and height.")
        return

    category = categorize_bmi(bmi)
    result_label.config(text=f"{name}'s BMI: {bmi} ({category})")

    entry = {
        "name": name,
        "weight": float(weight),
        "height": float(height),
        "bmi": bmi,
        "category": category
    }
    save_to_file(entry)
    update_history_tree()

def update_history_tree():
    for item in history_tree.get_children():
        history_tree.delete(item)
    history = load_history()
    for entry in history:
        history_tree.insert("", "end", values=(
            entry["name"], entry["weight"], entry["height"], entry["bmi"], entry["category"]
        ))

def clear_fields():
    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="")

# -------------------- GUI Setup --------------------
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("600x500")

# --- Input Fields ---
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Weight (kg):").grid(row=1, column=0, padx=10, pady=5)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Height (m):").grid(row=2, column=0, padx=10, pady=5)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1, padx=10, pady=5)

# --- Buttons ---
tk.Button(root, text="Calculate BMI", command=calculate_and_store).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="Clear", command=clear_fields).grid(row=4, column=0, columnspan=2)

# --- Result Display ---
result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
result_label.grid(row=5, column=0, columnspan=2, pady=10)

# --- History Viewer ---
tk.Label(root, text="BMI History").grid(row=6, column=0, columnspan=2)

columns = ("Name", "Weight", "Height", "BMI", "Category")
history_tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    history_tree.heading(col, text=col)
    history_tree.column(col, width=100)
history_tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

update_history_tree()
root.mainloop()