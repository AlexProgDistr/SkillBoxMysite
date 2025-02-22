from django.db import models
from django.contrib.auth.models import User


def avatar_directory_path(instance: "Profile", filename: str) -> str:
    return f"users/user_{instance.pk}/avatar/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500,  blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_directory_path)