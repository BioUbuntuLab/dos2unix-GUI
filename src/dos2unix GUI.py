import os
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def run_pipeline(input_file, pattern, mac2unix, progress_bar):

    # Start the progress bar
    progress_bar.start()

    if pattern=="":
        # Select input file
        infile = str(os.path.basename(input_file)).replace(" ","\ ")
    
    # Choose between dos and mac
    os_opt = "dos" if not mac2unix else "mac"

    # Change to the input file's directory
    os.chdir(os.path.dirname(input_file)) if pattern=="" else os.chdir(input_file)

    if pattern=="":
        command = f"{os_opt}2unix -e {infile}"
    else:
        command = f"{os_opt}2unix -e {pattern}"
    
    try:
        subprocess.run(["bash", "-c", command], check=True)
        progress_bar.stop()
        messagebox.showinfo("Success", f"{input_file} converted to unix format") if pattern=="" else messagebox.showinfo("Success", f"Files at {input_file} converted to unix format")

    except subprocess.CalledProcessError as e:
        progress_bar.stop()
        messagebox.showerror("Error",str(e))
        
def start_thread():
    input_file = input_file_var.get()
    pattern = pattern_var.get()
    mac2unix = mac2unix_var.get()

    if not input_file:
        if pattern == "":
            messagebox.showwarning("Input Error", "Please select an input file.")
            return
        else:
            messagebox.showwarning("Input Error", "Please select an input folder.")
            return
    
    # Start command in a new thread
    thread = threading.Thread(target=run_pipeline, args=(input_file, pattern, mac2unix, progress_bar))
    thread.start()

def select_operation():
    pattern = pattern_var.get()
    file_path = filedialog.askopenfilename() if pattern == "" else filedialog.askdirectory()
    input_file_var.set(file_path)

# Set up tkinter app
app = tk.Tk()
app.title("dos2unix GUI")

# Pattern
tk.Label(app, text="Pattern of files to convert:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
pattern_var = tk.StringVar(value="")
tk.Entry(app, textvariable=pattern_var, width=40).grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Input file selection
input_file_var = tk.StringVar()
tk.Label(app, text="Input File or Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
tk.Entry(app, textvariable=input_file_var, width=40).grid(row=1, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_operation).grid(row=1, column=2, padx=10, pady=10)

# Checkbox for additional option
mac2unix_var = tk.BooleanVar(value=False)
tk.Checkbutton(app, text="mac2unix conversion", variable=mac2unix_var).grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Progress Bar (indeterminate)
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=200)
progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=20)

# Start button
tk.Button(app, text="Run program", command=start_thread).grid(row=4, column=1, padx=10, pady=20)

app.mainloop()
