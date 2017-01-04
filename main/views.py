from django.conf import settings
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Designer
from .forms import FilterDesigners, UserCreateForm, UserUpdateForm


def landing(request):
    return render(request, 'main/landing.html')


def home(request):
    designers_promoted = Designer.objects.filter(promoted=True)
    designers_popular = Designer.objects.order_by('-votes')
    context = {'designers_promoted': designers_promoted, 'designers_popular': designers_popular, }
    return render(request, 'main/index.html', context)


@login_required(login_url='/login/')
def search(request):
    term = request.GET.get('search')
    designers = Designer.objects.filter(username__icontains=term)
    results = 0

    # calculation for what result message to display
    if len(designers) == 0:
        results = 1
    else:
        results = 2

    context = {'designers': designers, 'results': results, }

    return render(request, 'main/search.html', context)


@login_required(login_url='/login/')
def find(request):
    query = None
    results = 0
    form = FilterDesigners()

    # form handling
    if request.method == 'POST':
        form = FilterDesigners(request.POST)
        if form.is_valid():

            # assigns variables to the data passed in from the FilterDesigners form
            rating = form.cleaned_data['rating']
            print(rating)
            can_work = form.cleaned_data['can_work']
            print(can_work)
            thumbnail_cost = form.cleaned_data['thumbnail_cost']
            print(thumbnail_cost)
            channel_art_cost = form.cleaned_data['channel_art_cost']
            print(channel_art_cost)
            does_monthly = form.cleaned_data['does_monthly']
            print(does_monthly)




            # the range used for the last value in the restricted choice set e.g 100+
            if int(thumbnail_cost) == 2:
                thumbnail_cost_range = 25
            else:
                thumbnail_cost_range = 1

            if int(channel_art_cost) == 20:
                channel_art_cost_range = 80
            else:
                channel_art_cost_range = 5

            # the query that is built with edited params from the form
            # this needs to be simplified at some point
            if can_work is True and does_monthly is True:
                query = Designer.objects.filter(
                    votes__gte=int(rating), votes__lte=int(rating) + 25,
                    available=True,
                    monthly=True,
                    thumbnail_price__gte=float(thumbnail_cost),
                    thumbnail_price__lte=float(thumbnail_cost) + thumbnail_cost_range,
                    channel_art_price__gte=float(channel_art_cost),
                    channel_art_price__lte=float(channel_art_cost) + channel_art_cost_range,
                )
            elif can_work is True:
                query = Designer.objects.filter(
                    votes__gte=int(rating), votes__lte=int(rating) + 25,
                    available=True,
                    thumbnail_price__gte=float(thumbnail_cost),
                    thumbnail_price__lte=float(thumbnail_cost) + thumbnail_cost_range,
                    channel_art_price__gte=float(channel_art_cost),
                    channel_art_price__lte=float(channel_art_cost) + channel_art_cost_range,
                )
            elif does_monthly is True:
                query = Designer.objects.filter(
                    votes__gte=int(rating), votes__lte=int(rating) + 25,
                    monthly=True,
                    thumbnail_price__gte=float(thumbnail_cost),
                    thumbnail_price__lte=float(thumbnail_cost) + thumbnail_cost_range,
                    channel_art_price__gte=float(channel_art_cost),
                    channel_art_price__lte=float(channel_art_cost) + channel_art_cost_range,
                )
            else:
                query = Designer.objects.filter(
                    votes__gte=int(rating), votes__lte=int(rating) + 25,
                    thumbnail_price__gte=float(thumbnail_cost),
                    thumbnail_price__lte=float(thumbnail_cost) + thumbnail_cost_range,
                    channel_art_price__gte=float(channel_art_cost),
                    channel_art_price__lte=float(channel_art_cost) + channel_art_cost_range,
                )


            query = query.order_by('-votes')

            # calculation for what result message to display
            if len(query) == 0:
                results = 1
            else:
                results = 2
            print(results)
            print(query)

    context = {'form': form, 'query': query, 'results': results, }

    return render(request, 'main/find.html', context)


def designer_detail(request, designer_id):
    designer = get_object_or_404(Designer, pk=designer_id)
    duplicate = designer.votes.exists(designer_id)
    context = {'designer': designer, 'duplicate': duplicate, }
    return render(request, 'main/designer_detail.html', context)


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('find')
    template_name = "main/login.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignUp(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'main/signup.html'


class UpdateProfile(LoginRequiredMixin, generic.UpdateView):
    model = Designer
    form_class = UserUpdateForm
    success_url = reverse_lazy('home')
    template_name = 'main/profile_update.html'

    def get_object(self):
        return self.request.user


def designer_detail(request, designer_id):
    designer = get_object_or_404(Designer, pk=designer_id)
    duplicate = designer.votes.exists(designer_id)
    if request.method == 'POST':
            designer.votes.up(designer_id)

    context = {'designer': designer, 'duplicate': duplicate, }
    return render(request, 'main/designer_detail.html', context)

# def update_profile(request):
#
#     user = request.user
#     form = UserUpdateForm(request.POST, instance=user)
#     form.actual_user = request.user
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('update_profile_success'))
#     else:
#         form = UserUpdateForm()
#
#     context = {'form': form, }
#     return render(request, 'main/profile_update.html', context)

