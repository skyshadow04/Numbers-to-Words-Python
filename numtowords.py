import tkinter as tk
from tkinter import messagebox

uppercase_var = tk.BooleanVar(value=False)


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
root.geometry("450x320")
root.resizable(False, False)

tk.Label(root, text="Enter Amount (AED):", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 14), width=25, justify="center")
entry.pack(pady=5)
entry.insert(0, "1234.50")  # Placeholder example

uppercase_btn = tk.Button(root, text="Uppercase: OFF", font=("Arial", 10), command=toggle_uppercase)
uppercase_btn.pack(pady=(0, 10))

convert_btn = tk.Button(root, text="Convert to Words", font=("Arial", 12, "bold"), bg="#0073e6", fg="white", command=process_conversion)
convert_btn.pack(pady=5)

tk.Label(root, text="Result:", font=("Arial", 11)).pack()
result_text = tk.Text(root, font=("Arial", 11), height=4, width=45, wrap="word")
result_text.pack(pady=5)

root.mainloop()
