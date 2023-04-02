from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from ckeditor.fields import RichTextField

class UserAccountManager(BaseUserManager):
  def create_user(self, first_name, last_name, email, password=None):
    if not email:
      raise ValueError('Users must have an email address')

    email = self.normalize_email(email)
    email = email.lower()

    user = self.model(
      first_name=first_name,
      last_name=last_name,
      email=email,
    )

    user.set_password(password)
    user.save(using=self._db)

    return user
  
  def create_superuser(self, first_name, last_name, email, password=None):
    user = self.create_user(
      first_name,
      last_name,
      email,
      password=password,
    )

    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)

    return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.EmailField(unique=True, max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserAccountManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']

  def __str__(self):
    return self.email

class Tag(models.Model):
   name=models.CharField(max_length=10)
   def __str__(self):
      return self.name
  
def upload_to(instance,filename):
   return 'images/{filename}'.format(filename=filename)
   
class Question(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,unique=True)
    body = models.TextField()
    # info=RichTextField()
    ## add a image in the models
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,related_name='questions')
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    num_answers = models.PositiveIntegerField(default=0)
    num_comments = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvoted_by = models.ManyToManyField(UserAccount, blank=True,related_name='upvoted_questions')
    downvoted_by = models.ManyToManyField(UserAccount, blank=True,related_name='downvoted_questions')
    tags = models.ManyToManyField(Tag)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to=upload_to, blank=True,null=True)
    def __str__(self):
        return self.title

    def get_tags_display(self):
        return [choice[1] for choice in self.GENRE_CHOICES if choice[0] in self.tags]

    def save(self, *args, **kwargs):
        if not self.first_name:
            self.first_name = self.user.first_name
        super().save(*args, **kwargs)

# So the problem here occuring here is in the admin we are g

class Answer(models.Model):
   body=models.TextField()
   created_at=models.DateTimeField(auto_now_add=True)
   author=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
   question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
   upvotes = models.PositiveIntegerField(default=0)
   downvotes = models.PositiveIntegerField(default=0)
   upvotes_by = models.ManyToManyField(UserAccount, blank=True,related_name='upvoted_answers')
   downvotes_by = models.ManyToManyField(UserAccount,blank=True,related_name='downvoted_answers')


   def __str__(self):
      return f"Answer by {self.author} on {self.question}"

class Comment(models.Model):
   body=models.TextField()
   created_at=models.DateTimeField(auto_now_add=True)
   author=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
   answer=models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='comment')

   def __str__(self):
      return f"Comment by {self.author} on {self.answer}"

class QComment(models.Model):
   body=models.TextField()
   question=models.ForeignKey(Question,on_delete=models.CASCADE)
   author=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
   created_at=models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f"Comment by {self.author} on {self.question}"

