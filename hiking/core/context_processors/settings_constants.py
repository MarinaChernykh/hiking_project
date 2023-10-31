from django.conf import settings


def constants(request):
    return {'COMMENTS_ON_TRAIL_PAGE': settings.COMMENTS_ON_TRAIL_PAGE}
