from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import RegisterView, RetrieveUserView,CreateQuestionAPIView,QuestionDetail,QuestionList,AnswerList,AnswerDetail,CommentList,CommentDetail,CreateAnswerAPIView,LogoutView,CommentCreateView,QuestionUpdateAPIView,AnswerUpdateAPIView,CommentListView,QCommentView,QCommentListView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('register/', RegisterView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('user/', RetrieveUserView.as_view()),
    path('questions/create/',CreateQuestionAPIView.as_view(),name='create-question'),
    path('questions/', QuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('answers/create/',CreateAnswerAPIView.as_view()),
    path('questions/<int:question>/answers/',AnswerList.as_view()),
    path('answers/<int:pk>/',AnswerDetail.as_view()),
    path('comments/',CommentList.as_view()),
    path('comments/<int:pk>/',CommentDetail.as_view()),
    path('answers/<int:answer>/comment/', CommentListView.as_view(), name='comment-list'),
    path('answers/<int:answer_id>/comments/',CommentCreateView.as_view()),
    path('questions/<int:pk>/update/',QuestionUpdateAPIView.as_view()),
    path('answers/<int:pk>/update/',AnswerUpdateAPIView.as_view()),
    path('questions/<int:question_id>/comments/create/', QCommentView.as_view(), name='question-comments'),
    path('questions/<int:question_id>/comments/', QCommentListView.as_view(), name='qcomment_list'),
]