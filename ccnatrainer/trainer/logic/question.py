from trainer.models import * 
from django.core.exceptions import ObjectDoesNotExist

from random import shuffle

# Questions that have no answer selected
unusable_questions = [192, 194]


def get_all_questions():
    return list(Question.objects.all())

def get_first_question():
    return Question.objects.first()
        
def get_question(question_id):
    try:
        return Question.objects.get(question_number=question_id)
    except ObjectDoesNotExist:
        return None
        
def get_answers_to_question(question_id):
    answer_list = list(Answer.objects.filter(question__question_number=question_id))
    shuffle(answer_list)
    return answer_list

def get_correct_answers_to_question(question_id):
    all_answers = get_answers_to_question(question_id)
    correct_answers = []

    for answer in all_answers:
        if answer.is_correct:
            if "_" in answer.answer_text: # Question 148
                answer.answer_text = answer.answer_text[:answer.answer_text.find("_")]
            correct_answers.append(answer.answer_text.lower().strip())
    
    return correct_answers

def evaluate_question(question_id, chosen_answers):
    if not chosen_answers:
        return False
    
    correct_answers = get_correct_answers_to_question(question_id)
    
    if len(chosen_answers) != len(correct_answers):
        return False

    for i in range(len(chosen_answers)):
        chosen_answers[i] = chosen_answers[i].lower().strip()

    for correct_answer in correct_answers:
        if correct_answer not in chosen_answers:
            return False

    return True

def get_random_question_id():
    question_list = list(Question.objects.all())
    shuffle(question_list)
    return question_list[0].question_number
