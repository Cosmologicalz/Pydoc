import tkinter as tk
from tkinter import ttk, messagebox
import requests, webbrowser, json, os
from PIL import Image, ImageTk
from typing import Callable, Any, List
from datetime import datetime

def repair(
    file : str, 
    data : List[str] = ""
    ):
    """_summary_
    Used in the event a file is missing and stuff, you get it? but its very basic, just writes a whole new file and you have to put in each line as a matrix. Not super fun, huh.

    Args:
        file (str): _file path and extension._
        data (str, optional): _data to be written (Needs to be in a matrix if multiple lines)._ Defaults to "".
    """
    with open(file, "w") as f:
        f.writelines(data)

errors = [
    ["Exception", "An exception has occured"],
    ["KeyError", "A key is missing or corrupt\n\nClick yes to repair (Possible data loss if it is replacing a user edited key)"],
]

try:
    with open("resources/path.json", "r") as f:
        filePath = json.load(f)
        try:
            filePath = filePath["path"]
        except KeyError:
            result = messagebox.askyesno(errors[1][0], errors[1][1]+"\n\nlocation : resources/path.json", icon="error")
            if result:
                repair("resources/path.json", '{"path" : "file/"}')
                quit()        
except FileNotFoundError:
    result = messagebox.askyesno("FileNotFoundError", "The path.json file has not been found\nThis is a Manditory file and is required to run the program\n\nClick yes to repair (If you had a custom save location, it will be erased)", icon="error")
    if result:
        repair("resources/path.json", '{"path" : "file/"}')
        quit()
except Exception as e:
    messagebox.showerror(errors[0][0], errors[0][1]+f"\n{e}")
    quit()

try:
    with open("resources/types.json", "r") as f:
        typeData = json.load(f)
        try:
            CustomFileTypes = typeData["CustomFileTypes"]
        except KeyError:
            result = messagebox.askyesno(errors[1][0], errors[1][1]+"\n\nlocation : resources/types.json", icon="error")
            if result:
                repair("resources/types.json", '{"CustomFileTypes" : []}')
                quit()
except FileNotFoundError:
    result = messagebox.askyesno("FileNotFoundError", "The auth.json file has not been found\nThis is a Manditory file and is required to run the program\n\nClick yes to repair (Custom file extensions you have made will be lossed)", icon="error")
    if result:
        repair("resources/types.json", '{"CustomFileTypes" : []}')
        quit()
except Exception as e:
    messagebox.showerror(errors[0][0], errors[0][1]+f"\n{e}")
    quit()
    
try:
    with open("resources/saveConf.json", "r") as f:
        saveConfData = json.load(f)
        try:
            confBackup = saveConfData["backup"]
        except KeyError:
            result = messagebox.askyesno(errors[1][0], errors[1][1]+"\n\nlocation : resources/saveConf.json", icon="error")
            if result:
                repair("resources/types.json", '{"CustomFileTypes" : []}')
                quit()
except FileNotFoundError:
    result = messagebox.askyesno("FileNotFoundError", "The saveConf.json file has not been found\nThis is a Manditory file and is required to run the program\n\nClick yes to repair (Custom file extensions you have made will be lossed)", icon="error")
    if result:
        repair("resources/types.json", '{"CustomFileTypes" : []}')
        quit()
except Exception as e:    
    messagebox.showerror(errors[0][0], errors[0][1]+f"\n{e}")
    quit()
        
date  = datetime.now()
sec   = date.second
Min   = date.minute
hour  = date.hour
day   = date.day
month = date.month
year  = date.year
dateMatrix = [[day], [month], [year]]

