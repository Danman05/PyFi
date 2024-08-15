from tkinter import Toplevel, messagebox
import customtkinter as ctk

def open_settings(root, evaluator):
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x600")
    settings_window.configure(bg="#121212")
    
    def update_thresholds():
        evaluator.set_threshold("rsi_threshold", rsi_slider.get())
        evaluator.set_threshold("quick_ratio_threshold", quick_slider.get())
        evaluator.set_threshold("current_ratio_threshold", current_slider.get())
        evaluator.set_threshold("pe_ratio_threshold", pe_slider.get())

    def reset_thresholds():
        evaluator.set_default_threshold()
        pe_slider.set(evaluator.get_threshold(key='pe_ratio_threshold'))
        rsi_slider.set(evaluator.get_threshold(key='rsi_threshold'))
        quick_slider.set(evaluator.get_threshold(key='quick_ratio_threshold'))
        current_slider.set(evaluator.get_threshold(key='current_ratio_threshold'))
        update_label(pe_label, pe_slider)
        update_label(rsi_label, rsi_slider)
        update_label(quick_label, quick_slider)
        update_label(current_label, current_slider)

    # Function to update slider labels
    def update_label(label, slider):
        label.configure(text=f"{slider.get():.2f}")

    # PE Ratio Slider
    ctk.CTkLabel(settings_window, text="PE Ratio Threshold", bg_color="#121212").pack(pady=10)
    pe_slider = ctk.CTkSlider(settings_window, from_=5, to=50)
    pe_slider.set(evaluator.get_threshold(key='pe_ratio_threshold'))
    pe_slider.pack()
    pe_label = ctk.CTkLabel(settings_window, text=f"{pe_slider.get():.2f}", bg_color="#121212")
    pe_label.pack(pady=5)
    pe_slider.configure(command=lambda value: update_label(pe_label, pe_slider))

    # RSI Slider
    ctk.CTkLabel(settings_window, text="RSI Threshold", bg_color="#121212").pack(pady=10)
    rsi_slider = ctk.CTkSlider(settings_window, from_=10, to=70)
    rsi_slider.set(evaluator.get_threshold(key="rsi_threshold"))
    rsi_slider.pack()
    rsi_label = ctk.CTkLabel(settings_window, text=f"{rsi_slider.get():.2f}", bg_color="#121212")
    rsi_label.pack(pady=5)
    rsi_slider.configure(command=lambda value: update_label(rsi_label, rsi_slider))

    # Quick Ratio Slider
    ctk.CTkLabel(settings_window, text="Quick Ratio Threshold", bg_color="#121212").pack(pady=10)
    quick_slider = ctk.CTkSlider(settings_window, from_=0.5, to=3.0, number_of_steps=25)
    quick_slider.set(evaluator.get_threshold(key="quick_ratio_threshold"))
    quick_slider.pack()
    quick_label = ctk.CTkLabel(settings_window, text=f"{quick_slider.get():.2f}", bg_color="#121212")
    quick_label.pack(pady=5)
    quick_slider.configure(command=lambda value: update_label(quick_label, quick_slider))

    # Current Ratio Slider
    ctk.CTkLabel(settings_window, text="Current Ratio Threshold", bg_color="#121212").pack(pady=10)
    current_slider = ctk.CTkSlider(settings_window, from_=0.5, to=3.0, number_of_steps=25)
    current_slider.set(evaluator.get_threshold(key="current_ratio_threshold"))
    current_slider.pack()
    current_label = ctk.CTkLabel(settings_window, text=f"{current_slider.get():.2f}", bg_color="#121212")
    current_label.pack(pady=5)
    current_slider.configure(command=lambda value: update_label(current_label, current_slider))
    # Update Button
    ctk.CTkButton(settings_window, text="Update Thresholds", command=update_thresholds).pack(pady=20)
        # Update Button
    ctk.CTkButton(settings_window, text="Reset to defaults", command=reset_thresholds).pack(pady=20)
