from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.asgi import GraphQL
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import uvicorn
from schema import schema
from request_file import upload_files

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) configuration for handling API requests from different origins.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL configuration
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",  # Update with your GraphQL server endpoint
    use_json=True,
)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Add your file paths here
file_paths = ['path/to/file1.pdf', 'path/to/file2.pdf']

# Trigger file upload request
response = upload_files(file_paths)



# GraphQL schema for handling file uploads
upload_mutation = gql("""
mutation ($file: Upload!) {
  uploadFile(file: $file) {
    filename
  }
}
""")

# FastAPI route for file upload
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     try:
#         # Use GraphQL to upload the file to the server
#         variables = {"file": file}
#         result = client.execute(upload_mutation, variable_values=variables)
#         return JSONResponse(content=result)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# GraphQL endpoint for handling queries and mutations
# app.add_route("/graphql", GraphQLApp(schema=app.schema))
app.add_route("/graphql", GraphQL(schema=schema))

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