def saveFile(
    type: str = ".txt",
):
    process.config(text="Starting Save")
    progress.config(value=10)
    backup = confBackup
    file = filePath
    
    def prep():
        global Title, Date, Tags, Author, Proj, Text
        global ID

        process.config(text="Prepping")
        progress.config(value=20)

        process.config(text="Generating ID")
        progress.config(value=30)
        ID = (f"{day}{month}{year}-{version}").replace(" ", "")
        process.config(text="Generating ID (complete)")
        progress.config(value=40)

        process.config(text="Logging Save")
        progress.config(value=50)

        process.config(text="Collecting Metadata")
        progress.config(value=60)
        process.config(text="Collecting Metadata (title)")
        progress.config(value=70)
        Title = title.get()

        process.config(text="Collecting Metadata (date)")
        progress.config(value=80)
        Date =f"{dateD.get()}-{dateM.get()}-{dateY.get()}"
        
        process.config(text="Collecting Metadata (tags)")
        progress.config(value=90)
        Tag = tagsEntry.get()
        Tags = []
        if "," in Tag:
            for item in Tag.split(','):
                Tags.append(item.strip())

        process.config(text="Collecting Metadata (author)")
        progress.config(value=100)
        Author = author.get()

        process.config(text="Collecting Metadata (project)")
        progress.config(value=110)
        if proj:
            Proj = project.get()
            Proj = Proj + "/"
        else:
            Proj = ""

        process.config(text="Collecting Metadata (text)")
        progress.config(value=120)
        Text = textBox.get("1.0", "end-1c").split("\n")
        
        if Title == "":
            result = messagebox.askyesno("No Title", "You have no Title, are you sure you want to save", icon="warning", detail="It will be saved without a title")
            if result is False:
                progress.config(value=0)
                process.config(text="None")
                return ID
        if Tag == "":
            result = messagebox.askyesno("No Tag(s)", "You have no Tag(s), are you sure you want to save", icon="warning", detail="It will be saved without a tag")
            if result is False:
                progress.config(value=0)
                process.config(text="None")
                return ID   
        if Author == "":
            result = messagebox.askyesno("No Author", "You have no Author, are you sure you want to save", icon="warning", detail="This piece will have no evidence of being produced by humans")
            if result is False:
                progress.config(value=0)
                process.config(text="None")
                return ID
        if Text == "":
            result = messagebox.askyesno("No Text", "You have no text, are you sure you want to save", icon="warning", detail="Not gonna lie, I think the whole point of this is to write text")
            if result is False:
                progress.config(value=0)
                process.config(text="None")
                return ID
                
        process.config(text="Collecting Metadata (complete)")
        progress.config(value=130)
        process.config(text="Prepped!")
        progress.config(value=140)
    prep()

    def save(file, type):
        process.config(text="Creating File")
        progress.config(value=150)
        with open(f"file/{proj}{Title}{type}", "w") as f:
            f.write("")
            process.config(text="Creating File (Complete)")
            progress.config(value=160)

        #/////////// Metadata Writing /////////////////
        process.config(text="Writing")
        progress.config(value=170)
        with open(f"file/{Proj}{Title}{type}", "a") as f:
            f.write(f": md~Title:{Title}\n")
            f.write(f": md~Date:{Date}\n")
            for i in Tags:
                f.write(f": md~Tag:{i}\n")
            f.write(f": md~Author:{Author}\n")
            f.write(f": md~Project:{Proj}\n\n")
            for i in Text:
                f.writelines(i)
            process.config(text="Writing (complete)")
            progress.config(value=200)
    save(file, type)

    def bak(backup):
        if backup:
            process.config(text="Creating Bak File")
            progress.config(value=250)
            with open(f"file/bak/{Proj}{Title}.bak", "w") as f:
                f.write("")
                process.config(text="Creating Bak File (Complete)")
                progress.config(value=300)

            #/////////// Metadata Writing /////////////////
            process.config(text="Writing Bak")
            progress.config(value=350)
            with open(f"file/bak/{proj}{Title}{type}.bak", "a") as f:
                f.write(f": md~Title:{Title}\n")
                f.write(f": md~Date:{Date}\n")
                for i in Tags:
                    f.write(f": md~Tag:{i}\n")
                f.write(f": md~Author:{Author}\n")
                f.write(f": md~Project:{Proj}\n\n")
                for i in Text:
                    f.writelines(i)
                process.config(text="Writing Bak (complete)")
                progress.config(value=500)
        else:
            progress.config(value=500)
    bak(backup)
    
    with open("resources/saves.sav", "a") as saveLog:
        saveLog.write(f"{ID}, {Title} : {sec} {Min} {hour} ")  
    progress.config(value=0)
    process.config(text="None")
    return ID

