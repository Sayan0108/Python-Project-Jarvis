import speech_recognition as sr # pip install speech_recognition
import webbrowser # pip install webbrowser
import pyttsx3 # pip install pyttsx3
import musicLibrary
import requests # pip install requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "a7479dfb88244051a389ed55d12d7882"
weathapi = "49d7e941ac5cd65ddca4cfd3821c8ddd"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("http://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("http://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("http://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("http://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/everything?sources=the-times-of-india,ndtv,bloombergquint&apiKey={newsapi}")
        if r.status_code == 200:
            # parse the JSON response
            data = r.json()
            # Extract the articles
            articles = data.get("articles", [])
            # speak the headlines
            for article in articles:
                speak(article["title"])
    elif "weather" in c.lower():
        print("Which city's weather would you like to check?")
        speak("Which city's weather would you like to check?")
        # Capture city name using voice input
    with sr.Microphone() as source:
        print("Listening for city name...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        city = recognizer.recognize_google(audio)
        print(f"Recognized city: {city}")
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand the city name.")
        return
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting to the speech service.")
        return

    # Fetch weather details
    params = {"q": city, "appid": weathapi, "units": "metric"}
    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weathapi}&units=metric")
    data = r.json()

    # print("API Response:", data)

    if data["cod"] == 200:
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        weather_info = f"The weather in {city} is {weather_desc} with a temperature of {temp}°C."

        print(weather_info)
        speak(weather_info)
    else:
        return "Sorry, I couldn't fetch the weather details. Please check the city name."


if __name__ == "__main__":
    print("Initializing Jarvis.....")
    speak("Initializing Jarvis.....")
    while True:
        # Listen for the wake word Jarvis
        # obtain audio from the microphone
        r = sr.Recognizer()
        

        # recognize speech using recognize_google()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            print("Recognizing...")
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yeah")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    
                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))