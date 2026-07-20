# Number to Words Converter (Dirhams & Fils)

## Overview

The **Number to Words Converter (Dirhams & Fils)** is a desktop application developed in **Python** using the **Tkinter** graphical user interface (GUI). The application converts a numeric amount entered by the user into its equivalent words in **United Arab Emirates (UAE) currency**, displaying the amount in **Dirhams and Fils**.

This application is designed to simplify the conversion of monetary values for use in financial documents such as cheques, invoices, receipts, and accounting records.

---

## Features

- User-friendly graphical interface built with **Tkinter**
- Converts numeric amounts into words
- Supports **Dirhams** and **Fils**
- Accepts decimal values up to two decimal places
- Displays results instantly
- Input validation for invalid entries
- Standalone **Windows executable (.exe)** available
- No Python installation required when using the executable

---

## System Requirements

### Source Code
- Python 3.8 or later

### Executable Version
- Microsoft Windows 10 or Windows 11
- No additional software or Python installation required

---

## Project Structure

```
NumberToWordsConverter/
│
├── numtowords.py                 # Main application source code
├── dist/
│   └── numtowrods.exe   # Compiled executable
├── numtowords.spec
├── build/
├── README.md
```

---

## Running the Application

### Option 1: Using the Executable

1. Open the **dist** folder.
2. Double-click **NumberToWords.exe**.
3. Enter the desired amount.
4. Click the **Convert** button.
5. The converted amount will be displayed in words.

No Python installation is required.

---

### Option 2: Running the Source Code

1. Install Python 3.8 or newer.
2. Open a terminal or command prompt.
3. Navigate to the project folder.

Run:

```bash
python numtowords.py
```

---

## User Guide

1. Launch the application.
2. Paste one or more numeric amounts into the input field.
   - You can paste values directly from Excel.
   - Each value can be on its own line or separated by commas.

Example:

```
1234.50
67
1000.75
```

3. Click the **Convert to Words** button.

Output:

```
One Thousand Two Hundred Thirty Four Dirhams and Fifty Fils Only
Sixty Seven Dirhams Only
One Thousand Dirhams and Seventy-Five Fils Only
```

4. Copy the output and paste it back into Excel. Each converted value is placed on a separate line.

5. After converting, each valid input amount is appended to a history text file named `converted_numbers_{date}.txt`.
   The file records the original values with timestamps to help you track daily conversions.

Example Filename:
```
converted_numbers_2026-07-15
```


---

## Sample Conversions

| Input | Output |
|--------|--------|
| 0 | Zero Dirhams Only |
| 1 | One Dirham Only |
| 15.50 | Fifteen Dirhams and Fifty Fils Only |
| 100 | One Hundred Dirhams Only |
| 999.99 | Nine Hundred Ninety-Nine Dirhams and Ninety-Nine Fils Only |
| 1250.75 | One Thousand Two Hundred Fifty Dirhams and Seventy-Five Fils Only |
| 1000000 | One Million Dirhams Only |

---

## Input Rules

- Accepts positive numeric values
- Supports up to two decimal places
- Decimal values represent **Fils**
- Supports multiple lines or comma-separated values for batch conversion
- Invalid or empty entries are skipped and shown in a warning message

Examples of valid inputs:

```
10
10.5
10.50
1250.75
999999.99
```

Example Excel-style input:

```
1234.50 
67
1000.75
```

Examples of invalid inputs:

```
abc
12.345
-50
```

---

## Graphical User Interface

The application provides a simple and intuitive interface that includes:

- Multiline input field for batch amounts
- Clear input button
- Uppercase Switch
- Convert button
- Copy to Clipboard
- Output display area
- Error message dialog for invalid inputs
- Excel-friendly output with one converted phrase per line

The GUI was developed using Python's built-in **Tkinter** library to provide a lightweight and responsive desktop application.

---

## Building the Executable

The executable was created using **PyInstaller**.

To generate the executable:

```bash
pyinstaller --onefile --windowed numtowords.py
```

The generated executable can be found inside the **dist** folder.

---

## Application Uses

This application can be used for:

- Cheque preparation
- Invoice generation
- Receipt printing
- Payroll systems
- Financial reporting
- Accounting applications

---

## Limitations

- English language output only
- Supports UAE currency (AED) only
- Designed for Windows operating systems
- Accepts a maximum of two decimal places

---

## Future Enhancements

- Print functionality
- Multiple currency support
- Arabic language output
- Dark mode interface
- Customizable themes

---

**Developed using Python and Tkinter**

This project demonstrates the implementation of a graphical desktop application capable of converting numeric values into readable UAE currency words (Dirhams and Fils). The application is distributed as both Python source code and a standalone Windows executable for ease of use.
