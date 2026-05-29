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

def standardize_dates(df):
    """Converts date columns to a consistent DD/MM/YYYY string format, handling mixed formats."""
    for col in df.columns:
        if 'date' in col.lower():
            # 1. Convert to datetime object (handling mixed formats)
            converted_dates = pd.to_datetime(
                df[col], 
                dayfirst=True, 
                format='mixed', 
                errors='coerce'
            )
            # 2. Convert that object into a specific string format: DD/MM/YYYY
            df[col] = converted_dates.dt.strftime('%d/%m/%Y')
    return df

def clean_numeric_columns(df):
    """Removes currency symbols and commas, converting columns to numeric."""
    for col in df.columns:
        if df[col].dtype == 'object':
            # Check if the column contains currency symbols or thousands-separator commas
            if df[col].astype(str).str.contains(r'[$,]', regex=True).any():
                df[col] = df[col].astype(str).str.replace(r'[$,]', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def clean_and_report(input_file):
    try:
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

        # --- CLEANING PHASE ---
        # 1. Remove duplicates
        df.drop_duplicates(inplace=True)
        
        # 2. Handle whitespace-only cells (The AI Studio fix)
        df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)
        
        # 3. Remove completely empty rows
        df.dropna(how='all', inplace=True)
        
        # 4. Normalize Column Names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # 5. Trim whitespace from all string values
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        
        # 6. Standardize Dates (The Claude fix: converted to string for CSV output)
        df = standardize_dates(df)
        
        # 7. Clean Numeric/Currency Columns (The AI Studio addition)
        df = clean_numeric_columns(df)

        cleaned_rows = len(df)

        # --- EXPORT PHASE ---
        original_dir = os.path.dirname(input_file)
        output_dir = os.path.join(original_dir, "cleaned_output")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        clean_file = os.path.join(output_dir, f"cleaned_{timestamp}.csv")
        df.to_csv(clean_file, index=False)

        # --- VISUALIZATION PHASE ---
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

        # --- FINAL SUMMARY POPUP (Back to original detail) ---
        summary = f"""✅ Cleaning Complete!

Original rows: {original_rows}
Duplicates removed: {original_dupes}
Empty rows removed: {max(0, original_rows - int(original_dupes) - cleaned_rows)}
Final rows: {cleaned_rows}

Missing values per column:
{df.isnull().sum().to_string()}

Column data types:
{df.dtypes.to_string()}

📁 Output saved in:
{output_dir}"""

        messagebox.showinfo("Done!", summary)
        print(summary)

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("🧹 CSV Cleaner Tool")
    file = select_file()
    if file:
        clean_and_report(file)
    else:
        print("No file selected.")