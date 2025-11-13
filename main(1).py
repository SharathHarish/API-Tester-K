import tkinter as tk
from tkinter import ttk, messagebox
import requests, os, json
from datetime import datetime

# ------------------- THEMES -------------------
LIGHT_THEME = {
    "bg": "#f7f7f9",
    "fg": "#1c1c1c",
    "button_bg": "#27ae60",
    "button_fg": "#ffffff",
    "frame_bg": "#e8e8ec",
    "entry_bg": "#ffffff",
}
DARK_THEME = {
    "bg": "#1e1e1e",
    "fg": "#f5f5f5",
    "button_bg": "#27ae60",
    "button_fg": "#ffffff",
    "frame_bg": "#2d2d2d",
    "entry_bg": "#3b3b3b",
}

FONT_NORMAL = ("Times New Roman", 10)
FONT_BOLD = ("Times New Roman", 10, "bold")

current_theme = LIGHT_THEME
request_history = []
MAX_HISTORY = 20
current_env = {}

os.makedirs("environments", exist_ok=True)
os.makedirs("collections", exist_ok=True)

# ------------------- ENVIRONMENT FUNCTIONS -------------------
def load_environment(filename="default.json"):
    global current_env
    path = os.path.join("environments", filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            current_env = json.load(f)
    else:
        current_env = {}
    update_env_label()

def update_env_label():
    env_label.config(text=f"🌐 Environment: {os.path.splitext(current_env_name.get())[0]}")

# ------------------- THEME HANDLING -------------------
def apply_theme():
    root.config(bg=current_theme["bg"])
    for frame in [url_frame, response_frame, history_frame, env_frame, headers_frame, body_frame]:
        frame.config(bg=current_theme["frame_bg"])
    for w in [url_label, response_label, env_label, headers_label, body_label, status_label]:
        w.config(bg=current_theme["frame_bg"], fg=current_theme["fg"])
    for entry in [url_entry, headers_text, body_text, raw_text, json_text, headers_view]:
        entry.config(bg=current_theme["entry_bg"], fg=current_theme["fg"], insertbackground=current_theme["fg"])
    history_list.config(bg=current_theme["entry_bg"], fg=current_theme["fg"])
    send_btn.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    save_btn.config(bg="#6ab04c", fg="white")
    toggle_btn.config(bg=current_theme["frame_bg"], fg=current_theme["fg"])
    main_frame.config(bg=current_theme["bg"])

def toggle_theme():
    global current_theme
    if current_theme == LIGHT_THEME:
        current_theme = DARK_THEME
        toggle_btn.config(text="☀️ Light Mode")
    else:
        current_theme = LIGHT_THEME
        toggle_btn.config(text="🌙 Dark Mode")
    apply_theme()

# ------------------- HISTORY -------------------
def update_history_list():
    history_list.delete(0, tk.END)
    for method, url, time in request_history:
        history_list.insert(tk.END, f"[{time}] {method} → {url}")

def replay_request(event):
    selection = history_list.curselection()
    if not selection:
        return
    idx = selection[0]
    method, url, _ = request_history[idx]
    method_combo.set(method)
    url_entry.delete(0, tk.END)
    url_entry.insert(0, url)
    send_request()

# ------------------- REQUEST FUNCTIONS -------------------
def parse_headers():
    raw = headers_text.get("1.0", tk.END).strip()
    if not raw:
        return {}
    headers = {}
    for line in raw.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
    return headers

def send_request():
    url = url_entry.get().strip()
    method = method_combo.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    final_url = url
    for key, value in current_env.items():
        final_url = final_url.replace(f"{{{{{key}}}}}", value)

    headers = parse_headers()
    body_raw = body_text.get("1.0", tk.END).strip()
    json_data = None
    data = None

    if method in ["POST", "PUT", "PATCH"]:
        if body_raw:
            try:
                json_data = json.loads(body_raw)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON body.")
                return

    try:
        response = requests.request(method, final_url, headers=headers, json=json_data, data=data)
        elapsed = response.elapsed.total_seconds() * 1000  # ms

        # Update status bar
        status_label.config(text=f"Status: {response.status_code} | Time: {elapsed:.1f} ms")

        # Fill Tabs
        raw_text.delete("1.0", tk.END)
        json_text.delete("1.0", tk.END)
        headers_view.delete("1.0", tk.END)

        raw_text.insert(tk.END, response.text)
        for k, v in response.headers.items():
            headers_view.insert(tk.END, f"{k}: {v}\n")

        try:
            formatted = json.dumps(response.json(), indent=4)
            json_text.insert(tk.END, formatted)
        except:
            json_text.insert(tk.END, "(Not JSON)")

        timestamp = datetime.now().strftime("%H:%M:%S")
        request_history.insert(0, (method, url, timestamp))
        if len(request_history) > MAX_HISTORY:
            request_history.pop()
        update_history_list()
    except Exception as e:
        raw_text.delete("1.0", tk.END)
        raw_text.insert(tk.END, f"Error: {str(e)}")
        status_label.config(text="Request Failed")

def save_to_collection():
    data = {
        "method": method_combo.get(),
        "url": url_entry.get(),
        "headers": headers_text.get("1.0", tk.END).strip(),
        "body": body_text.get("1.0", tk.END).strip(),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    filename = f"req_{data['timestamp'].replace(':', '-')}.json"
    path = os.path.join("collections", filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Saved", f"Request saved to collections/{filename}")

# ------------------- UI -------------------
root = tk.Tk()
root.title("API Tester")
root.geometry("1150x720")

history_frame = tk.Frame(root, width=220, bg=current_theme["frame_bg"])
history_frame.pack(side="left", fill="y")
tk.Label(history_frame, text="History", bg=current_theme["frame_bg"], fg=current_theme["fg"], font=FONT_BOLD).pack(pady=5)
history_list = tk.Listbox(history_frame, bg=current_theme["entry_bg"], fg=current_theme["fg"],
                          font=FONT_NORMAL, activestyle="none", selectbackground="#2e86de")
history_list.pack(fill="both", expand=True, padx=10, pady=5)
history_list.bind("<Double-1>", replay_request)

main_frame = tk.Frame(root, bg=current_theme["bg"])
main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

url_frame = tk.Frame(main_frame, bg=current_theme["frame_bg"])
url_frame.pack(fill="x", pady=5)
url_label = tk.Label(url_frame, text="URL:", bg=current_theme["frame_bg"], fg=current_theme["fg"], font=FONT_BOLD)
url_label.pack(side="left", padx=5)

method_combo = ttk.Combobox(url_frame, values=["GET", "POST", "PUT", "DELETE", "PATCH"], width=10, state="readonly")
method_combo.current(0)
method_combo.pack(side="left", padx=5)
url_entry = tk.Entry(url_frame, font=FONT_NORMAL, bg=current_theme["entry_bg"], fg=current_theme["fg"], width=60)
url_entry.pack(side="left", padx=5, fill="x", expand=True)

send_btn = tk.Button(url_frame, text="Send Request", bg=current_theme["button_bg"],
                     fg=current_theme["button_fg"], font=FONT_BOLD, command=send_request)
send_btn.pack(side="left", padx=5)

save_btn = tk.Button(url_frame, text="💾 Save", bg="#6ab04c", fg="white", font=FONT_BOLD, command=save_to_collection)
save_btn.pack(side="left", padx=5)

toggle_btn = tk.Button(url_frame, text="🌙 Dark Mode", command=toggle_theme, font=FONT_BOLD)
toggle_btn.pack(side="left", padx=5)

# Environment
env_frame = tk.Frame(main_frame, bg=current_theme["frame_bg"])
env_frame.pack(fill="x", pady=3)
env_label = tk.Label(env_frame, text="🌐 Environment: default", bg=current_theme["frame_bg"], fg=current_theme["fg"], font=FONT_NORMAL)
env_label.pack(side="left", padx=8)
env_files = [f for f in os.listdir("environments") if f.endswith(".json")]
if not env_files:
    env_files = ["default.json"]
    if not os.path.exists("environments/default.json"):
        with open("environments/default.json", "w") as f:
            json.dump({"base_url": "https://jsonplaceholder.typicode.com"}, f, indent=4)
current_env_name = tk.StringVar(value=env_files[0])
env_combo = ttk.Combobox(env_frame, values=env_files, textvariable=current_env_name, state="readonly", width=25)
env_combo.pack(side="right", padx=10)
def on_env_change(event):
    load_environment(env_combo.get())
env_combo.bind("<<ComboboxSelected>>", on_env_change)
load_environment(env_combo.get())

# Headers
headers_frame = tk.Frame(main_frame, bg=current_theme["frame_bg"])
headers_frame.pack(fill="x", pady=5)
headers_label = tk.Label(headers_frame, text="Headers:", bg=current_theme["frame_bg"], fg=current_theme["fg"], font=FONT_BOLD)
headers_label.pack(anchor="w", padx=5)
headers_text = tk.Text(headers_frame, height=5, bg=current_theme["entry_bg"], fg=current_theme["fg"], font=FONT_NORMAL)
headers_text.pack(fill="x", padx=5, pady=5)

# Body
body_frame = tk.Frame(main_frame, bg=current_theme["frame_bg"])
body_frame.pack(fill="x", pady=5)
body_label = tk.Label(body_frame, text="Body (JSON):", bg=current_theme["frame_bg"], fg=current_theme["fg"], font=FONT_BOLD)
body_label.pack(anchor="w", padx=5)
body_text = tk.Text(body_frame, height=7, bg=current_theme["entry_bg"], fg=current_theme["fg"], font=FONT_NORMAL)
body_text.pack(fill="x", padx=5, pady=5)

# Response Tabs
response_frame = tk.Frame(main_frame, bg=current_theme["frame_bg"])
response_frame.pack(fill="both", expand=True, pady=5)

notebook = ttk.Notebook(response_frame)
tab_raw = tk.Frame(notebook)
tab_json = tk.Frame(notebook)
tab_headers = tk.Frame(notebook)
notebook.add(tab_raw, text="Raw")
notebook.add(tab_json, text="JSON")
notebook.add(tab_headers, text="Headers")
notebook.pack(fill="both", expand=True)

response_label = tk.Label(response_frame, text="Response:", bg=current_theme["frame_bg"], fg=current_theme["fg"], font=FONT_BOLD)
response_label.pack(anchor="w", padx=5, pady=3)

raw_text = tk.Text(tab_raw, bg=current_theme["entry_bg"], fg=current_theme["fg"], font=FONT_NORMAL, wrap="word")
raw_text.pack(fill="both", expand=True, padx=5, pady=5)
json_text = tk.Text(tab_json, bg=current_theme["entry_bg"], fg=current_theme["fg"], font=FONT_NORMAL, wrap="word")
json_text.pack(fill="both", expand=True, padx=5, pady=5)
headers_view = tk.Text(tab_headers, bg=current_theme["entry_bg"], fg=current_theme["fg"], font=FONT_NORMAL, wrap="word")
headers_view.pack(fill="both", expand=True, padx=5, pady=5)

status_label = tk.Label(response_frame, text="Status: — | Time: —", bg=current_theme["frame_bg"], fg=current_theme["fg"], font=FONT_NORMAL)
status_label.pack(fill="x", pady=2)

apply_theme()
root.mainloop()
