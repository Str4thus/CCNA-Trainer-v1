from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .logic import *

# Template views
def dashboard_tv(request):
    terminate_active_quiz()
    return render(request, "trainer/dashboard.html")

def quiz_tv(request):
    try:
        question, answers = get_current_quiz_question_data()
    except TypeError:
        return redirect("dashboard")
    
    context = {
        "is_multiple_choice": len(answers) > 1,
        "question": question,
        "answers": answers,
    }

    if question.question_type == "match":
        context["answer_image_url"] = answers[0].answer_text # Since a match question has only one answer (the image)

    return render(request, "trainer/quiz.html", context)

def training_tv(request, question_id): # question_id is the question_number! (since the question number is consistent, the id changes with every sync)
    try:
        question, answers = get_train_question_data(question_id)
    except TypeError:
        return redirect("dashboard")
    
    context = {
        "is_training": True,
        "is_multiple_choice": len(answers) > 1,
        "question": question,
        "answers": answers,
    }

    if question.question_type == "match":
        if question.question_number == 154:
            context["answer_image_url"] = "https://itexamanswers.net/wp-content/uploads/2016/02/23-final-ccna2.jpg"
        else:
            context["answer_image_url"] = answers[0].answer_text

    return render(request, "trainer/train.html", context)

def sync_tv(request):
    sync_database()
    return render(request, "trainer/dashboard.html")



# API Views
def start_training_av(request):
    result = {
        "id": get_first_question().question_number,
        "index": get_index_of_question(get_first_question().question_number)
    }
    
    return JsonResponse(result)


def create_quiz_av(request):
    post_params = request.POST

    size = post_params["size"]
    
    try:
        question_filter = post_params["filter"]
    except KeyError:
        question_filter = None
        
    create_quiz(size, question_filter)

    result = {
        "id": get_current_quiz_question_id()
    }
    
    return JsonResponse(result)

def evaluate_quiz_av(request):
    pass


def index_of_question_av(request):
    post_params = request.POST
    result = {
            "index": get_index_of_question(post_params["questionId"])
        }

    return JsonResponse(result)

def switch_av(request):
    post_params = request.POST
    
    try:
        post_params["isRandom"]
        q_id, index = get_random_training_question()
        result = {
            "id": q_id,
            "index": index
        }
    except KeyError:
        q_id, index = switch_train_question(int(post_params["index"]), bool(int(post_params["toNext"])))
        print(post_params["index"])
        print(index)
        result = {
            "id": q_id,
            "index": index
        }
    
    return JsonResponse(result)

def evaluate_question_av(request): # question_id is the question_number! (since the question number is consistent, the id changes with every sync)
    post_params = request.POST
    
    result = {
        "correct": evaluate_question(post_params.get("question_id"), post_params.getlist("chosenAnswers[]")),
        "answers": get_correct_answers_to_question(post_params.get("question_id")),
    }

    return JsonResponse(result)

