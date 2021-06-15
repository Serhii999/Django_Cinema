from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import *
from django.contrib import messages


class UserCreateView(CreateView):
    model = CinemaUser
    form_class = CinemaUserForm
    success_url = '/login'
    template_name = 'register.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(self.object.password)
        self.object.save()
        return super().form_valid(form)


class HallsListView(ListView):
    model = Hall
    template_name = 'main.html'
    login_url = 'login/'

    paginate_by = 3


class Login(LoginView):
    template_name = 'login.html'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


class HallCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'is_superuser'
    login_url = 'login/'
    form_class = HallCreateForm
    success_url = '/'
    template_name = 'hallcreate.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        repeat = Hall.objects.filter(title=obj.title)
        if repeat:
            messages.add_message(self.request, messages.ERROR, 'Зал с таким названием уже создан')
            return redirect('/')

        obj.save()
        return super().form_valid(form=form)


class SessionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'is_superuser'
    login_url = 'login/'
    form_class = SessionCreateForm
    success_url = '/'
    template_name = 'sessioncreate.html'
    model = Session

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        sessions = Session.objects.filter(start_date__gte=datetime.today(), hall=self.request.POST['hall_id'],
                                          finished_at__gte=obj.started_at)
        second_check = Session.objects.filter(start_date__gte=datetime.today(), hall=self.request.POST['hall_id'],
                                              started_at__lte=obj.finished_at)
        obj.hall_id = self.request.POST['hall_id']

        if obj.started_at >= obj.finished_at or \
                timedelta(minutes=30) >= timedelta(hours=obj.finished_at.hour, minutes=obj.finished_at.minute,
                                                   seconds=obj.finished_at.second) - \
                timedelta(hours=obj.started_at.hour, minutes=obj.started_at.minute, seconds=obj.finished_at.second) \
                >= timedelta(hours=4) \
                or obj.start_date > obj.end_date:
            messages.add_message(self.request, messages.ERROR, 'Некорректное время для сеанса')
            return redirect('/')
        if sessions and second_check:
            messages.add_message(self.request, messages.ERROR, 'Сеанс в это время уже идет')
            return redirect('/')
        return super().form_valid(form=form)


class TodaySessionView(ListView):
    model = Session
    template_name = 'today.html'
    login_url = 'login/'
    extra_context = {'purchase_form': TicketPurchaseForm}
    paginate_by = 5

    def get_queryset(self):
        if self.request.GET['day'] == 'today':
            if self.request.GET['sort'] == 'price':
                return super().get_queryset().filter(start_date=datetime.today(),
                                                     hall=self.request.GET['hall_id']).order_by('price')
            elif self.request.GET['sort'] == 'time':
                return super().get_queryset().filter(start_date=datetime.today(),
                                                     hall=self.request.GET['hall_id']).order_by('started_at')
            else:
                return super().get_queryset().filter(start_date=datetime.today(),
                                                     hall=self.request.GET['hall_id'])
        else:
            if self.request.GET['sort'] == 'price':
                return super().get_queryset().filter(start_date=datetime.today() + timedelta(days=1),
                                                     hall=self.request.GET['hall_id']).order_by('price')
            elif self.request.GET['sort'] == 'time':
                return super().get_queryset().filter(start_date=datetime.today() + timedelta(days=1),
                                                     hall=self.request.GET['hall_id']).order_by('started_at')
            else:
                return super().get_queryset().filter(start_date=datetime.today() + timedelta(days=1),
                                                     hall=self.request.GET['hall_id'])


class PurchaseTicketView(CreateView):
    form_class = TicketPurchaseForm
    success_url = '/'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        session = Session.objects.get(id=self.request.POST['session_id'])
        customer = CinemaUser.objects.get(id=self.request.POST['customer_id'])
        total_price = session.price * object.quantity
        customer.wallet -= total_price
        session.purchased_seats += object.quantity
        if total_price > object.user.wallet:
            messages.add_message(self.request, messages.ERROR, 'Нет столько денег!')
            return redirect('/')
        if session.hall.seats < session.purchased_seats:
            messages.add_message(self.request, messages.ERROR, 'В зале нет столько мест')
            return redirect('/')
        object.session_id = self.request.POST['session_id']
        object.customer_id = self.request.POST['customer_id']
        messages.add_message(self.request, messages.INFO, 'Билет(ы) успешно куплен(ы)')
        object.save()
        customer.save()
        session.save()
        return super().form_valid(form=form)


class Purchases(LoginRequiredMixin, ListView):
    model = TicketPurchase
    template_name = 'purchases.html'
    login_url = 'login/'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)


class UpdateHallView(LoginRequiredMixin, UpdateView):
    model = Hall
    permission_required = 'is_superuser'
    login_url = 'login/'
    form_class = HallUpdateForm
    success_url = '/'
    template_name = 'hallupdate.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        sessions = Session.objects.filter(purchased_seats__gt=0, hall=self.request.GET['hall_id'],
                                          start_date__gte=datetime.today())
        if sessions:
            messages.add_message(self.request, messages.ERROR, 'Билеты в этот зал уже куплены')
            return redirect('/')
        return super().form_valid(form=form)


class UpdateSessionView(LoginRequiredMixin, UpdateView):
    model = Session
    permission_required = 'is_superuser'
    login_url = 'login/'
    form_class = SessionUpdateForm
    success_url = '/'
    template_name = 'sessionupdate.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        sessions = Session.objects.filter(start_date=datetime.today(), hall=self.request.GET['hall_id'],
                                          finished_at__gte=obj.started_at).exclude(id=self.request.GET['session_id'])
        second_check = Session.objects.filter(start_date=datetime.today(), hall=self.request.GET['hall_id'],
                                              started_at__lte=obj.finished_at).exclude(id=self.request.GET['session_id'])
        obj.id = self.request.GET['session_id']
        obj.hall_id = self.request.GET['hall_id']
        obj.start_date = datetime.today()
        obj.end_date = datetime.today()
        sale = Session.objects.filter(id=self.request.GET['session_id'], purchased_seats__gt=0)
        if sale:
            messages.add_message(self.request, messages.ERROR, 'Билеты на этот сеанс уже куплены')
            return redirect('/')
        if sessions and second_check:
            messages.add_message(self.request, messages.ERROR, 'Сеанс в это время уже идет')
            return redirect('/')
        if timedelta(minutes=30) >= timedelta(hours=obj.finished_at.hour, minutes=obj.finished_at.minute,
                                              seconds=obj.finished_at.second) - \
                timedelta(hours=obj.started_at.hour, minutes=obj.started_at.minute, seconds=obj.finished_at.second) \
                >= timedelta(hours=4):
            messages.add_message(self.request, messages.ERROR, 'Некорректное время для сеанса')
            return redirect('/')
        obj.save()
        return super().form_valid(form=form)
