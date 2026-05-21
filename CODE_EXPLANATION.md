# 🔍 Code Explanation — CSV & Excel Smart Cleaner

A beginner-friendly breakdown of every function, method, and library used in `cleaner.py`.

---

## 📦 Imports — What Each Library Does

```python
import pandas as pd
```
> **Pandas** — The main data processing library. Think of it like Excel but in Python. It reads your CSV/Excel file into a "DataFrame" (like a table) and lets you clean, filter, and save it.

```python
import matplotlib.pyplot as plt
```
> **Matplotlib** — A chart/graph drawing library. We use it to create the bar chart (missing values) and pie chart (rows kept vs removed) and save them as a PNG image.

```python
import os
```
> **os** — Built-in Python library for interacting with your computer's file system. We use it to create folders, build file paths, and check directories.

```python
from datetime import datetime
```
> **datetime** — Built-in Python library for working with dates and times. We use it to add a timestamp to output filenames so they never overwrite each other.

```python
import tkinter as tk
from tkinter import filedialog, messagebox
```
> **Tkinter** — Python's built-in GUI (Graphical User Interface) library. We use it to show:
> - A **file picker popup** (so users browse for their file instead of typing a path)
> - A **messagebox popup** (to show the summary when cleaning is done)
> - An **error popup** (if wrong file type is selected)

---

## 🔧 Function 1 — `select_file()`

```python
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select your CSV or Excel file",
        filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
    )
    return file_path
```

### What it does:
Opens a standard Windows file picker dialog so the user can browse and select their file.

### Line by line:
| Line | Explanation |
|---|---|
| `root = tk.Tk()` | Creates a hidden Tkinter window (required to show any popup) |
| `root.withdraw()` | Immediately hides that window — we don't want a blank window, just the popup |
| `filedialog.askopenfilename(...)` | Opens the file picker dialog |
| `title=...` | The text shown at the top of the file picker window |
| `filetypes=[...]` | Filters what files the user can see — CSV, Excel, or all files |
| `return file_path` | Returns the full path of the selected file (e.g. `D:\data\sales.csv`) |

---

## 🔧 Function 2 — `clean_and_report(input_file)`

This is the **main function** — it does all the cleaning and reporting. Takes the file path as input.

---

### 📂 Step 1 — Load the File

```python
if input_file.endswith('.csv'):
    df = pd.read_csv(input_file, encoding='utf-8-sig')
elif input_file.endswith(('.xlsx', '.xls')):
    df = pd.read_excel(input_file)
else:
    messagebox.showerror("Error", "Only CSV or Excel files supported!")
    return
```

| Line | Explanation |
|---|---|
| `input_file.endswith('.csv')` | Checks if the file is a CSV by looking at its extension |
| `pd.read_csv(...)` | Reads the CSV file into a DataFrame (like loading it into a table) |
| `encoding='utf-8-sig'` | Handles special characters and files saved by older Excel versions — prevents crash on non-English data |
| `pd.read_excel(...)` | Reads Excel files (.xlsx or .xls) into a DataFrame |
| `messagebox.showerror(...)` | Shows an error popup if the file type is not supported |
| `return` | Stops the function early if wrong file type |

---

### 📊 Step 2 — Track Original State

```python
original_rows = len(df)
original_dupes = df.duplicated().sum()
```

| Line | Explanation |
|---|---|
| `len(df)` | Counts total number of rows in the original file |
| `df.duplicated()` | Returns True/False for each row — True if it's a duplicate |
| `.sum()` | Counts how many rows are True (i.e. how many duplicates exist) |

> We save these BEFORE cleaning so we can show the user what was removed.

---

### 🧹 Step 3 — Clean the Data

```python
df.drop_duplicates(inplace=True)
```
> Removes all duplicate rows. `inplace=True` means it modifies the existing DataFrame directly instead of creating a new one.

