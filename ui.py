import customtkinter
import pyperclip
from tkinter import filedialog, messagebox

from spotify_api import get_all_spotify_tracks
from youtube_api import search_youtube, download_mp3


# Window dimensions
window_width = 700
window_height = 700
group_spacing = 20
version = "1.0"


customtkinter.set_appearance_mode("dark") # Theme
# customtkinter.set_default_color_theme("./spotify_theme.json")
app = customtkinter.CTk()
app.title("Spoti3 - " + version) 
app.geometry(f"{window_width}x{window_height}")
app.resizable(False, True)  # Disable both horizontal and vertical resizing


is_fetched = False
music_list = []
download_path = "spoti3_downloads/"


# Paste url into playlist url entry field
def paste_url():
    s = pyperclip.paste()
    pyperclip.copy(s)

    if(s != ""):
        playlist_url_entry.delete(0, "end")
        playlist_url_entry.insert(0, s)


def clear_scrollbox():
    for widget in scrollable_frame.winfo_children():  # Iterate over all children widgets
                    widget.destroy()  # Destroy each widget

def add_to_scrollbox(text, color=None):
    label = customtkinter.CTkLabel(scrollable_frame, text=text, width=window_width, anchor="w", font=("Arial", 16), fg_color=color)
    label.pack(padx=20, pady=(0, 0))



def fetch_download_tracks():
    global is_fetched  # Declare as global to modify the value
    global music_list  # Declare locally

    if is_fetched:
        if not music_list:
            messagebox.showwarning("No Tracks Fetched", "No tracks fetched to download. Please fetch tracks again.")
            is_fetched = False
            fetch_download_button.configure(text="Fetch Tracks From Playlist")
            return

        prompt_before_download = prompt_download_checkbox.get() == "yes"  # Check if prompt before download is enabled
        clear_scrollbox()

        for music in music_list:
            url, title, duration = search_youtube(music['title'], music['artist'])
            if url is None:
                add_to_scrollbox(f"[ERROR]{music['title']} ({music['artist']}) | Skipping...")
                continue

            if prompt_before_download:
                user_choice = messagebox.askyesno("Download Confirmation", f"Do you want to download {title} of length {duration} minutes")
                if not user_choice:
                    continue

            add_to_scrollbox(f"DOWNLOADING: {title}")
            filename = f"{music['title']} ({music['artist']}).mp3"
            success, message = download_mp3(url, download_path, filename)

            if success:
                add_to_scrollbox(f" [SUCCESS] {filename}", color="green")
                add_to_scrollbox("")
            else:
                add_to_scrollbox(f" [FAILED]  {filename}", color="red")
                add_to_scrollbox("")
        
        messagebox.showinfo("Downloads Complete!", "Your Downloads are complete!")
        is_fetched = False
        fetch_download_button.configure(text="Fetch Tracks From Playlist")

    else:
        playlist_url = playlist_url_entry.get().strip()
        if not playlist_url:
            messagebox.showwarning("Input Error", "Please enter a valid Spotify playlist URL.")
            return

        clear_scrollbox()

        music_list = get_all_spotify_tracks(playlist_url)

        if music_list:
            add_to_scrollbox(f"Found {len(music_list)} tracks in playlist")
            for count, track in enumerate(music_list):
                add_to_scrollbox(f"{count+1}.  {track['title']} ({track['artist']})")
            is_fetched = True
            fetch_download_button.configure(text="Download Tracks")
        else:
            messagebox.showinfo("No Tracks", "No tracks found in this playlist.")


# Function to open the folder picker dialog and display the selected folder path
def pick_folder():
    global download_path

    folder_path = filedialog.askdirectory()  # Open folder picker dialog
    if folder_path:  # If a folder is selected
        download_folder_entry.configure(state="normal")
        download_folder_entry.delete(0, "end")
        download_folder_entry.insert(0, folder_path)  # Display the folder path
        download_folder_entry.configure(state="disabled")
        download_path = folder_path


# Enter Spotify playlist URL
playlist_url_label = customtkinter.CTkLabel(app, text="Playlist URL:", fg_color="transparent", font=("Arial", 16, "bold"), anchor="w", width=window_width)
playlist_url_label.pack(padx=20, pady=(group_spacing, 5))

playlist_url_entry = customtkinter.CTkEntry(app, placeholder_text="Enter Spotify playlist URL", width=window_width, height=50, font=("Arial", 16), corner_radius=0)
playlist_url_entry.pack(padx=20, pady=(0, 5))

paste_url_button = customtkinter.CTkButton(app, text="Paste Clipboard", command=paste_url, width=window_width, height=35, font=("Arial", 16, "bold"), corner_radius=0, fg_color="grey")
paste_url_button.pack(padx=20, pady=(0, group_spacing))

# Pick Tracks Download Folder
download_folder_label = customtkinter.CTkLabel(app, text="Tracks Download Folder:", fg_color="transparent", font=("Arial", 16, "bold"), anchor="w", width=window_width)
download_folder_label.pack(padx=20, pady=(0, 5))

download_folder_entry = customtkinter.CTkEntry(app, placeholder_text="./Download_mp3", width=window_width, height=50, font=("Arial", 16), corner_radius=0)
download_folder_entry.insert(0, download_path)
download_folder_entry.configure(state="disabled")
download_folder_entry.pack(padx=20, pady=(0, 5))

pick_download_folder_button = customtkinter.CTkButton(app, text="Pick Download Folder", command=pick_folder, width=window_width, height=35, font=("Arial", 16, "bold"), corner_radius=0)
pick_download_folder_button.pack(padx=20, pady=(0, group_spacing))

# Track list display scrollable frame
scrollable_frame = customtkinter.CTkScrollableFrame(app, width=window_width, corner_radius=0)
scrollable_frame.pack(padx=20, pady=(0, group_spacing), fill="both", expand=True)

welcome_text = [
    "",
    "[+]  Welcome to Spoti3!",
    "[+]  An open-source Spotify downloader.",
    "[+]  Created by https://github.com/0x902",
    "[+]  Download Spotify music easily.",
    "[+]  Free, simple, and fast!"
]

for text in welcome_text:
    add_to_scrollbox(text)

prompt_download = customtkinter.StringVar(value="yes")
prompt_download_checkbox = customtkinter.CTkCheckBox(app, text="Prompt before each track",  variable=prompt_download, onvalue="yes", offvalue="no", corner_radius=0, font=("Arial", 16))
prompt_download_checkbox.pack(padx=20, pady=(0, group_spacing))

fetch_download_button = customtkinter.CTkButton(app, text="Fetch Tracks From Playlist", command=fetch_download_tracks, width=window_width, height=50, font=("Arial", 18), corner_radius=0)
fetch_download_button.pack(padx=20, pady=(0, group_spacing))

app.mainloop()
