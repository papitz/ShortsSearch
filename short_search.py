# This is the entry point script for short search
# It will handle indexing directories and querying the indexed data

import click
from util.index_dir import index_directory

@click.command()
@click.option('--dir_to_index', required=False, help='Directory to index')
@click.option('--index_file', help='File that holds the index')
@click.option('--query', help='Query to run on indexed data')

def cli(dir_to_index, index_file, query):
    print('Welcome to short search!')
    if dir_to_index:
        print("TODO: indexing logic here")
        index_directory(dir_to_index)
    if index_file:
        print(index_file)
        print("TODO: read index file or smth")
    if query:
        print(query)
        print("TODO: search logic here")

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python short_search.py /path/to/folder")
#         sys.exit(1)
#
#     folder_path = sys.argv[1]
#     if not os.path.isdir(folder_path):
#         print("Invalid folder path.")
#         sys.exit(1)
#
#     output_file = "output.txt"  
#
#     with open(output_file, "w") as file:
#         # Find all mp4 files in the folder
#         mp4_files = glob.glob(os.path.join(folder_path, '*.mp4'))
#
#         # Convert each .mp4 file to .wav
#         for video_file in mp4_files:
#             convert_video_to_audio_ffmpeg(video_file)
#
#         # Find all .wav files in the provided folder path
#         wav_files = glob.glob(os.path.join(folder_path, '*.wav'))
#
#         # Transcribe each .wav file and write the transcription, summary, and keywords to the file
#         for audio_file in wav_files:
#             transcription = transcribe_audio(audio_file)
#            
#             if transcription:
#                 file.write(f"File: {os.path.basename(audio_file)}\n")
#                 file.write(f"Transcription: {transcription}\n\n")
#                 summary = summ(transcription)
#                 kw_model = KeyBERT()
#                 keywords = kw_model.extract_keywords(transcription)
#                 file.write(f"Summary: {summary}\n\n")
#                 file.write(f"Keywords: {keywords}\n\n")
# 
