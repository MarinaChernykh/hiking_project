from django import forms
from django.core.exceptions import ValidationError

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for users to set rating for trail and leave text comment.
    """
    class Meta:
        model = Comment
        fields = ('ranking', 'text')
        labels = {
            'ranking': 'Насколько вам понравился маршрут?',
            'text': 'Поделитесь впечатлениями о прогулке'
        }

    def clean(self):
        """Validates whether at least one field is filled in."""
        super().clean()
        ranking = self.cleaned_data.get('ranking')
        text = self.cleaned_data.get('text')
        if ranking is None and (text.strip() == '' or text is None):
            raise ValidationError('Вы должны заполнить хотя бы одно поле')


class SearchForm(forms.Form):
    """Form to enter search query."""
    query = forms.CharField()
