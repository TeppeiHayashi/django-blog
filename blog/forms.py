from django import forms
from blog.models import Comment, Reply
from blog.widgets import CustomMarkdownxWidget

class CreateCommentForm(forms.ModelForm):
    
    class Meta:
        model =Comment
        fields = ('name', 'text')
        widgets = {
            'text': CustomMarkdownxWidget(
                attrs={'placeholder': '本文: Markdown形式で記述できます。',
                       'class': 'active'}),
        }
        
class CreateReplyForm(forms.ModelForm):
     
    class Meta:
        model = Reply
        fields = ('name', 'text')
        widgets = {
            'text': CustomMarkdownxWidget(
                attrs={'placeholder': '本文: Markdown形式で記述できます。',
                       'class': 'active'}),
        }
        