#!/bin/sh
gunicorn care4care.wsgi -b 127.0.0.1:8123 -w 2