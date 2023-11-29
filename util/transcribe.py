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
