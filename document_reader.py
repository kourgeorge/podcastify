import os
import re
import fitz
import utils
from openai_utils import gpt4
from docx import Document


class ContentReader:
    max_pages = 20

    def __init__(self, file_path):
        self.file_path = file_path
        self.text_list = self.pdf_to_text(file_path) if ContentReader.is_pdf(
            file_path) else self.docx_to_text(file_path) if ContentReader.is_docx(file_path) else open(file_path, 'r').read()
        self.title = None
        self.authors = None

    @staticmethod
    def pdf_to_text(file_path, start_page=1, end_page=max_pages):
        doc = fitz.open(file_path)
        total_pages = doc.page_count

        if end_page is None:
            end_page = total_pages

        text_list = []

        for i in range(start_page - 1, end_page):
            text = doc.load_page(i).get_text("text")
            text = ContentReader.preprocess(text)
            text = utils.remove_unreadable_items(text)
            text_list.append(text)

        doc.close()
        return text_list

    def docx_to_text(file_path):
        doc = Document(file_path)
        text_list = []

        for para in doc.paragraphs:
            text_list.append(para.text)

        return text_list

    def extract_title(self):
        if self.title is None:
            paper_title = gpt4(
                'You are provided with a text extracted from a scientific paper in PDF format. Extract the title of the paper',
                self.content)
            self.title = paper_title
        return self.title

    def extract_authors(self):
        if self.authors is None:
            self.authors = gpt4(
                'You are provided with a text extracted from a scientific paper in PDF format. Extract the list of authors',
                self.content)
        return self.authors

    def get_content(self):
        return " ".join(self.text_list)

    def save(self, output_path):
        open(os.path.join(output_path, self.title + '.txt'), 'w').write(self.content)

    @staticmethod
    def preprocess(text):
        text = text.replace('\n', ' ')
        text = re.sub('\s+', ' ', text)
        text = re.sub(r'\b\d+\b', '', text)  # Remove standalone numbers
        text = re.sub(r'(\w)-\s*(\w)', r'\1\2', text)
        return text

    @staticmethod
    def is_pdf(file_path):
        _, extension = os.path.splitext(file_path)
        return extension.lower() == '.pdf'

    @staticmethod
    def is_docx(file_path):
        _, extension = os.path.splitext(file_path)
        return extension.lower() == '.docx'
