from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings

from .models import Region, Trail
from .forms import CommentForm


def index(request):
    top_trails = Trail.objects.all()[:settings.TRAILS_PER_PAGE]
    # regions = Region.objects.all()
    # last_region = regions.last()
    last_region = Region.objects.last()
    context = {
        # 'regions': regions,
        'last_region': last_region,
        'top_trails': top_trails,
    }
    return render(request, 'trails/index.html', context=context)


def region_detail(request, region):
    region = get_object_or_404(Region, slug=region)
    images = region.photos.all()
    top_trails = region.trails.all()[:settings.TOP_TRAILS_PER_PAGE]
    # regions = Region.objects.all()
    context = {
        'region': region,
        # 'regions': regions,
        'images': images,
        'top_trails': top_trails,
    }
    return render(request, 'trails/region.html', context=context)


def region_trails_list(request, region):
    region = get_object_or_404(Region, slug=region)
    trails = region.trails.filter(is_published=True)
    paginator = Paginator(trails, settings.TRAILS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # regions = Region.objects.all()
    context = {
        'page_obj': page_obj,
        # 'regions': regions,
        'current_region': region,
    }
    return render(request, 'trails/trails_list.html', context)


def trails_list(request):
    trails = Trail.objects.filter(is_published=True)
    paginator = Paginator(trails, settings.TRAILS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # regions = Region.objects.all()
    context = {
        'page_obj': page_obj,
        # 'regions': regions,
    }
    return render(request, 'trails/trails_list.html', context)


def trail_detail(request, trail):
    current_trail = get_object_or_404(Trail, slug=trail)
    images = current_trail.photos.all()
    top_trails = Trail.objects.filter(region=current_trail.region)[:settings.TOP_TRAILS_PER_PAGE]
    # regions = Region.objects.all()
    # form = CommentForm()
    form = CommentForm()
    comments = current_trail.comments.filter(is_active=True)
    count = comments.count()
    context = {
        'trail': current_trail,
        # 'regions': regions,
        'images': images,
        'top_trails': top_trails,
        'form': form,
        'comments': comments[:settings.COMMENTS_ON_TRAIL_PAGE],
        'count': count
    }
    return render(request, 'trails/trail_details.html', context=context)


@require_POST
@login_required
def add_comment(request, trail):
    current_trail = get_object_or_404(Trail, slug=trail)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.trail = current_trail
        comment.save()
    return redirect('trails:trail_detail', trail=trail)


def comments_list(request, trail):
    current_trail = get_object_or_404(Trail, slug=trail)
    comments = current_trail.comments.filter(is_active=True)
    paginator = Paginator(comments, settings.COMMENTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    top_trails = Trail.objects.filter(region=current_trail.region)[:settings.TOP_TRAILS_PER_PAGE]
    context = {
        'trail': current_trail,
        'top_trails': top_trails,
        'page_obj': page_obj,
    }
    return render(request, 'trails/comments_list.html', context=context)
