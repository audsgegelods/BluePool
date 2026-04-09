1. execute 'pip install googlemaps'
2. execute 'pip install django-htmx"
3. modify settings.py such that GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
4. add 'django_htmx' to INSTALLED_APPS and 'django_htmx.middleware.HtmxMiddleware' to MIDDLEWARE
5. insert GOOGLE_API_KEY = <Key> into the .env
