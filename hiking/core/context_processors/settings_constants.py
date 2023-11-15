from django.conf import settings


def constants(request):
    """Settings constants to be available in templates."""
    return {
        'TRAILS_NUMBER_INDEX_PAGE': settings.TRAILS_NUMBER_INDEX_PAGE,
        'TRAILS_NUMBER_REGION_PAGE': settings.TRAILS_NUMBER_REGION_PAGE,
        'TRAILS_NUMBER_ALLTRAILS_PAGE': settings.TRAILS_NUMBER_ALL_TRAILS_PAGE,
        'TRAILS_NUMBER_TRAIL_PAGE': settings.TRAILS_NUMBER_TRAIL_PAGE,
        'COMMENTS_NUMBER_TRAIL_PAGE': settings.COMMENTS_NUMBER_TRAIL_PAGE
    }
