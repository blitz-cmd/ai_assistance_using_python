import pyttsx3
import speech_recognition as sr
import datetime
import pyaudio
import wikipedia
import webbrowser
import os
import vlc
import random
import smtplib
import cricketbot
import time
import requests
from datetime import datetime as dt




engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
en_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice', en_voice_id)
#print(voices[0].id)
engine.setProperty('voices',voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("good morning")
    elif hour>=12 and hour<=18:
        speak("good afternoon")
    else:
        speak("good evening")
    speak("I am Burp, Deep's assistance! how may i help you")
    
class ScoreGet:
    def __init__(self):
        self.url_get_all_matches = "http://cricapi.com/api/matches"
        self.url_get_score="http://cricapi.com/api/cricketScore"
        self.api_key = "DBVIPRw2ehNE67A3CjTcwLcBWt92"
        self.unique_id = ""  # unique to every match

    def get_unique_id(self):
        uri_params = {"apikey": self.api_key}
        resp = requests.get(self.url_get_all_matches, params=uri_params)
        resp_dict = resp.json()
        uid_found=0
        for i in resp_dict['matches']:
            if (i['team-1'] == "India" or i['team-2'] == "India" and i['matchStarted']):
                #todays_date = dt.today().strftime('%Y-%m-%d')
                todays_date = "2020-02-23"
                if todays_date == i['date'].split("T")[0]:
                    uid_found=1
                    self.unique_id=i['unique_id']
                    print(self.unique_id)
                    break
        if not uid_found:
            self.unique_id=-1

        send_data=self.get_score(self.unique_id)
        return send_data
    
    def get_score(self,unique_id):
        data="" #stores the cricket match data
        if unique_id == -1:
            data="No India matches today"
        else:
            uri_params = {"apikey": self.api_key, "unique_id": self.unique_id}
            resp=requests.get(self.url_get_score,params=uri_params)
            data_json=resp.json()
            #print(data_json)
            try:
                data="Here's the score : "+ "\n" + data_json['stat'] +'\n' + data_json['score']
            except KeyError as e:
                data="Something went wrong"
        return data
    
def takeCommand():
    #take microphone input from user & return string as output
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening:")
        r.pause_threshold=1
        audio=r.listen(source) 
        
    try:
        print("Recognising.....")
        query=r.recognize_google(audio, language='en-in')
        print(f"Deep said is: {query}\n")
        
    except Exception as e:
        #print(e)
        print("Say that again please....")
        return "none"
    return query

def sendEmail(to, content):
    #f=open('words.txt','q')
    #content=f.read
    #print(content)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('srfrter133@gmail.com', 'qwerty1234@')
    server.sendmail('srfrter133@gmail.com', to, content)
    server.close()
    
    
    
if __name__ == "__main__":
    #speak("deep is hacker")
    wishMe()
    while True:
        query=takeCommand().lower()
        #logic for executing task based on query
        
        
        if 'wikipedia' in query:
            speak('Searching wikipedia....')
            query=query.replace("according to wikipedia","")
            print(query)
            results=wikipedia.summary(query,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
            
        
        #elif "open youtube" in query:
        #   chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        #   webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)
        #   c=webbrowser.get('chrome')
        #   c.open("youtube.com")
        
        
        elif "site" in query:
            query=query.replace("open this site ","")
            chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)
            c=webbrowser.get('chrome')
            c.open(query+".com")
            
        
        elif "search" in query:
            query=query.replace("search","")
            chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)
            c=webbrowser.get('chrome')
            c.open("https://www.google.com/search?q="+query+"&oq="+query+"&aqs=chrome.0.69i59j0l6j69i60.1376j0j9&sourceid=chrome&ie=UTF-8")
            
        elif "play" in query:
            music_dir="C:\\Users\\deepd\\OneDrive\\Music"
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[0]))
            
        elif "time" in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            
        elif "open" in query:
            programpath="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(programpath)
            
        elif 'send email' in query:
            try:
                speak("What should I write?")
                content = takeCommand()
                to = "dj.debnath2000@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry not able to send message!!")
                
        elif 'exit' in query:
            exit(1)
            
        elif 'send cricket' in query:
            #cricketbot.ScoreGet
            #cricketbot.
            match_obj=ScoreGet()
            send_message=match_obj.get_unique_id()
            print(send_message)
            from twilio.rest import Client
            account_sid = 'ACd0fc68caca0a695fc4d5d14097d851bb'
            auth_token = '7ef13652edbfb44a66b36ee70a32bc31'
            client = Client(account_sid, auth_token)
            message = client.messages.create( body=send_message, from_='whatsapp:+14155238886', to='whatsapp:+919967926830' )
            
        elif 'reminder' in query:
            speak("What shall I remind you about")
            rem=takeCommand()
            speak("In how many minute")
            min=takeCommand()
            min=float(min)
            min=min*60
            time.sleep(min)
            speak(rem)

            