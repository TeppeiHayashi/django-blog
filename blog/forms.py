from django import forms
from blog.models import Comment, Reply
from blog.widgets import CustomMarkdownxWidget


class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'text')
        widgets = {
            'name': forms.widgets.TextInput(
                attrs={'value': '名無し'}
            ),
            'text': CustomMarkdownxWidget(
                attrs={'placeholder': '本文: Markdown形式で記述できます。',
                       'class': 'active'}),
        }

    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)

    def save(self):
        comment = super().save(commit=False)
        comment.post = self.post
        comment.save()
        return comment


class CreateReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ('name', 'text')
        widgets = {
            'name': forms.widgets.TextInput(
                attrs={'value': '名無し'}
            ),
            'text': CustomMarkdownxWidget(
                attrs={'placeholder': '本文: Markdown形式で記述できます。',
                       'class': 'active'}),
        }

    def __init__(self, *args, **kwargs):
        self.comment = kwargs.pop('comment', None)
        super().__init__(*args, **kwargs)

    def save(self):
        reply = super().save(commit=False)
        reply.comment = self.comment
        reply.save()
        return reply
