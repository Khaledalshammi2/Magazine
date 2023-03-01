from django import forms
from .models import Author
from django.utils.translation import gettext as _
from django.utils.translation import ngettext_lazy

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

    def clean_bio(self):
        message = _("too short")
        bio = self.cleaned_data["bio"]
        if len(bio) > 5:
            return bio
        else:
            raise forms.ValidationError(message)


# another example
# class AuthorForm2(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = '__all__'
#     def clean_bio(self):
#         error_message = ngettext_lazy(
#             "%d letter, too short",
#             "%d letters, too short",
#         )
#         bio = self.cleaned_data["bio"]
#         if len(bio) > 5:
#             return bio
#         else:
#             raise forms.ValidationError(error_message % len(bio))
