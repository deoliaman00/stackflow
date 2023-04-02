from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Question,Answer,Comment,QComment,Tag
from ckeditor.fields import RichTextField
import logging


class UserCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email', 'password')

  def validate(self, data):
    user = User(**data)
    password = data.get('password')

    try:
      validate_password(password, user)
    except exceptions.ValidationError as e:
      serializer_errors = serializers.as_serializer_error(e)
      raise exceptions.ValidationError(
        {'password': serializer_errors['non_field_errors']}
      )

    return data


  def create(self, validated_data):
    user = User.objects.create_user(
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name'],
      email=validated_data['email'],
      password=validated_data['password'],
    )

    return user


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id','first_name', 'last_name', 'email',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=('id','name',)

# this is the serializer that is handling the post request of a question getting posted by the user     
class QuestionCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = Question
        fields = ['id','first_name','title', 'user', 'body', 'tags', 'upvotes', 'downvotes', 'num_answers', 'num_comments', 'created_at','image',]
    def create(self,validated_data):
        print("This is line no 1 ")
        print(validated_data)
        tags=validated_data.pop('tags')
        print("This is line no 2 ")
        print(tags)
        question=Question.objects.create(**validated_data)
        print("This is line no 3 ")
        print(question)
        question.tags.add(*tags)
        print("This is line no 4 ")
        print(question)
        return question
    
class QuestionSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = representation['created_at'][:10]
        return representation
    class Meta:
        model = Question
        fields = ['id','first_name','title','image', 'user', 'body', 'tags', 'upvotes', 'downvotes', 'num_answers', 'num_comments', 'created_at']

#This will be the serializer that will take care of the Answer of the Question that was made

class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id','body','title','upvotes', 'downvotes')

    def update(self, instance, validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.body=validated_data.get('body',instance.body)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            if 'upvotes' in validated_data:
                if user in instance.upvoted_by.all():
                    instance.upvoted_by.remove(user)
                    instance.upvotes -= 1
                else:
                    instance.upvoted_by.add(user)
                    instance.upvotes += 1
                    if user in instance.downvoted_by.all():
                        instance.downvoted_by.remove(user)
                        instance.downvotes -= 1
            elif 'downvotes' in validated_data:
                if user in instance.downvoted_by.all():
                    instance.downvoted_by.remove(user)
                    instance.downvotes -= 1
                else:
                    instance.downvoted_by.add(user)
                    instance.downvotes += 1
                    if user in instance.upvoted_by.all():
                        instance.upvoted_by.remove(user)
                        instance.upvotes -= 1
        instance.save()
        return instance

class AnswerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'upvotes', 'downvotes')

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            if 'upvotes' in validated_data:
                if user in instance.upvotes_by.all():
                    instance.upvotes_by.remove(user)
                    instance.upvotes -= 1
                else:
                    instance.upvotes_by.add(user)
                    instance.upvotes += 1
                    if user in instance.downvotes_by.all():
                        instance.downvotes_by.remove(user)
                        instance.downvotes -= 1
            elif 'downvotes' in validated_data:
                if user in instance.downvotes_by.all():
                    instance.downvotes_by.remove(user)
                    instance.downvotes -= 1
                else:
                    instance.downvotes_by.add(user)
                    instance.downvotes += 1
                    if user in instance.upvotes_by.all():
                        instance.upvotes_by.remove(user)
                        instance.upvotes -= 1
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
  author=serializers.ReadOnlyField(source='author.first_name')
  answer=serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all())
  def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = representation['created_at'][:10]
        return representation
  class Meta:
    model=Comment
    fields=['id','body','created_at','author','answer']

class QCommentSerializer(serializers.ModelSerializer):
   author=serializers.ReadOnlyField(source='author.first_name')
   def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = representation['created_at'][:10]
        return representation
   class Meta:
      model=QComment
      fields=['body','author','created_at']


class AnswerSerializer(serializers.ModelSerializer):
  comment=CommentSerializer(many=True,read_only=True)
  author=serializers.ReadOnlyField(source='author.first_name')
  question=serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(),required=True)
  def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = representation['created_at'][:10]
        return representation
  class Meta:
    model=Answer
    fields=['id','body','created_at','question','comment','upvotes','downvotes','created_at','author']
