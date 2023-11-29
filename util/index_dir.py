from util.transcribe import transcribe_audio, convert_video_to_audio_ffmpeg
from util.get_object_from_video import detect_objects_in_video
from ultralytics import YOLO
import subprocess
import os
import sys
import glob
import json
from summarizers import Summarizers
from keybert import KeyBERT

MIN_CONFIDENCE = 0.1


def index_directory(folder_path):
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        sys.exit(1)

    output_file = f"{folder_path}_output.json"

    model = YOLO("yolov8x-cls.pt")
    summ = Summarizers("normal")

    with open(output_file, "w") as file:
        # Find all mp4 files in the folder
        mp4_files = glob.glob(os.path.join(folder_path, "*.mp4"))

        # Convert each .mp4 file to .wav
        data_json = {}
        for video_file in mp4_files:
            filename_no_ext = os.path.splitext(os.path.basename(video_file))[0]
            convert_video_to_audio_ffmpeg(video_file)

            # Get the data
            detected_objects = index_video(video_file, model, MIN_CONFIDENCE)
            audio_data = index_audio(os.path.join(folder_path, filename_no_ext + ".wav"), summ)

            # Save in dict
            data_json[filename_no_ext] = audio_data
            data_json[filename_no_ext]['detected_objects'] = detected_objects


        # Find all .wav files in the provided folder path
        json.dump(data_json, file)


def index_audio(audio_file, summ):
    # Transcribe each .wav file and write the transcription, summary, and keywords to the file
    # for audio_file in wav_files:
    transcription = transcribe_audio(audio_file)

    if transcription:
        summary = summ(transcription)
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(transcription)
        # transcription_data[os.path.basename(audio_file)] = {
        transcription_data = {
            "transcription": transcription,
            "summary": summary,
            "keywords": [kw[0] for kw in keywords],
        }

    return transcription_data


def index_video(video_file, model, min_confidence):
    detected_objects = detect_objects_in_video(video_file, model, min_confidence)
    print(f"SET: {str(detected_objects)}")
    return list(detected_objects)
