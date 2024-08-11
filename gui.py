import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, Toplevel, Scale, ttk, HORIZONTAL
from symbol import check_stock, symbol_data, thresholds
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd

# Initialize tkinter window
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
root = ctk.CTk()
root.title("Analysis Tool - Daniel Spurrell")
root.geometry("1024x768")
root.configure(bg="#f0f0f0")

# Initialize a variable to keep track of the image label
image_label = None
tab_view = ctk.CTkTabview(root)
tab_1 = tab_view.add("Chart")
tab_2 = tab_view.add("Financials")
tab_3 = tab_view.add("Screener")
tab_view.pack()
def open_settings():
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x500")
    settings_window.configure(bg="#121212")
    
    def update_thresholds():
        global thresholds
        thresholds["pe_ratio_threshold"] = pe_slider.get()
        thresholds["rsi_threshold"] = rsi_slider.get()
        thresholds["quick_ratio_threshold"] = quick_slider.get()
        thresholds["current_ratio_threshold"] = current_slider.get()
        messagebox.showinfo("Settings", "Thresholds updated successfully!")

    # Function to update slider labels
    def update_label(label, slider):
        label.configure(text=f"{slider.get():.2f}")

    # PE Ratio Slider
    ctk.CTkLabel(settings_window, text="PE Ratio Threshold", bg_color="#121212").pack(pady=10)
    pe_slider = ctk.CTkSlider(settings_window, from_=5, to=50)
    pe_slider.set(thresholds.get('pe_ratio_threshold'))
    pe_slider.pack()
    pe_label = ctk.CTkLabel(settings_window, text=f"{pe_slider.get():.2f}", bg_color="#121212")
    pe_label.pack(pady=5)
    pe_slider.configure(command=lambda value: update_label(pe_label, pe_slider))

    # RSI Slider
    ctk.CTkLabel(settings_window, text="RSI Threshold", bg_color="#121212").pack(pady=10)
    rsi_slider = ctk.CTkSlider(settings_window, from_=10, to=70)
    rsi_slider.set(thresholds.get("rsi_threshold"))
    rsi_slider.pack()
    rsi_label = ctk.CTkLabel(settings_window, text=f"{rsi_slider.get():.2f}", bg_color="#121212")
    rsi_label.pack(pady=5)
    rsi_slider.configure(command=lambda value: update_label(rsi_label, rsi_slider))

    # Quick Ratio Slider
    ctk.CTkLabel(settings_window, text="Quick Ratio Threshold", bg_color="#121212").pack(pady=10)
    quick_slider = ctk.CTkSlider(settings_window, from_=0.5, to=3.0, number_of_steps=25)
    quick_slider.set(thresholds.get("quick_ratio_threshold"))
    quick_slider.pack()
    quick_label = ctk.CTkLabel(settings_window, text=f"{quick_slider.get():.2f}", bg_color="#121212")
    quick_label.pack(pady=5)
    quick_slider.configure(command=lambda value: update_label(quick_label, quick_slider))

    # Current Ratio Slider
    ctk.CTkLabel(settings_window, text="Current Ratio Threshold", bg_color="#121212").pack(pady=10)
    current_slider = ctk.CTkSlider(settings_window, from_=0.5, to=3.0, number_of_steps=25)
    current_slider.set(thresholds.get("current_ratio_threshold"))
    current_slider.pack()
    current_label = ctk.CTkLabel(settings_window, text=f"{current_slider.get():.2f}", bg_color="#121212")
    current_label.pack(pady=5)
    current_slider.configure(command=lambda value: update_label(current_label, current_slider))
    # Update Button
    tk.Button(settings_window, text="Update Thresholds", bg="#007BFF", fg="white", command=update_thresholds).pack(pady=20)

def on_check_stock():
    global fin_data_label
    symbol = symbol_entry.get().upper()
    draw_chart()
    fin_data = check_stock(symbol)
    fin_data_label.configure(text=fin_data)
def draw_chart():
    global image_label  # Use global to modify the reference
    symbol = symbol_entry.get().upper()
    time_frame = date_frame_combo.get()

    # Create the candlestick chart
    candle_data = symbol_data(ticker=symbol, period=time_frame)
    dates = pd.to_datetime(candle_data.index.values).strftime('%Y-%m-%d').tolist()

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
    # Save the figure as an image file (PNG) using kaleido image engine instead of orca
    pio.write_image(fig, 'candlestick.png', engine='kaleido')

    # Load the image and keep a reference to it
    candlestick_image = tk.PhotoImage(file="candlestick.png")
    
    # If an image_label already exists, update it; otherwise, create a new one
    if image_label:
        image_label.config(image=candlestick_image)
    else:
        image_label = tk.Label(tab_1, image=candlestick_image, text="")
        image_label.pack()

    # Ensure the image reference is kept
    image_label.image = candlestick_image



# Tab 1

# Input field for the stock symbol
symbol_label = ctk.CTkLabel(tab_1, text="Enter Ticker:", font=("Roboto", 12))
symbol_label.pack(pady=10)

symbol_entry = ctk.CTkEntry(tab_1, font=("Roboto", 14))
symbol_entry.insert(0,"AAPL")
symbol_entry.pack(pady=5)

date_frame_combo = ctk.CTkComboBox(tab_1, state='readonly', values=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'ytd', 'max'])
date_frame_combo.set('ytd')
date_frame_combo.pack()

# Button to trigger the stock check
check_button = ctk.CTkButton(tab_1, text="Check Stock", font=("Roboto", 12), command=on_check_stock)
check_button.pack(pady=20)

# Settings button in the top-right corner
settings_button = ctk.CTkButton(root, text="⚙", font=("Roboto", 10), width=50, command=open_settings)
settings_button.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=10)


# Tab 2

fin_data_label = ctk.CTkLabel(tab_2, text="Enter ticker and results will appear here", anchor="w", justify="left",)
fin_data_label.pack()

# Run the application
root.mainloop()
