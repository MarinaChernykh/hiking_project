from django.contrib import admin

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
    # raw_id_fields = ['author']
    inlines = [RegionPhotoInline]


@admin.register(Trail)
class AdminTrail(admin.ModelAdmin):
    list_display = ['name', 'region', 'level', 'distance', 'time', 'elevation_gain', 'is_published']
    list_editable = ['is_published']
    list_filter = ['region', 'level', 'is_published']
    search_fields = ['name', 'short_description', 'full_description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TrailPhotoInline]
