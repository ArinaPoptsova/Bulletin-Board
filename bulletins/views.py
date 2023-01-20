import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from bulletins.models import Bulletin, Response
from sign.models import User
from .filters import ResponseFilter
from .forms import BulletinForm, AddResponseForm


class BulletinListView(ListView):
    queryset = Bulletin.objects.filter(is_active=True)
    fields = ('author__name', 'title', 'text', 'category', 'date')


class BulletinDetailView(DetailView):
    model = Bulletin
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = AddResponseForm()
        if self.request.user.username:
            data['myresponse'] = self.object.response_set.get(author=self.request.user)
        return data


class BulletinCreateView(LoginRequiredMixin, CreateView):
    model = Bulletin
    form_class = BulletinForm
    template_name = 'bulletins/edit_bulletin.html'
    success_url = '/bulletins/'

    def form_valid(self, form):
        bulletin = form.save(commit=False)
        bulletin.author = self.request.user
        return super().form_valid(form)


class BulletinUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Bulletin
    form_class = BulletinForm
    slug_field = 'slug'
    template_name = 'bulletins/edit_bulletin.html'
    success_url = '/bulletins/'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class AddResponse(LoginRequiredMixin, View):
    def post(self, request, slug):
        form = AddResponseForm(request.POST)
        bulletin = Bulletin.objects.get(slug=slug)
        author = request.user
        if form.is_valid():
            form = form.save(commit=False)
            form.author = author
            form.bulletin = bulletin
            form.save()
            # msg = EmailMultiAlternatives(
            #     subject=f'{form.author.username} responsed',
            #     body=form.text,
            #     from_email='lolkovalolka@yandex.ru',
            #     to=[bulletin.author.email]
            # )
            # msg.send()
        return redirect(bulletin.get_absolute_url())


class ResponseView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'bulletins/responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('bulletin').filter(bulletin__author=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
def accept(request, pk):
    response = Response.objects.get(id=pk)
    response.is_accepted = True
    response.save()
    return redirect('/bulletins/responses/')


@login_required
def delete_response(request, pk):
    response = Response.objects.get(id=pk)
    response.delete()
    return redirect('/bulletins/responses/')
