import json
from pathlib import Path
import requests
import os
import fitz


class PdfAccess:
    pdf_url = "https://adviser.vitality.co.uk/adviser.vitality.co.uk/media-online/advisers/literature/health" \
              "/compliance/vhb0181-personal-healthcare-ipid.pdf?_its" \
              "=JTdCJTIydmlkJTIyJTNBJTIyZTczZmVlYjEtNDg5Mi00YTVjLTgzYTYtNzUzY2U3M2U1ZDYyJTIyJTJDJTIyc3RhdGUlMjIlM0ElMjJybHR%2BMTcwMjQ2ODQ1MX5sYW5kfjJfOTkzNTZfZGlyZWN0X2UzMTM4OGE0NDI3NzExOTVlOTU5OTBlNDFkYzczNmU5JTIyJTJDJTIyc2l0ZUlkJTIyJTNBMTcwMjElN0Q%3D"
    filename = 'healthInsurance.pdf'

    def downloadPDF(self):
        filename = Path(self.filename)
        response = requests.get(self.pdf_url)
        filename.write_bytes(response.content)

    def getPDFText(self):
        pdf_document = self.accessPDF()
        pdf_text = ""
        for page_num in range(pdf_document.page_count):
            pdf_text += pdf_document[page_num].get_text()

        return pdf_text

    def accessPDF(self):
        check_file = os.path.isfile(self.filename)
        if check_file:
            pdf_document = fitz.open(self.filename)
            return pdf_document
        else:
            self.downloadPDF()
            self.accessPDF()

    def accessPath(self):
        check_file = os.path.isfile(self.filename)
        if check_file:
            return self.filename
        else:
            self.downloadPDF()
            return self.filename

    @staticmethod
    def getDataSet():
        f = open('data.json')
        data = json.load(f)
        return data
