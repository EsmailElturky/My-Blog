from django.forms import ModelForm
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['user_name', 'user_email', 'text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].label = "Your name:"
        self.fields['user_email'].label = "Your email:"
        self.fields['text'].label = "Your comment:"
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Enter your name here'})
        self.fields['user_email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Enter your email here'})
        self.fields['text'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Enter your comment here', 'rows': 5})
