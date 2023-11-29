# This is the entry point script for short search
# It will handle indexing directories and querying the indexed data

import click
from util.index_dir import index_directory
from util.create_index import create_index, read_json
from util.search_index import search_index


@click.command()
@click.option('--dir_to_index', required=False, help='Directory to index')
@click.option('--index_file', help='File that holds the index')
@click.option('--index_dir', help='Directory to index into or read index from')
@click.option('--query', help='Query to run on indexed data')
@click.option('--field', help='Field to query. Options: detected_objects, keywords, summary and transcription')

def cli(dir_to_index, index_file, index_dir, query, field):
    print('Welcome to short search!')
    if dir_to_index:
        print(f"Indexing all video files in {dir_to_index}")
        #  TODO: Add index file here
        index_directory(dir_to_index)
        print("Successfully indexed videos!")
    if index_dir and index_file:
        print("Building indexing from file")
        print(f"Index file: {index_file}")
        index_data = read_json(index_file)
        create_index(index_data, output_index_dir)
        print("Successfully built index")
    if query and field and index_dir:
        print(query, field)
        print("TODO: search logic here")
        if field not in ["detected_objects", "keywords", "summary", "transcription"]:
            print("Invalid field. Please refer to one of the following field: detected_objects, keywords, summary and transcription.")
        search_index(index_dir, query, field)
