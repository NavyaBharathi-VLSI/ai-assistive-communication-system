import os
import speech_recognition as sr
from PIL import Image, ImageTk
import tkinter as tk

# Tkinter setup for GIF
root = tk.Tk()  # For GIF images
root.title("GIF Animation")  # For GIF images

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 2
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)
    except Exception as e:
        print(e)
        return "None"

    if query.lower() == "sorry":
        gif_image = Image.open("./sorry.gif")
        gif_tk = ImageTk.PhotoImage(gif_image)
        label = tk.Label(root, image=gif_tk)
        label.pack()

        def update_gif_frame(frame_index):
            try:
                # Set the next frame
                gif_image.seek(frame_index)
                gif_tk = ImageTk.PhotoImage(gif_image)
                label.configure(image=gif_tk)
                label.image = gif_tk
                # Schedule the next frame update
                root.after(100, update_gif_frame, (frame_index + 1) % gif_image.n_frames)
            except EOFError:
                # Once the GIF ends, restart from the first frame
                update_gif_frame(0)

        update_gif_frame(0)
        root.mainloop()

    elif query.lower() == "thanks":
        gif_image = Image.open("./thankyou.gif")
        gif_tk = ImageTk.PhotoImage(gif_image)
        label = tk.Label(root, image=gif_tk)
        label.pack()

        def update_gif_frame(frame_index):
            try:
                # Set the next frame
                gif_image.seek(frame_index)
                gif_tk = ImageTk.PhotoImage(gif_image)
                label.configure(image=gif_tk)
                label.image = gif_tk
                # Schedule the next frame update
                root.after(100, update_gif_frame, (frame_index + 1) % gif_image.n_frames)
            except EOFError:
                # Once the GIF ends, restart from the first frame
                update_gif_frame(0)

        update_gif_frame(0)
        root.mainloop()

    elif query.lower() == "nice to meet you":
        gif_image = Image.open("./nice to meet you.gif")
        gif_tk = ImageTk.PhotoImage(gif_image)
        label = tk.Label(root, image=gif_tk)
        label.pack()

        def update_gif_frame(frame_index):
            try:
                # Set the next frame
                gif_image.seek(frame_index)
                gif_tk = ImageTk.PhotoImage(gif_image)
                label.configure(image=gif_tk)
                label.image = gif_tk
                # Schedule the next frame update
                root.after(100, update_gif_frame, (frame_index + 1) % gif_image.n_frames)
            except EOFError:
                # Once the GIF ends, restart from the first frame
                update_gif_frame(0)

        update_gif_frame(0)
        root.mainloop()

    elif query.lower() == "how do you do":
        gif_image = Image.open("./howdoyoudo.gif")
        gif_tk = ImageTk.PhotoImage(gif_image)
        label = tk.Label(root, image=gif_tk)
        label.pack()

        def update_gif_frame(frame_index):
            try:
                # Set the next frame
                gif_image.seek(frame_index)
                gif_tk = ImageTk.PhotoImage(gif_image)
                label.configure(image=gif_tk)
                label.image = gif_tk
                # Schedule the next frame update
                root.after(100, update_gif_frame, (frame_index + 1) % gif_image.n_frames)
            except EOFError:
                # Once the GIF ends, restart from the first frame
                update_gif_frame(0)

        update_gif_frame(0)
        root.mainloop()

    return query

takeCommand()
