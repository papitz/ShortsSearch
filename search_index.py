import os
import sys
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, OrGroup

def search_index(index_dir, query_str, field):
    ix = open_dir(index_dir)

    og = OrGroup.factory(1) #Customizable from value 0-1
    with ix.searcher() as searcher:
        query = QueryParser(field, ix.schema, group=og).parse(query_str)
        results = searcher.search(query, limit=None)

        if len(results) == 0:
            print(f"No results found for '{query_str}' in {field}.")
        else:
            for result in results:
                print(f"Video ID: {result['video_id']}")
                print(f"Matched {field}: {result[field]}")
                print("")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python search_index.py + index path + 'query string' + field")
        sys.exit(1)

    index_dir = sys.argv[1]
    query_str = sys.argv[2]
    field = sys.argv[3]

    if not os.path.exists(index_dir) or not os.path.isdir(index_dir):
        print("Invalid index directory.")
        sys.exit(1)

    if field not in ["detected_objects", "keywords", "summary", "transcription"]:
        print("Invalid field. Please refer to one of the following field: detected_objects, keywords, summary and transcription.")
        sys.exit(1)

    search_index(index_dir, query_str, field)