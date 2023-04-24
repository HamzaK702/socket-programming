import socket
import threading
import tkinter as tk
from tkinter import filedialog
import pyaudio
import wave
import os

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
HOST = '127.0.0.1' # Change this to the IP address or hostname of the server
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server is listening on {HOST}:{PORT}")

# List to store connected client sockets
client_sockets = []

# Create an instance of PyAudio
p = pyaudio.PyAudio()

# Function to play audio from a file
def play_audio(filename):
    wf = wave.open(filename, 'rb')
    stream_out = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)
    data = wf.readframes(CHUNK)
    while data:
        for client_socket in client_sockets:
            client_socket.sendall(data)
        data = wf.readframes(CHUNK)
    stream_out.stop_stream()
    stream_out.close()

# Function to stop the server
def stop_server():
    for client_socket in client_sockets:
        client_socket.close()
    server_socket.close()
    p.terminate()
    root.quit()

# Function to handle client connections
def handle_clients():
    while True:
        client_socket, client_addr = server_socket.accept()
        client_sockets.append(client_socket)
        print(f"Connection from {client_addr} established.")
        

# def broadcast():
#     client_thread = threading.Thread(target=play_audio(), args="filename.wav")
#     client_thread.start()
    
         # Receive the file name and file size from the client
         # if not file_name.endswith(".mp3"):
 
        while True:
            client_socket, client_addr = server_socket.accept()
            client_sockets.append(client_socket)

            file_info = client_socket.recv(1024).decode()
            file_name, file_size = file_info.split('|')

    # Convert file size to integer
            file_size = int(file_size)

    # Create a new file to write the received data
            with open(file_name, 'wb') as file:
        # Loop to receive file data in chunks
             while file_size > 0:
                data = client_socket.recv(1024)
                file.write(data)
                file_size -= len(data)

            print(f"File '{file_name}' received and saved successfully.")
 

# Create a GUI window
root = tk.Tk()
root.title("Audio Server")

# Add a label
label = tk.Label(root, text="Select an audio file to play:", font=("Helvetica", 16))
label.pack(pady=20)

# Function to open file dialog and select a file
def select_file():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File", filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
    print(f"{filename} selected for broadcasting")
    if filename:
        play_audio(filename)
            



# Add a button to select a file
select_button = tk.Button(root, text="Select Audio to broadcast", font=("Helvetica", 14), command=select_file)
select_button.pack()


# broadcast_button = tk.Button(root, text="Receive File", font=("Helvetica", 14), command=receive_file)
# broadcast_button.pack()
# Add a button to stop the server
stop_button = tk.Button(root, text="Stop Server", font=("Helvetica", 14), command=stop_server)
stop_button.pack()



# Start client handling thread
client_thread = threading.Thread(target=handle_clients)
client_thread.start()

# Start the GUI event loop
root.mainloop()
