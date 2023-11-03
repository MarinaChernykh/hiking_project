from django.db.models import Avg, Count, F
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

from .models import Region, Trail
from .forms import CommentForm, SearchForm


def index(request):
    return render(request, 'trails/index.html')


def region_detail(request, slug_region):
    region = get_object_or_404(
        Region.objects.prefetch_related('photos'),
        slug=slug_region
    )
    context = {
        'region': region,
    }
    return render(request, 'trails/region_detail.html', context=context)


def trails_list(request, slug_region=None):
    if slug_region:
        region = get_object_or_404(Region, slug=slug_region)
        trails = region.trails.filter(is_published=True)
    else:
        region = None
        trails = Trail.objects.filter(is_published=True)
    trails = (trails
              .select_related('region')
              .annotate(avg_rank=Avg('comments__ranking'))
              .order_by(F('avg_rank').desc(nulls_last=True))
            #   .order_by('-avg_rank')
            )
    paginator = Paginator(trails, settings.TRAILS_NUMBER_ALL_TRAILS_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'region': region,
    }
    return render(request, 'trails/trails_list.html', context)


def trail_detail(request, slug_trail):
    trail = get_object_or_404(
        Trail.objects.select_related('region').prefetch_related('photos'),
        slug=slug_trail, is_published=True
    )
    form = CommentForm()
    comments = trail.comments.filter(is_active=True).select_related('author')
    agregate_comments = comments.aggregate(Avg('ranking'), Count('id'))
    context = {
        'trail': trail,
        'average_rating': agregate_comments['ranking__avg'],
        'count': agregate_comments['id__count'],
        'comments': comments[:settings.COMMENTS_NUMBER_TRAIL_PAGE],
        'form': form,
    }
    return render(request, 'trails/trail_details.html', context=context)


@login_required
def add_comment(request, slug_trail):
    trail = get_object_or_404(Trail, slug=slug_trail, is_published=True)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.trail = trail
        comment.save()
    return redirect('trails:trail_detail', slug_trail=slug_trail)


def comments_list(request, slug_trail):
    trail = get_object_or_404(
        Trail.objects.select_related('region'),
        slug=slug_trail, is_published=True
    )
    comments = trail.comments.filter(is_active=True).select_related('author')
    paginator = Paginator(comments, settings.COMMENTS_NUMBER_COMMENTS_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'trail': trail,
        'page_obj': page_obj,
    }
    return render(request, 'trails/comments_list.html', context=context)


def trails_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (Trail.objects
                       .filter(is_published=True)
                       .annotate(search=SearchVector(
                           'name', 'short_description', 'full_description',
                           'start_point_description', 'aqua'),)
                       .filter(search=query))
    context = {
        'form': form,
        'query': query,
        'results': results,
    }
    return render(request, 'trails/search.html', context=context)
