from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.template.defaultfilters import slugify

from .models import Songs


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email',)


class AddSongForm(forms.ModelForm):
    class Meta:
        model = Songs
        fields = ['name', 'file', 'cover', 'text', 'temp', 'ton', 'hashtags', 'price']

    def save(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        slug = slugify(cleaned_data['name'])
        instance = super().save(commit=False)
        instance.slug = slug
        instance.save()
        return instance


