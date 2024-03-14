import os
from anthropic import Anthropic
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, scrolledtext, ttk
from tkinter import messagebox
from tkinter import scrolledtext

API_URL = "https://api.anthropic.com/v1/messages"

def apply_formatting(text):
    text = text.replace("```", "\n")
    return text

def read_file_content(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def send_request_to_claude(prompt, api_key, max_tokens):
    try:
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="claude-3-haiku-20240307"
        )
        return message.content
    except Exception as e:
        messagebox.showerror("Fehler", str(e))
        return None

def select_project_path():
    project_path = filedialog.askdirectory()
    project_path_var.set(project_path)

def select_files():
    selected_files = filedialog.askopenfilenames()
    for file in selected_files:
        if file not in selected_files_listbox.get(0, tk.END):
            selected_files_listbox.insert(tk.END, file)

def remove_selected_file():
    selected_index = selected_files_listbox.curselection()
    if selected_index:
        selected_files_listbox.delete(selected_index)

def send_request():
    mode = mode_var.get()
    max_tokens = int(max_tokens_var.get())
    api_key = api_key_var.get()
    question = question_text.get("1.0", tk.END).strip()

    if mode == "project":
        project_path = project_path_var.get()
        file_extensions = file_extensions_var.get().split(",")

        project_files = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if any(file.endswith(ext.strip()) for ext in file_extensions):
                    file_path = os.path.join(root, file)
                    project_files.append(file_path)

        project_content = ""
        for file_path in project_files:
            content = read_file_content(file_path)
            project_content += f"Datei: {file_path}\n\n{content}\n\n"

        prompt = f"Projekt:\n\n{project_content}\n\nFrage: {question}\n\nAntwort:"
    else:
        selected_files = selected_files_listbox.get(0, tk.END)

        files_content = ""
        for file_path in selected_files:
            content = read_file_content(file_path)
            files_content += f"Datei: {file_path}\n\n{content}\n\n"

        prompt = f"Dateien:\n\n{files_content}\n\nFrage: {question}\n\nAntwort:"

    response = send_request_to_claude(prompt, api_key, max_tokens)
    print(response)
    if response:
        answer_text.delete("1.0", tk.END)
        if isinstance(response, list) and len(response) > 0:
            answer_content = response[0]
            if isinstance(answer_content, dict) and "text" in answer_content:
                formatted_text = apply_formatting(answer_content["text"])
                answer_text.insert(tk.END, formatted_text)
                answer_text.tag_configure("code", background="#f0f0f0", font=("Courier", 10))
                answer_text.tag_add("code", "1.0", tk.END)
            elif hasattr(answer_content, "text"):
                formatted_text = apply_formatting(answer_content.text)
                answer_text.insert(tk.END, formatted_text)
                answer_text.tag_configure("code", background="#f0f0f0", font=("Courier", 10))
                answer_text.tag_add("code", "1.0", tk.END)
            else:
                answer_text.insert(tk.END, "Ungültiges Antwortformat.")
        else:
            answer_text.insert(tk.END, "Keine Antwort erhalten.")

def toggle_mode():
    mode = mode_var.get()
    if mode == "project":
        project_path_label.config(text="Projekt-Pfad:")
        project_path_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        project_path_button.grid(row=1, column=2, padx=5, pady=5)
        file_extensions_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        file_extensions_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        selected_files_label.grid_remove()
        selected_files_listbox.grid_remove()
        selected_files_button.grid_remove()
        remove_file_button.grid_remove()
    else:
        project_path_label.grid_remove()
        project_path_entry.grid_remove()
        project_path_button.grid_remove()
        file_extensions_label.grid_remove()
        file_extensions_entry.grid_remove()

        selected_files_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.N)
        selected_files_listbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
        selected_files_button.grid(row=1, column=2, padx=5, pady=5)
        remove_file_button.grid(row=2, column=2, padx=5, pady=5)

def copy_answer():
    answer = answer_text.get("1.0", tk.END)
    window.clipboard_clear()
    window.clipboard_append(answer)

def save_settings():
    settings = {
        "mode": mode_var.get(),
        "project_path": project_path_var.get(),
        "file_extensions": file_extensions_var.get(),
        "max_tokens": max_tokens_var.get(),
        "api_key": api_key_var.get()
    }
    with open("settings.txt", "w") as file:
        for key, value in settings.items():
            file.write(f"{key}={value}\n")
    window.destroy()

