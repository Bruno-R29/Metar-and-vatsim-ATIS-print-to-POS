import tkinter as tk
from tkinter import ttk
import requests
import win32print

# vatsim
def get_vatsim_data():
    """Fetch VATSIM data from the API."""
    url = "https://data.vatsim.net/v3/vatsim-data.json"
    headers = {'Accept': 'application/json'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching data from VATSIM API: {e}"}


def find_atis_by_icao(icao_code, vatsim_data):
    """Search for ATIS info based on ICAO code."""
    if "error" in vatsim_data:
        return vatsim_data["error"]
    
    atis_list = vatsim_data.get('atis', [])
    for atis in atis_list:
        callsign = atis.get('callsign', '').upper()
        if icao_code.upper() in callsign:
            frequency = atis.get('frequency', 'N/A')
            text_atis = "\n".join(atis.get('text_atis', []))
            return f"Controller Callsign: {callsign}\nFrequency: {frequency} MHz\n\n{text_atis}"
    return f"No ATIS information found for ICAO code {icao_code.upper()}."


def fetch_atis():
    icao_code = entry.get().strip().upper()
    if not icao_code:
        result_text.set("ICAO code cannot be empty.")
        return
    vatsim_data = get_vatsim_data()
    atis_info = find_atis_by_icao(icao_code, vatsim_data)
    result_text.set(atis_info)
    print_to_printer(atis_info)

# metar editt
def get_metar_for_icao(icao_code):
    base_url = f"https://aviationweather.gov/api/data/metar?taf=true&ids={icao_code}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}\nResponse content: {response.text}"
    except Exception as e:
        return f"Error: {e}"


def fetch_metar():
    icao_code = entry.get().strip().upper()
    if not icao_code:
        result_text.set("ICAO code cannot be empty.")
        return
    metar_data = get_metar_for_icao(icao_code)
    result_text.set(metar_data)
    print_to_printer(metar_data)

# default printer change it if you need it on another printer
def print_to_printer(data):
    try:
        printer_name = win32print.GetDefaultPrinter()
        hprinter = win32print.OpenPrinter(printer_name)
        hjob = win32print.StartDocPrinter(hprinter, 1, ("Aviation Data", None, "RAW"))
        try:
            win32print.StartPagePrinter(hprinter)
            lines = data.split("\n")
            for line in lines:
                raw_data = line.encode('utf-8')
                win32print.WritePrinter(hprinter, raw_data)
                win32print.WritePrinter(hprinter, b"\n")
            win32print.EndPagePrinter(hprinter)
        finally:
            win32print.EndDocPrinter(hprinter)
            win32print.ClosePrinter(hprinter)
    except Exception as e:
        result_text.set(f"Failed to print: {e}")


root = tk.Tk()
root.title("Aviation Weather & ATIS")


label = ttk.Label(root, text="Enter ICAO code:")
label.pack(pady=10)

entry = ttk.Entry(root, width=40)
entry.pack(pady=10)

atis_button = ttk.Button(root, text="Fetch ATIS", command=fetch_atis)
atis_button.pack(pady=5)

metar_button = ttk.Button(root, text="Fetch METAR", command=fetch_metar)
metar_button.pack(pady=5)

result_text = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_text, wraplength=400, justify="left")
result_label.pack(pady=10)


root.mainloop()
