"""Task that can perform my burp assistance:-
-according to wikipedia <query>
-exit
-open this site <query>
-search <query>
-play music or change music
-whats the time
-whats the date
-thank you
-what can you do for me
-how old are you
-tell me about yourself
-who created you
-say hello
-send email
-send cricket score
-reminder"""


"""library to be installed using pip
-pip install tkinter
-pip install pyttsx3
-pip install speechrecognition
-pip install pyaudio
-pip install wikipedia
-pip install requests"""


from tkinter import *                                   #python gui
import pyttsx3                                          #text to speech conversion library
import speech_recognition as sr                         #speech recognition library
import datetime                                         
import pyaudio                                          #the cross-platform audio I/O library
import wikipedia
import webbrowser
import os                                               #provide functions for interacting with os
#import vlc
import random
import smtplib                                          #SMTP server for sending email and routing email between mail server
#import cricketbot
import time
import requests                                         #make a request to a web page and print the response
from datetime import datetime as dt


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
en_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"              #give voice to speech
engine.setProperty('voice', en_voice_id)
#print(voices[0].id)
engine.setProperty('voices',voices[0].id)

window = Tk()

global var
global var1

var = StringVar()
var1 = StringVar()

def speak(audio):                    #speak the text
    engine.say(audio)
    engine.runAndWait()              #Runs an event loop until all commands queued up until this method call complete.
    
def wishMe():                        #function to wish the user
    hour=int(datetime.datetime.now().hour)
    if hour>=5 and hour<=12:
        var.set("Good Morning") 
        window.update()              #update gui frame
        speak("good morning")
    elif hour>=12 and hour<=18:
        var.set("Good Afternoon") 
        window.update()             #update gui frame
        speak("good afternoon")
    else:
        var.set("Good Evening") 
        window.update()             #update gui frame
        speak("good evening")
    speak("I am Burp, How may i help you")

def sendEmail(to, content):         #function to send mail through SMTP
    #f=open('words.txt','q')
    #content=f.read
    #print(content)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your email id', 'your password')
    server.sendmail('your email id', to, content)
    server.close()
    
class ScoreGet:                     #function to send cricket score to user
    def __init__(self):
        self.url_get_all_matches = "http://cricapi.com/api/matches"
        self.url_get_score="http://cricapi.com/api/cricketScore"
        self.api_key = "your crick api"     #get api from twilio
        self.unique_id = ""         # unique to every match

    def get_unique_id(self):
        uri_params = {"apikey": self.api_key}
        resp = requests.get(self.url_get_all_matches, params=uri_params)
        resp_dict = resp.json()     #print response in json format
        uid_found=0
        for i in resp_dict['matches']:
            if (i['team-1'] == "India" or i['team-2'] == "India" and i['matchStarted']):
                todays_date = dt.today().strftime('%Y-%m-%d')
                #todays_date = "2020-02-23"
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
        data=""                       #stores the cricket match data
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
    

def takeCommand():                      #take microphone input from user & return string as output
    r=sr.Recognizer()
    with sr.Microphone() as source:
        var.set("Listening...")
        window.update()                 #update gui frame
        print("Listening:")
        r.energy_threshold=300          # minimum audio energy to consider for recording
        r.pause_threshold=2             # seconds of non-speaking audio before a phrase is considered complete
        audio=r.listen(source) 
        
    try:
        var.set("Recognizing...")
        window.update()                                         #update gui frame
        print("Recognising.....")
        query=r.recognize_google(audio, language='en-in')       #using google speech recognition module
        print(f"User said is: {query}\n")
        
    except Exception as e:
        #print(e)
        var.set("Say that again please....")
        window.update()                                         #update gui frame
        print("Say that again please....")
        return "none"
    var1.set(query)
    window.update()                                             #update gui frame
    return query


