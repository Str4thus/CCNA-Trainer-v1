import json

from trainer.models import *
from .scrape import scrape_question_data

def sync_database(): 
    print("Syncing database...")
    questions = scrape_question_data()

    clear_database()
    _populate_database(questions)

    print("Synced database!")
     
def clear_database():
    Question.objects.all().delete()
    print("Cleared questions...")

    Answer.objects.all().delete()
    print("Cleared answers...")



def _populate_database(questions):
    print("Populating database with " + str(len(questions)) + " entries...")

    for question in questions:
        # Create Question Entry
        q = Question(question_number=question["question_number"], question_type=question["question_type"], 
                        question_text=question["question_text"], has_image=question["has_image"])
        if q.has_image:
            q.image_url = question["image_url"]
        q.save()

        # Create Answer Entries
        if (len(question["possible_answers"]) == 0):
            a = Answer(question=q, answer_text=question["correct_answers"][0], is_correct=True)
            a.save()
        else:
            for answer_text in question["possible_answers"]:
                a = Answer(question=q, answer_text=answer_text, is_correct=(answer_text in question["correct_answers"]))
                a.save()
    
    print("Populated database!")

