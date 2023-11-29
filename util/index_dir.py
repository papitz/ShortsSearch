from util.transcribe import transcribe_audio, convert_video_to_audio_ffmpeg
from util.get_object_from_video import detect_objects_in_video
from ultralytics import YOLO
import subprocess
import os
import sys
import glob
from summarizers import Summarizers
from keybert import KeyBERT

MIN_CONFIDENCE = 0.1


def index_directory(folder_path):
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        sys.exit(1)

    output_file = f"{folder_path}_output.txt"

    model = YOLO("yolov8x-cls.pt")
    summ = Summarizers("normal")

    with open(output_file, "w") as file:
        # Find all mp4 files in the folder
        mp4_files = glob.glob(os.path.join(folder_path, "*.mp4"))

        # Convert each .mp4 file to .wav
        for video_file in mp4_files:
            convert_video_to_audio_ffmpeg(video_file)
            detected_objects = index_video(video_file, model, MIN_CONFIDENCE)
            file.write(f"Objects: {detected_objects}\n")

        # Find all .wav files in the provided folder path
        wav_files = glob.glob(os.path.join(folder_path, "*.wav"))
        index_audio(wav_files, file, summ)


def index_audio(wav_files, file, summ):
    # Transcribe each .wav file and write the transcription, summary, and keywords to the file
    for audio_file in wav_files:
        transcription = transcribe_audio(audio_file)

        if transcription:
            file.write(f"File: {os.path.basename(audio_file)}\n")
            file.write(f"Transcription: {transcription}\n\n")
            summary = summ(transcription)
            kw_model = KeyBERT()
            keywords = kw_model.extract_keywords(transcription)
            file.write(f"Summary: {summary}\n\n")
            file.write(f"Keywords: {keywords}\n\n")

def index_video(video_file, model, min_confidence):
    detected_objects = detect_objects_in_video(video_file, model, min_confidence)
    print(f"SET: {str(detected_objects)}")
    return str(detected_objects)


