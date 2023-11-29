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
