from django import forms

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


class SearchForm(forms.Form):
    """Form to enter search query."""
    query = forms.CharField()
