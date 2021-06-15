from django.forms import ModelForm
from .models import *
from django import forms


class CinemaUserForm(ModelForm):
    confirm_pass = forms.CharField(max_length=100)

    class Meta:
        model = CinemaUser
        fields = ('username', 'password', 'confirm_pass')

    def clean(self):
        clean_data = super().clean()
        if clean_data.get('password') != clean_data.get('confirm_pass'):
            raise forms.ValidationError('Passwords are not equal!')


class HallCreateForm(ModelForm):
    class Meta:
        model = Hall
        fields = ('title', 'image', 'seats')


class SessionCreateForm(ModelForm):
    class Meta:
        model = Session
        fields = ('image', 'started_at', 'finished_at', 'start_date', 'end_date', 'price', 'film')


class TicketPurchaseForm(ModelForm):
    class Meta:
        model = TicketPurchase
        fields = ('quantity',)


class HallUpdateForm(ModelForm):
    class Meta:
        model = Hall
        fields = ('image', 'title', 'seats')


class SessionUpdateForm(ModelForm):
    class Meta:
        model = Session
        fields = ('image', 'started_at', 'finished_at', 'price', 'film')
