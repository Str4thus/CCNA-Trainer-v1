import random
from .question import *

training_questions = [q.question_number for q in get_all_questions()] # Ids
    
def get_train_question_data(question_id):
    if question_id not in training_questions:
        return None
    
    question = get_question(question_id)
    answers = get_answers_to_question(question_id)
    
    return (question, answers)

def switch_train_question(current_index, to_next):
    if (not to_next and current_index - 1 < 0) or (to_next and current_index + 1 > len(training_questions) - 1): # Return current question if out of bounds
        return training_questions[current_index], current_index
    
    next_index = current_index + 1 if to_next else current_index - 1
    current_train_question_id = training_questions[next_index]
    print("yeet", next_index)
    return current_train_question_id, next_index

def get_random_training_question():
    random_index = random.randint(0, len(training_questions))
    return training_questions[random_index], random_index

def get_index_of_question(question_id):
    return training_questions.index(int(question_id))