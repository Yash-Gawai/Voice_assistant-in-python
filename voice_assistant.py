import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import requests
from bs4 import BeautifulSoup
import datetime

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")

engine.setProperty("voice", voices[1].id)  # 1 for female and 0 for male voice


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def take_command(): # Function is called wherever user input in the form of speech is to be taken
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print("User said: {} \n".format(query))
    except Exception as e:
        print(e)
        speak("I didn't understand")
        return "None"
    return query

def name():
    speak("Hello! I am your assistant....")
    speak("What should I call you as?")
    user_name = take_command()
    speak("Welcome {}".format(user_name))

def wishing():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Good Morning!")
    elif hour>= 12 and hour<15:
        speak("Good Afternoon!")  
    else:
        speak("Good Evening!") 
    speak("How can I help you?")


class WordMeanings:
    def finding_meaning(self,query): # To search the website for the queried word
        query = query.split(" ")
        word_to_search = query[-1]
        scrape_url = "https://www.oxfordlearnersdictionaries.com/definition/english/" + word_to_search
        headers = {"User-Agent": ""}
        web_response = requests.get(scrape_url, headers=headers)
        if web_response.status_code == 200:
            soup = BeautifulSoup(web_response.text, "html.parser")
            try:
                self.show_origin(soup)
                self.show_definitions(soup)
            except AttributeError:
                speak("Word not found!!")
        else:
            speak("Failed to get response...")

    def show_origin(self,soup): # To print out the origin of the queried word
        try:
            origin = soup.find("span", {"unbox": "wordorigin"})
            print("Origin: ",origin.text)
        except AttributeError:
            pass

    def show_definitions(self,soup): # To fidn the definition of the queried word
        senses = soup.find_all("li", class_="sense")
        speak("Here's one meaning of the word per the oxford dictionary")
        count = 1
        for s in senses:
            definition = s.find("span", class_="def").text
            if count == 1:
                speak(definition)
                count+=1
            # Examples
                examples = s.find_all("ul", class_="examples") # Returns a sentence using the queried word
                for e in examples:
                    for ex in e.find_all("li"):
                        if count == 2:
                            speak("Here's an example for you....")
                            speak(ex.text)
                            count+=1
            else:
                speak("Printing a few other meanings....") # Prints meaning of the word of more than one is present
                print(definition)
                count+=1
                if count >= 5:
                    break


def weather_getter():
    api_key = "you api key here" # API key can be found by signing in to the webite and putting it here
    speak("Tell me the name of the city...")
    city_name = take_command()
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={api_key}" # To find the coordinated of the location
    response = requests.get(geo_url)
    abc = response.json()
    if abc:
        lat = abc[0]["lat"]
        lon = abc[0]["lon"]
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}" # To search for the info using the coordinates
        resp = requests.get(weather_url)
        x = resp.json()
        y = x["main"]
        current_temperature = int(y["temp"]) - 273.13 # To conver the temperature to Celcius
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        speak("{} is having {} right now with a temperature of {:.2f} degree Celcius. Humidity is at {} percent".format(city_name,weather_description,current_temperature,current_humidiy))
    else:
        speak("City not found")

def time_getter():
    time_now = str(datetime.datetime.now()).split(" ") 
    a = time_now[1][0:5] # Remove the date and only keep the time
    d = datetime.datetime.strptime(a, "%H:%M")
    s = d.strftime("%I:%M %p") # Converts the time from 24 hour to 12 hour format
    hh = s[0:2].lstrip("0") # Removes and preceeding zeros
    mm = s[3:]
    speak(f"The current time is {hh} {mm}") # Tells the time in 12-hour format, eg 2:34 PM


if __name__ == "__main__":
    name()
    wishing()
    while True:
        query = take_command().lower()
        if "meaning of" in query:
            speak("Searching for the meaning...")
            WordMeanings().finding_meaning(query)            
        elif "are you" in query:
            speak("I'm a voice assistant. No name for now.")
        elif "Open youtube" in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")
        elif "google " in query:
            speak("Searching google")
            search_term = query.split(" ")
            webbrowser.open("https://www.google.com/search?q="+search_term[-1])
        elif "open github" in query:
            speak("opening github")
            webbrowser.open("github.com")
        elif "open stackoverflow" in query:
            speak("opening stackoverflow")
            webbrowser.open("stackoverflow.com")
        elif "weather" in query:
            weather_getter()
        elif "open spotify" in query:
            speak("opening spotify")
            webbrowser.open("spotify.com")
        elif "time now" in query:
            time_getter()
        elif "play music" in query:
            speak("opening music")
            webbrowser.open("spotify.com")
        elif "local disk d" in query:
            speak("opening local disk D")
            webbrowser.open("D://")
        elif "local disk c" in query:
            speak("opening local disk C")
            webbrowser.open("C://")
        elif "local disk e" in query:
            speak("opening local disk E")
            webbrowser.open("E://")
        elif "sleep" in query:
            speak("Shutting down! See you later then!")
            exit(0)