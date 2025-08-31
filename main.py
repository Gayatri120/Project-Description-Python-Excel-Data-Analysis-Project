import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, messagebox

df = None  # global DataFrame

# Load Excel
def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            messagebox.showinfo("Success", "File Loaded Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot read file\n{e}")

# Clean data
def clean_data():
    global df
    if df is None:
        messagebox.showerror("Error", "Load a file first!")
        return
    before = df.shape[0]
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    after = df.shape[0]
    messagebox.showinfo("Cleaning Done", f"Removed {before - after} rows.")

# Analyze data
def analyze_data():
    global df
    if df is None:
        messagebox.showerror("Error", "Load a file first!")
        return
    try:
        total_members = df['Member Name'].nunique()
        total_exercises = df['Exercise Type'].nunique()
        total_calories = df['Calories Burned'].sum()
        avg_calories = df['Calories Burned'].mean()

        result.set(f"Unique Members: {total_members}\n"
                   f"Exercise Types: {total_exercises}\n"
                   f"Total Calories Burned: {total_calories:,.0f}\n"
                   f"Average Calories per Session: {avg_calories:,.1f}")
    except Exception as e:
        messagebox.showerror("Error", f"Analysis failed\n{e}")

# Create charts
def create_charts():
    global df
    if df is None:
        messagebox.showerror("Error", "Load a file first!")
        return
    try:
        # Most common exercise
        df['Exercise Type'].value_counts().plot(kind='bar', title="Exercise Frequency")
        plt.xlabel("Exercise Type")
        plt.ylabel("Count")
        plt.show()

        # Calories by Member
        df.groupby('Member Name')['Calories Burned'].sum().plot(kind='pie', autopct='%1.1f%%')
        plt.title("Calories Burned by Member")
        plt.ylabel("")
        plt.show()

        # Weight Used 
        df['Weight Used (kg)'].dropna().plot(kind='hist', bins=10, title="Weight Used Distribution")
        plt.xlabel("Weight (kg)")
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Charts failed\n{e}")

# ---------------- GUI ----------------
root = Tk()
root.title("🏋️ Gym Progress Tracker Analytics")
root.geometry("450x350")

Button(root, text=" Load File", command=load_file, width=25).pack(pady=5)
Button(root, text=" Clean Data", command=clean_data, width=25).pack(pady=5)
Button(root, text=" Analyze Data", command=analyze_data, width=25).pack(pady=5)
Button(root, text=" Create Charts", command=create_charts, width=25).pack(pady=5)

result = StringVar()
Label(root, textvariable=result, bg="white", width=55, height=6, anchor="w", justify=LEFT).pack(pady=10)

root.mainloop()
