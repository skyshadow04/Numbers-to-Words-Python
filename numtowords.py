import os
import sys
import tkinter as tk
from tkinter import messagebox

uppercase_var = None


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def number_to_words(n):
    if n == 0: return "Zero"
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    units = ["", "Thousand", "Million", "Billion"]
    
    def get_below_thousand(num):
        if num < 10: return ones[num]
        if num < 20: return teens[num-10]
        if num < 100: return tens[num//10] + (" " + ones[num%10] if num%10 else "")
        return ones[num//100] + " Hundred" + (" " + get_below_thousand(num%100) if num%100 else "")

    res, i = "", 0
    while n > 0:
        if n % 1000 != 0:
            res = get_below_thousand(n % 1000) + " " + units[i] + " " + res
        n //= 1000
        i += 1
    return res.strip()

def currency_to_words(amount_str):
    # Split into Dirhams and Fils parts
    if '.' in amount_str:
        dirham_part, fil_part = amount_str.split('.')
        fil_part = fil_part[:2]  # Keep only 2 decimal places
        if len(fil_part) == 1:   # Pad single digit (.5 -> 50 fils)
            fil_part += '0'
    else:
        dirham_part, fil_part = amount_str, '00'

    dirhams = int(dirham_part) if dirham_part else 0
    fils = int(fil_part) if fil_part else 0

    if dirhams == 0 and fils == 0:
        return "Zero Dirhams"

    result = []
    
    # Process Dirhams
    if dirhams > 0:
        dirham_words = number_to_words(dirhams)
        suffix = "Dirham" if dirhams == 1 else "Dirhams"
        result.append(f"{dirham_words} {suffix}")
        
    # Process Fils
    if fils > 0:
        fil_words = number_to_words(fils)
        suffix = "Fil" if fils == 1 else "Fils"
        result.append(f"{fil_words} {suffix}")

    return " and ".join(result) + " Only"

def toggle_uppercase():
    if uppercase_var is None:
        return
    uppercase_var.set(not uppercase_var.get())
    uppercase_btn.config(text="Uppercase: ON" if uppercase_var.get() else "Uppercase: OFF")
    if entry.get().strip():
        process_conversion()


def process_conversion():
    try:
        user_input = entry.get().strip()
        if not user_input:
            raise ValueError("Empty")
            
        # Validate that it is a positive floating-point number
        float_val = float(user_input)
        if float_val < 0 or float_val > 999999999999.99:
            raise ValueError("Out of bounds")
            
        word_result = currency_to_words(user_input)
        if uppercase_var.get():
            word_result = word_result.upper()
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, word_result)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive amount (e.g., 1250.50) up to 999 Billion.")

# GUI Setup
root = tk.Tk()
root.title("AED Currency to Words Converter")
root.geometry("520x420")
root.resizable(False, False)
root.configure(bg="#f4f7fb")

uppercase_var = tk.BooleanVar(value=False)

icon_path = resource_path("icon.ico")
if os.path.exists(icon_path):
    try:
        root.iconbitmap(default=icon_path)
        root.wm_iconbitmap(icon_path)
    except tk.TclError:
        pass

main_frame = tk.Frame(root, bg="#f4f7fb")
main_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=20)

header = tk.Label(
    main_frame,
    text="Number to Words Converter",
    font=("Segoe UI", 16, "bold"),
    fg="#102a43",
    bg="#f4f7fb"
)
header.pack(pady=(0, 10))

subtitle = tk.Label(
    main_frame,
    text="Convert amounts to words with a modern, clean look",
    font=("Segoe UI", 10),
    fg="#486581",
    bg="#f4f7fb"
)
subtitle.pack(pady=(0, 16))

card = tk.Frame(main_frame, bg="white", bd=0, highlightthickness=1, highlightbackground="#d9e2ec")
card.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

input_label = tk.Label(card, text="Enter Amount (AED)", font=("Segoe UI", 11, "bold"), fg="#243b53", bg="white")
input_label.pack(anchor="w", padx=16, pady=(16, 6))

entry = tk.Entry(
    card,
    font=("Segoe UI", 14),
    width=28,
    justify="center",
    bd=1,
    relief="solid",
    highlightthickness=1,
    highlightcolor="#7b61ff",
    highlightbackground="#cbd2d9"
)
entry.pack(padx=16, pady=4)
entry.insert(0, "1234.50")

button_row = tk.Frame(card, bg="white")
button_row.pack(pady=(10, 8))

uppercase_btn = tk.Button(
    button_row,
    text="Uppercase: OFF",
    font=("Segoe UI", 10),
    bg="#e9eef7",
    fg="#243b53",
    relief="flat",
    padx=10,
    pady=6,
    command=toggle_uppercase
)
uppercase_btn.pack(side=tk.LEFT, padx=(0, 8))

convert_btn = tk.Button(
    button_row,
    text="Convert to Words",
    font=("Segoe UI", 11, "bold"),
    bg="#2563eb",
    fg="white",
    relief="flat",
    padx=12,
    pady=6,
    command=process_conversion
)
convert_btn.pack(side=tk.LEFT)

result_label = tk.Label(card, text="Result", font=("Segoe UI", 11, "bold"), fg="#243b53", bg="white")
result_label.pack(anchor="w", padx=16, pady=(10, 6))

result_frame = tk.Frame(card, bg="white")
result_frame.pack(fill=tk.BOTH, padx=16, pady=(0, 16))

result_text = tk.Text(result_frame, font=("Segoe UI", 11), height=8, width=34, wrap="word", bd=1, relief="solid")
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

result_scroll = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
result_scroll.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=result_scroll.set)

root.mainloop()
