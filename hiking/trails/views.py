from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from .models import Region, Trail


def index(request):
    top_trails = Trail.objects.all()[:settings.OBJECTS_PER_PAGE]
    regions = Region.objects.all()
    last_region = regions.last()
    context = {
        'regions': regions,
        'last_region': last_region,
        'top_trails': top_trails,
    }
    return render(request, 'trails/index.html', context=context)


def region_detail(request, region):
    region = get_object_or_404(Region, slug=region)
    images = region.photos.all()
    top_trails = region.trails.all()[:settings.TOP_TRAILS_PER_PAGE]
    regions = Region.objects.all()
    context = {
        'region': region,
        'regions': regions,
        'images': images,
        'top_trails': top_trails,
    }
    return render(request, 'trails/region.html', context=context)


def region_trails_list(request, region):
    region = get_object_or_404(Region, slug=region)
    trails = region.trails.filter(is_published=True)
    paginator = Paginator(trails, settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    regions = Region.objects.all()
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'current_region': region,
    }
    return render(request, 'trails/trails_list.html', context)


def trails_list(request):
    trails = Trail.objects.filter(is_published=True)
    paginator = Paginator(trails, settings.OBJECTS_PER_PAGE)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    regions = Region.objects.all()
    context = {
        'page_obj': page_obj,
        'regions': regions,
    }
    return render(request, 'trails/trails_list.html', context)


def trail_detail(request, trail):
    trail = get_object_or_404(Trail, slug=trail)
    images = trail.photos.all()
    top_trails = Trail.objects.filter(region=trail.region)[:settings.TOP_TRAILS_PER_PAGE]
    regions = Region.objects.all()
    context = {
        'trail': trail,
        'regions': regions,
        'images': images,
        'top_trails': top_trails,
    }
    return render(request, 'trails/trail_details.html', context=context)
