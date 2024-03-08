# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import asyncio

import graphene
from graphene_file_upload.scalars import Upload

from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
import uvicorn

app = FastAPI()

# GraphQL configuration
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",  # Update with your GraphQL server endpoint
    use_json=True,
)
client = Client(transport=transport, fetch_schema_from_transport=True)

# GraphQL schema for handling file uploads
upload_mutation = gql(
    """
mutation ($file: Upload!) {
  uploadFile(file: $file) {
    filename
  }
}
"""
)


# FastAPI route for file upload
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Use GraphQL to upload the file to the server
        variables = {"file": file}
        result = client.execute(upload_mutation, variable_values=variables)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

schema = strawberry.Schema(query=Query)
# GraphQL endpoint for handling queries and mutations
app.add_route("/graphql", GraphQLApp(schema=app.schema))

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    # from pdfAccess import PdfAccess
    # pdf_text = PdfAccess().accessPDF()

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    # from EmbeddingsPDF import EmbeddingsPDF

    # emd = EmbeddingsPDF()
    # file = "healthInsurance.pdf"
    # pdf_docs = open(file, "rb")
    # raw_text = emd.get_pdf_text([pdf_docs])
    # # 2 Get the text chunks
    # text_chunks = emd.get_text_chunks(raw_text)

    # vectorstore = EmbeddingsPDF().get_chroma_embeddings()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
