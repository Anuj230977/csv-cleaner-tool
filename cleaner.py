import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select your CSV or Excel file",
        filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
    )
    return file_path

def clean_and_report(input_file):
    print(f"\n📂 Loading file: {input_file}")

    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    elif input_file.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(input_file)
    else:
        messagebox.showerror("Error", "Only CSV or Excel files supported!")
        return

    print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")

    original_rows = len(df)
    original_dupes = df.duplicated().sum()

    # Clean
    df.drop_duplicates(inplace=True)
    df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)
    df.dropna(how='all', inplace=True)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    for col in df.columns:
        if 'date' in col:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    cleaned_rows = len(df)

    # Save next to original file
    original_dir = os.path.dirname(input_file)
    output_dir = os.path.join(original_dir, "cleaned_output")
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    clean_file = os.path.join(output_dir, f"cleaned_{timestamp}.csv")
    df.to_csv(clean_file, index=False)

    # Charts
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('CSV Cleaner - Data Report', fontsize=14, fontweight='bold')

    if not missing.empty:
        axes[0].bar(missing.index, missing.values, color='tomato')
        axes[0].set_title('Missing Values per Column')
        axes[0].set_xlabel('Columns')
        axes[0].set_ylabel('Count')
        axes[0].tick_params(axis='x', rotation=45)
    else:
        axes[0].text(0.5, 0.5, '✅ No Missing Values!',
                     ha='center', va='center', fontsize=12, color='green')
        axes[0].set_title('Missing Values')

    removed = original_rows - cleaned_rows
    kept = cleaned_rows
    axes[1].pie([kept, removed],
                labels=[f'Kept ({kept})', f'Removed ({removed})'],
                colors=['#4CAF50', '#f44336'],
                autopct='%1.1f%%', startangle=90)
    axes[1].set_title('Rows Kept vs Removed')

    chart_file = os.path.join(output_dir, f"report_{timestamp}.png")
    plt.tight_layout()
    plt.savefig(chart_file, dpi=150)
    plt.close()

    # Popup summary
    summary = f"""✅ Cleaning Complete!

Original rows: {original_rows}
Duplicates removed: {original_dupes}
Empty rows removed: {original_rows - int(original_dupes) - cleaned_rows}
Final rows: {cleaned_rows}

Missing values per column:
{df.isnull().sum().to_string()}

Column data types:
{df.dtypes.to_string()}

📁 Output saved in:
{output_dir}"""

    messagebox.showinfo("Done!", summary)
    print(summary)

if __name__ == "__main__":
    print("🧹 CSV Cleaner Tool")
    file = select_file()
    if file:
        clean_and_report(file)
    else:
        print("No file selected.")