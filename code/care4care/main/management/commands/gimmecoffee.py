# GimmeCoffee.py
# --------------
# Get Coffeescript files from the COFFEE_DIR directory, and
# outputs the compiled Javascript to the JS_DIR directory.
#
# Author: Michael Heraly
# Date: November 2014

from django.core.management.base import BaseCommand
import os
import coffeescript


CURRENT_DIR_PATH = os.path.abspath('.')     # = app directory (directory containing manage.py)
APP_NAME   = 'main'
APP_DIR    = os.path.join(CURRENT_DIR_PATH, APP_NAME)
COFFEE_DIR = os.path.join(APP_DIR, 'static/coffee')
JS_DIR     = os.path.join(APP_DIR, 'static/js')


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.contentChanged = False
        coffee_files = os.walk(COFFEE_DIR)
        for (dirpath, dirnames, filenames) in coffee_files:
            self.compile_files(filenames)

        if self.contentChanged:
            # Django doc (https://docs.djangoproject.com/en/1.7/howto/custom-management-commands/)
            # tells that it is better to use 'self.stdout.write'
            self.stdout.write('Here is your coffee, sir!')
        else:
            self.stdout.write('Your cup is already full, sir!')


    def file_name_without_ext (self, file_name):
        (shortname, extension) = os.path.splitext(file_name)
        return shortname


    def compile_files(self, coffee_files):
        for coffee in coffee_files:
            f = open(os.path.join(COFFEE_DIR, coffee), 'r')
            code = f.read()
            output_file_name = self.file_name_without_ext(coffee)
            self.compile_coffee_to_js(output_file_name, code)
            f.close()


    def compile_coffee_to_js (self, coffee_name, code):
        # Compilation
        compiled_js = None
        try:
            compiled_js = coffeescript.compile(code)
        except Exception as e:
            self.stdout.write('A problem occurred while preparing your coffee...')
            print(e)
            exit(1)


        # Getting the output file
        js_file_name = coffee_name + '.js'
        js_output_file_name = os.path.join(JS_DIR, js_file_name)
        # Compare new content with the previous one
        if os.path.isfile(js_output_file_name):
            js_file = open(js_output_file_name, 'r')
            js_content = js_file.read()
            js_file.close()
            if compiled_js == js_content:
                # Content unchanged
                return
        # Content changed
        self.stdout.write('Serving coffee... '+js_file_name)
        self.contentChanged = True
        # => update the content of the output file
        js_file = open(js_output_file_name, 'w')
        # Write the js compiled from coffee
        js_file.write(compiled_js)
        js_file.close()

