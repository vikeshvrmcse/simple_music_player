import customtkinter as ctk
from PIL import Image
from pygame import mixer
import os
import pygame
from tkinter import filedialog, Listbox, END, PhotoImage
from mutagen.mp3 import MP3

# Initialize pygame mixer
mixer.init()

# Application configurations
background_color = "white"
app_name = "Music Player"
app_initial_size = "1000x650+300x300"

# Initialize the main application window
root = ctk.CTk()
root.geometry(app_initial_size)
root.configure(fg_color=background_color)
root.title(app_name)

# Variables
ganas = []
current_song_index = 0
paused = False

# Load music from a directory
def load_music():
    global ganas
    ganas = []  # Clear previous songs list
    root.directory = filedialog.askdirectory()

    for file in os.listdir(root.directory):
        if file.endswith(".mp3"):
            ganas.append(file)
    
    playlist.delete(0, END)  # Clear previous playlist entries
    for song in ganas:
        playlist.insert(END, song)
        
song_length=0

def get_song_length(song_path):
    audio = MP3(song_path)
    return audio.info.length

# Play or resume music
def play_music():
    global current_song, paused
    if ganas:
        if paused:
            pygame.mixer.music.unpause()
            paused = False
        else:
            song_index = playlist.curselection()
            if song_index:
                current_song = ganas[song_index[0]]
                song_path = os.path.join(root.directory, current_song)
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()
                song_length = get_song_length(song_path)
                slider.configure(to=song_length)
                paused = False
                update_slider_position()



# Pause music
def pause_music():
    global paused
    if not paused:
        mixer.music.pause()
        paused = True

# Stop music
def stop_music():
    global paused
    mixer.music.stop()
    paused = False

# Play next song
def next_music():
    global current_song_index, paused
    if ganas:
        current_song_index = (current_song_index + 1) % len(ganas)
        playlist.selection_clear(0, END)
        playlist.selection_set(current_song_index)
        play_music()

# Play previous song
def prev_music():
    global current_song_index, paused
    if ganas:
        current_song_index = (current_song_index - 1) % len(ganas)
        playlist.selection_clear(0, END)
        playlist.selection_set(current_song_index)
        play_music()

def update_slider_position():
    if pygame.mixer.music.get_busy():
        position = pygame.mixer.music.get_pos() / 1000  # Current position in seconds
        slider.set(position)
        root.after(1000, update_slider_position)

# Seek playback position when slider is moved
def on_slider_move(value):
    pygame.mixer.music.set_pos(float(value))


label = ctk.CTkLabel(root, text="Welcome to the Music Player", font=("arial", 30, "italic"))
label.pack(pady=20)

# UI Elements
songs_dir_button = ctk.CTkButton(root, text="Select Songs Folder", font=("arial", 25, "bold"), height=50, command=load_music)
songs_dir_button.pack(padx=(10, 10), fill="x")

songs_frame = ctk.CTkFrame(root)
songs_frame.pack(fill="both", padx=(10, 10), pady=(10, 10))

# Standard tkinter Listbox within a customtkinter frame
playlist = Listbox(songs_frame, bg="lightgray", fg="black", selectbackground="blue", font=("Arial", 14), width=50, height=15)
playlist.pack(pady=(10, 10), padx=(10, 10), fill="both")

# Load images for buttons
play_image = ctk.CTkImage(Image.open("icons/play.png"), size=(50, 50))
pause_image = ctk.CTkImage(Image.open("icons/pause.png"), size=(50, 50))
stop_image = ctk.CTkImage(Image.open("icons/stop.png"), size=(50, 50))
previous_image = ctk.CTkImage(Image.open("icons/previous.png"), size=(50, 50))
next_image = ctk.CTkImage(Image.open("icons/next.png"), size=(50, 50))

# Button frame
button_frame = ctk.CTkFrame(root)
button_frame.pack(padx=(10, 10), pady=(10, 10), fill="x")

# Configure grid columns to expand equally
button_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

# Control buttons

play_button = ctk.CTkButton(button_frame, image=play_image, command=play_music, corner_radius=20, text="", fg_color="transparent", hover_color="white")
play_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

pause_button = ctk.CTkButton(button_frame, image=pause_image, command=pause_music, corner_radius=20,text="", fg_color="transparent", hover_color="white")
pause_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew", )

stop_button = ctk.CTkButton(button_frame, image=stop_image, command=stop_music, corner_radius=20, text="", fg_color="transparent", hover_color="white")
stop_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

previous_button = ctk.CTkButton(button_frame, image=previous_image, command=prev_music, corner_radius=20, text="", fg_color="transparent", hover_color="white")
previous_button.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

next_button = ctk.CTkButton(button_frame, image=next_image, command=next_music, corner_radius=20, text="", fg_color="transparent", hover_color="white")
next_button.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

# Playback Position Slider
slider = ctk.CTkSlider(root, from_=0, to=100, command=on_slider_move)
slider.pack(pady=(10, 5), padx=(10, 10), fill="x")


root.after(201, lambda :root.iconbitmap('icons/folder-music.ico'))

# Main loop
root.mainloop()