def helpWindow():
    helper = tk.Toplevel()
    helper.title("Help")
    helper.geometry("559x600")
    helper.resizable(False, False)
    helper.rowconfigure(0, weight=1)
    helper.columnconfigure(0, weight=1)
    
    notebook = ttk.Notebook(helper)
    notebook.grid(row=0, column=0, sticky="news")

    texts = ttk.Frame(notebook)
    notebook.add(texts, text="texts")
    
    editing = ttk.Labelframe(texts, text="Markdown")
    editing.grid(row=0, column=0, padx=5, pady=5)
    
    headings = ttk.Labelframe(editing, text="Headings")
    headings.grid(row=0, column=0, sticky="nwes", padx=5, pady=5)
    headingLabel = ttk.Label(headings, text=f"#\t: Heading 1\n##\t: Heading 2\n###\t: Heading 3\n\nThe more #, the smaller the heading.\n\n### Welcome\n## Welcome\n## Welcome\n{("─"*16)}")
    headingLabel.grid(row=0, column=0)
    headingLabel2 = ttk.Label(headings, text="Welcome", font=("Arial", 32))
    headingLabel2.grid(row=1, column=0, sticky="w")
    headingLabel3 = ttk.Label(headings, text="Welcome", font=("Arial", 16))
    headingLabel3.grid(row=2, column=0, sticky="w")
    headingLabel4 = ttk.Label(headings, text="Welcome", font=("Arial", 8))
    headingLabel4.grid(row=3, column=0, sticky="w")
    
    
    textStyles = ttk.Labelframe(editing, text="Text Styles")
    textStyles.grid(row=0, column=1, sticky="nwes", padx=5, pady=5)
    textStylesLabel = ttk.Label(textStyles, text="** **\tBold  |  * *\tItalic  |  ~~ ~~\tstrikethrough\n\nWrapping text with '**' makes the text bold\nWrapping text with '*' make the text Italic\n\tYou can combine the two above '***' to make \n\tthem both italic and bold\nWrapping text with '~~' strikesthough the text*")
    textStylesLabel.grid(row=0, column=0)
    headingLabel2 = ttk.Label(headings, text="Welcome", font=("Arial", 32))
    headingLabel2.grid(row=1, column=0, sticky="w")
    
    lists = ttk.Labelframe(editing, text="Lists")
    lists.grid(row=1, column=0, sticky="nwes", padx=5, pady=5, columnspan=2)
    listsLabel = ttk.Label(lists, text="-\tBullets\t\t - Bullet Item 1\t\t1. Ordered Item 1\n#. \tOrdered\t\t - Bullet Item 2\t\t2. Ordered Item 2\n\t\t\t - Bullet Item 3\t\t3. Ordered Item 3")
    listsLabel.grid(row=0, column=0)

