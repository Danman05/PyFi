import tkinter as tk
import customtkinter as ctk
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import threading
import logging


# Workspace imports

from GUI.settings_component import open_settings

from const import _SYMBOL_LOCATIONS_, _SYMBOL_EXCHANGES_, _ALLOWED_PERIODS_

from ticker import Ticker
from scanner import Scanner
from evaluator import Evaluator
from symbol_fetcher import get_count_of_filtered_symbols

# Initialize tkinter window
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
root = ctk.CTk()
root.title("Analysis Tool - Daniel Spurrell")
root.geometry("1024x768")
root.configure(bg="#f0f0f0")

logging.basicConfig(
    filename="Log.txt",
    format='%(asctime)s: %(levelname)s: %(message)s',
    level=logging.INFO
)

evaluator = Evaluator()
scanner = Scanner()

# Initialize a variable to keep track of the image label
image_label = None

# Tabview
tab_view = ctk.CTkTabview(root)
tab_1 = tab_view.add("Chart")
tab_2 = tab_view.add("Financials")
tab_3 = tab_view.add("Scanner")

tab_view.pack()

# Define options for locations and exchanges
locations = _SYMBOL_LOCATIONS_

exchanges = _SYMBOL_EXCHANGES_

# Variable to store the selected location and exchange
selected_location = ctk.StringVar(value=locations[0])
selected_exchange = ctk.StringVar()


global fin_data_label 

def on_check_stock():

    global fin_data_label

    symbol = symbol_entry.get().upper()
    time_period = date_frame_combo.get()

    ticker = Ticker(ticker=symbol, history_period=time_period, skip_info=True)
    draw_chart(ticker.history)

    symbol_report = evaluator.generate_report(symbol)
    fin_data_label.configure(text=symbol_report)

def create_thread(target_function, *args, **kwargs):
    return threading.Thread(target=target_function, args=args, kwargs=kwargs)

def draw_chart(ticker_history):
    global image_label  # Use global to modify the reference

    # Create the candlestick chart
    candle_data = ticker_history
    dates = pd.to_datetime(ticker_history.index.values).strftime('%Y-%m-%d').tolist()

    # Create the candlestick chart
    fig = go.Figure(
        data=[
            go.Candlestick(
            x=dates,
                open=candle_data['Open'].values,
                high=candle_data['High'].values,
                low=candle_data['Low'].values,
                close=candle_data['Close'].values
            ),
        ], 
    )
    # Update the layout to set background colors
    fig.update_layout(
        plot_bgcolor='black',  # Background color of the plotting area
        paper_bgcolor='black', # Background color of the entire figure
        xaxis=dict(
            rangebreaks=[
                dict(bounds=["sat", "mon"]), #Hide weekends
            ],
            showgrid=False,  # Hide the grid lines
            zeroline=False,  # Hide the zero line
            showticklabels=True,
            color='white'     # Color of the x-axis labels
        ),
        yaxis=dict(
            showgrid=False,  # Hide the grid lines
            zeroline=False,  # Hide the zero line
            showticklabels=True,
            color='white'     # Color of the y-axis labels
        ),
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
        
    )
    file_location = 'assets/src/candlestick.png'
    # Save the figure as an image file (PNG) using kaleido image engine instead of orca
    pio.write_image(fig, file_location, engine='kaleido')

    # Load the image and keep a reference to it
    candlestick_image = tk.PhotoImage(file=file_location)
    
    # If an image_label already exists, update it; otherwise, create a new one
    if image_label:
        image_label.config(image=candlestick_image)
    else:
        image_label = tk.Label(tab_1, image=candlestick_image, text="")
        image_label.pack()

    # Ensure the image reference is kept
    image_label.image = candlestick_image

def open_file_dialog():
    # Ask the user to select a directory
    directory = ctk.filedialog.askdirectory()
    
    if directory:
        # Define the file path using the selected directory
        file_path = f"{directory}/buying_opportunities.csv"

        evaluator.save_opportunities_to_csv(file_path)
        logging.info(f"CSV file saved to {file_path}")

# Function to update exchange options based on the selected location
def update_exchanges(*args):
    location = selected_location.get()
    
    # Update the second select box options
    exchange_menu.configure(values=exchanges[location])
    selected_exchange.set(exchanges[location][0])  # Set default selection to the first option
    
def set_scan_count(*args):
    location = selected_location.get().lower()
    exchange = selected_exchange.get().upper()
    count = get_count_of_filtered_symbols(location, exchange)
    scan_button.configure(text=f'Scan {count} symbols', command= lambda: scan_exchange_symbols(location, exchange))

def scan_exchange_symbols(location, exchange):

    def wait_for_thread(thread: threading.Thread):
        thread.join()
        set_scan_count()
        save_to_csv_button.pack(pady=10)


    save_to_csv_button.pack_forget()
    scan_button.configure(text="Scanning - This might take some time", command=None)

    # Create thread that scans all possible symbols
    scan_thread = create_thread(scanner.scan_symbols, scan_location=location, exchange=exchange, evaluator=evaluator)
    scan_thread.start()

    # Create another thread that waits for the scanning thread, prevents UI from blocking.
    # There might be a better way to handle this without blocking UI, but this is the way for now
    create_thread(wait_for_thread, scan_thread).start()


# Tab 1

# Input field for the stock symbol
symbol_label = ctk.CTkLabel(tab_1, text="Enter Ticker:", font=("Roboto", 12))
symbol_label.pack(pady=10)

symbol_entry = ctk.CTkEntry(tab_1, font=("Roboto", 14))
symbol_entry.insert(0,"AAPL")
symbol_entry.pack(pady=5)

date_frame_combo = ctk.CTkComboBox(tab_1, state='readonly', values=_ALLOWED_PERIODS_)
date_frame_combo.set('ytd')
date_frame_combo.pack()

# Button to trigger the stock check
check_button = ctk.CTkButton(tab_1, text="Check Stock", font=("Roboto", 12), command=lambda: create_thread(on_check_stock).start())
check_button.pack(pady=20)

# Settings button in the top-right corner
settings_button = ctk.CTkButton(root, text="⚙", font=("Roboto", 10), width=50, command= lambda: open_settings(root, evaluator))
settings_button.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=10)

# Tab 2

fin_data_label = ctk.CTkLabel(tab_2, text="Enter ticker and results will appear here", anchor="w", justify="left",)
fin_data_label.pack()

# Tab 3

# Create the first select box (Location)
location_menu = ctk.CTkOptionMenu(tab_3, variable=selected_location, values=locations)
location_menu.pack(pady=20)

# Link the update function to location selection change
selected_location.trace_add(['write'], update_exchanges)

# Create the second select box (Exchange)
exchange_menu = ctk.CTkOptionMenu(tab_3, variable=selected_exchange)
exchange_menu.pack(pady=20)

selected_exchange.trace_add(['write'], lambda *args: create_thread(set_scan_count).start())

scan_button = ctk.CTkButton(tab_3, text='Gathering information...')
scan_button.pack(pady=10)

save_to_csv_button = ctk.CTkButton(tab_3, text='Save result as CSV', command=open_file_dialog)

# Initialize with the default location
update_exchanges()

# Run the application
root.mainloop()
