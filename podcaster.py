import threading
import time

import pyttsx3
from PyPDF2 import PdfReader

import re

from SpeechGenerator import SpeechGenerator
from openai_utils import gpt3, gpt4
from utils import get_timestamp


def pdf_to_txt(pdf_file):
    pdf_file = open(pdf_file, 'rb')
    pdf_reader = PdfReader(pdf_file)

    paper_text= ""
    for page_num in range(0, len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]

        # Remove the header and footer from the page
        # page.mediabox.upper_right = page.mediabox.upper_right
#        page.mediabox.lowerLeft = (page.mediabox.getLowerLeft_x(), 0)

        text = page.extract_text()
        if page_num==0:
            paper_title = f"Title: {gpt4('You are provided with a text extracted from a scientific paper in PDF format. Extract the title of the paper',text)}\n"
            paper_text += paper_title
            paper_text+= f"Authors: {gpt4('You are provided with a text extracted from a scientific paper in PDF format. Extract the list of authors', text)}\n"


        text = re.sub(r"\[\d+?\]", "", text)
        # Remove captions
        text = re.sub(r"Figure\s+\d+?\s*:.+", "", text)
        text = remove_unreadable_items(text)

        cleaning_prompt = "You are provided with a text extracted from a scientific paper in PDF format." \
                          "Your task is to clean this text by removing any naudible content such as tables, figures, figure captions, " \
                          "equations, mathematical expressions, references, citations and any other non-sensical text. " \
                          "Only coherent and meaningful sentences should be retained. You can remove content which do not seem important or fragmanted. " \
                          "Also remove line numbering if exists and new lines." \
                          "This text will serve as the basis for generating an interview. Feel free to omit any portions that are unnecessary for simulating an interview with the author of the paper." \

        cleaned_text = gpt4(cleaning_prompt, text, model="gpt-3.5-turbo")

        paper_text+=f' {cleaned_text}'

    pdf_file.close()
    open(f"to_delete/text-{paper_title}_.txt", 'w').write(paper_text)

    return paper_text


def convert_text_to_interview(paper_text):
    system_prompt = "You are provided with a text extracted from a scientific paper in PDF format. " \
                    "Your objective is to simulate a podcast of an intrerview between the an interviewer the leading author." \
                    "The interview should clarify to the listener the information in the paper and create an" \
                    "intelligible interview that can be effectively vocalized." \
                    "Make sure you do not miss any important insights and takeaway points." \
                    "The transcript for the interview podcast should adhere to the formatting guidelines where each line begins with either 'Interviewer:' or 'Author:'." \
                    "Each turn should be presented as a single line, which may encompass one or more sentences." \
                    "Ensure that you do not attribute any previous findings or work utilized by the author to the author himeself."\
                    "If there is a requirement for technical terminology or background information, take the time to discuss and elucidate them with the author. " \
                    "This will ensure that the podcast remains accessible to a wide audience."\
                    "Minimize the use of specialized terms and abbreviations whenever feasible."\
                    "The name of the podcast is the smallcaster so make sure you mention that in the welcome statement of the interviewer."

    interview_text = gpt4(system_prompt, paper_text)
    open(f"interview_text_{get_timestamp()}.txt", 'w').write(interview_text)

    return interview_text


def remove_unreadable_items(text):
    # Remove citations like "(Macal, 2016, p. 145)"
    text = re.sub(r'\(\w+((, )\w+)*(, p\. \d+)?\)', '', text)

    # Remove citations like "(Pyka & Fagiolo, 2007)" and "North & Macal, 2007)"
    text = re.sub(r'\([\w\s&]+, \d+\)', '', text)

    # Remove citations like "(Macal, 2016, p. 146, referring to Bankes, 2002)"
    text = re.sub(r'\(\w+, \d+, p\. \d+, referring to \w+, \d+\)', '', text)

    # Remove citations like "(Axtell & Epstein, 1994; Gilbert & Terna, 2000)"
    text = re.sub(r'\([\w\s&]+, \d+;\s[\w\s&]+, \d+\)', '', text)

    # Remove citations like "(Hoog, 2019; Edali & Yücel, 2019; Lamperti, Roventini, & Sani, 2018)"
    text = re.sub(r'\([\w\s&,]+, \d+;\s[\w\s&,]+, \d+;\s[\w\s&,]+, \d+\)', '', text)

    # Remove author names and affiliations like "Bernd Ebersberger\nInnovation Management University of Hohenheim Stuttgart,"
    text = re.sub(r'\w+\s\w+\n[\w\s]+,', '', text)

    # Define a regular expression pattern to match line numbers
    text = re.sub(r'^\s*\d+\s*[-–]?\s*', '', text, flags=re.MULTILINE)

    return text


def line_starts_with_name(line):
    pattern = r'^\w+\s*:'
    return bool(re.match(pattern, line))


def read_interview(interview_text):
    # Set properties if needed (e.g., engine.setProperty('rate', 150))
    generator = SpeechGenerator()

    # Split the interview text into lines
    lines = interview_text.split('\n')

    # Iterate through the lines
    for line in lines:
        if line.startswith("Interviewer:"):
            print("Interviewer:")
            generator.add_turn(line[len("Interviewer:")+1:], voice=1)
        elif line_starts_with_name(line) and not line.startswith("Interviewer:"):
            print("Interviewee:")
            generator.add_turn(line[line.find(":")+1:], voice=2)

    generator.play_with_intro()


if __name__ == '__main__':

    #paper_text = pdf_to_txt('/Users/georgekour/Downloads/predicting-QA-semantic-consistency.pdf')

    paper_content = open("/Users/georgekour/repositories/pdf_voice/outputs/paper_text_2023_10_03_22_37.txt", 'r').read()

    # print(paper_text)
    ## google_test2speech(text)
    interview_text = convert_text_to_interview(paper_content)

    #interview_text = open('/Users/georgekour/repositories/pdf_voice/interview_text_2023_10_04_01_54.txt', 'r').read()

    print(interview_text)

    read_interview(interview_text)

    # system_prompt = "You have been provided with a text extracted from a scientific paper in PDF format. "
    # "Your objective is to identify and extract the coherent and "
    # "intelligible sections of text that can be effectively vocalized, in order to ensure the paper's comprehensibility."
    # "Ignore reference, figures, and tables but pay special attention to the sections and text."
    #
    # system_prompt = "You have been provided with a text extracted from a scientific paper in PDF format. "
    # "Your objective is to summarize the information in the paper and create an"
    # "intelligible text that can be effectively vocalized, in order to ensure the paper's comprehensibility." \
    # "Make sure you do not miss any important insights and takeway points."
    # "Do not hesitate to extract important text portions from the text."
    # "Ignore reference, figures, and tables but pay special attention to the sections and text."
    #