def play():
    btn2['state'] = 'disabled'
    btn0['state'] = 'disabled'
    btn1.configure(bg = 'orange')
    wishMe()
    while True:
        btn1.configure(bg = 'orange')
        query = takeCommand().lower()       #convert any query to lowercase
        
        
        
        if 'wikipedia' in query:            #search in wikipedia
            speak('Searching wikipedia....')
            query=query.replace("according to wikipedia","")        #replacing some query with blank space before feeding again in the query
            #print(query)
            results=wikipedia.summary(query,sentences=2)
            speak("According to wikipedia")
            #print(results)
            var.set(results)
            window.update()                 #update gui frame
            speak(results)
            
            
            
        elif 'exit' in query:               #exit from loop
            #exit(1)
            btn1.configure(bg = '#5C85FB')
            btn2['state'] = 'normal'        #bring button to normal state
            btn0['state'] = 'normal'        #bring button to normal state
            window.update()                 #update gui frame
            speak("Bye sir")
            break
        
        
        
        elif "site" in query:               #open any site in google chrome
            query=query.replace("open this site ","")
            chrome_path="your chrome path including chrome.exe"
            webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)
            var.set('opening '+query)
            window.update()                 #update gui frame
            speak('opening '+query)
            c=webbrowser.get('chrome')
            c.open(query+".com")
            
            
        
        elif "search" in query:             #search any query in google chrome
            query=query.replace("search","")
            chrome_path="your chrome path including chrome.exe"
            webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)
            var.set('searching '+query)
            window.update()                 #update gui frame
            speak('searching '+query)
            c=webbrowser.get('chrome')
            c.open("https://www.google.com/search?q="+query+"&oq="+query+"&aqs=chrome.0.69i59j0l6j69i60.1376j0j9&sourceid=chrome&ie=UTF-8")
        
        
        
        elif ('play music' in query) or ('change music' in query):          #play music or change music from music library
            var.set('Here are your favorites')
            window.update()                                                 #update gui frame
            speak('Here are your favorites')
            music_dir = 'user music library path'                           #path of Music Library
            songs = os.listdir(music_dir)
            n = random.randint(0,0)                                         #choose random music from library
            os.startfile(os.path.join(music_dir, songs[n]))                 #play music

        
        
        elif 'the time' in query:                                           #give time in response`
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            var.set("Sir the time is %s" % strtime)
            window.update()                                                 #update gui frame
            speak("Sir the time is %s" %strtime)
        
        
        
        elif 'the date' in query:                                           #give date in response
            strdate = datetime.datetime.today().strftime("%d %m %y")
            var.set("Sir today's date is %s" %strdate)
            window.update()                                                 #update gui frame
            speak("Sir today's date is %s" %strdate) 
        
        
        
        elif 'thank you' in query:                                          #give some rsponse
            var.set("Welcome Sir")
            window.update()                                                 #update gui frame
            speak("Welcome Sir")
            
            

        elif 'what can you do for me' in query:
            var.set('I can do multiple tasks for you sir. Tell me whatever you want to perform sir')
            window.update()                                                 #update gui frame
            speak('I can do multiple tasks for you sir. tell me whatever you want to perform sir')



        elif 'old are you' in query:
            var.set("I was created on 8 April 2020 during the qurantine period. So, I am not so old enough to be mature")
            window.update()                                                 #update gui frame
            speak("I was created on 8 April 2020 during the qurantine period. So, I am not so old enough to be mature")
        
        
        
        elif 'tell me about yourself' in query:
            var.set("Myself Burp Sir. I am AI-Assistance made in python. I can perform various task as commanded by sir")
            window.update()                                                  #update gui frame
            speak('Myself Burp Sir. I am AI-Assistance made in python. I can perform various task as commanded by sir')



        elif 'who created you' in query:
            var.set('My Creator is User')
            window.update()                                                  #update gui frame
            speak('My Creator is User')



        elif 'say hello' in query:
            var.set('Hello Everyone! My self Burp, AI-Assistance in python')
            window.update()                                                   #update gui frame
            speak('Hello Everyone! My self Burp, AI-Assistance in python')



        elif 'send email' in query:                                     #send email to user
            try:
                var.set("What should I write")
                window.update()                                         #update gui frame
                speak('what should I write')
                content = takeCommand()
                speak("sending email to Deep")
                to = "email id in which you want to send email"
                sendEmail(to, content)
                var.set('Email has been sent!')
                window.update()                                         #update gui frame
                speak('Email has been sent!')

            except Exception as e:
                print(e)
                var.set("Sorry Sir! I was not able to send this email")
                window.update()                                         #update gui frame
                speak('Sorry Sir! I was not able to send this email')

            
            
        elif 'send cricket score' in query:                             #send cricket score in whatsapp
            #cricketbot.ScoreGet
            #cricketbot.
            try:
                match_obj=ScoreGet()
                send_message=match_obj.get_unique_id()
                print(send_message)
                from twilio.rest import Client
                account_sid = 'your account_sid'        #available from crickapi
                auth_token = 'your auth_token'          #available from crickapi
                client = Client(account_sid, auth_token)
                message = client.messages.create( body=send_message, from_='whatsapp:twilio number', to='whatsapp:your number with country code' )       #available from twilio and then whatsapp beta
                var.set("Score has been sent to yout WhatsApp") 
                window.update()                                         #update gui frame
                speak("Score has been sent to yout WhatsApp")
                
            except Exception as e:
                print(e)
                var.set("Sorry Sir! I was not able to send you cricket score")
                window.update()                                         #update gui frame
                speak('Sorry Sir! I was not able to send you cricket score')
            
        
        
        elif 'reminder' in query:                                       #gentle reminder to user
            var.set("What shall I remind you about")
            window.update()                                             #update gui frame
            speak("What shall I remind you about")
            rem=takeCommand()
            var.set("In how many minute")
            window.update()                                             #update gui frame
            speak("In how many minute")
            min=takeCommand()
            min=float(min)
            min=min*60
            time.sleep(min)                                             #put the function to sleep
            var.set("Reminder is: "+rem)
            window.update()                                             #update gui frame
            speak(rem)
             
def update(ind):            #update the frame in gui
    frame = frames[(ind)%100]
    ind += 1
    label.configure(image=frame)
    window.after(100, update, ind)


label2 = Label(window, textvariable = var1, bg = '#FAB60C')         #update the response in gui
label2.config(font=("Courier", 20))
var1.set('User Said:')
label2.pack()

label1 = Label(window, textvariable = var, bg = '#ADD8E6')          #update the response in gui
label1.config(font=("Courier", 20))
var.set('Welcome')
label1.pack()

frames = [PhotoImage(file='your gif file path',format = 'gif -index %i' %(i)) for i in range(100)]      #location of frame
window.title('BURP')                #tile of gui

label = Label(window, width = 500, height = 500)
label.pack()
window.after(0, update, 0)

btn0 = Button(text = 'WISH ME',width = 20, command = wishMe, bg = '#5C85FB')            #function and properties of button0 ,i.e, WISH ME
btn0.config(font=("Courier", 12))
btn0.pack()
btn1 = Button(text = 'PLAY',width = 20,command = play, bg = '#5C85FB')                  #function and properties of button1 ,i.e, PLAY
btn1.config(font=("Courier", 12))
btn1.pack()
btn2 = Button(text = 'EXIT',width = 20, command = window.destroy, bg = '#5C85FB')       #function and properties of button2 ,i.e, EXIT
btn2.config(font=("Courier", 12))
btn2.pack()


window.mainloop()               #running gui
