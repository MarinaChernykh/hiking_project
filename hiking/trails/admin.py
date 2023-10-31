from django.contrib import admin
from django.db.models import Avg

from . models import Region, Trail, RegionPhoto, TrailPhoto, Comment


class RegionPhotoInline(admin.TabularInline):
    model = RegionPhoto


class TrailPhotoInline(admin.TabularInline):
    model = TrailPhoto


@admin.register(Region)
class AdminRegion(admin.ModelAdmin):
    list_display = ['name', 'slug', 'main_image']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RegionPhotoInline]


@admin.register(Trail)
class AdminTrail(admin.ModelAdmin):
    list_display = [
        'name', 'region', 'level', 'distance', 'time',
        'elevation_gain', 'is_published', 'get_avg_ranking'
    ]
    list_editable = ['is_published']
    list_filter = ['region', 'level', 'is_published']
    search_fields = ['name', 'short_description', 'full_description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TrailPhotoInline]

    def get_avg_ranking(self, obj):
        avg_ranking = (obj.comments
                       .filter(is_active=True)
                       .aggregate(Avg('ranking'))['ranking__avg'])
        if avg_ranking:
            avg_ranking = round(avg_ranking, 1)
        return avg_ranking

    get_avg_ranking.short_description = 'Средний рейтинг'


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = [
        'trail', 'author', 'get_short_text', 'ranking',
        'created', 'is_active'
    ]
    list_editable = ['is_active']
    list_filter = ['trail', 'author', 'ranking', 'is_active']
    search_fields = ['text']

    def get_short_text(self, obj):
        return obj.text[:50]

    get_short_text.short_description = 'Текст комментария'
