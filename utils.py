import datetime
import re


def remove_unreadable_items(text):

    text = re.sub(r'\|', '', text)  # Remove '|'
    text = re.sub(r'(\b\w{1,2}\b)', '', text)  # Remove single and two-letter words
    text = re.sub(r'\n', ' ', text)  # Replace newlines with spaces

    # Remove figure captions
    text = re.sub(r'Figure \d+', '', text)

    # Remove citations and references
    text = re.sub(r'\[\d+\]', '', text)

    # Remove any remaining non-alphanumeric characters
    text = re.sub(r'[^\w\s.,?!]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()


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

    text = re.sub(r"\[\d+?\]", "", text)
    # Remove captions
    text = re.sub(r"Figure\s+\d+?\s*:.+", "", text)

    return text

def line_starts_with_name(line):
    pattern = r'^\w+\s*:'
    return bool(re.match(pattern, line))


def get_timestamp():
	return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")



