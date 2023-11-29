# Shorts Search

A proof of concept search engine for short videos, based on object detection and speech to text.

## Installation

Highly recommended using a virtual environment.

```
python -m venv venv
source ./venv/bin/activate
```

Install requirements first and the application second.

```
pip install -r requirements
pip install .
```

## Usage

Use the `short_search` command from a terminal.
Parameters can be used with each other or in isolation. 
If all are used the order is:
1. Reading data from the videos in a directory and writing them to a JSON file
2. Indexing the data
3. Using the query to search the specified field

```
Usage: short_search [OPTIONS]

Options:
  --dir_to_index TEXT  Directory to index
  --index_file TEXT    File that holds the index
  --index_dir TEXT     Directory to index into or read index from
  --query TEXT         Query to run on indexed data
  --field TEXT         Field to query. Options: detected_objects, keywords,
                       summary and transcription
  --help               Show this message and exit.
```

## Frameworks used

### Speech to text

https://pypi.org/project/SpeechRecognition/

### Search Engine

https://whoosh.readthedocs.io/en/latest/intro.html

### Object detection

OpenCV with YOLOv3 ML network
