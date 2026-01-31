import tkinter as tk
from tkinter import ttk, messagebox


errors = [
    ["Exception", "An exception has occured"]
]
version = "0.1"
build   = "1.31.2026"

try:
    root = tk.Tk()
    root.title("Pydoc")
    root.geometry("1000x700")
    style = ttk.Style()
    style.theme_use("clam")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    
    #\\\\\\\\\\\ Header \\\\\\\\\\\
    header = ttk.Frame(root)
    header.grid(row=0, column=0, sticky="ew")
    header.columnconfigure(0, weight=1)
    
    versionText = ttk.Button(header, text=f"{version} / {build}", takefocus=0, command= lambda : messagebox.showinfo("version and build", f"Version : {version}\nBuild     : {build}"))
    versionText.grid(row=0, column=0, sticky="e")
    
    notebook = ttk.Notebook(root)
    notebook.grid(row=1, column=0, sticky="nnew")

    #\\\\\\\\\\\ Doc Titles and stuff \\\\\\\\\\\
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Metadata")
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Text Editing")

    
    root.mainloop()
except Exception as e:
    messagebox.showerror(errors[0][0], errors[0][1])