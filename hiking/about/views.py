from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'


class AboutOutfitView(TemplateView):
    template_name = 'about/outfit.html'


class AboutnavigationView(TemplateView):
    template_name = 'about/navigation.html'
