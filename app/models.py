# Importing the BaseModel class from the pydantic library, which is used for data validation and settings management.
from pydantic import BaseModel

# Defining a class `QueryParam` that inherits from `BaseModel`.
# This class is used to define the structure and default values for query parameters.
class QueryParam(BaseModel):
    # A boolean field named `stream` with a default value of True.
    # This could be used to indicate whether streaming is enabled or not.
    stream: bool = True

# Defining another class `WebSocketQuery` that also inherits from `BaseModel`.
# This class represents the structure of a WebSocket query.
class WebSocketQuery(BaseModel):
    # A string field named `query` to hold the main query text.
    query: str
    # A string field named `prompt` to hold additional information or context for the query.
    prompt: str
    # A field named `param` of type `QueryParam`, which embeds the `QueryParam` class.
    # This allows for nested data validation and structure within the WebSocket query.
    param: QueryParam
