# Group 11: Project 3
# Jihaad Fadika, Ameer Faique, Christina Consentino, Angelina Tyre
import tkinter as tk
from tkinter import filedialog
import datetime
import json

class MainWindow(tk.Tk):
    # Main application window for managing notes and code snippets.
    def __init__(self):
        super().__init__()
        self.geometry("800x600")  # Set the window size
        self.title('Notebook and Snippet Manager')  # Set the window title

        self.notebook = []  # List to store all notes
        self.snippets = []  # List to store all code snippets

        # Main frame that holds all other widgets
        self.frame_main = tk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=True)
        self.frame_main.config(bg='light gray')

        # Frame to display notes in the window
        self.frame_notes = tk.Frame(self.frame_main, bg='gray')
        self.frame_notes.grid(row=1, column=2, rowspan=6, sticky='w')

        # Buttons for various functionalities
        self.btn_new_note = tk.Button(self.frame_main, text='Create New Note', command=self.new_note)
        self.btn_new_note.grid(padx=10, pady=10, row=1, column=1)

        self.btn_open_notebook = tk.Button(self.frame_main, text='Open Notebook', command=self.open_notebook)
        self.btn_open_notebook.grid(padx=10, pady=10, row=2, column=1)

        self.btn_save_notebook = tk.Button(self.frame_main, text='Save Notebook', command=self.save_notebook)
        self.btn_save_notebook.grid(padx=10, pady=10, row=3, column=1)

        self.btn_create_snippet = tk.Button(self.frame_main, text='Create Snippet', command=self.create_snippet)
        self.btn_create_snippet.grid(padx=10, pady=10, row=4, column=1)

        self.btn_quit = tk.Button(self.frame_main, text='Quit', command=self.destroy)
        self.btn_quit.grid(padx=10, pady=10, row=5, column=1)

    def new_note(self):
        # Opens a form to create a new note.
        NoteForm(self, self.notebook)
        
    def create_snippet(self):
        # Opens a form to create a new code snippet.
        SnippetForm(self, self.snippets)

    def clear_frame(self, target_frame):
        # Clears all widgets from the specified frame.
        for widgets in target_frame.winfo_children():
            widgets.destroy()

    def show_notes(self):
        # Displays all notes in the notes frame.
        self.clear_frame(self.frame_notes)
        for note in self.notebook:
            new_note = MakeNote(master=self.frame_notes, note_dict=note)
            new_note.pack(padx=10, pady=10, fill=tk.X)

    def open_notebook(self):
        # Opens a JSON file and loads notes from it.
        filepath = filedialog.askopenfilename(initialdir="./", filetypes=[("json files", "*.json")])
        if filepath:
            with open(filepath, "r") as file:
                self.notebook = json.load(file)
            self.show_notes()

    def save_notebook(self):
        # Saves all notes into a JSON file.
        file = filedialog.asksaveasfile(initialdir="./", defaultextension=".json", filetypes=[("json file", ".json")])
        if file:
            json_out = json.dumps(self.notebook, indent=2)
            file.write(json_out)
            file.close()
            self.show_notes()

class NoteForm(tk.Toplevel):
    # Form for creating or editing notes.
    def __init__(self, master, notebook, note_dict=None):
        super().__init__(master)
        self.geometry("600x400")
        self.title('Edit Note' if note_dict else 'New Note')
        self.notebook = notebook
        self.note_dict = note_dict

        self.frame_main = tk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=True)
        self.frame_main.config(bg='light gray')

        # Widgets for note data entry
        tk.Label(self.frame_main, text='Note Title:').grid(row=1, column=0)
        self.note_title = tk.Entry(self.frame_main)
        self.note_title.grid(row=1, column=1)
        self.note_title.insert(0, note_dict['title'] if note_dict else '')

        tk.Label(self.frame_main, text='Note Text:').grid(row=2, column=0)
        self.note_text = tk.Text(self.frame_main, height=10)
        self.note_text.grid(row=2, column=1)
        if note_dict:
            self.note_text.insert('1.0', note_dict['text'])

        tk.Label(self.frame_main, text='Note Link:').grid(row=3, column=0)
        self.note_link = tk.Entry(self.frame_main)
        self.note_link.grid(row=3, column=1)
        self.note_link.insert(0, note_dict['link'] if note_dict else '')

        tk.Label(self.frame_main, text='Note Tags:').grid(row=4, column=0)
        self.note_tags = tk.Entry(self.frame_main)
        self.note_tags.grid(row=4, column=1)
        self.note_tags.insert(0, note_dict['tags'] if note_dict else '')

        submit_btn = tk.Button(self.frame_main, text='Submit', command=self.submit)
        submit_btn.grid(row=5, column=1)

    def submit(self):
        # Collects data from form, updates or adds to notebook.
        note_dict = {
            'title': self.note_title.get(),
            'text': self.note_text.get('1.0', tk.END).strip(),
            'link': self.note_link.get(),
            'tags': self.note_tags.get(),
            'meta': f'Last modified: {datetime.datetime.now().isoformat()}'
        }
        if self.note_dict:
            # Update existing note
            self.notebook[self.notebook.index(self.note_dict)] = note_dict
        else:
            # Add new note
            self.notebook.append(note_dict)
        self.master.show_notes()
        self.destroy()

class MakeNote(tk.Button):
    # Widget representing a single note in the notebook. (Jihaad and Ameer)
    def __init__(self, master=None, note_dict=None):
        super().__init__(master)
        self.note_dict = note_dict
        self.config(text=f"{note_dict['title']}\n{note_dict['meta']}")
        self.bind("<Button-1>", self.note_open)

    def note_open(self, event):
        # Opens the note for editing.
        NoteForm(self.master.master, self.master.master.notebook, note_dict=self.note_dict)

class SnippetForm(tk.Toplevel):
    # Form for creating new code snippets.(Christina and Angelina)
    def __init__(self, master, snippets):
        super().__init__(master)
        self.geometry("400x300")
        self.title('New Snippet')
        self.snippets = snippets

        self.snippet_text = tk.Text(self)
        self.snippet_text.pack()

        submit_btn = tk.Button(self, text='Submit Snippet', command=self.submit_snippet)
        submit_btn.pack()

    def submit_snippet(self):
        # Collects snippet content and adds to the list of snippets.
        snippet_content = self.snippet_text.get('1.0', 'end').strip()
        self.snippets.append({'content': snippet_content, 'created': datetime.datetime.now().isoformat()})
        self.destroy()

if __name__ == '__main__':
    main_window = MainWindow()
    main_window.mainloop()
