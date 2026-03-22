import os
import tkinter as tk
from tkinter import messagebox

def speak_text():
    text = text_box.get("1.0", tk.END).strip()  # Get text and remove extra spaces
    if text:
        os.system(f'espeak "{text}"')  # Use espeak for Linux
    else:
        messagebox.showwarning("Input Error", "Please enter some text to speak!")

# Create GUI Window
window = tk.Tk()
window.title("Text to Speech (Linux)")

# Label
label = tk.Label(window, text="Enter text to speak:")
label.pack(pady=10)

# Text Box
text_box = tk.Text(window, height=10, width=40)
text_box.pack(pady=10)

# Speak Button
speak_button = tk.Button(window, text="Speak", command=speak_text)
speak_button.pack(pady=10)

# Run GUI
window.mainloop()
