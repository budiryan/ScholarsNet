import os


# Security is for later
WTF_CSRF_ENABLED = False
SECRET_KEY = 'you-will-never-guess'
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'sqlite', 'paperDB.db')
