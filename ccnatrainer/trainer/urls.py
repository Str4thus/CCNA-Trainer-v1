from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard_tv, name='dashboard'),
    #path('sync/', views.sync_tv, name='sync'),
    
    #path('quiz/', views.quiz_tv, name="quiz"),
    #path('quiz/create/', views.create_quiz_av, name="quiz_create"),
    #path('quiz/evaluate/', views.evaluate_quiz_av, name="quiz_evaluate"),
    
    path('train/', views.start_training_av, name="start_train"),
    path('train/<int:question_id>/', views.training_tv, name='train'),
    
    path('question/evaluate/', views.evaluate_question_av, name='question_evaluate'),
    path('switch/', views.switch_av, name='switch'),#
    path('question/index/', views.index_of_question_av, name='index')
]