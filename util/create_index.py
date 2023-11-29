import json
import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID

#Define the schema
schema = Schema(
    video_id=ID(stored=True, unique=True),
    transcription=TEXT(stored=True),
    summary=TEXT(stored=True),
    keywords=TEXT(stored=True),
    detected_objects=TEXT(stored=True)
)

#Read data from a JSON file
def read_json(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return {}

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            
        if not isinstance(data, dict):
            print(f"Invalid format in file: {file_path}")
            return {}

        return data

    except json.JSONDecodeError as e:
        print(f"Error reading JSON file {file_path}: {e}")
        return {}


#Merge data from JSON files
def merge_data(transcription_data, object_data):
    merged_data = {}
    for video_id, data in transcription_data.items():
        merged_data[video_id] = {
            "transcription": data.get("transcription", ""),
            "summary": data.get("summary", ""),
            "keywords": ', '.join(data.get("keywords", [])),
            "detected_objects": ', '.join(object_data.get(video_id, []))
        }
    return merged_data

#Create the index
def create_index(data, index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    ix = create_in(index_dir, schema)
    writer = ix.writer()
    for video_id, content in data.items():
        writer.add_document(
            video_id=video_id,
            transcription=content["transcription"],
            summary=content["summary"],
            keywords=content["keywords"],
            detected_objects=content["detected_objects"]
        )
    writer.commit()