```python
df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)
```
> Finds cells that contain only whitespace (spaces, tabs) and converts them to proper `NaN` (Not a Number — Python's way of saying "empty"). 
> - `r'^\s*$'` is a **regex pattern** meaning: start of cell (`^`), zero or more spaces (`\s*`), end of cell (`$`)

```python
df.dropna(how='all', inplace=True)
```
> Removes rows where **every single column** is empty/NaN. `how='all'` means ALL columns must be empty — it won't remove a row just because one value is missing.

```python
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
```
> Cleans up column names in 3 steps chained together:
> - `.str.strip()` — removes spaces from start/end of column names
> - `.str.lower()` — converts to lowercase (`Name` → `name`)
> - `.str.replace(' ', '_')` — replaces spaces with underscores (`First Name` → `first_name`)

```python
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
```
> Goes through every single cell and removes extra spaces — but only if it's text (string). Numbers and dates are left alone.
> - `lambda x:` — a small one-line function
> - `isinstance(x, str)` — checks if the cell value is a string/text
> - `x.strip()` — removes leading/trailing spaces

```python
for col in df.columns:
    if 'date' in col:
        df[col] = pd.to_datetime(df[col], errors='coerce')
```
> Loops through all column names. If any column has "date" in its name, it tries to convert that column to a proper datetime format.
> - `errors='coerce'` — if a value can't be converted to a date, it becomes NaN instead of crashing

---

### 💾 Step 4 — Save the Cleaned File

```python
original_dir = os.path.dirname(input_file)
output_dir = os.path.join(original_dir, "cleaned_output")
os.makedirs(output_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
clean_file = os.path.join(output_dir, f"cleaned_{timestamp}.csv")
df.to_csv(clean_file, index=False)
```

| Line | Explanation |
|---|---|
| `os.path.dirname(input_file)` | Gets the folder where the original file lives |
| `os.path.join(...)` | Builds a proper file path that works on any OS |
| `os.makedirs(..., exist_ok=True)` | Creates the `cleaned_output` folder — `exist_ok=True` means no error if it already exists |
| `datetime.now().strftime(...)` | Gets current date+time as a string like `20260518_175915` |
| `df.to_csv(..., index=False)` | Saves the cleaned DataFrame as a CSV — `index=False` prevents adding an unwanted row number column |

---

### 📈 Step 5 — Generate Charts

```python
missing = df.isnull().sum()
missing = missing[missing > 0]
```
> - `df.isnull()` — True/False table: True wherever a value is missing
> - `.sum()` — counts missing values per column
> - `missing[missing > 0]` — keeps only columns that actually have missing values (ignores columns with 0 missing)

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
```
> Creates a figure with **2 side-by-side charts** (1 row, 2 columns). Size is 12 inches wide, 5 inches tall.

**Chart 1 — Bar chart (missing values):**
```python
axes[0].bar(missing.index, missing.values, color='tomato')
```
> Draws a red bar chart. X-axis = column names, Y-axis = count of missing values.

**Chart 2 — Pie chart (rows kept vs removed):**
```python
axes[1].pie([kept, removed],
            labels=[f'Kept ({kept})', f'Removed ({removed})'],
            colors=['#4CAF50', '#f44336'],
            autopct='%1.1f%%', startangle=90)
```
> Draws a green/red pie chart showing what percentage of rows were kept vs removed.
> - `autopct='%1.1f%%'` — shows percentage on each slice (e.g. 75.0%)
> - `startangle=90` — starts the first slice from the top

```python
plt.tight_layout()
plt.savefig(chart_file, dpi=150)
plt.close()
```
> - `tight_layout()` — auto-adjusts spacing so nothing overlaps
> - `savefig(..., dpi=150)` — saves the chart as PNG at 150 DPI (good quality)
> - `plt.close()` — frees up memory after saving

---

### 💬 Step 6 — Show Summary Popup

```python
summary = f"""✅ Cleaning Complete!
Original rows: {original_rows}
Duplicates removed: {original_dupes}
...
"""
messagebox.showinfo("Done!", summary)
```
> - `f"""..."""` — an f-string with triple quotes for multi-line text. Variables inside `{}` are automatically filled in.
> - `messagebox.showinfo(...)` — shows a popup dialog with the summary text

---

## 🚀 Main Entry Point

```python
if __name__ == "__main__":
    file = select_file()
    if file:
        clean_and_report(file)
    else:
        print("No file selected.")
```

| Line | Explanation |
|---|---|
| `if __name__ == "__main__":` | Standard Python — this code only runs when you directly run this file, not when it's imported by another script |
| `select_file()` | Opens the file picker popup |
| `if file:` | Checks if the user actually selected a file (not cancelled) |
| `clean_and_report(file)` | Runs the main cleaning function with the selected file |

---

## 🧠 Key Concepts Summary

| Concept | Used For |
|---|---|
| **DataFrame** | Pandas table structure — holds all your CSV/Excel data in memory |
| **inplace=True** | Modifies the DataFrame directly instead of creating a copy |
| **NaN / pd.NA** | Python's way of representing missing/empty values |
| **regex** | Pattern matching — used to find whitespace-only cells |
| **lambda** | A small anonymous one-line function |
| **f-string** | String formatting — insert variable values directly into text using `{}` |
| **os.path** | Cross-platform file path building |
| **DPI** | Dots Per Inch — controls image quality when saving charts |

---

*Generated for portfolio documentation purposes — csv-cleaner-tool by Anuj*
