from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Comment


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['description', 'image']
        labels = {
            'description': 'Описание поста',
            'image': 'Ваше фото',
        }

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Напишите здесь что-нибудь'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise ValidationError("no description :(")
        return description

    def clean_image(self):
        AVAILABLE_EXTENSIONS = ['jpeg', 'jpg', 'png', 'gif']
        image = self.cleaned_data.get('image')
        if image:
            extension = str(image.name).rsplit('.', 1)[-1]
            if not extension in AVAILABLE_EXTENSIONS:
                raise ValidationError('wrong extension! >.<"')
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Текст комментария"})
        }