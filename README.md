# Home Assistant Voice Assistant
A voice assistant made in python that interacts with the Home Assistant API

## What you need to know before installing
* The code only runs on linux
* It uses Google Cloud for STT and TTS
* The wake word detection is done locally
* It comes with 3 wake words:
  * ok home
  * hey house
  * _hey home_             works by accident
## Installation
1. Create a directory for a script: `mkdir /path/to/your/directory`
2. Go into that directory: `cd /path/to/your/directory`
3. Clone the repository: `git clone https://github.com/mrLeonTheMaster/Home-Assistant-Voice-Assistant.git`
4. Make the files executable: `chmod a+x ./first_time.py ./assistant.py`
5. Run the first time setup: `./first_time.py`
6. Run the final file: `./assistant.py`
