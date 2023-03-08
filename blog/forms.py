from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy
from django.forms import formset_factory


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

    profile_image = forms.ImageField(widget=forms.FileInput, label=_("Profile Image"))

    def clean_bio(self):
        message = _("too short")
        bio = self.cleaned_data["bio"]
        if len(bio) > 5:
            return bio
        else:
            raise forms.ValidationError(message)

    def clean_bio_ar(self):
        message = _("too short")
        bio_ar = self.cleaned_data["bio_ar"]
        if len(bio_ar) > 5:
            return bio_ar
        else:
            raise forms.ValidationError(message)

    def clean_name(self):
        message = _("This email address is already used.")
        name = self.cleaned_data['name']
        if Author.objects.filter(name=name).exists():
            raise forms.ValidationError(message)
        else:
            return name

    def clean_email(self):
        message = _("This email address is already used.")
        email = self.cleaned_data['email']
        if Author.objects.filter(email=email).exists():
            raise forms.ValidationError(message)
        else:
            return email


class MagazineForm(forms.ModelForm):
    class Meta:
        model = Magazine
        fields = '__all__'

    def clean_title(self):
        message = _("too short")
        title = self.cleaned_data["title"]
        if len(title) > 3:
            return title
        else:
            raise forms.ValidationError(message)

    def clean_title_ar(self):
        message = _("too short")
        title_ar = self.cleaned_data["title_ar"]
        if len(title_ar) > 3:
            return title_ar
        else:
            raise forms.ValidationError(message)

    def clean_description(self):
        message = _("too short")
        description = self.cleaned_data['description']
        if len(description) > 3:
            return description
        else:
            raise forms.ValidationError(message)

    def clean_description_ar(self):
        message = _("too short")
        description_ar = self.cleaned_data['description_ar']
        if len(description_ar) > 3:
            return description_ar
        else:
            raise forms.ValidationError(message)


MagazineFormset = formset_factory(MagazineForm, extra=1, can_delete=True)


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

    def clean_content(self):
        message = _("too short")
        content = self.cleaned_data['content']
        if len(content) > 10:
            return content
        else:
            raise forms.ValidationError(message)

    def clean_content_ar(self):
        message = _("too short")
        content_ar = self.cleaned_data['content_ar']
        if len(content_ar) > 10:
            return content_ar
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

# class MyForm(forms.ModelForm):
#     class Meta:
#         model = Car
#         fields = ['date']
#         widgets = {
#             'my_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, localize=True),
#         }

# class ProfitForm(forms.Form):
#    storage = forms.IntegerField()
#    profit = forms.DecimalField(max_digits=4, decimal_places=2, localize=True)


# class NameForm(forms.Form):
#     your_name = forms.CharField(max_length=50, label=_("Enter your name"))
#

class EmailForm(forms.Form):
    subject = forms.CharField(required=True, label=_("Subject"))
    message = forms.CharField(widget=forms.Textarea, required=True, label=_("Message"))
    sender = forms.EmailField(required=True, label=_("Sender"))


EmailFormset = formset_factory(EmailForm, extra=2)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()
