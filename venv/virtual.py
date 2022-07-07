import calendar
import datetime
import os
import smtplib
import subprocess
import time
import webbrowser

import pyautogui as pygui
import pyttsx3
import pywhatkit as pywhatkit
import pyjokes
import speech_recognition as sr
import wikipedia
import wolframalpha
import requests
from datetime import date
from email.message import EmailMessage
from forex_python.converter import CurrencyRates
from geopy.geocoders import Nominatim
from geopy import distance

print('Loading your AI personal assistant - G One')

# Initializing the audio engine
engine = pyttsx3.init('sapi5')

# Getting the voices from the engine
voices = engine.getProperty('voices')

# Setting the first voice we get as a property to our engine
engine.setProperty('voice', 'voices[0].id')  # voices[0].id = male voice


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif 12 <= hour < 19:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")


def sendEmail():
    senderemail = "doautomaticreply@gmail.com"
    password = "Alteomihali1997."
    email_list = {
        "test": "alteomihali3@gmail.com",
        "test1": "mihalialteo@gmail.com"
    }
    try:
        email = EmailMessage()
        email['To'] = email_list["test"]
        speak("What is the subject of the email?")
        email["Subject"] = takeCommand().capitalize()
        email['From'] = senderemail
        speak("What should I send?")
        email.set_content(takeCommand())
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(senderemail, password)
        s.send_message(email)
        s.close()
        speak("Email has been sent")
        print("Email has been sent")
    except Exception as e:
        print(e)
        speak("Unable to send the Email")
        time.sleep(3)


def search_on_google(query):
    pywhatkit.search(query)


def get_random_quote():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']


# def get_trending_movies():
#     trending_movies = []
#     apiKey = '8c247ea0b4b56ed2ff7d41c9a833aa77'
#     res = requests.get(
#         f"https://api.themoviedb.org/3/trending/movie/day?api_key={apiKey}").json()
#     results = res["results"]
#     for r in results:
#         trending_movies.append(r["original_title"])
#     return trending_movies[:5]


def takeCommand():
    # Creating a recognizer object to listen to the audio
    r = sr.Recognizer()

    # Open the microphone and start recording
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')

        except Exception:
            speak("Pardon, please say that again")
            return "None"
        return statement


speak("Loading your AI personal assistant G-One")
wishMe()

