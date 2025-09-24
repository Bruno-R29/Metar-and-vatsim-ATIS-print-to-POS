# Metar-and-vatsim-ATIS-print-to-POS
A simple python application built with tkinter that fetches ATIS from VATSIM and METAR for any ICAO airport code. The ATIS will only work if there is anyone online controlling the requested airport and providing ATIS service. The application supports printing the fetched data directly to your default windows printer, something to make your flights feel a litle more realistic specially if you have a POS printer aka thermal printer. 
The ATIS function also displays controller callsign and frequency.
I made it so it has two buttons, so if you just want metar+TAF or atis you dont need to print both


Requirements:
Modules:
tkinter	
requests	
pywin32	(pip install win32printing)
ttk

Windows only for printing due to win32print
