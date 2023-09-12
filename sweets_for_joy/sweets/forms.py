from django.forms import ModelForm
from .models import Catalog


class TodoForm(ModelForm):
    class Meta:
        model = Catalog
        fields = ['title', 'picture', 'description', 'favourite']


class WorkForm(ModelForm):
    class Meta:
        model = Catalog
        fields = ('title', 'picture', 'description', 'price', 'date_completed', 'favourite', 'user')


class ViewForm(ModelForm):
    class Meta:
        model = Catalog
        fields = ['title', 'picture']