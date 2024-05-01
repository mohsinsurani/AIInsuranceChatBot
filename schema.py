# schema.py

import strawberry
import typing
from typing import Annotated
from fastapi import FastAPI, File
from strawberry.file_uploads import Upload


@strawberry.input
class FolderInput:
    files: typing.List[Upload]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def read_typeA_pdf(self, folder_input: FolderInput) -> str:
        file_names = []
        for uploaded_file in folder_input.files:
            # Save the file or implement your file handling logic here
            file_names.append(uploaded_file.filename)
        return f"Uploaded files: {', '.join(file_names)}"


@strawberry.type
class Query:
    @strawberry.field
    def getAnswer(self, question: str) -> str:
        # Implement logic to provide answers based on the question
        return f"Answer to '{question}'"


schema = strawberry.Schema(query=Query, mutation=Mutation)
