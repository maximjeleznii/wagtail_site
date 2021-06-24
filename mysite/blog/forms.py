from django import forms

class DeleteCommentForm(forms.Form):
    comment_id = forms.CharField(max_length=1000, required=True)

class ToggleCommentForm(forms.Form):
    toggled_page = forms.CharField(max_length=1000, required=True)