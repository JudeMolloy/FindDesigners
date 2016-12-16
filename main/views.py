from .models import Designer
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .forms import FilterDesigners


def landing(request):
    designers_promoted = Designer.objects.filter(promoted=True)
    designers_popular = Designer.objects.order_by('-up_votes')
    context = {'designers_promoted': designers_promoted, 'designers_popular': designers_popular, }
    return render(request, 'main/index.html', context)


def search(request):
    query = None
    form = FilterDesigners()

    # form handling
    if request.method == 'POST':
        form = FilterDesigners(request.POST)
        if form.is_valid():

            rating = form.cleaned_data['rating']
            print(rating)
            can_work = form.cleaned_data['can_work']
            print(can_work)
            thumbnail_cost = form.cleaned_data['thumbnail_cost']
            print(thumbnail_cost)

            # the range used for the last value in the restricted choice set e.g £100+
            if thumbnail_cost is None:
                thumbnail_cost[0] = 0
                thumbnail_cost_range = 25
            elif int(thumbnail_cost[0]) == 2:
                thumbnail_cost_range = 25
            else:
                thumbnail_cost_range = 1

            # the query that is built with edited params from the form
            query = Designer.objects.filter(
                up_votes__gte=int(rating), up_votes__lte=int(rating) + 25,
                available=can_work,
                thumbnail_price__gte=float(thumbnail_cost),
                thumbnail_price__lte=float(thumbnail_cost) + thumbnail_cost_range,
            )
            print(query)

    context = {'form': form, 'query': query, }

    return render(request, 'main/find.html', context)


def designer_detail(request, designer_id):
    designer = get_object_or_404(Designer, pk=designer_id)
    context = {'designer': designer, }
    return render(request, 'main/designer_detail.html', context)
