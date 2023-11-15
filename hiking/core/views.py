from django.shortcuts import render


def page_not_found(request, exception):
    """Renders customised 404 page."""
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def server_error(request):
    """Renders customised 500 page."""
    return render(request, 'core/500.html', status=500)


def permission_denied(request, exception):
    """Renders customised 403 page."""
    return render(request, 'core/403.html', status=403)


def csrf_failure(request, reason=''):
    """Renders customised 403 csrf page."""
    return render(request, 'core/403csrf.html')
