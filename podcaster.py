import os.path

import document_reader
import utils
from Editor import Editor
from SpeechGenerator import SpeechGenerator
from openai_utils import gpt4

output_directory = '/Users/georgekour/repositories/pdf_voice/outputs'


class Podcaster:

    @staticmethod
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
            elif utils.line_starts_with_name(line) and not line.startswith("Interviewer:"):
                print("Author")
                generator.add_turn(line[line.find(":")+1:], voice=2)

        generator.play_with_intro(output_folder=os.path.join(output_directory,'podcasts'), intro_file='Intro.wav')


if __name__ == '__main__':

    document = document_reader.ContentReader('/Users/georgekour/Downloads/98626_0_art_file_991363_rybdtr_convrt.pdf')

    # print(paper_text)
    ## google_test2speech(text)
    interview_text = Editor.create_podcast_transcript(document.get_content())
    #interview_text = open("/Users/georgekour/repositories/pdf_voice/outputs/interviews/interview_safety_paper.txt", 'r').read()
    #tags = ["humoristic", "explain to 5 years old", "informative"]
    tags = ["informative"]
    interview_text = Editor.edit_transcript(interview_text,tags, os.path.join(output_directory,'interviews'))

    # interview_text = open(
    #     '/outputs/content/transcript_Automatic Generation of Attention Rules For Containment of Machine Learning Model Errors.txt', 'r').read()

    print(interview_text)

    Podcaster.vocalize_interview(interview_text)
