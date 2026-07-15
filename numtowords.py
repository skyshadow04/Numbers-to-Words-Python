import os
import sys
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

uppercase_var = None


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_history_file_path():
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(base_dir, f"converted_numbers_{today}.txt")


def append_number_to_history(number, file_path=None):
    history_path = file_path or get_history_file_path()
    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as history_file:
            existing_lines = [line.rstrip("\n") for line in history_file if line.strip()]
    else:
        existing_lines = []

    next_index = len(existing_lines) + 1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(history_path, "a", encoding="utf-8") as history_file:
        history_file.write(f"{next_index}. {number} {timestamp}\n")


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


def clear_input():
    entry.delete(0, tk.END)
    entry.focus_set()
    result_text.delete("1.0", tk.END)
    reset_copy_feedback()


def reset_copy_feedback():
    if copy_btn is not None:
        copy_btn.config(text="Copy to Clipboard", bg="#0f766e", fg="white")
    if status_label is not None:
        status_label.config(text="", fg="#16a34a")


def animate_copy_feedback(success=True):
    if success:
        copy_btn.config(text="Copying...", bg="#0f766e", fg="white")
        status_label.config(text="Copying to clipboard", fg="#0f766e")
        root.after(180, lambda: copy_btn.config(text="Copied ✓", bg="#16a34a", fg="white"))
        root.after(180, lambda: status_label.config(text="Copied to clipboard", fg="#16a34a"))
        root.after(1200, reset_copy_feedback)
    else:
        copy_btn.config(text="Nothing to copy", bg="#b91c1c", fg="white")
        status_label.config(text="No result available", fg="#b91c1c")
        root.after(1200, reset_copy_feedback)


def copy_to_clipboard():
    try:
        text_to_copy = result_text.get("1.0", tk.END).strip()
        if not text_to_copy:
            raise ValueError("No result")
        root.clipboard_clear()
        root.clipboard_append(text_to_copy)
        animate_copy_feedback(True)
    except Exception:
        animate_copy_feedback(False)


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
        append_number_to_history(user_input)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, word_result)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive amount (e.g., 1250.50) up to 999 Billion.")

def main():
    global root, uppercase_var, entry, clear_btn, uppercase_btn, convert_btn, copy_btn, status_label, result_text

    root = tk.Tk()
    root.title("LDWS AED Currency to Words Converter")
    root.geometry("540x500")
    root.resizable(False, False)
    root.configure(bg="#f3f6fb")

    uppercase_var = tk.BooleanVar(value=False)

    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(default=icon_path)
            root.wm_iconbitmap(icon_path)
        except tk.TclError:
            pass

    main_frame = tk.Frame(root, bg="#f3f6fb")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=20)

    header = tk.Label(
        main_frame,
        text="Number to Words Converter",
        font=("Segoe UI", 18, "bold"),
        fg="#0f172a",
        bg="#f3f6fb"
    )
    header.pack(pady=(0, 6))

    subtitle = tk.Label(
        main_frame,
        text="Convert AED amounts into polished words in a clean, modern layout",
        font=("Segoe UI", 10),
        fg="#64748b",
        bg="#f3f6fb"
    )
    subtitle.pack(pady=(0, 14))

    card = tk.Frame(main_frame, bg="#ffffff", bd=0, highlightthickness=1, highlightbackground="#dbeafe")
    card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

    input_label = tk.Label(card, text="Enter Amount (AED)", font=("Segoe UI", 11, "bold"), fg="#1e293b", bg="white")
    input_label.pack(anchor="w", padx=18, pady=(16, 6))

    input_row = tk.Frame(card, bg="white")
    input_row.pack(fill=tk.X, padx=18, pady=4)

    entry = tk.Entry(
        input_row,
        font=("Segoe UI", 14),
        width=28,
        justify="center",
        bd=0,
        relief="flat",
        highlightthickness=1,
        highlightcolor="#2563eb",
        highlightbackground="#cbd5e1"
    )
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    entry.insert(0, "1234.50")

    clear_btn = tk.Button(
        input_row,
        text="Clear",
        font=("Segoe UI", 10),
        bg="#e2e8f0",
        fg="#334155",
        relief="flat",
        padx=10,
        pady=6,
        command=clear_input
    )
    clear_btn.pack(side=tk.RIGHT, padx=(8, 0))

    button_row = tk.Frame(card, bg="white")
    button_row.pack(pady=(10, 8))

    uppercase_btn = tk.Button(
        button_row,
        text="Uppercase: OFF",
        font=("Segoe UI", 10),
        bg="#f1f5f9",
        fg="#334155",
        relief="flat",
        padx=12,
        pady=6,
        command=toggle_uppercase
    )
    uppercase_btn.pack(side=tk.LEFT, padx=(0, 8))

    convert_btn = tk.Button(
        button_row,
        text="Convert to Words",
        font=("Segoe UI", 10),
        bg="#2563eb",
        fg="white",
        relief="raised",
        bd=0,
        padx=12,
        pady=6,
        command=process_conversion
    )
    convert_btn.pack(side=tk.LEFT, padx=(0, 8))

    copy_btn = tk.Button(
        button_row,
        text="Copy to Clipboard",
        font=("Segoe UI", 10),
        bg="#0f766e",
        fg="white",
        relief="raised",
        bd=0,
        padx=12,
        pady=6,
        command=copy_to_clipboard
    )
    copy_btn.pack(side=tk.LEFT)

    status_label = tk.Label(
        button_row,
        text="",
        font=("Segoe UI", 9),
        fg="#16a34a",
        bg="white"
    )
    status_label.pack(side=tk.LEFT, padx=(8, 0))

    result_label = tk.Label(card, text="Result", font=("Segoe UI", 11, "bold"), fg="#1e293b", bg="white")
    result_label.pack(anchor="w", padx=18, pady=(10, 6))

    result_frame = tk.Frame(card, bg="white")
    result_frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 16))

    result_text = tk.Text(result_frame, font=("Segoe UI", 11), height=10, wrap="word", bd=1, relief="solid", bg="#f8fafc")
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    result_scroll = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
    result_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    result_text.config(yscrollcommand=result_scroll.set)

    root.mainloop()


if __name__ == "__main__":
    main()
