"""
Django settings for care4care project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import gettext_lazy as _
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '933db#k3=a5gccs)wl)a1tcek$3&!f3@zdywv1gevrh+t*&r_5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
    'django_jenkins',
    'pagination',
    'main',
    'branch',
    'news',
    'bootstrap3',
    'registration',
    'multiselectfield',
    'bootstrap3_datetime',
    'easy_thumbnails',
    'postman',
    'ajax_select',
    'rosetta',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "care4care.context_processors.member_type_global",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)


STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

ROOT_URLCONF = 'care4care.urls'

WSGI_APPLICATION = 'care4care.wsgi.application'


JENKINS_TASKS = (
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_pylint',
)

PYLINT_RCFILE = os.path.join(BASE_DIR, 'pylintrc')

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LANGUAGES = (
    ('fr', _('Français')),
    ('en', _('Anglais')),
    ('nl', _('Néerlandais')),
)

DEFAULT_LANGUAGE = 0

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/assets/'
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
#    '/var/www/static/',
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')


LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# django-registration-redux
# https://django-registration-redux.readthedocs.org/en/latest/quickstart.html
AUTH_USER_MODEL = 'main.User'
ACCOUNT_ACTIVATION_DAYS = 365
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#AutoComplete
AJAX_SELECT_BOOTSTRAP = False
AJAX_SELECT_INLINES = 'inline'

AJAX_LOOKUP_CHANNELS = {
       # pass a dict with the model and the field to search against
       'user'  : ('care4care.lookups', 'UserLookup'),
}

#Postman
POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_SHOW_USER_AS = 'get_full_name'
POSTMAN_AUTOCOMPLETER_APP = {
    'name': 'ajax_select',  # default is 'ajax_select'
    'field': 'AutoCompleteField',  # default is 'AutoCompleteField'
    'arg_name': 'channel',  # default is 'channel'
    'arg_default': 'user',  # no default, mandatory to enable the feature
}

PAGINATION_DEFAULT_PAGINATION = 15

SOCIALACCOUNT_ADAPTER = 'care4care.adapter.MyAccountAdapter'

ACCOUNT_EMAIL_VERIFICATION = "none"


SOCIALACCOUNT_PROVIDERS = \
    { 'google':
        { 'SCOPE': ['profile', 'email'],
          'AUTH_PARAMS': { 'access_type': 'online' } },
        'facebook':
           {'SCOPE': ['email', 'publish_stream'],
            'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
            'METHOD': 'oauth2',
            #'LOCALE_FUNC': 'path.to.callable',
            'VERIFIED_EMAIL': False,
            'VERSION': 'v2.2'}}
