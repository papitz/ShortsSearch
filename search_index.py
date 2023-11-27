from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.filedb.filestore import RamStorage
from whoosh.fields import Schema, TEXT, NUMERIC

def search_index(query_string):
    # Create a query parser and search for a specific object
    schema = Schema(time=NUMERIC(stored=True),
                    label=TEXT(stored=True),
                    confidence=NUMERIC(stored=True))

    # Open the existing index
    storage = RamStorage()
    index = storage.open_index(schema=schema)

    # Create a query parser for the 'label' field of the schema
    query_parser = QueryParser("label", schema=index.schema)
    query = query_parser.parse(query_string)

    # Perform the search
    with index.searcher() as searcher:
        results = searcher.search(query)
        for result in results:
            print(f"Time: {result['time']}, Label: {result['label']}, Confidence: {result['confidence']}")