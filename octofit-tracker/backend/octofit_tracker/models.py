from djongo import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.ObjectIdField(primary_key=True, editable=False)
    # Additional fields can be added here
    pass


class Team(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField('User', related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    calories_burned = models.PositiveIntegerField()
    date = models.DateField()
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')


class Workout(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    suggested_for = models.ManyToManyField('User', related_name='suggested_workouts', blank=True)


class LeaderboardEntry(models.Model):
    id = models.ObjectIdField(primary_key=True, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='leaderboard_entries')
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='leaderboard_entries')
    score = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'team', 'date')
