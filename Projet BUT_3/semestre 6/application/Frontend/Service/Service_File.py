import fitz
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pandas as pd
from Exception.FileTypeIsNotAcceptedException import FileTypeIsNotAcceptedException
from googletrans import Translator

class Service_File:
    def __init__(self):
        pass

    def file_for_string(self, file):
        translator = Translator()
        
        if file.name.endswith('.docx'):
            string = self.word_to_string(file)
            language = translator.detect(string).lang.upper()
            if language != "EN":
                string = translator.translate(string, src=language, dest="en").text
            return string
        
        elif file.name.endswith('.pdf'):
            string = self.pdf_to_string(file)
            language = translator.detect(string).lang.upper()
            if language != "EN":
                string = translator.translate(string, src=language, dest="en").text
            return string
        
        elif file.name.endswith('.xlsx'):
            string = self.excel_to_string(file)
            language = translator.detect(string).lang.upper()
            if language != "EN":
                string = translator.translate(string, src=language, dest="en").text
            return string
        
        elif file.name.endswith('.csv'):
            string = self.csv_to_string(file)
            language = translator.detect(string).lang.upper()
            if language != "EN":
                string = translator.translate(string, src=language, dest="en").text
            return string
        
        else:
            raise FileTypeIsNotAcceptedException('File type is not accepted. Please upload a .docx, .pdf, .xlsx or .csv file.')

    def pdf_to_string(self, file):
        string = ""
        with fitz.open(stream=file.getvalue()) as doc:
            for page in doc:
                string += page.get_text()
        return string

    def word_to_string(self, file):
        doc = Document(file)
        full_text = []

        for para in doc.paragraphs:
            full_text.append(para.text)

        return '\n'.join(full_text)
    
    def excel_to_string(self, file):
        df = pd.read_excel(file)
        return self.dataframe_to_formatted_string(df)

    def csv_to_string(self, file):
        df = pd.read_csv(file)        
        return self.dataframe_to_formatted_string(df)

    def dataframe_to_formatted_string(self, df):
        formatted_string = ', '.join(df.columns) + '\n'
        
        for index, row in df.iterrows():
            line_values = [str(value) for value in row]
            formatted_string += ', '.join(line_values) + '\n'
        
        return formatted_string.strip()