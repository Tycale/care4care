#!/bin/sh
python manage.py run_gunicorn -b 127.0.0.1 -w 2