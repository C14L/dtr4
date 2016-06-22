from django import forms

from dtrprofile.models import UserProfile


class UserEditProfileForm(forms.ModelForm):
    # Some user profile basics like PASL, height, weight
    class Meta:
        model = UserProfile
        fields = ('dob', 'gender', 'country', 'city', )
        widgets = {'dob': forms.DateInput(), 'gender': forms.RadioSelect(), }


class UserEditPicsForm(forms.Form):
    pic = forms.ImageField()


class UserEditDetailsForm(forms.ModelForm):
    # Items with a single choices
    class Meta:
        model = UserProfile
        fields = ('height', 'weight', 
                  'eyecolor', 'haircolor', 
                  'relationship_status', 
                  'longest_relationship', 
                  'has_children', 'want_children', 'would_relocate', 
                  'smoke', 'pot', 'drink', 
                  'sports', 'diet',
                  'religion', 'religiosity', 'spirituality',
                  'education', 'jobfield', 'income', )
        widgets = {}
        for f in fields:
            widgets[f] = forms.RadioSelect()


class UserEditAbouMeForm(forms.ModelForm):
    # Items with free length text
    class Meta:
        model = UserProfile
        fields = ('aboutme', )
        widgets = {}


class UserEditSettingsForm(forms.ModelForm):
    # Items with settings data like current language, receive email
    # notifications, etc.
    class Meta:
        model = UserProfile
        fields = ('weight', ) 
        widgets = {}


class UserEditDesignForm(forms.ModelForm):
    # CSS style for user profile.
    class Meta:
        model = UserProfile
        fields = ('style_active', 'style', )
        widgets = {}