class settingsSave:
    def Author(auth : ttk.Entry):
        defaultAuth = auth.get()

        try:
            with open("resources/auth.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            result = messagebox.askyesno("FileNotFoundError", "The auth.json file has not been found\nThis is a Situational file and in this situation it is needed\n\nClick yes to repair (The default author will be lossed)", icon="error")
            if result:
                repair("resources/auth.json", '{"author" : ""}')
            
            root.destroy()

        data["author"] = defaultAuth

        with open("resources/auth.json", "w") as f:
            json.dump(data, f, indent=4)
            
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

def isProject():
    if enableProjectVar.get() == 1:
        proj = True
        project.state(["!disabled"])
    else:
        proj = False
        project.state(["disabled"])

def sett():
    setting = tk.Toplevel()
    setting.title("Settings")
    #setting.geometry("500x500")
    setting.columnconfigure(0, weight=1)
    setting.rowconfigure(0, weight=1)
    
    theMainFrame = ttk.Frame(setting)
    theMainFrame.grid(row=0, column=0, sticky="news")
    
    metadataSection = ttk.Labelframe(theMainFrame, text="Metadata Section Settings")
    metadataSection.grid(row=0, column=0, sticky="news", padx=5, pady=5)
    
    defaultAuthorLabel = ttk.Label(metadataSection, text="Default Author : ")
    defaultAuthorLabel.grid(row=0, column=0, sticky="news", padx=5, pady=5)
    
    defaultAuthor = ttk.Entry(metadataSection, width=30)
    defaultAuthor.grid(row=0, column=1, padx=5, pady=5)
    
    saveAuth = ttk.Button(metadataSection, text="Apply", padding=0, takefocus=0, command= lambda : settingsSave.Author(defaultAuthor))
    saveAuth.grid(row=0, column=2, padx=5, pady=5)

def saveMenuDef(event=None):
    saveMenu.tk_popup(save.winfo_rootx(), save.winfo_rooty() + save.winfo_height())

def gitHubWikiMenuDef(event=None):
    gitHubWikiMenu.tk_popup(gitHubTreeButton.winfo_rootx(), gitHubTreeButton.winfo_rooty() + gitHubTreeButton.winfo_height())

def tagPrev():
    tags = tagsEntry.get()
    if tags:
        if "," in tags:
            matrix = [[item.strip()] for item in tags.split(",")]
            
            tagPrev = tk.Toplevel(root)
            tagPrev.title("Tag Preview")
            tagPrev.resizable(False, False)
            
            box = ttk.Treeview(tagPrev, columns=("Tag",), show="headings")
            box.heading("Tag", text="Tag")
            box.column("Tag", width=300)
            box.grid(row=0, column=0, sticky="nsew")
            
            for i in box.get_children():
                box.delete(i)
            for row in matrix:
                box.insert("", "end", values=row)
            
        else:
            messagebox.showinfo("Tag Preview", tags)
    else:
        messagebox.showinfo("Tag Preview", "No Tags Written")

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
        
proj = False
version = "0.3"
build   = "2.1.2026"

# ├
# │
# ─
# └
wikis = [
    ["└ Test Page", "https://github.com/Cosmologicalz/Pydoc/wiki/Test-Page"]
]

try:
    root = tk.Tk()
    root.title("Pydoc")
    root.geometry("1000x700")
    root.minsize(width=1000, height=150)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Small.TNotebook.Tab", font=("TkDefaultFont", 8), padding=[2, 2])
    root.columnconfigure(0, weight=1)
    #root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)
    
    #\\\\\\\\\\\ Header \\\\\\\\\\\
    header = ttk.Frame(root)
    header.grid(row=0, column=0, sticky="ew")
    header.columnconfigure(4, weight=1)
    header.columnconfigure(5, weight=0)
    
    helpButton = ttk.Button(header, text="Help", padding=-1, command=helpWindow)
    helpButton.grid(row=0, column=0, padx=1)
    
    if True:
        img = Image.open("assets/github.png")
        img = img.resize((12, 13), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
    gitHub = ttk.Button(header, image=img, takefocus=0, padding=0, command= lambda : webbrowser.open("https://github.com/Cosmologicalz/Pydoc"))
    gitHub.image = img
    gitHub.grid(row=0, column=1, padx=1, pady=1)
    
    if True:
        img = Image.open("assets/wiki.png")
        img = img.resize((12, 13), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
    gitHubWiki = ttk.Button(header, image=img, takefocus=0, padding=0, command= lambda : webbrowser.open("https://github.com/Cosmologicalz/Pydoc/wiki"))
    gitHubWiki.image = img
    gitHubWiki.grid(row=0, column=2, padx=[1, 0], pady=1)
    
    gitHubWikiMenu = tk.Menu(root, tearoff=0)
    gitHubWikiMenu.add_command(label="Home", command= lambda : webbrowser.open("https://github.com/Cosmologicalz/Pydoc/wiki"))
    gitHubWikiMenu.add_separator()
    for name, link in wikis:
        gitHubWikiMenu.add_command(label=name, command= lambda : webbrowser.open(link))

    gitHubTreeButton = ttk.Button(header, takefocus=0, text="", command=gitHubWikiMenuDef, padding=-1, width=0.5)
    gitHubTreeButton.grid(row=0, column=3, padx=[0, 1], pady=2, sticky="n") 
    
    middleSection = ttk.Frame(header)
    middleSection.grid(row=0, column=4)
    
    settings = ttk.Button(middleSection, text="Settings", padding=0, command=sett, underline=0)
    settings.grid(row=0, column=0, padx=1, pady=1)
    
    versionText = ttk.Button(header, padding=0, text=f"{version} / {build}", takefocus=0, command= lambda : messagebox.showinfo("version, build, and latest release", f"Version : {version}\nBuild     : {build}\nLatest    : {str(latest_tag).replace("v", "")}\t\t\t"))
    versionText.grid(row=0, column=5, sticky="e")
    
    notebook = ttk.Notebook(root, height=70)
    notebook.grid(row=2, column=0, sticky="new")

    textBox = tk.Text(root, font=("arial"))
    textBox.grid(row=3, column=0, sticky="news")

    #\\\\\\\\\\\ Doc Titles and stuff \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    Metadata = ttk.Frame(notebook)
    notebook.add(Metadata, text="Metadata")
    textEditing = ttk.Frame(notebook)
    notebook.add(textEditing, text="Text Editing")
    
    #\\\\\\\\\\\ Text Editing Tab \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    textEditing.columnconfigure(0, weight=1)
    textEditing.rowconfigure(0, weight=1)
    
    textEditingNotebook = ttk.Notebook(textEditing, style="Small.TNotebook")
    textEditingNotebook.grid(row=0, column=0, sticky="news")
    
    Text = ttk.Frame(textEditingNotebook)
    textEditingNotebook.add(Text, text="Text", padding=0)
    Markdown = ttk.Frame(textEditingNotebook)
    textEditingNotebook.add(Markdown, text="Markdown", padding=0)
    
    saveMenu = tk.Menu(root, tearoff=0)
    saveMenu.add_command(label="text", command=lambda : saveFile())
    saveMenu.add_command(label="html", command=lambda : saveFile(".html"))
    saveMenu.add_command(label="markdown", command=lambda : saveFile(".md"))
    saveMenu.add_separator()
    for ext in CustomFileTypes:
        saveMenu.add_command(label=ext)

    save = ttk.Button(textEditing, text="Save", command=saveMenuDef)
    save.grid(row=0, column=1, sticky="news", padx=3, pady=[3,0])
    
    progress = ttk.Progressbar(textEditing, length=500, maximum=500)
    progress.place(x=105, y=2)
    
    process = ttk.Label(textEditing, text="None", background="#bab5ab", font=("Arial", 7))
    process.place(x=110, y=3)
    
    txt = ttk.Button(textEditing, text=".txt", padding=-2, command=lambda : saveFile())
    txt.place(x=610, y=3)
    
    html = ttk.Button(textEditing, text=".html", padding=-2, command=lambda : saveFile(".txt"))
    html.place(x=680, y=3)    
    
    md = ttk.Button(textEditing, text=".md", padding=-2, command=lambda : saveFile(".md"))
    md.place(x=750, y=3)
        
    #\\\\\\\\\\\ Text Tab \\\\\\\\\\\
        
    textHelp = ttk.Label(Text, text="Regular Text\nJust Write")
    textHelp.grid(row=0, column=0)
    
    #\\\\\\\\\\\ Markdown Tab \\\\\\\\\\\
        
    headings = ttk.Labelframe(Markdown, text="Headings")
    headings.grid(row=0, column=0)
    
    text = ttk.Label(headings, text="# / ## / ###\tMore # = Smaller Text")
    text.grid(row=0, column=0)
    
    if True:
        img = Image.open("assets/info.png")
        img = img.resize((16, 16), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
    headingsInfo = ttk.Button(headings, image=img, takefocus=0, padding=-2, command= lambda : messagebox.showinfo("Headings help and info", f"# / ## / ###  |  More # = Smaller Text\n\n\t#\tis Large Text\n\t##\tis Medium Text\n\t###\tis small text"))
    headingsInfo.image = img
    headingsInfo.grid(row=0, column=1, padx=1, pady=1)
    
    textStyles = ttk.Labelframe(Markdown, text="Text Styles")
    textStyles.grid(row=0, column=1, padx=3)
    
    text = ttk.Label(textStyles, text="** **\tBold  |  * *\tItalic  |  ~~ ~~\tstrikethrough")
    text.grid(row=0, column=0)
    
    if True:
        img = Image.open("assets/info.png")
        img = img.resize((16, 16), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
    textStylesInfo = ttk.Button(textStyles, image=img, takefocus=0, padding=-2, command= lambda : messagebox.showinfo("Text Styles help and info", f"** **\tBold  |  * *\tItalic  |  ~~ ~~\tstrikethrough\n\nWrapping text with '**' makes the text bold\nWrapping text with '*' make the text Italic\n\tYou can combine the two above '***' to make \n\tthem both italic and bold\nWrapping text with '~~' strikesthough the text"))
    textStylesInfo.image = img
    textStylesInfo.grid(row=0, column=1, padx=1, pady=1)
    
    lists = ttk.Labelframe(Markdown, text="lists")
    lists.grid(row=0, column=3)
    
    text = ttk.Label(lists, text="-\tBullets  |  number. \tOrdered")
    text.grid(row=0, column=0)    
    
    helpPage = ttk.Button(Markdown, text="Help", padding=0, command=helpWindow)
    helpPage.grid(row=0, column=4, padx=3, pady=1, sticky="s")
    
    #\\\\\\\\\\\ Metadata Tab \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    upperRow = ttk.Frame(Metadata)    
    upperRow.grid(row=0, column=0, sticky="ew")
    lowerRow = ttk.Frame(Metadata)    
    lowerRow.grid(row=1, column=0, sticky="ew")
    
    #\\\\\\\\\\\ upper \\\\\\\\\\\
    
    titleLabel = ttk.Label(upperRow, text="Title :")
    titleLabel.grid(row=0, column=0, padx=2, pady=5)
    
    title = ttk.Entry(upperRow, width=40)
    title.grid(row=0, column=1, padx=2, pady=2)
    title.insert(0, "New Document")
    
    Date = ttk.Label(upperRow, text="Date (D/M/Y) :")
    Date.grid(row=0, column=2, padx=[15, 2], pady=5)
    
    dateD = ttk.Entry(upperRow, width=5)
    dateD.grid(row=0, column=3, padx=2, pady=5)
    dateD.insert(0, dateMatrix[0])
    
    textSeparator(upperRow, 0, 4)
    
    dateM = ttk.Entry(upperRow, width=5)
    dateM.grid(row=0, column=5, padx=2, pady=5)
    dateM.insert(0, dateMatrix[1])
    
    textSeparator(upperRow, 0, 6)
    
    dateY = ttk.Entry(upperRow, width=10)
    dateY.grid(row=0, column=7, padx=2, pady=5)
    dateY.insert(0, dateMatrix[2])
    
    tagsLabel = ttk.Label(upperRow, text="Tags :")
    tagsLabel.grid(row=0, column=8, padx=[15, 2], pady=5)
    tagsEntry = ttk.Entry(upperRow, width=49)
    tagsEntry.grid(row=0, column=9, padx=2, pady=5, sticky="ew")
    tagsEntry.insert(0, "general")
    
    if True:
        img = Image.open("assets/info.png")
        img = img.resize((16, 16), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
    tagInfo = ttk.Button(upperRow, image=img, takefocus=0, padding=-2, command= lambda : messagebox.showinfo("Tags help and info", f"To write a tag, just simply put in a string\n\nFor multiple, enter in a comma (',') between each tag"))
    tagInfo.image = img
    tagInfo.grid(row=0, column=11, padx=1, pady=1)
    
    tagPrevButton = ttk.Button(upperRow, text="Preview", padding=-2, command=tagPrev)
    tagPrevButton.grid(row=0, column=10)    
    
    #\\\\\\\\\\\ lower \\\\\\\\\\\
        
    authorLabel = ttk.Label(lowerRow, text="Author :")
    authorLabel.grid(row=0, column=0, padx=2, pady=5)
    
    author = ttk.Entry(lowerRow, width=30)
    author.grid(row=0, column=1, padx=2, pady=2)
        
    enableProjectVar = tk.IntVar()
    enableProject = ttk.Checkbutton(lowerRow, text="isProject", takefocus=0, command=isProject, variable=enableProjectVar,)
    enableProject.grid(row=0, column=2, padx=[15, 2], pady=5)
    textSeparator(lowerRow, 0, 3, "|")
    projectLabel = ttk.Label(lowerRow, text="Project :")
    projectLabel.grid(row=0, column=4, padx=2, pady=5)
    
    project = ttk.Combobox(lowerRow, width=50)
    project.grid(row=0, column=5, padx=2, pady=5, sticky="ew")
    project.state(["disabled"])
    
    if True:
        img = Image.open("assets/info.png")
        img = img.resize((16, 16), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
    projectInfo = ttk.Button(lowerRow, image=img, takefocus=0, padding=-2, command= lambda : messagebox.showinfo("Project help and info", f"This simply is creates a folder within the 'file' folder, so you can write '/' to make sub projects if needed\n\nDont use '\\' ever or place a '/' at the beginning or end of the project name or else it wont work"))
    projectInfo.image = img
    projectInfo.grid(row=0, column=6, padx=1, pady=1)    
    
    with open("resources/auth.json", "r") as f:
        defaultAuthor = json.load(f)
        defaultAuthor = defaultAuthor["author"]
        
    if defaultAuthor:
        author.insert(0, defaultAuthor)
    
    root.mainloop()
except Exception as e:
    messagebox.showerror(errors[0][0], errors[0][1]+f"\n{e}")
