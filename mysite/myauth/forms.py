from django import  forms


from .models import Profile


class AvatarChange(forms.ModelForm):
    """ Форма смены аватарки пользователя """
    class Meta:
        model = Profile
        fields = 'avatar',