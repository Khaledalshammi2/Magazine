from django import forms
from .models import Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

    def clean_bio(self):
        bio = self.cleaned_data["bio"]
        if len(bio) > 3:
            return bio
        else:
            raise forms.ValidationError("too short")