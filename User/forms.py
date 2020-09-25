from django import forms

from User.models import User, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'birthday', 'gender', 'location']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        cleaned_data = super().clean()
        if cleaned_data['max_distance'] < cleaned_data['min_distance']:
            raise forms.ValidationError('最大距离必须大于最小距离')
        return cleaned_data['max_distance']

    def clean_max_dating_age(self):
        cleaned_data = super().clean()
        if cleaned_data['max_dating_age'] < cleaned_data['min_dating_age']:
            raise forms.ValidationError('最大年龄必须大于最小年龄')
        return cleaned_data['max_dating_age']