if __name__ == '__main__':

    while True:
        speak("Tell me, how can I help you now?")
        statement = takeCommand().lower()
        if statement == 0:
            continue


        def take_notes():
            r5 = sr.Recognizer()
            with sr.Microphone() as source:
                print('What is your "TO DO LIST" for today?')
                engine.say('What is your "TO DO LIST" for today?')
                engine.runAndWait()
                audio = r5.listen(source)
                audio = r5.recognize_google(audio)
                print(audio)
                today = date.today()
                today = str(today)
                with open('MyNotes.txt', 'a') as f:
                    f.write('\n')
                    f.write(today)
                    f.write('\n')
                    f.write(audio)
                    f.write('\n')
                    f.close()
                engine.say('Notes have been taken')
                engine.runAndWait()
                time.sleep(3)


        if "how are you" in statement:
            listening = True
            speak("I am fine, thank you!")

        elif "send a whatsapp message" in statement or 'open whatsapp' in statement or 'send a message' in statement:
            try:
                speak("To whom you want to send the message? Please enter the number in the console:")
                wp_number = input("Enter the number: ")
                speak("What is the message?")
                webbrowser.open("https://web.whatsapp.com/send?phone=" +
                                f" +355 " + wp_number + '&text=' + takeCommand())
                time.sleep(30)
                speak("Message is ready to be sent")
                pygui.press('enter')
                speak("Message was sent successfully!")

            except Exception as e:
                print(e)
                speak("Unable to send the Message")

        elif 'notes' in statement or 'take my notes' in statement or 'add new notes for today' in statement:
            take_notes()
            print('Notes Noted!!')

        elif 'send me an email' in statement or 'send email' in statement or 'email' in statement:
            sendEmail()

        elif 'convert currency' in statement or 'convert' in statement or 'currency exchange' in statement:
            try:
                curr_list = {
                    'dollar': 'USD', 'euro': 'EUR', 'british pound': 'GBP',
                    'swiss franc': 'CHF', 'canadian dollar': 'CAD',
                    'australian dollar': 'AUD', 'singapore dollar': 'SGP', 'ruble': 'RUB',
                    'turkish lira': 'TRY', 'ukrainian': 'UKH'
                }

                cur = CurrencyRates()
                speak('From which currency do you want to convert?')
                from_cur = takeCommand()
                src_cur = curr_list[from_cur.lower()]
                print(src_cur)
                speak('To which currency do you want to convert?')
                to_cur = takeCommand()
                dest_cur = curr_list[to_cur.lower()]
                print(dest_cur)
                speak('Tell me the value of currency you want to convert')
                val_cur = int(takeCommand())
                print(cur.convert(src_cur, dest_cur, val_cur))
                speak(cur.convert(src_cur, dest_cur, val_cur))

            except Exception as e:
                speak("Couldn't get what you said")

            time.sleep(2)

        elif 'quotes' in statement or 'give me a new quote' in statement or 'random quote for today' in statement:
            speak(f"Here's your quote for today")
            quote = get_random_quote()
            print(quote)
            speak(quote)

        elif 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement or 'please, open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Youtube is opened now")
            time.sleep(5)

        elif 'open google chrome' in statement or 'show me the chrome' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is opened now")
            time.sleep(5)

        elif 'search on google' in statement or 'google' in statement or 'search online' in statement:
            speak('What do you want to search on Google?')
            query = takeCommand().lower()
            search_on_google(query)
            time.sleep(5)

        elif 'open calendar' in statement or 'show me the calendar' in statement:
            webbrowser.open_new_tab("https://www.google.com/calendar")
            speak("Google Calendar is opened now")
            time.sleep(5)

        elif 'tell me the time' in statement or 'current time' in statement or 'what day is today' in statement:
            now = datetime.datetime.now()
            date = datetime.datetime.today()
            strTime = now.strftime("%H:%M:%S")
            weekday = calendar.day_name[date.weekday()]
            print(f"Current time is {strTime} and today is {weekday}")
            speak(f"Current time is {strTime} and today is {weekday}")

        elif 'show me the weather today' in statement or 'what\'s the weather like' in statement or \
                'show today\'s weather' in statement or 'show weather' in statement or 'weather' in statement:
            # api_key = "1915fa522c5dd2c6f25c606ebec195cf"
            # base_url = "https://api.openweathermap.org/data/2.5/weather?"
            # speak("What's the city name?")
            # city_name = takeCommand()
            # complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
            # response = requests.get(complete_url)
            # x = response.json()
            # if x["cod"] != "404":
            #     y = x["main"]
            #     current_temperature = y["temp"]
            #     feels_like = y["feels_like"]
            #     current_humidity = y["humidity"]
            #     z = x["weather"]
            #     weather_description = z[0]["description"]
            #     print("The weather in " + city_name + " is: Temperature in Celsius unit = " + str(current_temperature)
            #           + "\n Feels like " + str(feels_like) + "℃ " +
            #           "\n Humidity (in percentage): " + str(current_humidity) +
            #           "\n Description: " + str(weather_description)
            #           )
            #     speak("The weather in " + city_name + " is: Temperature in Celsius unit is "
            #           + str(current_temperature)
            #           + "\n Feels like " + str(feels_like) + "℃ " +
            #           "\n Humidity in percentage: " + str(current_humidity) +
            #           "\n Description: " + str(weather_description)
            #           )
            # else:
            #     speak(" City Not Found ")

            try:
                api_key = "1915fa522c5dd2c6f25c606ebec195cf"
                base_url = "https://api.openweathermap.org/data/2.5/weather?"
                speak("What's the city name?")
                city = takeCommand()
                complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"
                response = requests.get(complete_url)
                api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid" \
                                                                                    "=1915fa522c5dd2c6f25c606ebec195cf "
                w_data = response.json()
                weather = w_data['weather'][0]['main']
                temp = int(w_data['main']['temp'])
                feels_like = int(w_data['main']['feels_like'])
                humidity = w_data['main']['humidity']
                visibility = w_data['visibility']
                wind = w_data['wind']['speed']
                sunrise = time.strftime("%H:%M:%S", time.localtime(w_data['sys']['sunrise']))
                sunset = time.strftime("%H:%M:%S", time.localtime(w_data['sys']['sunset']))

                data1 = f"Condition: {weather} \nTemperature: {str(temp)}°C"
                data2 = f"Feels like: {str(feels_like)}°C \nHumidity: {str(humidity)}% \n" \
                        f"Visibility: {str(visibility)} metres \nWind: {str(wind)} km/hr \nSunrise: {sunrise} CEST " \
                        f"\nSunset: {sunset} CEST"
                print(f"Gathering weather information of {city}...")
                speak(f"Gathering weather information of {city}...")
                print(data1)
                speak(data1)
                print(data2)
                speak(data2)

            except Exception as e:
                speak(" City Not Found ")
                continue

        elif 'distance' in statement or 'cities distance' in statement or 'show the distance between cities' in statement:
            geocoder = Nominatim(user_agent="Alteo")
            speak("Tell me the first city name")
            location1 = takeCommand()
            speak("Tell me the second city name")
            location2 = takeCommand()

            coordinates1 = geocoder.geocode(location1)
            coordinates2 = geocoder.geocode(location2)

            lat1, long1 = coordinates1.latitude, coordinates1.longitude
            lat2, long2 = coordinates2.latitude, coordinates2.longitude

            place1 = (lat1, long1)
            place2 = (lat2, long2)
            distance_places = distance.distance(place1, place2)

            print(f"The distance between {location1} and {location2} is {distance_places}")
            speak(f"The distance between {location1} and {location2} is {distance_places}")
            time.sleep(2)

        # elif 'trending movies' in statement or 'show me the movies' or 'trending right now' in statement:
        #     speak(f"Some of the trending movies are: {get_trending_movies()}")
        #     speak("I am printing it on the screen")
        #     print(*get_trending_movies(), sep='\n')

        elif 'find my ip' in statement or 'find my location' in statement:
            speak('Please wait. Let me check')
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                speak('Your IP address is ' + ipAdd)
                url = 'https://get.geojs.io/'
                geo_requests = requests.get(url).json()
                geo_data = geo_requests
                print(geo_data)
                city = geo_data['City']
                country = geo_data['Country']
                speak(f'I think we are in {city} city of {country}')
            except Exception as e:
                speak("Sorry, due to network issue, I am not able to find where we are")
                print(e)

        elif 'who are you' in statement or 'what can you do' in statement:
            print('I am G-one version 1 point 1 your personal assistant. I am programmed to tasks like'
                  'opening youtube, chrome, google calendar, predict time, search in wikipedia, predict weather'
                  'in different cities, get top headline news from CNN, ask geographical questions about countries'
                  'and other information')
            speak('I am G-one version 1 point 1 your personal assistant. I am programmed to tasks like'
                  'opening youtube, chrome, google calendar, predict time, search in wikipedia, predict weather'
                  'in different cities, get top headline news from CNN, ask geographical questions about countries'
                  'and other information')

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by Alteo")
            print("I was built by Alteo")

        elif 'get the latest news' in statement or 'show me the news' in statement or 'news' in statement:
            news = webbrowser.open_new_tab("https://edition.cnn.com/")
            speak('Here are some of the latest headlines for today')
            print('Here are some of the latest headlines for today')
            time.sleep(5)

        elif 'web' in statement:
            statement = statement.replace("web", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'play' in statement:
            song = statement.replace('play', '')
            speak('Playing ' + song)
            pywhatkit.playonyt(song)
            time.sleep(5)

        elif 'open the code' in statement.lower():
            codePath = "C:\\Users\\CRS\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
            speak("The code is opened now in Visual Studio")
            time.sleep(3)

        elif 'run command prompt' in statement.lower() or 'open command' in statement.lower():
            os.system('start cmd /k "Your Command Prompt Command"')
            print('Command Prompt is ready now')
            speak('Command Prompt is ready now')
            time.sleep(3)

        elif 'run my song' in statement or 'execute the song' in statement or 'song' in statement:
            music_dir = 'C:\\Music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
            time.sleep(4)

        elif 'ask' in statement:
            speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question = takeCommand()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            print(answer)
            speak(answer)

        elif 'in map' in statement:
            location = statement.replace('in map', '')
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get().open(url)
            speak('Here is the map of ' + location)
            print('Here is the map of ' + location)
            time.sleep(5)

        elif 'joke' in statement:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif 'good bye' in statement or 'ok bye' in statement or 'stop' in statement:
            speak('Your personal assistant G-one is shutting down, Good bye')
            print('Your personal assistant G-one is shutting down, Good bye')
            break

        elif "log off" in statement or "sign out" in statement:
            speak("Ok, your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        elif 'thank you' in statement:
            speak('You\'re welcome. Anything else you want me to do?')
            print('You\'re welcome. Anything else you want me to do?')

time.sleep(3)
