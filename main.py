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
    with open(file_path, "r") as file:
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

def send_request():
    project_path = project_path_var.get()
    file_extensions = file_extensions_var.get().split(",")
    max_tokens = int(max_tokens_var.get())
    api_key = api_key_var.get()
    question = question_text.get("1.0", tk.END).strip()

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

def save_settings():
    settings = {
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
                if key == "project_path":
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

input_frame = ttk.LabelFrame(main_frame, text="Eingabe")
input_frame.pack(fill=tk.BOTH, expand=True)

output_frame = ttk.LabelFrame(main_frame, text="Ausgabe")
output_frame.pack(fill=tk.BOTH, expand=True)

project_path_var = tk.StringVar()
project_path_label = ttk.Label(input_frame, text="Projektpfad:")
project_path_label.pack(anchor=tk.W)
project_path_entry = ttk.Entry(input_frame, width=50, textvariable=project_path_var, font=("Segoe UI", 10))
project_path_entry.pack(fill=tk.X, padx=5, pady=5)
project_path_button = ttk.Button(input_frame, text="Durchsuchen", command=select_project_path)
project_path_button.pack(anchor=tk.E, padx=5, pady=5)

file_extensions_var = tk.StringVar(value=".gd")
file_extensions_label = ttk.Label(input_frame, text="Dateiendungen (durch Komma getrennt):")
file_extensions_label.pack(anchor=tk.W)
file_extensions_entry = ttk.Entry(input_frame, width=50, textvariable=file_extensions_var, font=("Segoe UI", 10))
file_extensions_entry.pack(fill=tk.X, padx=5, pady=5)

max_tokens_var = tk.StringVar(value="4096")
max_tokens_label = ttk.Label(input_frame, text="Maximale Token-Länge:")
max_tokens_label.pack(anchor=tk.W)
max_tokens_combobox = ttk.Combobox(input_frame, textvariable=max_tokens_var, values=["512", "1024", "2048", "4096"], state="readonly", font=("Segoe UI", 10))
max_tokens_combobox.pack(anchor=tk.W, padx=5, pady=5)

api_key_var = tk.StringVar()
api_key_label = ttk.Label(input_frame, text="API-Schlüssel:")
api_key_label.pack(anchor=tk.W)
api_key_entry = ttk.Entry(input_frame, width=50, textvariable=api_key_var, show="*", font=("Segoe UI", 10))
api_key_entry.pack(fill=tk.X, padx=5, pady=5)

question_label = ttk.Label(input_frame, text="Frage oder Aufgabe:")
question_label.pack(anchor=tk.W)
question_text = scrolledtext.ScrolledText(input_frame, height=5, font=("Segoe UI", 10))
question_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

send_button = ttk.Button(input_frame, text="Senden", command=send_request)
send_button.pack(anchor=tk.E, padx=5, pady=5)

answer_label = ttk.Label(output_frame, text="Antwort:")
answer_label.pack(anchor=tk.W)
answer_text = scrolledtext.ScrolledText(output_frame, height=10, font=("Segoe UI", 10))
answer_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

load_settings()

window.protocol("WM_DELETE_WINDOW", save_settings)
window.mainloop()