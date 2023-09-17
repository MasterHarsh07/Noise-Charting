import tkinter as tk
from tkinter import *
import os
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Designing window for registration
 
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")
 
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_user).pack()



# Designing window for login 
 
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()



# Implementing event on register button
 
def register_user():
 
    username_info = username.get()
    password_info = password.get()
 
    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()
 
    username_entry.delete(0, END)
    password_entry.delete(0, END)
 
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
 
# Implementing event on login button 
 
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
 
    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()
 
        else:
            password_not_recognised()
 
    else:
        user_not_found()
 
# Designing popup for login success
 
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=new_login_success).pack()
    
 
# Designing popup for login invalid password
 
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
 
# Deleting popups
 
def new_login_success():
    global new_screen
    new_screen=Toplevel(login_success_screen)
    new_screen.title("Noise")
    new_screen.geometry("300x250")
    Button(new_screen,text="Measure Noise", height="2", width="30",command = noise).pack()
  
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
 

def noise():
    global new_screen1
    new_screen1=Toplevel(new_screen)
    new_screen1.title("Measurement and Results")
    new_screen1.geometry("300x250")

    var=StringVar()
    Label(new_screen1,textvariable=var).pack()
        
    duration = 10  # seconds
    fs = 44100  # sampling frequency
    recording = sd.rec(int(fs * duration), samplerate=fs, channels=1)
    sd.wait()

    # Convert the recording to a numpy array and calculate the frequency spectrum
    samples = recording.reshape(-1)
    freqs = np.fft.fftfreq(len(samples)) * fs
    complex_spectrum = np.fft.fft(samples)
    amplitude_spectrum = np.abs(complex_spectrum)

    # Find the dominant frequency by locating the peak in the amplitude spectrum
    dominant_freq_idx = np.argmax(amplitude_spectrum)
    dominant_freq = freqs[dominant_freq_idx]
    var.set(dominant_freq)
    # Calculate value for charts
    time=[1,2,3,4,5,6,7,8,9,10]
    freq=[]
    for i in range(0,10):
        freq.append(dominant_freq-i+6)

    # Set up email parameters
    sender_email = "d20z112@psgitech.ac.in"
    receiver_email = "harshavarthanpk@gmail.com"
    subject = "Alert Message"
    body = "you are under heavy noise zone."


    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    if dominant_freq > 500:
    #draw charts
        var.set(f"The dominant frequency is {dominant_freq:.2f} Hz.")
        Label(new_screen1,text="you are under Warning zone").pack()
        Label(new_screen1,text="Email sent...").pack()

    # Convert message to string and send via SMTP server
        text = message.as_string()
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, "yoze qhpu tfig mmbb")#use 2 step password verification here....
            smtp.sendmail(sender_email, receiver_email, text)
            smtp.quit()


    # Plot the power spectrum
        plt.bar(time,freq)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("duration (s)")
        plt.show()

    else:
        var.set(f"The dominant frequency is {dominant_freq:.2f} Hz.")
        Label(new_screen1,text="you are under Normal zone").pack()
        Label(new_screen1,text="Email Not sent...").pack()
        plt.bar(time,freq)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("duration (s)")
        plt.show()
    





# Designing Main(first) window
 
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()
 
    main_screen.mainloop()
 
 
main_account_screen()



















