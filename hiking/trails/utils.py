from django.core.paginator import Paginator


def get_page(request, objects, objects_per_page):
    paginator = Paginator(objects, objects_per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
