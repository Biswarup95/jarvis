import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
from PyQt5 import QtWidgets, QtGui, QtCore
import sys

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am JARVIS. How may I help you?")

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('biswarupkhatua95@gmail.com', 'bgmailk95')
    server.sendmail('biswarupkhatua95@gmail.com', to, content)
    server.close()

class JarvisApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(JarvisApp, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("JARVIS")
        self.setGeometry(100, 100, 400, 400)
        
        # Set the window background color to white
        self.setStyleSheet("background-color: white;")
        
        # Display microphone icon
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(150, 20, 100, 100))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.updateListeningState(False)

        # Display command options
        self.optionsLabel = QtWidgets.QLabel("Available commands:", self)
        self.optionsLabel.setGeometry(50, 140, 300, 30)
        self.optionsLabel.setStyleSheet("color: black;")  # Set text color to black

        # Set up QTextEdit to show the commands with white background and black text
        self.commandsDisplay = QtWidgets.QTextEdit(self)
        self.commandsDisplay.setGeometry(50, 180, 300, 150)
        self.commandsDisplay.setReadOnly(True)
        self.commandsDisplay.setStyleSheet("background-color: white; color: black;")
        self.commandsDisplay.setText(
            "Commands:\n"
            "- Wikipedia\n"
            "- Open YouTube\n"
            "- Open Google\n"
            "- Open Stack Overflow\n"
            "- Open ChatGPT\n"
            "- The time\n"
            "- Send Email\n"
            "- Quit"
        )

    def updateListeningState(self, listening):
        if listening:
            self.label.setPixmap(QtGui.QPixmap("microphone_icon.png").scaled(100, 100, QtCore.Qt.KeepAspectRatio))
        else:
            self.label.clear()

    def takeCommand(self):
        self.updateListeningState(True)
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        self.updateListeningState(False)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            print("Say that again please...")
            return "None"
        return query



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    jarvisApp = JarvisApp()
    jarvisApp.show()
    wishMe()

    while True:
        query = jarvisApp.takeCommand().lower()

        # Process the query
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'open chatgpt' in query:
            webbrowser.open("https://chat.openai.com/")
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir, the time is {strTime}")
        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = jarvisApp.takeCommand()
                to = "biswarupkhatua95@yahoo.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send the email.")
        elif 'quit' in query:
            speak("Goodbye!")
            jarvisApp.close()  # Close the main window
            break  # Exit the loop and close the application