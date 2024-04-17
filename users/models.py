from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from storages.backends.s3boto3 import S3Boto3Storage

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=30,blank=False)
    email = models.EmailField(unique=True)
    # 管理サイトにアクセスできるか
    is_staff = models.BooleanField(default=False)
    # ログイン中しているかどうか
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # ユーザー作成やスーパーユーザー作成などのカスタムロジックを実装
    objects = CustomUserManager()

    @property
    def profile(self):
        Profile.objects.get(user=self)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Profile.objects.get_or_create(user=self)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    affiliation = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', storage=S3Boto3Storage(), blank=True, null=True)

    # def __str__(self):
    #     return self.user

class Job(models.Model):
    name = models.CharField(max_length=100)

class Skill(models.Model):
    name = models.CharField(max_length=100)

class UserJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

class Product(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='product_thumbnails/', storage=S3Boto3Storage(), blank=True, null=True)
    detail_url = models.URLField(max_length=200, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='receiver')
    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.receiver}"

    class Meta:
        ordering = ['created_at']

    @property
    def sender_user(self):
        return self.sender
    
    @property
    def receiver_user(self):
        return self.receiver

# 元々のmodel
# class Job(models.Model):
#     name = models.CharField(max_length=100)

# class Skill(models.Model):
#     name = models.CharField(max_length=100)

# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     affiliation = models.CharField(max_length=255, default='')
#     profile = models.TextField()
#     profile_image = models.ImageField(upload_to='profile_images/')
#     jobs = models.ManyToManyField(Job, through='StudentJob')
#     skills = models.ManyToManyField(Skill, through='StudentSkill')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class StudentJob(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     job = models.ForeignKey(Job, on_delete=models.CASCADE)

# class StudentSkill(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

# class Recruiter(models.Model):
#     name = models.CharField(max_length=100)
#     company = models.CharField(max_length=100)
#     industry = models.CharField(max_length=100)
#     role = models.CharField(max_length=100)
#     company = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     profile = models.TextField()
#     profile_image = models.ImageField(upload_to='profile_images/')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class StudentRecruiter(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)

# class Chatroom(models.Model):
#     student_recruiter = models.ForeignKey(StudentRecruiter, on_delete=models.CASCADE)
#     matching_status = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class ChatroomMessage(models.Model):
#     chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)