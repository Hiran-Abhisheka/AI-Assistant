import tkinter as tk
from tkinter import scrolledtext
import openai
import speech_recognition as sr
import pyttsx3


openai.api_key = "API_KEY"



recognizer = sr.Recognizer()
engine = pyttsx3.init()

def respond_to_user():
    try:
        with sr.Microphone() as source:
            chat_display.insert(tk.END, "Listening...\n")
            window.update()
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio)
            chat_display.insert(tk.END, f"You: {user_input}\n", "user")
            window.update()

            response = generate_gpt_response(user_input)
            chat_display.insert(tk.END, f"Assistant: {response}\n\n", "assistant")
            window.update()
            speak(response)
    except sr.UnknownValueError:
        chat_display.insert(tk.END, "Assistant: Sorry, I could not understand the audio.\n\n", "assistant")
        speak("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        chat_display.insert(tk.END, "Assistant: Could not request results from the speech recognition service.\n\n", "assistant")
        speak("Could not request results from the service.")
    except Exception as e:
        chat_display.insert(tk.END, f"Error: {str(e)}\n", "error")
        print(f"Error: {str(e)}")

def generate_gpt_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"GPT API Error: {str(e)}")
        return "Sorry, I couldn't get a response from the AI service."

def speak(text):
    engine.say(text)
    engine.runAndWait()

window = tk.Tk()
window.title("AI Assistant")

window.geometry("500x600")
window.configure(bg="#2c3e50")

frame = tk.Frame(window, bg="#34495e")
frame.pack(pady=10)

chat_display = scrolledtext.ScrolledText(
    frame, width=60, height=20, wrap=tk.WORD, font=("Arial", 12),
    bg="#ecf0f1", fg="#2c3e50", relief=tk.FLAT
)
chat_display.pack(padx=10, pady=10)

chat_display.tag_config("user", foreground="#2980b9", font=("Arial", 12, "bold"))
chat_display.tag_config("assistant", foreground="#27ae60", font=("Arial", 12, "italic"))
chat_display.tag_config("error", foreground="#e74c3c", font=("Arial", 12, "italic"))

speak_button = tk.Button(
    window, text="Speak", command=respond_to_user,
    font=("Arial", 14), bg="#3498db", fg="white", activebackground="#2980b9", relief=tk.FLAT
)
speak_button.pack(pady=20)

window.mainloop()