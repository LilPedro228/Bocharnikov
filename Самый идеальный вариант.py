import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image, ImageTk

class SpeechRecognitionApp:
    def __init__(self):
        self.language = "en-US"
        self.dark_mode = False
        self.record_duration = 60
        self.app = tk.Tk()
        self.app.title("Speech Recognition App")

        # Изменен фоновый цвет и добавлено изображение фона
        self.bg_color = "#2C3E50" if self.dark_mode else "#ECF0F1"
        self.app.configure(bg=self.bg_color)

        # Загрузка изображения фона
        bg_image_path = "background_image.jpg"  # Замените на путь к вашему изображению
        self.bg_image = ImageTk.PhotoImage(Image.open(bg_image_path))
        self.background_label = tk.Label(self.app, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Добавлены изображения для кнопок
        self.language_image = ImageTk.PhotoImage(Image.open("language_button.png"))  # Замените на путь к вашему изображению
        self.microphone_image = ImageTk.PhotoImage(Image.open("microphone_button.png"))  # Замените на путь к вашему изображению
        self.upload_image = ImageTk.PhotoImage(Image.open("upload_button.png"))  # Замените на путь к вашему изображению
        self.dark_mode_image = ImageTk.PhotoImage(Image.open("dark_mode_button.png"))  # Замените на путь к вашему изображению

        # Добавлены изображения на кнопки
        self.language_button = tk.Button(self.app, image=self.language_image, command=self.toggle_language, bd=0)
        self.language_button.pack(pady=20)

        self.start_button = tk.Button(self.app, image=self.microphone_image, command=self.start_recording, bd=0)
        self.start_button.pack(pady=20)

        self.upload_button = tk.Button(self.app, image=self.upload_image, command=self.upload_audio_file, bd=0)
        self.upload_button.pack(pady=20)

        self.result_label = tk.Label(self.app, text="Текст: ", font=("Helvetica", 14), bg=self.bg_color, fg="#3498DB")
        self.result_label.pack()

        self.dark_mode_button = tk.Button(self.app, image=self.dark_mode_image, command=self.toggle_dark_mode, bd=0)
        self.dark_mode_button.pack(pady=20)

        self.app.mainloop()

    def toggle_language(self):
        self.language = "ru-RU" if self.language == "en-US" else "en-US"
        self.result_label.config(text="Язык: " + self.language)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.bg_color = "#2C3E50" if self.dark_mode else "#ECF0F1"
        self.app.configure(bg=self.bg_color)
        for widget in self.app.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=self.bg_color)
            elif isinstance(widget, tk.Label):
                widget.configure(bg=self.bg_color, fg="#3498DB")

    def start_recording(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Говорите...")
            audio = recognizer.listen(source)
        self.process_audio(audio)

    def upload_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Аудиофайлы", "*.wav")])
        if file_path:
            try:
                audio = AudioSegment.from_file(file_path)
                play(audio)
                audio.export("temp.wav", format="wav")
                audio = AudioSegment.from_wav("temp.wav")
                self.process_audio(audio)
            except Exception as e:
                self.result_label.config(text="Ошибка при загрузке файла: {0}".format(e))

    def process_audio(self, audio):
        recognizer = sr.Recognizer()
        try:
            text = recognizer.recognize_google(audio, language=self.language)
            self.result_label.config(text="Текст: " + text)
        except sr.UnknownValueError:
            self.result_label.config(text="Не удалось распознать аудио")
        except sr.RequestError as e:
            self.result_label.config(text="Ошибка сервиса: {0}".format(e))

# Создаем экземпляр приложения
app_instance = SpeechRecognitionApp()
