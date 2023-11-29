# additional libraries:
#     keybert: https://pypi.org/project/keybert/
#     summarizers: https://pypi.org/project/summarizers/#description
#

import subprocess
import os
import sys
import glob
import speech_recognition as sr
import json
from summarizers import Summarizers
from keybert import KeyBERT

summ = Summarizers("normal")

# Converting .mp4 to .wav
def convert_video_to_audio_ffmpeg(video_file, output_ext="wav"):
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

# Transcribe the .wav audio
def transcribe_audio(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        # read the entire audio file
        audio = r.record(source)

    # Recognize speech using Google Speech Recognition
    try:
        print("Transcribing: " + audio_file)
        transcription = r.recognize_google(audio)
        return transcription

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/folder")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        sys.exit(1)

    output_file = "output.txt"  

    with open(output_file, "w") as file:
        # Find all mp4 files in the folder
        mp4_files = glob.glob(os.path.join(folder_path, '*.mp4'))

        # Convert each .mp4 file to .wav
        for video_file in mp4_files:
            convert_video_to_audio_ffmpeg(video_file)

        # Find all .wav files in the provided folder path
        wav_files = glob.glob(os.path.join(folder_path, '*.wav'))

        # Transcribe each .wav file and write the transcription, summary, and keywords to the file
        transcription_data = {}
        for audio_file in wav_files:
            transcription = transcribe_audio(audio_file)
            
            if transcription:
                summary = summ(transcription)
                kw_model = KeyBERT()
                keywords = kw_model.extract_keywords(transcription)
                transcription_data[os.path.basename(audio_file)] = {
                    "transcription": transcription,
                    "summary": summary,
                    "keywords": [kw[0] for kw in keywords]
                }

        # Save the transcription data to a JSON file
        with open("transcription_data.json", "w") as file:
            json.dump(transcription_data, file)
 
