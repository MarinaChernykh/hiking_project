from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Avg
from django.conf import settings

from .models import Region, Trail, Comment
from .forms import CommentForm


def index(request):
    last_region = Region.objects.last()
    context = {
        'last_region': last_region,
    }
    return render(request, 'trails/index.html', context=context)


def region_detail(request, slug_region):
    region = get_object_or_404(Region, slug=slug_region)
    images = region.photos.all()
    context = {
        'region': region,
        'images': images,
    }
    return render(request, 'trails/region_detail.html', context=context)


def trails_list(request, slug_region=None):
    if slug_region:
        region = get_object_or_404(Region, slug=slug_region)
        trails = region.trails.filter(is_published=True)
    else:
        region = None
        trails = Trail.objects.filter(is_published=True)
    trails = trails.annotate(avg_rank = Avg('comments__ranking')).order_by('-avg_rank')
    paginator = Paginator(trails, settings.TRAILS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'region': region
    }
    return render(request, 'trails/trails_list.html', context)


def trail_detail(request, slug_trail):
    trail = get_object_or_404(Trail, slug=slug_trail, is_published=True)
    average_rating = trail.comments.aggregate(Avg('ranking'))['ranking__avg']
    images = trail.photos.all()
    form = CommentForm()
    comments = trail.comments.filter(is_active=True)
    count = comments.count()
    context = {
        'trail': trail,
        'average_rating': average_rating,
        'images': images,
        'form': form,
        'comments': comments[:settings.COMMENTS_ON_TRAIL_PAGE],
        'count': count,
    }
    return render(request, 'trails/trail_details.html', context=context)


@require_POST
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
    trail = get_object_or_404(Trail, slug=slug_trail, is_published=True)
    comments = trail.comments.filter(is_active=True)
    paginator = Paginator(comments, settings.COMMENTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'trail': trail,
        'page_obj': page_obj,
    }
    return render(request, 'trails/comments_list.html', context=context)
