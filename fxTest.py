import datetime
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import threading
import time


weak_count_eur = 0
weak_count_usd = 0
weak_count_tie = 0

# Function to scrape forex data
def scrape_forex_data():
    url = "https://www.investing.com/currencies"  # Replace with the actual URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
  # Extract daily change values for EUR/USD, EUR/JPY, and USD/JPY
    def get_daily_change(pair_id):
        row = soup.find("tr", id=f"pair_{pair_id}")
        if row:
            # Get the second last <td> element (daily change percentage)
            daily_change_td = row.find_all("td")[-2]
            daily_change = daily_change_td.text.strip()
            return float(daily_change.strip('%'))  # Remove '%' and convert to float
        return 0.0  # Default value if the row is not found
    
    eurusd_change = round(get_daily_change(1),2)  # Assuming EUR/USD has pair_id="1"
    eurjpy_change = round(get_daily_change(9),2)  # Assuming EUR/JPY has pair_id="2"
    usdjpy_change = round(get_daily_change(3),2)  # Assuming USD/JPY has pair_id="3"
    
    return eurusd_change, eurjpy_change, usdjpy_change

# Function to update the GUI
def update_gui():
    global weak_count_eur
    global weak_count_usd
    global weak_count_tie
    while True:
        eurusd_change, eurjpy_change, usdjpy_change = scrape_forex_data()
        
        # Calculate the difference
        difference = round(eurusd_change - eurjpy_change, 2)
        
        # Update the labels
        eurusd_label.config(text=f"EURUSD: {eurusd_change}%")
        eurjpy_label.config(text=f"EURJPY: {eurjpy_change}%")
        usdjpy_label.config(text=f"USDJPY: {usdjpy_change}%")
        difference_label.config(text=f"Difference (EURUSD - EURJPY): {difference}%")

        usdjpy_change = -1 * usdjpy_change
        label =""
        if usdjpy_change < difference:
            label = "EUR"
            weak_count_eur = weak_count_eur+1
        elif usdjpy_change > difference:
            label = 'USD'
            weak_count_usd = weak_count_usd+1
        else:
            label = "TIE"
            weak_count_tie = weak_count_tie+1
        
        weakness_label.config(text=f"Current Weakness: {label}")
        weakness_counter_label.config(text=f"Weaknesses Counter\n    EUR | TIE | USD\n       {weak_count_eur}    |   {weak_count_tie}   |   { weak_count_usd}")
        time.sleep(20)
def reset_counters():
    global weak_count_eur
    global weak_count_tie
    global weak_count_usd
    weak_count_eur = 0
    weak_count_usd = 0
    weak_count_tie = 0
    weakness_counter_label.config(text=f"Weaknesses Counter\n    EUR | TIE | USD\n       {weak_count_eur}    |   {weak_count_tie}   |   { weak_count_usd}")
    timestamp_start_label.config(text=f"{datetime.datetime.now().replace(microsecond=0)}")
# Create the main window
root = tk.Tk()
root.title("Forex Daily Change Monitor")

# Create labels to display the data
eurusd_label = ttk.Label(root, text="EURUSD: N/A", font=('Arial', 14))
eurusd_label.pack(pady=10)

eurjpy_label = ttk.Label(root, text="EURJPY: N/A", font=('Arial', 14))
eurjpy_label.pack(pady=10)

usdjpy_label = ttk.Label(root, text="USDJPY: N/A", font=('Arial', 14))
usdjpy_label.pack(pady=10)

difference_label = ttk.Label(root, text="Difference (EURUSD - EURJPY): N/A", font=('Arial', 14))
difference_label.pack(pady=10)

weakness_label = ttk.Label(root, text="Current Weakness: >:D", font=('Arial', 14))
weakness_label.pack(pady=10)

weakness_counter_label = ttk.Label(root, text="Weakness counter loading..", font=('Arial', 14))
weakness_counter_label.pack(pady=10)

weakness_counter_reset_btn = ttk.Button(root, text="Reset", command=lambda: reset_counters())
weakness_counter_reset_btn.pack(pady=10)

timestamp_start_label = ttk.Label(root, text=f"{datetime.datetime.now().replace(microsecond=0)}")
timestamp_start_label.pack(pady=10)


# Start the scraping thread
scraping_thread = threading.Thread(target=update_gui, daemon=True)
scraping_thread.start()

# Run the GUI loop
root.mainloop()