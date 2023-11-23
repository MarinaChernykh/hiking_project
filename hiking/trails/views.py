from django.db.models import Avg, Count, F
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.postgres.search import (
    SearchVector, SearchQuery, SearchRank)
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

from .models import Region, Trail, Comment, Favorite
from .forms import CommentForm, SearchForm
from .utils import get_page


def index(request):
    """
    Renders index page.
    Gets all regions list (navigation) and top trails list
    from context processor and inclusion tag.
    """
    return render(request, 'trails/index.html')


def region_detail(request, slug_region):
    """
    Renders page with detailed information about region.
    Gets all regions list (navigation) and top region trails
    from context processor and inclusion tag.
    """
    region = get_object_or_404(
        Region.objects.prefetch_related('photos'),
        slug=slug_region
    )
    context = {
        'region': region,
    }
    return render(request, 'trails/region_details.html', context=context)


def trails_list(request, slug_region=None):
    """
    Renders page with trails list for selected region (if slug_region)
    or total list (if slug_region is None).
    Gets all regions list (navigation) from context processor.
    """
    if slug_region:
        region = get_object_or_404(Region, slug=slug_region)
        trails = region.trails.filter(is_published=True)
    else:
        region = None
        trails = Trail.objects.filter(is_published=True)
    trails = (trails
              .select_related('region')
              .annotate(avg_rank=Avg('comments__ranking'))
              .annotate(count_favorite=Count('favorite'))
              .order_by(F('avg_rank').desc(nulls_last=True), '-count_favorite')
              )
    favorites = []
    if request.user.is_authenticated:
        favorites = (Favorite.objects
                     .filter(user=request.user)
                     .values_list('trail', flat=True))
    page_obj = get_page(
        request, trails, settings.TRAILS_NUMBER_ALL_TRAILS_PAGE)
    context = {
        'page_obj': page_obj,
        'region': region,
        'favorites': favorites,
    }
    return render(request, 'trails/trails_list.html', context)


def trail_detail(request, slug_trail):
    """
    Renders page with detailed information about trail.
    Gets all regions list (navigation) and top region trails
    from context processor and inclusion tag.
    """
    trail = get_object_or_404(
        Trail.objects.select_related('region').prefetch_related('photos'),
        slug=slug_trail, is_published=True
    )
    favorite = (Favorite.objects
                .filter(user=request.user, trail=trail).exists()
                if request.user.is_authenticated
                else False)
    form = CommentForm()
    comments = trail.comments.filter(is_active=True).select_related('author')
    agregate_comments = comments.aggregate(Avg('ranking'), Count('id'))
    context = {
        'trail': trail,
        'favorite': favorite,
        'average_rating': agregate_comments['ranking__avg'],
        'count': agregate_comments['id__count'],
        'comments': comments[:settings.COMMENTS_NUMBER_TRAIL_PAGE],
        'form': form,
    }
    return render(request, 'trails/trail_details.html', context=context)


@login_required
def add_comment(request, slug_trail):
    """
    Creates new comment if user is authenticated or redirects to login.
    """
    trail = get_object_or_404(Trail, slug=slug_trail, is_published=True)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.trail = trail
        comment.save()
        messages.success(request, 'Комментарий успешно сохранен.')
    else:
        messages.error(request, 'Возникла ошибка.  Комментарий не сохранен.')
    return redirect('trails:trail_detail', slug_trail=slug_trail)


@login_required
def edit_comment(request, slug_trail, pk):
    comment = get_object_or_404(Comment, pk=pk, is_active=True)
    if request.user != comment.author:
        return redirect('trails:trail_detail', slug_trail)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        messages.success(request, 'Изменения успешно сохранены.')
        return redirect('trails:trail_detail', comment.trail.slug)
    return render(request, 'trails/comment_edit.html', {'form': form})


@login_required
def delete_comment(request, slug_trail, pk):
    comment = get_object_or_404(Comment, pk=pk, is_active=True)
    if request.user != comment.author:
        return redirect('trails:trail_detail', slug_trail)
    form = CommentForm(instance=comment)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий успешно удалён.')
        return redirect('trails:trail_detail', slug_trail)
    return render(request, 'trails/comment_delete.html', {'form': form})


def comments_list(request, slug_trail):
    """
    Renders comments to trail paginated list.
    Gets all regions list (navigation) and top region trails
    from context processor and inclusion tag.
    """
    trail = get_object_or_404(
        Trail.objects.select_related('region'),
        slug=slug_trail, is_published=True
    )
    comments = trail.comments.filter(is_active=True).select_related('author')
    page_obj = get_page(
        request, comments, settings.COMMENTS_NUMBER_COMMENTS_PAGE)
    context = {
        'trail': trail,
        'page_obj': page_obj,
    }
    return render(request, 'trails/comments_list.html', context=context)


def trails_search(request):
    """Postgres full text search in trails text data."""
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = (
                SearchVector(
                    'name', weight='A', config='russian')
                + SearchVector(
                    'short_description', weight='B', config='russian')
                + SearchVector(
                    'full_description', weight='B', config='russian')
                + SearchVector(
                    'start_point_description', weight='C', config='russian')
                + SearchVector(
                    'aqua', weight='C', config='russian')
            )
            search_query = SearchQuery(query, config='russian')

            results = (Trail.objects.filter(is_published=True)
                       .annotate(search=search_vector,
                                 rank=SearchRank(search_vector, search_query))
                       .filter(search=search_query)
                       .filter(rank__gte=0.3)
                       .order_by('-rank'))
    context = {
        'form': form,
        'query': query,
        'results': results,
    }
    return render(request, 'trails/search.html', context=context)


@login_required
def favorite_list(request):
    """Current user's favorite trails list."""
    trails = (Trail.objects
              .filter(favorite__user=request.user, is_published=True)
              .select_related('region')
              .annotate(avg_rank=Avg('comments__ranking'))
              .order_by(F('avg_rank').desc(nulls_last=True))
              )
    favorites = trails.values_list('id', flat=True)
    page_obj = get_page(
        request, trails, settings.TRAILS_NUMBER_ALL_TRAILS_PAGE)
    context = {
        'page_obj': page_obj,
        'favorites': favorites
    }
    return render(request, 'trails/favorite.html', context)


@login_required
def add_favorite(request, slug_trail):
    """Add trail to current user's favorites."""
    trail = get_object_or_404(Trail, slug=slug_trail, is_published=True)
    Favorite.objects.get_or_create(user=request.user, trail=trail)
    return redirect('trails:favorite_list')


@login_required
def delete_favorite(request, slug_trail):
    """Delete trail from current user's favorites."""
    trail = get_object_or_404(Trail, slug=slug_trail, is_published=True)
    Favorite.objects.filter(user=request.user, trail=trail).delete()
    redirect_path = request.META.get('HTTP_REFERER') or 'trails:favorite_list'
    return redirect(redirect_path)
