from django import template
from django.db.models import Avg, F

from trails.models import Trail


register = template.Library()


@register.inclusion_tag('trails/includes/top_trails_list.html')
def show_top_trails(obj_number, region=None):
    if region:
        top_trails = Trail.objects.filter(is_published=True, region=region)
    else:
        top_trails = Trail.objects.filter(is_published=True)

    top_trails = (top_trails
                  .select_related('region')
                  .annotate(avg_rank=Avg('comments__ranking'))
                  .order_by(
                      F('avg_rank').desc(nulls_last=True))[:obj_number])
    return {'top_trails': top_trails, 'region': region}
