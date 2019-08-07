from ariadne import load_schema_from_path, QueryType, make_executable_schema
from ariadne.asgi import GraphQL

import json
import logging


# load schema from file...
schema = load_schema_from_path("schema.graphql")


# Create type instance for Query type defined in our schema...
query = QueryType()


@query.field("Films")
def resolve_film(*_, title):
    logging.info("Reading json")

    with open('tst.json', 'r') as outfile:
        data = json.load(outfile)
    
    return data


executable_schema = make_executable_schema(schema, query)
app = GraphQL(executable_schema, debug=True)
