from django import template
from django.db.models import Avg, F

from trails.models import Trail, Favorite


register = template.Library()


@register.inclusion_tag('trails/includes/top_trails_list.html', takes_context=True)
def show_top_trails(context, obj_number, region=None):
    """Creates tag to insert top-trails block."""
    if region:
        top_trails = Trail.objects.filter(is_published=True, region=region)
    else:
        top_trails = Trail.objects.filter(is_published=True)

    top_trails = (top_trails
                  .select_related('region')
                  .annotate(avg_rank=Avg('comments__ranking'))
                  .order_by(
                      F('avg_rank').desc(nulls_last=True))[:obj_number])
    user = context['request'].user
    favorites = []
    if user.is_authenticated:
        favorites = Favorite.objects.filter(user=user).values_list('trail', flat=True)
    return {
        'top_trails': top_trails,
        'region': region,
        'favorites': favorites,
    }
