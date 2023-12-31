import os.path

import utils
from openai_utils import gpt4


class Editor:
    create_podcast_systemprompt = """
You are provided with a text extracted from a scientific paper in PDF format. 
Your objective is to simulate a podcast of an interview between the interviewer and the leading author. 
The interview should clarify to the listener the information in the paper and create an intelligible interview that can be effectively vocalized. 
Make sure you do not miss any important insights and takeaway points. 
Each turn should be presented as a single line, which may encompass one or more sentences. 
Ensure that you do not attribute any previous findings or work utilized by the author to the author himself. 
If there is a requirement for technical terminology or background information, take the time to discuss and elucidate them with the author. 
This will ensure that the podcast remains accessible to a wide audience. 
Minimize the use of specialized terms and abbreviations whenever feasible. 
If needed to mention, the interviewer name is Rowan. 
The name of the podcast is the Smallcaster so make sure you mention that in the welcome statement of the interviewer. 
In creating the transcript each line must begin with either 'Interviewer:' or 'Author:'.
"""
    edit_podcast_systemprompt = """
Edit the following podcast interview transcript according to the user instructions.
In any case, make sure you keep the main scientific points.
"""

    @staticmethod
    def create_podcast_transcript(paper_content):
        return gpt4(Editor.create_podcast_systemprompt, paper_content)

    @staticmethod
    def edit_transcript(transcript, tags):
        userprompt = ''
        for tag in tags:
            if tag == "humoristic":
                userprompt += f"\nAdd a touch of humor to the transcript."
            elif tag == "for_child":
                userprompt += f"\nSimplify the content to make it understandable to a 5-year-old"
            elif tag == "informative":
                userprompt += f"\nEnhance the content with additional informative details."

        edited_transcript = gpt4(Editor.edit_podcast_systemprompt+userprompt, transcript)

        return edited_transcript

    @staticmethod
    def save(transcript, output_folder):
        open(os.path.join(output_folder,f"interview_{utils.get_timestamp()}.txt"), "w").write(transcript)
