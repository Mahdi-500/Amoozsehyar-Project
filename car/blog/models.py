from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class SignUp(models.Model):

    class GenderChoices(models.TextChoices):
        FEMALE = "FE", ("Female")
        MALE = "MA", ("Male")
        CORROSAN = 'CR', ("Corrosan")
    
    # ? user info
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(choices=GenderChoices.choices, default=GenderChoices.MALE, max_length=2)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    # ? date info
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username


class Login(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class Post(models.Model):

    class EngineChoices(models.TextChoices):
        V = 'V', ("V type")
        I = "i", ("inline")
        F = "F", ("Flat")
        B = "B", ("Boxer")
        W = "W", ("W type")
        R = "R", ("Rotary")

    class StatusChoices(models.TextChoices):
        DRAFT = "DR", ("Draft")
        ACCEPTED = "AC", ("Accept")
        REJECTED = "RJ", ("Rejected")

    class Published(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(status=Post.StatusChoices.ACCEPTED)

    # ? customized manager
    objects = models.Manager()  # default manager
    Publish = Published()  # new manager

    # ? user info
    author = models.ForeignKey(SignUp, on_delete=models.CASCADE, related_name='author')

    # ? post info
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    engine_type = models.CharField(choices=EngineChoices, default=EngineChoices.I, max_length=2)
    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.DRAFT, max_length=2)

    # ? date info
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    status_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "-created"
            ]
        
        indexes = [models.Index(fields=[
            'author'
            ])]

    def get_absolute_url(self):
        return reverse("blog:post detail", kwargs={"id":self.id, "username":self.author.username})