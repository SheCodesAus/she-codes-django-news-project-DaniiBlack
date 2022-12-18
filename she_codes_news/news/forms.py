from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import NewsStory, Comment

User = get_user_model()

class StoryForm(ModelForm):
    class Meta:
        model = NewsStory
        fields = ['title', 'pub_date', 'content', 'image_url', 'categories']
        widgets = {
            'pub_date': forms.DateInput(format=('%m/%d/%Y'),
            attrs={
                'class':'form-control',
                'placeholder':'Select a date',
                'type':'date'
                }
            ),
        }

ORDER_CHOICE= (
    ('', "newest first"),
    ('oldfirst', "oldest first")
)

class FilterForm(forms.Form):
    categories = forms.ChoiceField(label="categories", choices=[('', '----'), ('clickbait','Clickbait'), ('politics','Politics'), ('travel','Travel'), ('badbitch', 'Bad bitch, its a genre')], required=False)
    categories.widget.attrs.update({'class' : 'categories-input'})
    author = forms.ModelChoiceField(label="author", queryset=User.objects.all(), required=False)
    author.widget.attrs.update({'class' : 'author-input'})
    search = forms.CharField(label="search", required=False)
    search.widget.attrs.update({'class' : 'search-input'})

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]