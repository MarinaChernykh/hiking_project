from django.shortcuts import render, get_object_or_404

from .models import Region, Trail


def index(request):
    context = {'title': 'Tot'}
    return render(request, 'trails/index.html', context=context)


def region_detail(request, region):
    region = get_object_or_404(Region, slug=region)
    images = region.photos.all()
    top_trails = region.trails.all()[:3]
    context = {
        'region': region,
        'images': images,
        'top_trails': top_trails
    }
    return render(request, 'trails/region.html', context=context)


def region_trails_list(request, region):
    pass


def trails_list(request):
    pass


def trail_detail(request, trail):
    pass

