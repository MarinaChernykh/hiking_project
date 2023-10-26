from ..models import Region


def regions(request):
    return {
        'regions': Region.objects.all()
    }
