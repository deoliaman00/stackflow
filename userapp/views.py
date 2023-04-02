from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import permissions, status,generics
from .serializers import UserCreateSerializer, UserSerializer,QuestionCreateSerializer,QuestionSerializer,AnswerSerializer,CommentSerializer,QuestionUpdateSerializer,AnswerUpdateSerializer,QCommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .models import Question,Answer,Comment,QComment
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser

user_account = get_user_model()
class RegisterView(APIView):
  def post(self, request):
    data = request.data

    serializer = UserCreateSerializer(data=data)

    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.create(serializer.validated_data)
    user = UserSerializer(user)

    return Response(user.data, status=status.HTTP_201_CREATED)



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            # delete the refresh token from the database
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            print(refresh_token)
            token.blacklist()
            # return a success response
            return Response({'success': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            # return an error response
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

      
class RetrieveUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = request.user
    user = UserSerializer(user)

    return Response(user.data, status=status.HTTP_200_OK)

class CreateQuestionAPIView(CreateAPIView):
    serializer_class=QuestionCreateSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)

    def create(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all().order_by(F('created_at').desc(nulls_last=True))
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# try to make it reusable
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CreateAnswerAPIView(CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        question=serializer.validated_data['question']
        serializer.save(author=self.request.user)
        question.num_answers=Answer.objects.filter(question=question).count()
        question.save()
            
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, answer_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, answer_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, answer_id):
        answer = Answer.objects.get(id=answer_id)
        serializer.save(author=self.request.user, answer=answer)

class QCommentView(generics.CreateAPIView):
   queryset=Comment.objects.all()
   serializer_class=QCommentSerializer
   permission_classes=[IsAuthenticatedOrReadOnly]
   def perform_create(self, serializer,*args, **kwargs):
      question_id=self.kwargs['question_id']
      question=Question.objects.get(id=question_id)
      serializer.save(author=self.request.user,question=question)
      question.num_comments+=1
      question.save()

class QCommentListView(generics.ListAPIView):
    serializer_class = QCommentSerializer
    # permission_classes = [AllowAny]

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        queryset = QComment.objects.filter(question_id=question_id)
        return queryset
      
class AnswerList(generics.ListCreateAPIView):
   serializer_class=AnswerSerializer
   def get_queryset(self):
      question_id=self.kwargs['question']
      return Answer.objects.filter(question_id=question_id)

class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset=Answer.objects.all()
   serializer_class=AnswerSerializer

## now we will be adding comment section to the answers list
class CommentList(generics.ListCreateAPIView):
   queryset=Comment.objects.all()
   serializer_class=CommentSerializer

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset=Comment.objects.all()
   serializer_class=CommentSerializer

class CommentListView(generics.ListAPIView):
   serializer_class=CommentSerializer
   def get_queryset(self):
      answer=self.kwargs.get('answer')
      queryset=Comment.objects.filter(answer=answer)
      return queryset
   


class QuestionUpdateAPIView(generics.UpdateAPIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionUpdateSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        upvotes = request.data.get('upvotes', None)
        downvotes = request.data.get('downvotes', None)
        title=request.data.get('title',None)
        body=request.data.get('body',None)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class AnswerUpdateAPIView(generics.UpdateAPIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerUpdateSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        upvotes = request.data.get('upvotes', None)
        downvotes = request.data.get('downvotes', None)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
