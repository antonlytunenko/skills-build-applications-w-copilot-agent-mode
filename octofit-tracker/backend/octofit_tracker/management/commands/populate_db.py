from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, LeaderboardEntry
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data

        for obj in Activity.objects.all():
            obj.delete()
        for obj in LeaderboardEntry.objects.all():
            obj.delete()
        for obj in Workout.objects.all():
            obj.delete()
        for obj in Team.objects.all():
            obj.delete()
        # Workaround for Djongo SQLDecodeError: delete users one by one except superuser
        for user in User.objects.all():
            if not user.is_superuser:
                user.delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (superheroes)
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'first_name': 'Tony', 'last_name': 'Stark', 'team': marvel},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'first_name': 'Steve', 'last_name': 'Rogers', 'team': marvel},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'first_name': 'Peter', 'last_name': 'Parker', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'first_name': 'Bruce', 'last_name': 'Wayne', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'first_name': 'Clark', 'last_name': 'Kent', 'team': dc},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'first_name': 'Diana', 'last_name': 'Prince', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(
                username=u['username'],
                email=u['email'],
                first_name=u['first_name'],
                last_name=u['last_name'],
                password='password123'
            )
            u['team'].members.add(user)
            user_objs.append(user)

        # Create workouts
        workout1 = Workout.objects.create(name='Morning Cardio', description='30 minutes of running and jumping jacks')
        workout2 = Workout.objects.create(name='Strength Training', description='Pushups, squats, and pull-ups')
        workout1.suggested_for.set(user_objs[:3])  # Marvel
        workout2.suggested_for.set(user_objs[3:])  # DC

        # Create activities
        for user in user_objs:
            Activity.objects.create(
                user=user,
                activity_type='Running',
                duration=30,
                calories_burned=300,
                date=timezone.now().date(),
                team=user.teams.first()
            )

        # Create leaderboard entries
        for user in user_objs:
            LeaderboardEntry.objects.create(
                user=user,
                team=user.teams.first(),
                score=1000,
                date=timezone.now().date()
            )

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
