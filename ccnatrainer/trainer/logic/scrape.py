import re
import requests

from bs4 import BeautifulSoup

from .question import unusable_questions

def scrape_question_data():
    r = requests.get("https://itexamanswers.net/ccna-2-v6-0-final-exam-answers-routing-switching-essentials.html")
    soup = BeautifulSoup(r.content, "html.parser")
    return _retrieve_question_data(soup.find_all("div", class_="pf-content")[0].select("div > p"))


def _retrieve_question_data(elements):
    question_pattern = "^\A\d+\.\s"
    questions = []

    for element in elements:
        if re.match(question_pattern, element.get_text()): # if its a question
            question_data = _generate_question_data(element) # Can be None, if question is in "unusable_questions"
            if (question_data):
                questions.append(question_data)
        
    return questions

def _determine_question_type(question_text):
    question_text = question_text[question_text.find(".")+2:]
    if (question_text.find("Refer to the exhibit") == 0):
        question_type = "image"
    elif (question_text.find("Fill in the blank") == 0):
        question_type = "fill"
    elif (question_text.find("Match") == 0):
        question_type = "match"
    else:
        question_type = "normal"

    return question_type

def _generate_question_data(element):
    """
        Don't look into this. Please. 
        There are so many special cases due to the huge inconsistency of the DOM-Tree when it comes to questions and answers
        You have been warned.
    """
    question_number = int(element.get_text()[:element.get_text().find(".")])

    if (question_number in unusable_questions):
        return None

    question_data = {
        "question_number": int(question_number), # Cutoff '.' 
        "question_type": _determine_question_type(element.get_text()),
        "question_element": element,
        "question_text": element.get_text(),
        
        "has_image": False,
        "image_url": None,
        
        "answer_element": element.next_sibling.next_sibling if element.next_sibling == "\n" else element.next_sibling,
        "possible_answers": [],
        "correct_answers": [],
    }


    # Find image url, if present
    if (question_data["question_type"] == "match"):
        if len(question_data["question_element"].find_all("img")) == 2:
            question_data["answer_element"] = question_data["question_element"]
            images = question_data["answer_element"].find_all("img")
        else:
            images = question_data["answer_element"].find_all("img") if len(question_data["answer_element"].find_all("img")) > 0 else question_data["question_element"].find_all("img") 
                
            if (len(images) != 2):
                images = question_data["question_element"].find_all("img") if len(question_data["question_element"].find_all("img")) > 0 else question_data["question_element"].find_all("img") 
                next_element = question_data["question_element"].next_sibling.next_sibling if question_data["question_element"].next_sibling == "\n" else question_data["question_element"].next_sibling
                images.append(next_element.find("img"))

            if (len(images) != 2):
                next_element = question_data["answer_element"].next_sibling.next_sibling if question_data["answer_element"].next_sibling == "\n" else question_data["answer_element"].next_sibling
                images.append(next_element.find("img"))
                
        question_data["image_url"] = images[0]["src"]
        question_data["answer_element"] = images[1]
            
        question_data["has_image"] = True

    elif (question_data["question_type"] == "image"):
        try:
            if question_data["question_element"].find("img"):
                question_data["image_url"] = question_data["question_element"].find("img")["src"]
            else:
                next_element = question_data["question_element"].next_sibling.next_sibling if question_data["question_element"].next_sibling == "\n" else question_data["question_element"].next_sibling
                next_next_element = next_element.next_sibling.next_sibling if next_element.next_sibling == "\n" else next_element.next_sibling

                question_data["image_url"] = next_element.find("img")["src"]
                question_data["answer_element"] = next_next_element
                
            question_data["has_image"] = True
            
        except (TypeError):
            # "Refer to the exhibit" is not a question with an image
            question_data["question_type"] = "normal"


    # Select correct answer
    if question_data["question_type"] == "match":
        question_data["correct_answers"] = [question_data["answer_element"]["src"]]

        if question_data["question_number"] == 154: # The solution pic comes first, but only in this question (wtf...?)
            question_data["correct_answers"], question_data["image_url"] = question_data["image_url"], question_data["correct_answers"][0]

    elif question_data["question_type"] == "fill":
        solution_indices = [match.start() for match in re.finditer("__", question_data["question_text"])]
        position_of_asterisk = question_data["question_text"].find("*")

        solution_start = solution_indices[0]
        solution_end = solution_indices[1] if solution_indices[1] > position_of_asterisk else position_of_asterisk + 1
        solution = question_data["question_text"][solution_start + 2 : solution_end].strip()

        question_data["question_text"] = question_data["question_text"][ : solution_start] + "_____" + question_data["question_text"][solution_end : ]
        
        if solution[-1] == "*":
            solution = solution[:-1]
        if solution[-1] == "_":
            solution = solution[:-2]

        question_data["correct_answers"] = [solution]
    
    else:
        if question_data["answer_element"].find("img"):
            question_data["answer_element"] = question_data["answer_element"].next_sibling.next_sibling

        if question_data["answer_element"].find_all("li"): # Multiple choice
            answer_elements = question_data["answer_element"].find_all("li")
            answers = []
            for answer_element in answer_elements:
                answer_text = answer_element.get_text()

                if answer_element.find("span"):
                    answer_text = answer_text[: -1]
                    question_data["correct_answers"].append(answer_text)

                answers.append(answer_text)
            
            question_data["possible_answers"] = answers
        else: # Single answer
            answer_element = question_data["answer_element"].find("strong")
            answer_text = answer_element.get_text()[: -1]
            question_data["correct_answers"] = answer_text

    return question_data


