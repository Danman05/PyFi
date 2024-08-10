import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, Toplevel, Scale, ttk, HORIZONTAL
from symbol import check_stock, symbol_data
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd

# Initialize tkinter window
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
root = ctk.CTk()
root.title("Analysis Tool - Daniel Spurrell")
root.geometry("900x700")
root.configure(bg="#f0f0f0")

# Initialize a variable to keep track of the image label
image_label = None

def open_settings():
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x300")
    settings_window.configure(bg="#f0f0f0")
    
    def update_thresholds():
        global pe_ratio_threshold, rsi_threshold, quick_ratio_threshold, current_ratio_threshold
        pe_ratio_threshold = pe_slider.get()
        rsi_threshold = rsi_slider.get()
        quick_ratio_threshold = quick_slider.get()
        current_ratio_threshold = current_slider.get()
        messagebox.showinfo("Settings", "Thresholds updated successfully!")
    
    # PE Ratio Slider
    tk.Label(settings_window, text="PE Ratio Threshold", bg="#f0f0f0").pack(pady=10)
    pe_slider = Scale(settings_window, from_=5, to=50, orient=HORIZONTAL, bg="#e0e0e0")
    pe_slider.set(pe_ratio_threshold)
    pe_slider.pack()

    # RSI Slider
    tk.Label(settings_window, text="RSI Threshold", bg="#f0f0f0").pack(pady=10)
    rsi_slider = Scale(settings_window, from_=10, to=70, orient=HORIZONTAL, bg="#e0e0e0")
    rsi_slider.set(rsi_threshold)
    rsi_slider.pack()

    # Quick Ratio Slider
    tk.Label(settings_window, text="Quick Ratio Threshold", bg="#f0f0f0").pack(pady=10)
    quick_slider = Scale(settings_window, from_=0.5, to=3.0, resolution=0.1, orient=HORIZONTAL, bg="#e0e0e0")
    quick_slider.set(quick_ratio_threshold)
    quick_slider.pack()

    # Current Ratio Slider
    tk.Label(settings_window, text="Current Ratio Threshold", bg="#f0f0f0").pack(pady=10)
    current_slider = Scale(settings_window, from_=0.5, to=3.0, resolution=0.1, orient=HORIZONTAL, bg="#e0e0e0")
    current_slider.set(current_ratio_threshold)
    current_slider.pack()

    # Update Button
    tk.Button(settings_window, text="Update Thresholds", bg="#007BFF", fg="white", command=update_thresholds).pack(pady=20)

def on_check_stock():
    symbol = symbol_entry.get().upper()
    draw_chart()
    messagebox.showinfo("Analysis Result", check_stock(symbol))

def draw_chart():
    global image_label  # Use global to modify the reference
    print("drawing chart")
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
        image_label = tk.Label(root, image=candlestick_image, text="")
        image_label.pack()

    # Ensure the image reference is kept
    image_label.image = candlestick_image

# Input field for the stock symbol
symbol_label = ctk.CTkLabel(root, text="Enter Ticker:", font=("Roboto", 12))
symbol_label.pack(pady=10)

symbol_entry = ctk.CTkEntry(root, font=("Roboto", 14))
symbol_entry.pack(pady=5)

date_frame_combo = ctk.CTkComboBox(root, state='readonly', values=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'ytd', 'max'])
date_frame_combo.set('1y')
date_frame_combo.pack()

# Button to trigger the stock check
check_button = ctk.CTkButton(root, text="Check Stock", font=("Roboto", 12), command=on_check_stock)
check_button.pack(pady=20)

# Settings button in the top-right corner
settings_button = ctk.CTkButton(root, text="⚙ Settings", font=("Roboto", 10), command=open_settings)
settings_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

# Run the application
root.mainloop()
