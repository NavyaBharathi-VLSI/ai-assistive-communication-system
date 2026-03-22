import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to convert speech to text continuously
def continuous_speech_to_text():
    # Use the default microphone for input
    with sr.Microphone() as source:
        print("speak")
        recognizer.adjust_for_ambient_noise(source)
        print("Ready to listen... Speak now!")

        while True:
            try:
                print("Listening for speech...")
                # Capture the audio from the microphone
                audio = recognizer.listen(source)

                # Recognize the speech using Google's speech recognition
                print("Recognizing...")
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")

            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
            except sr.RequestError:
                print("Sorry, the speech service is unavailable. Please try again later.")
            except KeyboardInterrupt:
                print("Speech-to-text stopped by user.")
                break

# Call the function
continuous_speech_to_text()
