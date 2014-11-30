from django.forms.widgets import RadioSelect

class OneJobSelect(RadioSelect):
    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        return [data.get(name, None)]

