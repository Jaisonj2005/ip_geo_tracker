import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading

def fetch_geo_data():
    target_ip = entry_ip.get().strip()
    
    if not target_ip:
        messagebox.showerror("Input Error", "Please enter a valid IP address or domain.")
        return

    btn_track.config(state=tk.DISABLED)
    lbl_status.config(text="Querying OSINT databases...", fg="#e67e22")
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, f"[*] Tracing route and location for: {target_ip}\n")
    text_output.insert(tk.END, "-" * 55 + "\n")
    
    # Run the HTTP request in a background thread
    threading.Thread(target=process_api_call, args=(target_ip,), daemon=True).start()

def process_api_call(target):
    try:
        # We use ip-api.com - it is free for non-commercial use and requires no API key
        url = f"http://ip-api.com/json/{target}"
        response = requests.get(url, timeout=5)
        data = response.json()

        # The API returns a 'fail' status for reserved/private IPs (e.g., 192.168.1.1)
        if data.get("status") == "fail":
            error_msg = data.get("message", "Unknown error")
            text_output.insert(tk.END, f"[!] Tracking failed: {error_msg.capitalize()}.\n")
            text_output.insert(tk.END, "Hint: Are you trying to track a local/private IP?\n")
            lbl_status.config(text="Query Failed", fg="#c0392b")
        else:
            insert_text("Resolved IP", data.get("query"))
            insert_text("Country", data.get("country"))
            insert_text("Region/State", data.get("regionName"))
            insert_text("City", data.get("city"))
            insert_text("ZIP/Postal Code", data.get("zip"))
            insert_text("Timezone", data.get("timezone"))
            insert_text("ISP", data.get("isp"))
            insert_text("ASN/Organization", data.get("as"))
            insert_text("Coordinates", f"Lat: {data.get('lat')}, Lon: {data.get('lon')}")
            
            text_output.insert(tk.END, "-" * 55 + "\n[*] Geolocation OSINT complete.\n")
            lbl_status.config(text="Tracking Successful", fg="#27ae60")

    except requests.exceptions.RequestException as e:
        text_output.insert(tk.END, f"[!] Network error occurred: {str(e)}\n")
        lbl_status.config(text="Network Error", fg="#c0392b")
    except Exception as e:
        text_output.insert(tk.END, f"[!] An unexpected error occurred: {str(e)}\n")
        lbl_status.config(text="Error", fg="#c0392b")

    text_output.config(state=tk.DISABLED)
    btn_track.config(state=tk.NORMAL)

def insert_text(label, value):
    if not value:
        value = "N/A"
    text_output.insert(tk.END, f"{label+':':<20} {value}\n")

# --- Tkinter GUI Layout ---
root = tk.Tk()
root.title("SOC Toolkit - IP Geolocation Tracker")
root.geometry("550x480")
root.resizable(False, False)

frame = ttk.Frame(root, padding="15")
frame.pack(fill=tk.BOTH, expand=True)

lbl_title = tk.Label(frame, text="IP Geolocation & ASN Tracker", font=("Helvetica", 13, "bold"))
lbl_title.pack(anchor="w", pady=(0, 10))

# Input Frame
input_frame = tk.Frame(frame)
input_frame.pack(fill=tk.X, pady=(0, 10))

lbl_ip = tk.Label(input_frame, text="Target IP / Domain:", font=("Helvetica", 10))
lbl_ip.pack(side=tk.LEFT, padx=(0, 5))

entry_ip = ttk.Entry(input_frame, width=25, font=("Consolas", 10))
entry_ip.pack(side=tk.LEFT, padx=(0, 10))
entry_ip.insert(0, "8.8.8.8")

btn_track = tk.Button(input_frame, text="Trace Location", command=fetch_geo_data, bg="#2980b9", fg="white", font=("Helvetica", 9, "bold"))
btn_track.pack(side=tk.LEFT)

lbl_status = tk.Label(frame, text="Ready", font=("Helvetica", 9, "italic"), fg="#555")
lbl_status.pack(anchor="w", pady=(0, 5))

# Output Console Display
text_frame = tk.Frame(frame)
text_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_output = tk.Text(text_frame, font=("Consolas", 10), bg="#1e1e1e", fg="#ecf0f1", yscrollcommand=scrollbar.set)
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text_output.config(state=tk.DISABLED)
scrollbar.config(command=text_output.yview)

root.mainloop()