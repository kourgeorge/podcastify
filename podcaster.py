import os.path

from PyPDF2 import PdfReader
import re
import utils
from Editor import Editor
from SpeechGenerator import SpeechGenerator
from openai_utils import gpt3, gpt4
from utils import get_timestamp

max_pages = 20
output_directory = '/Users/georgekour/repositories/pdf_voice/outputs'


def pdf_to_txt(pdf_file):
    pdf_file = open(pdf_file, 'rb')
    pdf_reader = PdfReader(pdf_file)

    paper_title = 'title'
    paper_text= ""
    for page_num in range(0, min(max_pages,len(pdf_reader.pages))):
        page = pdf_reader.pages[page_num]

        # Remove the header and footer from the page
        # page.mediabox.upper_right = page.mediabox.upper_right
#        page.mediabox.lowerLeft = (page.mediabox.getLowerLeft_x(), 0)


        page_text = page.extract_text()
        if page_num == 0:
            paper_title = gpt4('You are provided with a text extracted from a scientific paper in PDF format. Extract the title of the paper', page_text)
            paper_text += f"Title: {paper_title}\n"
            paper_text += f"Authors: {gpt4('You are provided with a text extracted from a scientific paper in PDF format. Extract the list of authors', page_text)}\n"

        page_text = utils.remove_unreadable_items(page_text)

        cleaning_prompt = "You are provided with a text extracted from a scientific paper in PDF format." \
                          "Your task is to clean this text by removing any inaudible content such as tables, figures, figure captions, " \
                          "equations, mathematical expressions, references, citations and any other non-sensical text. " \
                          "Only coherent and meaningful sentences should be retained. You can remove content which do not seem important or fragmanted. " \
                          "Also remove line numbering if exists and new lines. Do not rephrase or add text that are not in the original text." \
                          "This text will serve as the basis for generating an interview. Feel free to omit any portions that are unnecessary for understanding the paper." \
        #
        # cleaned_text = gpt4(cleaning_prompt, page_text, model="gpt-3.5-turbo")
        # cleaned_text = utils.TextCleaner.clean(prompt=f'Instaction:{cleaning_prompt}\nPdfText:{page_text}')
        cleaned_text = page_text
        paper_text+=f' {cleaned_text}'

    pdf_file.close()
    open(f"{paper_title}.txt", 'w').write(paper_text)

    return paper_text, paper_title


def line_starts_with_name(line):
    pattern = r'^\w+\s*:'
    return bool(re.match(pattern, line))


def vocalize_interview(interview_text):
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
            print("Author")
            generator.add_turn(line[line.find(":")+1:], voice=2)

    generator.play_with_intro(output_folder=os.path.join(output_directory,'podcasts'), intro_file='Intro_podcast.wav')


if __name__ == '__main__':

    #paper_content, paper_title = pdf_to_txt('/Users/georgekour/Downloads/Policy_Experiments.pdf')

    #paper_content = open("/Users/georgekour/repositories/pdf_voice/outputs/Space is a latent sequence: A theory of the hippocampus.txt", 'r').read()

    # print(paper_text)
    ## google_test2speech(text)
    #interview_text = Editor.create_podcast_transcript(paper_content)
    interview_text = open("/Users/georgekour/repositories/pdf_voice/outputs/interviews/interview_safety_paper.txt", 'r').read()
    #tags = ["humoristic", "explain to 5 years old", "informative"]
    tags = ["humoristic", "informative"]
    interview_text = Editor.edit_transcript(interview_text,tags)

    # interview_text = open(
    #     '/outputs/content/transcript_Automatic Generation of Attention Rules For Containment of Machine Learning Model Errors.txt', 'r').read()

    print(interview_text)

    vocalize_interview(interview_text)