def load_settings():
    try:
        with open("settings.txt", "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                if key == "mode":
                    mode_var.set(value)
                    toggle_mode()
                elif key == "project_path":
                    project_path_var.set(value)
                elif key == "file_extensions":
                    file_extensions_var.set(value)
                elif key == "max_tokens":
                    max_tokens_var.set(value)
                elif key == "api_key":
                    api_key_var.set(value)
                    api_key_entry.configure(show="*")
    except FileNotFoundError:
        pass

window = tk.Tk()
window.title("Claude API Request")
window.geometry("800x600")

main_frame = ttk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

settings_frame = ttk.LabelFrame(main_frame, text="Einstellungen")
settings_frame.pack(fill=tk.X, padx=5, pady=5)

max_tokens_var = tk.StringVar(value="4096")
max_tokens_label = ttk.Label(settings_frame, text="Maximale Token-Länge:")
max_tokens_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
max_tokens_combobox = ttk.Combobox(settings_frame, textvariable=max_tokens_var, values=["512", "1024", "2048", "4096"], state="readonly", font=("Segoe UI", 10))
max_tokens_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

api_key_var = tk.StringVar()
api_key_label = ttk.Label(settings_frame, text="API-Schlüssel:")
api_key_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
api_key_entry = ttk.Entry(settings_frame, width=50, textvariable=api_key_var, show="*", font=("Segoe UI", 10))
api_key_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W+tk.E)

input_frame = ttk.LabelFrame(main_frame, text="Eingabe")
input_frame.pack(fill=tk.BOTH, expand=True)

output_frame = ttk.LabelFrame(main_frame, text="Ausgabe")
output_frame.pack(fill=tk.BOTH, expand=True)

mode_var = tk.StringVar(value="project")
mode_label = ttk.Label(input_frame, text="Modus:")
mode_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
mode_project_radiobutton = ttk.Radiobutton(input_frame, text="Projekt", variable=mode_var, value="project", command=toggle_mode)
mode_project_radiobutton.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
mode_files_radiobutton = ttk.Radiobutton(input_frame, text="Dateien", variable=mode_var, value="files", command=toggle_mode)
mode_files_radiobutton.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

project_path_var = tk.StringVar()
project_path_label = ttk.Label(input_frame, text="Projekt-Pfad:")
project_path_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
project_path_entry = ttk.Entry(input_frame, width=50, textvariable=project_path_var, font=("Segoe UI", 10))
project_path_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
project_path_button = ttk.Button(input_frame, text="Durchsuchen", command=select_project_path)
project_path_button.grid(row=1, column=2, padx=5, pady=5)

file_extensions_var = tk.StringVar(value=".gd")
file_extensions_label = ttk.Label(input_frame, text="Dateiendungen (durch Komma getrennt):")
file_extensions_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
file_extensions_entry = ttk.Entry(input_frame, width=50, textvariable=file_extensions_var, font=("Segoe UI", 10))
file_extensions_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

selected_files_label = ttk.Label(input_frame, text="Ausgewählte Dateien:")
selected_files_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.N)
selected_files_listbox = tk.Listbox(input_frame, width=50, font=("Segoe UI", 10))
selected_files_listbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)
selected_files_button = ttk.Button(input_frame, text="Dateien auswählen", command=select_files)
selected_files_button.grid(row=1, column=2, padx=5, pady=5)
remove_file_button = ttk.Button(input_frame, text="Datei entfernen", command=remove_selected_file)
remove_file_button.grid(row=2, column=2, padx=5, pady=5)

question_label = ttk.Label(input_frame, text="Prompt:")
question_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
question_text = scrolledtext.ScrolledText(input_frame, height=5, font=("Segoe UI", 10))
question_text.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

send_button = ttk.Button(input_frame, text="Senden", command=send_request)
send_button.grid(row=4, column=2, padx=5, pady=5, sticky=tk.E)

answer_label = ttk.Label(output_frame, text="Antwort:")
answer_label.pack(anchor=tk.W)
answer_text = scrolledtext.ScrolledText(output_frame, height=10, font=("Segoe UI", 10))
answer_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

copy_button = ttk.Button(output_frame, text="Antwort Kopieren", command=copy_answer)
copy_button.pack(anchor=tk.E, padx=5, pady=5)

load_settings()
toggle_mode()

window.protocol("WM_DELETE_WINDOW", save_settings)
window.mainloop()