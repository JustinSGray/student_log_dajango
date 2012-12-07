import sqlite3

from django.core.management.base import BaseCommand, CommandError

from log.models import User

class Command(BaseCommand):

    def handle(self, *args, **option):
      user_name = args[0]
      email = args[1]
      password = args[2]

      user = User.objects.create_user(user_name, email, password)
      user.save()