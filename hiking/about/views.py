from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Static page about author."""
    template_name = 'about/author.html'


class AboutOutfitView(TemplateView):
    """Static page about outfit and equipment."""
    template_name = 'about/outfit.html'


class AboutnavigationView(TemplateView):
    """Static page about navigation in mountaints."""
    template_name = 'about/navigation.html'
