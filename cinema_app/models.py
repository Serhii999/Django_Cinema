import django
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.utils import timezone


class CinemaUser(AbstractUser):
    wallet = models.PositiveIntegerField(default=10000)

    def __str__(self):
        return "{}".format(self.username)


class Hall(models.Model):
    image = models.ImageField(upload_to='media', default='defaulthall.jpg', blank=True, null=True)
    title = models.CharField(max_length=100)
    seats = models.PositiveIntegerField(default=10)

    def __str__(self):
        return "{}".format(self.title)


class Session(models.Model):
    image = models.ImageField(upload_to='media', default='film.jpg', blank=True, null=True)
    started_at = models.TimeField()
    finished_at = models.TimeField()
    start_date = models.DateField(default=django.utils.timezone.now)
    end_date = models.DateField(default=django.utils.timezone.now)
    price = models.PositiveIntegerField(default=1)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    film = models.CharField(max_length=100)
    purchased_seats = models.PositiveIntegerField(default=0)


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id is None:
            list = []
            d = self.start_date
            while d <= self.end_date:
                list.append(Session(image=self.image, start_date=d,
                        end_date=self.end_date, hall=self.hall, film=self.film,
                        purchased_seats=self.purchased_seats, started_at=self.started_at,
                        finished_at=self.finished_at, price=self.price
                        ))
                d = d + timedelta(days=1)
            Session.objects.bulk_create(list)
        else:
            super().save()


    # def clean(self):
    #     if self.start_date < datetime.date(datetime.today()):
    #         raise ValidationError('Создавать сеансы можно только с сегодняшнего дня')
    #     elif self.end_date < self.start_date:
    #         raise ValidationError('Меня не проведешь')
    #
    # def __str__(self):
    #     return "{} at {}".format(self.film, self.hall)

class TicketPurchase(models.Model):
    customer = models.ForeignKey(CinemaUser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


    def __str__(self):
        return "{} from {} ".format(self.session, self.customer)



# Create your models here.
