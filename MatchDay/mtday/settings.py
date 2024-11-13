import os
import django
from django.conf import settings
from django.db import models

# Step 1: Configure Django settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        'mtday',  # Add your app name here
    ]
)

# Step 2: Setup Django environment
django.setup()

# Step 3: Define User model (for sign up and login)
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    district = models.CharField(max_length=100)  # Add district information

    def __str__(self):
        return self.username

# Step 4: Migrate the database
if __name__ == "__main__":
    from django.core.management import call_command
    call_command('makemigrations', 'mtday')
    call_command('migrate')

    # Optional: Create a test user
    if not User.objects.filter(username="testuser").exists():
        User.objects.create(username="testuser", email="test@example.com", password="password123", district="")
        print("Test user created.")
    else:
        print("Test user already exists.")
