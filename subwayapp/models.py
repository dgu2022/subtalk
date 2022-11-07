from django.conf import settings
from django.db import models
from django.utils import timezone

class SubwayForm(models.Model):
    user_key = models.ForeignKey('users.User', on_delete=models.CASCADE)
    subwayLineNumber = models.CharField(max_length=6)
    getOffStationName = models.CharField(max_length=20)
    trainNumber = models.CharField(max_length=4)
    userNickname = models.CharField(max_length=20)

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title