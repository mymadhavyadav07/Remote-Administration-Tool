<h1 align="center">🤖💻 Remote Administration Tool</h1>

<p align="center">Take command of your laptop remotely through Telegram with this cutting-edge bot!</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#🚀-getting-started">Getting Started</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

![Telegram Laptop Control Bot](https://github.com/mymadhavyadav07/Remote-Administration-Tool/blob/main/banner.png)

## 🌐 Overview
Ever wished you could control your laptop from anywhere using just your Telegram app? Look no further! This telegram bot allows you to access and manage various functionalities of your laptop remotely, providing convenience and flexibility like never before. Whether it's capturing webcam snapshots, recording audio, executing shell commands, or even receiving key press logs, this bot has got you covered.

## 🚀 Getting Started

1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-username/telegram-laptop-control-bot.git
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Create Telegram-Bot:** ![reference](https://core.telegram.org/bots/tutorial)
  
4. **Initialize variables in main.py:**
   ```python
   TOKEN = ""   # Initialize Telegram-Bot Token
   SHELL_DIR = r"absolute/path/to/shell/directory"   # Initialize Directory to execute shell commands
   DIRECTORY = r"absolute/path/to/output/directory"  # Initialize Output Directory

5. **Initialize variables in key-logger.py:**
   ```python
   log_dir = r"absolute/path/to/output/directory"   # Initialize Directory to store Key-Logs

6. **Convert main.py to .exe:**
   ```bash
   pyinstaller main.py --onefile --noconsole

7. **Convert key-logger.py to .exe:**
   ```bash
   pyinstaller key-logger.py --onefile --noconsole

8. **Move both executables to startup folder 📥**


## 🌟 Features

- **Webcam Capture:** Snap photos using your laptop's webcam.
- **Audio Recording:** Capture crisp audio from your device's microphone.
- **Audio Playback:** Stream audio files sent via Telegram.
- **Shell Commands:** Execute commands directly on your laptop.
- **Screenshot Capture:** Get instant screenshots on demand.
- **Key Press Logging:** Receive keystrokes as text files on Telegram.


## 📝 Usage

Simply interact with the bot using Telegram commands:

- `/start` - Initialize the bot and access its features.
- `/help` - Get list of available commands.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance this project.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Let's revolutionize how you interact with your laptop through Telegram! 💬🔥
