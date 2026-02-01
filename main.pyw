import tkinter as tk
from tkinter import ttk, messagebox
import requests
import typing
from typing import Callable, Any

def textSeparator(
        master : Any, 
        row : int, 
        column : int, 
        char : str="/"
        ):
    """_summary_

    Args:
        master (Any): _The master or parent, like a Frame or a root._
        row (int): _The row it goes on._
        column (int): _The column it goes on._
        char (str, optional): _A ASCII character._ Defaults to `"/"`.

    Returns:
        _type_: _description_
    """
    
    sep = ttk.Label(master, text=char)
    sep.grid(row=row, column=column)
    return sep

r = requests.get("https://api.github.com/repos/Cosmologicalz/Pydoc/releases/latest").json()
latest_tag = r.get("tag_name", None)
if latest_tag is None:
    latestVersion = "No Releases"
else:
    assets = r.get("assets", [])
    if assets:
        latestVersion = assets[0]["browser_download_url"]
    else:
        latestVersion = r.get("zipball_url")
        
errors = [
    ["Exception", "An exception has occured"]
]
version = "0.2.2"
build   = "1.31.2026"

try:
    root = tk.Tk()
    root.title("Pydoc")
    root.geometry("1000x700")
    style = ttk.Style()
    style.theme_use("clam")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)
    
    #\\\\\\\\\\\ Header \\\\\\\\\\\
    header = ttk.Frame(root)
    header.grid(row=0, column=0, sticky="ew")
    header.columnconfigure(0, weight=1)
    
    versionText = ttk.Button(header, padding=0, text=f"{version} / {build}", takefocus=0, command= lambda : messagebox.showinfo("version, build, and latest release", f"Version : {version}\nBuild     : {build}\nLatest    : {str(latest_tag).replace("v", "")}"))
    versionText.grid(row=0, column=0, sticky="e")
    
    notebook = ttk.Notebook(root, height=70)
    notebook.grid(row=2, column=0, sticky="new")

    #\\\\\\\\\\\ Doc Titles and stuff \\\\\\\\\\\
    Metadata = ttk.Frame(notebook)
    notebook.add(Metadata, text="Metadata")
    textEditing = ttk.Frame(notebook)
    notebook.add(textEditing, text="Text Editing")
    
    #\\\\\\\\\\\ Metadata Tab \\\\\\\\\\\
    titleLabel = ttk.Label(Metadata, text="Title :")
    titleLabel.grid(row=0, column=0, padx=2, pady=5)
    
    title = ttk.Entry(Metadata, width=40)
    title.grid(row=0, column=1, padx=2, pady=2)
    
    Date = ttk.Label(Metadata, text="Date (D/M/Y) :")
    Date.grid(row=0, column=2, padx=[15, 2], pady=5)
    
    dateD = ttk.Entry(Metadata, width=5)
    dateD.grid(row=0, column=3, padx=2, pady=5)
    
    textSeparator(Metadata, 0, 4)
    
    dateM = ttk.Entry(Metadata, width=5)
    dateM.grid(row=0, column=5, padx=2, pady=5)
    
    textSeparator(Metadata, 0, 6)
    
    dateY = ttk.Entry(Metadata, width=10)
    dateY.grid(row=0, column=7, padx=2, pady=5)

    
    root.mainloop()
except Exception as e:
    messagebox.showerror(errors[0][0], errors[0][1])
