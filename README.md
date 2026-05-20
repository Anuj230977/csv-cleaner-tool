# 🧹 CSV & Excel Smart Cleaner

> A powerful yet simple tool that cleans messy CSV/Excel files and generates a beautiful visual report — no coding required for end users.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?style=flat-square&logo=pandas)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=flat-square&logo=windows)

---

## ✨ What It Does

| Feature | Description |
|---|---|
| 🗑️ Remove Duplicates | Automatically detects and removes duplicate rows |
| 🧼 Remove Empty Rows | Cleans out fully blank rows from your data |
| ✂️ Trim Whitespace | Strips extra spaces from all cells |
| 🔤 Standardize Columns | Converts column names to clean lowercase format |
| 📅 Fix Date Columns | Auto-detects and standardizes date formats |
| 📊 Visual Report | Generates a PNG chart showing missing values and rows kept vs removed |
| 💬 Popup Summary | Shows a detailed summary when cleaning is complete |

> ⚠️ **Note:** Missing values (e.g. a blank age field) are **flagged and reported** but NOT auto-filled. This is intentional — the tool never guesses your data.

---

## 🖥️ For End Users — No Coding Needed!

If you have been given the `CSV-Cleaner.exe` file:

1. **Double-click** `CSV-Cleaner.exe`
2. A file picker window will open — **browse and select** your CSV or Excel file
3. Wait a few seconds while the tool cleans your data
4. A **popup summary** will appear showing what was cleaned
5. Find your results in a folder called `cleaned_output` — created automatically **next to your original file**

Inside `cleaned_output` you will find:
- `cleaned_YYYYMMDD_HHMMSS.csv` → your clean data file
- `report_YYYYMMDD_HHMMSS.png` → a visual chart of the cleaning report

**That's it. No installation, no terminal, no Python needed.** ✅

---

## 👨‍💻 For Developers — Running from Source

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Anuj230977/csv-cleaner-tool.git
cd csv-cleaner-tool

# Install dependencies
pip install pandas matplotlib openpyxl
```

### Run the tool

```bash
python cleaner.py
```

A file picker popup will open. Select your CSV or Excel file and let the tool do the rest.

---

## 📦 Building the .exe Yourself (Windows)

Want to create the one-click `.exe` file?

```bash
# Step 1 — Install PyInstaller
pip install pyinstaller

# Step 2 — Build the exe
pyinstaller --onefile --windowed --name "CSV-Cleaner" cleaner.py

# Step 3 — Find your exe
# It will be located at: dist/CSV-Cleaner.exe
```

> The `build/` and `dist/` folders are created automatically. You only need `dist/CSV-Cleaner.exe` to share with clients.

---

## 📁 Project Structure

```
csv-cleaner-tool/
├── cleaner.py          # Main Python script
├── CSV-Cleaner.spec    # PyInstaller build config
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

---

## 🛠️ Built With

- [Python](https://python.org) — Core language
- [Pandas](https://pandas.pydata.org) — Data cleaning engine
- [Matplotlib](https://matplotlib.org) — Chart generation
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — GUI file picker & popups
- [PyInstaller](https://pyinstaller.org) — Convert to .exe

---

## 💼 Use Cases

- 🏪 Small business owners cleaning customer/sales data
- 📊 Data entry teams removing duplicates from exports
- 🎓 Students cleaning datasets for projects
- 📋 Anyone with a messy Excel file they want cleaned fast

---

## 👨‍🎓 About

Built by **Anuj** — TY BBA-CA Student  
Freelance developer specializing in Python automation, data tools, and web development.  
📧 anuj1230567@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/anujjadhav) | [GitHub](https://github.com/Anuj230977)

---

## 📄 License

MIT License — free to use and modify.
