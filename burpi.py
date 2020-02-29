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
    speak("I am Burp! How may I help you?")
    
class ScoreGet:
    def __init__(self):
        self.url_get_all_matches = "http://cricapi.com/api/matches"
        self.url_get_score="http://cricapi.com/api/cricketScore"
        self.api_key = "your_api_key"       #get your api from cricapi.com
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
        print(f"User said is: {query}\n")
        
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
    server.login('your_email_id', 'your_password')
    server.sendmail('your_email_id', to, content)
    server.close()
    
    
    
if __name__ == "__main__":
    
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
            
        
        elif "site" in query:
            query=query.replace("open this site ","")
            chrome_path="path_where_your_chrome.exe_is_saved"
            webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)
            c=webbrowser.get('chrome')
            c.open(query+".com")
            
        
        elif "search" in query:
            query=query.replace("search","")
            chrome_path="path_where_your_chrome.exe_is_saved"
            webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)
            c=webbrowser.get('chrome')
            c.open("https://www.google.com/search?q="+query+"&oq="+query+"&aqs=chrome.0.69i59j0l6j69i60.1376j0j9&sourceid=chrome&ie=UTF-8") #this query may change in future
            
        elif "play" in query:
            music_dir="path_where_all_your_songs_are saved(till_the_folder_not files)"
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[0]))  #you can use random function for playing random songs
            
        elif "time" in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            
        elif "open" in query:
            programpath="path_of_your_app.exe_which_you_want_to_open"
            os.startfile(programpath)
            
        elif 'send email' in query:
            try:
                speak("What should I write?")
                content = takeCommand()
                to = "receiver's_email_address"    #sometimes mail is marked as spam
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
            account_sid = 'your_account_sid_from_crickapi_profile'
            auth_token = 'your_auth_token_from_crickapi_profile'
            client = Client(account_sid, auth_token)
            message = client.messages.create( body=send_message, from_='whatsapp:number_saved_while_you_use_twilio_api_for whatsapp_bot', to='whatsapp:your_number_with_country_code' )
            
        elif 'reminder' in query:
            speak("What shall I remind you about")
            rem=takeCommand()
            speak("In how many minute")
            min=takeCommand()
            min=float(min)
            min=min*60
            time.sleep(min)
            speak(rem)

            
