from django import forms

from books.models import BookNotes


class BookNotesEditForm(forms.ModelForm):
    class Meta:
        model = BookNotes
        fields = "__all__"
        exclude = ['user', 'addtime', 'clicknum', 'favornum', 'commtnum']
