import socket
import pyaudio
import tkinter as tk
import threading 
import os
from tkinter import filedialog

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
HOST = '127.0.0.1' # Change this to the IP address or hostname of the server
PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def choose_file():
    file_path = filedialog.askopenfilename()
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(tk.END, file_path)


def send_file():
    file_path = entry_file_path.get()
    if not file_path:
        tk.messagebox.showerror("Error", "Please choose a file to send.")
        return

    try:
        # Define the server address and port
        SERVER_ADDRESS = '127.0.0.1'  # localhost
        SERVER_PORT = 12345

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

        # Get the file name from the file path
        file_name = os.path.basename(file_path)

        # Send the file name and file size to the server
        file_size = os.path.getsize(file_path)
        client_socket.send(f"{file_name}|{file_size}".encode())

        # Open the file and send file data to the server in chunks
        with open(file_path, 'rb') as file:
            while file_size > 0:
                data = file.read(1024)
                client_socket.send(data)
                file_size -= len(data)

        print("File sent successfully.")
        print(f"file sent to {client_socket}")
        # Close the socket
        client_socket.close()

    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to send file: {e}")



# Create an instance of PyAudio
p = pyaudio.PyAudio()

# Open a streaming stream as output
stream_out = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

# Function to stop the client
def stop_client():
    client_socket.close()
    p.terminate()
    root.quit()

# Function to handle audio playback from the server
def play_audio():
    while True:
        data = client_socket.recv(CHUNK)
        stream_out.write(data)

# Create a GUI window
root = tk.Tk()
root.title("Audio Client")

# Add a label
label = tk.Label(root, text="CLIENT", font=("Helvetica", 16))
label.pack(pady=20)

# Create file path entry
entry_file_path = tk.Entry(root, width=50)
entry_file_path.pack(pady=10)

 

# Create buttons for choosing file and sending file
btn_choose_file = tk.Button(root, text="Choose File", command=choose_file)
btn_choose_file.pack()
btn_send_file = tk.Button(root, text="Send File", command=send_file)
btn_send_file.pack(pady=10)

# Create buttons for choosing audio and playing audio
# btn_browse_audio = tk.Button(root, text="Browse Audio", command=browse_audio)
# btn_browse_audio.pack()
# btn_play_audio = tk.Button(root, text="Play Audio", command=play_audio)
# btn_play_audio.pack(pady=10)



# Add a button to stop the client
stop_button = tk.Button(root, text="Stop Client", font=("Helvetica", 14), command=stop_client)
stop_button.pack()

# Start audio playback thread
audio_thread = threading.Thread(target=play_audio)
audio_thread.start()

# Start the GUI event loop
root.mainloop()
