from django.shortcuts import render, get_object_or_404

from .models import Region, Trail


def index(request):
    top_trails = Trail.objects.all()[:6]
    regions = Region.objects.all()
    last_region = regions.last()
    context = {
        'regions': regions,
        'last_region': last_region,
        'top_trails': top_trails
    }
    return render(request, 'trails/index.html', context=context)


def region_detail(request, region):
    region = get_object_or_404(Region, slug=region)
    images = region.photos.all()
    top_trails = region.trails.all()[:3]
    regions = Region.objects.all()
    context = {
        'region': region,
        'regions': regions,
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

