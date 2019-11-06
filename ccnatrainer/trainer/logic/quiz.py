import random

from .question import *

_quiz_question_ids = []
_quiz_question_cursor = None

def get_current_quiz_question_data():
    question = get_question(get_current_quiz_question_id())
    answers = get_answers_to_question(get_current_quiz_question_id())
    
    return (question, answers)
    
def create_quiz(size, question_filter):
    global _quiz_question_ids
    global _quiz_question_cursor
    
    total_number_of_questions = Question.objects.count()
    
    question_id_pool = list(range(1, total_number_of_questions + 1))
    
    for question in unusable_questions:
        question_id_pool.remove(question)
    
    _quiz_question_ids = random.sample(question_id_pool, int(size))
    _quiz_question_cursor = 0

def get_current_quiz_question_id():
    global _quiz_question_ids
    global _quiz_question_cursor
    
    return _quiz_question_ids[_quiz_question_cursor]

def switch_quiz_question(to_next):
    global _quiz_question_ids
    global _quiz_question_cursor
    
    if not is_quiz_active():
        return None
    
    if (not to_next and _quiz_question_cursor - 1 < 0) or (to_next and _quiz_question_cursor + 1 > len(_quiz_question_ids) - 1): # Return current question if out of bounds
        return _quiz_question_ids[_quiz_question_cursor]
    
    _quiz_question_cursor = _quiz_question_cursor + 1 if to_next else _quiz_question_cursor - 1

    return _quiz_question_ids[_quiz_question_cursor]

def terminate_active_quiz():
    global _quiz_question_ids
    global _quiz_question_cursor
    
    _quiz_question_ids = []
    _quiz_question_cursor = None

def is_quiz_active():
    global _quiz_question_ids
    global _quiz_question_cursor
    return bool(len(_quiz_question_ids) > 0 and _quiz_question_cursor != None)
