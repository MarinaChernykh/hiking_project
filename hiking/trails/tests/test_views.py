import shutil
import tempfile
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from django.urls import reverse
from django.conf import settings
from django import forms

from trails.models import Region, Trail, Comment


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
SOME_GIF = (
        b'\x47\x49\x46\x38\x39\x61\x02\x00'
        b'\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
        b'\x00\x00\x00\x2C\x00\x00\x00\x00'
        b'\x02\x00\x01\x00\x00\x02\x02\x0C'
        b'\x0A\x00\x3B'
)
uploaded = SimpleUploadedFile(
    name='small.gif',
    content=SOME_GIF,
    content_type='image/gif'
)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TrailsViewsTests(TestCase):
    """Views templates and context tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Test User')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.region = Region.objects.create(
            name='Тестовый регион',
            slug='test-region-slug',
            description_intro='Тестовое описание региона',
            main_image=uploaded,
            mobile_image=uploaded,
        )
        cls.trail = Trail.objects.create(
            name='Тестовый трек',
            slug='test-trail-slug',
            short_description='Тестовое описание маршрута',
            region=cls.region,
            main_image=uploaded,
            mobile_image=uploaded,
            card_image=uploaded,
            is_published=True,
        )
        cls.comment = Comment.objects.create(
            trail=cls.trail,
            author=cls.user,
            ranking=5
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_reverse_name_uses_correct_template(self):
        """
        URL called by reverse name uses correct template.
        """
        url_templates_names = {
            reverse('trails:index'): 'trails/index.html',
            reverse(
                'trails:region_detail',
                kwargs={'slug_region': self.region.slug}
            ): 'trails/region_details.html',
            reverse(
                'trails:trail_detail',
                kwargs={'slug_trail': self.trail.slug}
            ): 'trails/trail_details.html',
            reverse(
                'trails:region_trails_list',
                kwargs={'slug_region': self.region.slug}
            ): 'trails/trails_list.html',
            reverse('trails:trails_list'): 'trails/trails_list.html',
            reverse(
                'trails:comments_list',
                kwargs={'slug_trail': self.trail.slug}
            ): 'trails/comments_list.html',
            reverse('trails:trails_search'): 'trails/search.html'
        }
        for reverse_name, template in url_templates_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_region_detail_page_show_correct_context(self):
        """
        Template, called by 'region_detail' url name, gets correct context.
        """
        response = (self.guest_client.get(
            reverse('trails:region_detail',
                    kwargs={'slug_region': 'test-region-slug'})))
        self.assertEqual(
            response.context.get('region').name,
            'Тестовый регион')
        self.assertEqual(
            response.context.get('region').description_intro,
            'Тестовое описание региона')

    def test_trail_detail_page_show_correct_context(self):
        """
        Template, called by 'trail_detail' url name, gets correct context.
        """
        response = (self.guest_client.get(
            reverse('trails:trail_detail',
                    kwargs={'slug_trail': 'test-trail-slug'})))
        self.assertEqual(
            response.context.get('trail').name, 'Тестовый трек')
        self.assertEqual(
            response.context.get('trail').short_description,
            'Тестовое описание маршрута')
        self.assertEqual(response.context.get('average_rating'), 5.0)
        self.assertEqual(response.context.get('count'), 1)
        self.assertEqual(
            response.context.get('comments')[0], self.comment)
        self.assertIsInstance(
            response.context.get('form').fields['ranking'],
            forms.fields.TypedChoiceField)
        self.assertIsInstance(
            response.context.get('form').fields['text'],
            forms.fields.CharField)

    def test_region_trails_list_page_show_correct_context(self):
        """
        Template, called by 'region_trails_list' url name,
        gets correct context.
        """
        response = (self.guest_client.get(
            reverse('trails:region_trails_list',
                    kwargs={'slug_region': 'test-region-slug'})))
        self.assertEqual(
            response.context.get('region').name, 'Тестовый регион')
        self.assertEqual(
            response.context.get('region').description_intro,
            'Тестовое описание региона')

        first_trail = response.context.get('page_obj')[0]
        self.assertEqual(first_trail.name, 'Тестовый трек')
        self.assertEqual(
            first_trail.short_description, 'Тестовое описание маршрута')

    def test_trails_list_page_show_correct_context(self):
        """
        Template, called by 'trails_list' url name, gets correct context.
        """
        response = (self.guest_client.
                    get(reverse('trails:trails_list')))
        first_trail = response.context.get('page_obj')[0]
        self.assertEqual(first_trail.name, 'Тестовый трек')
        self.assertEqual(
            first_trail.short_description,
            'Тестовое описание маршрута')
        self.assertEqual(response.context.get('region'), None)

    def test_comments_list_page_show_correct_context(self):
        """
        Template, called by 'comments_list' url name, gets correct context.
        """
        response = (self.guest_client.
                    get(reverse(
                        'trails:comments_list',
                        kwargs={'slug_trail': self.trail.slug})))
        first_comment = response.context.get('page_obj')[0]
        self.assertEqual(first_comment.trail, self.trail)
        self.assertEqual(first_comment.author, self.user)
        self.assertEqual(first_comment.ranking, 5)
        self.assertEqual(response.context.get('trail'), self.trail)

    def test_trails_search_page_without_query_show_correct_context(self):
        """
        Template, called by 'trails_search' url name without any query data,
        gets correct context.
        """
        response = (self.guest_client.
                    get(reverse('trails:trails_search')))
        self.assertEqual(response.context.get('query'), None)
        self.assertEqual(response.context.get('results'), [])
        self.assertIsInstance(
            response.context.get('form').fields['query'],
            forms.fields.CharField)

    def test_trails_search_page_with_query_show_correct_context(self):
        """
        Template, called by 'trails_search' url name with query data,
        gets correct context.
        """
        response = (self.guest_client.get(
            f"{reverse('trails:trails_search')}?query=трек"))
        self.assertEqual(response.context.get('query'), 'трек')
        search_result = response.context.get('results')
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0], self.trail)
        self.assertEqual(search_result[0].name, 'Тестовый трек')
        self.assertIsInstance(
            response.context.get('form').fields['query'],
            forms.fields.CharField)

    def test_all_regions_context_is_available_all_pages(self):
        """
        All regions list (custom context processor)
        is available in each page context.
        """
        cache.clear()
        new_regions_qty = 3
        regions = [
            Region(
                name=f'Тестовый регион {i + 1}',
                slug=f'test-region-{i + 1}',
                main_image=uploaded,
                mobile_image=uploaded)
            for i in range(new_regions_qty)
        ]
        Region.objects.bulk_create(regions)
        urls = [
            reverse('trails:index'),
            reverse(
                'trails:region_detail',
                kwargs={'slug_region': self.region.slug}),
            reverse(
                'trails:trail_detail',
                kwargs={'slug_trail': self.trail.slug}),
            reverse(
                'trails:region_trails_list',
                kwargs={'slug_region': self.region.slug}),
            reverse('trails:trails_list'),
            reverse(
                'trails:comments_list',
                kwargs={'slug_trail': self.trail.slug}),
            reverse('trails:trails_search')
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                expected_regions_number = Region.objects.count()
                context_regions_number = len(response.context['regions'])
                self.assertEqual(
                    context_regions_number, expected_regions_number)

    def test_inactive_trails_not_shown(self):
        """
        Trail with status 'is_published=False' is not shown on any page.
        """
        inactive_trail = Trail.objects.create(
            name='Тестовый трек',
            slug='inactive-trail-slug',
            region=self.region,
            main_image=uploaded,
            mobile_image=uploaded,
            card_image=uploaded,
            is_published=False,
        )
        urls = {
            reverse('trails:index'): 'top_trails',
            reverse(
                'trails:region_detail',
                kwargs={'slug_region': self.region.slug}
            ): 'top_trails',
            reverse(
                'trails:trail_detail',
                kwargs={'slug_trail': self.trail.slug}
            ): 'top_trails',
            reverse(
                'trails:comments_list',
                kwargs={'slug_trail': self.trail.slug}
            ): 'top_trails',
            reverse(
                'trails:region_trails_list',
                kwargs={'slug_region': self.region.slug}
            ): 'page_obj',
            reverse('trails:trails_list'): 'page_obj',
        }
        for url, context_key in urls.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                trails = response.context.get(context_key)
                self.assertEqual(len(trails), 1)
                self.assertNotEqual(trails[0], inactive_trail)
        response = self.authorized_client.get(
            reverse(
                'trails:trail_detail',
                kwargs={'slug_trail': inactive_trail.slug}
            ))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def comment_inactive_not_shown(self):
        """Comment with status 'is_active=False' is not shown."""
        inactive_comment = Comment.objects.create(
            trail=self.trail,
            author=self.user,
            ranking=1,
            is_active=False
        )
        urls = {
            reverse(
                'trails:trail_detail',
                kwargs={'slug_trail': self.trail.slug}
            ): 'comments',
            reverse(
                'trails:comments_list',
                kwargs={'slug_trail': self.trail.slug}
            ): 'page_obj',
        }
        for url, context_key in urls.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                comments = response.context.get(context_key)
                self.assertEqual(len(comments), 1)
                self.assertNotEqual(comments[0], inactive_comment)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class RankingTests(TestCase):
    """Trails ranking tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Test User')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.region = Region.objects.create(
            name='Тестовый регион',
            slug='test-region-slug',
            main_image=uploaded,
            mobile_image=uploaded,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_trail_average_rating_is_correct(self):
        """
        Trail avg ranking is correct
        on trail details page and in inclusion tag.
        """
        trail = Trail.objects.create(
            name='Тестовый трек',
            slug='test-trail-slug',
            region=self.region,
            main_image=uploaded,
            mobile_image=uploaded,
            card_image=uploaded,
            is_published=True,
        )
        comments = [
            Comment(trail=trail, author=self.user, ranking=5),
            Comment(trail=trail, author=self.user, ranking=4),
            Comment(trail=trail, author=self.user, text='No rank'),
        ]
        Comment.objects.bulk_create(comments)
        response = (self.authorized_client.get(
            reverse(
                'trails:trail_detail',
                kwargs={'slug_trail': 'test-trail-slug'})
        ))
        self.assertEqual(response.context['average_rating'], 4.5)
        response = (self.authorized_client.get(reverse('trails:index')))
        self.assertEqual(response.context['top_trails'][0].avg_rank, 4.5)

    def test_trails_ordered_rating_desc(self):
        """
        Trails are ordered according to their avg ranking (desc).
        Trails without any rankings following last.
        """
        trails_qty = 3
        trails = [
            Trail(
                name=f'Тестовый трек {i+1}',
                slug=f'test-trail-{i+1}',
                region=self.region,
                main_image=uploaded,
                mobile_image=uploaded,
                card_image=uploaded,
                is_published=True)
            for i in range(trails_qty)
        ]
        Trail.objects.bulk_create(trails)
        trails = Trail.objects.all()
        comments = [
            Comment(trail=trails[0], author=self.user, ranking=2),
            Comment(trail=trails[0], author=self.user, ranking=3),
            Comment(trail=trails[1], author=self.user, text='No rank'),
            Comment(trail=trails[2], author=self.user, ranking=1),
            Comment(trail=trails[2], author=self.user, ranking=5),
        ]
        Comment.objects.bulk_create(comments)
        urls = {
            reverse('trails:index'): 'top_trails',
            reverse(
                'trails:region_detail',
                kwargs={'slug_region': self.region.slug}
            ): 'top_trails',
            reverse(
                'trails:trail_detail',
                kwargs={'slug_trail': trails[0].slug}
            ): 'top_trails',
            reverse(
                'trails:comments_list',
                kwargs={'slug_trail': trails[0].slug}
            ): 'top_trails',
            reverse(
                'trails:region_trails_list',
                kwargs={'slug_region': self.region.slug}
            ): 'page_obj',
            reverse('trails:trails_list'): 'page_obj',
        }
        for url, context_key in urls.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                trails = response.context.get(context_key)
                self.assertEqual(trails[0].name, 'Тестовый трек 3')
                self.assertEqual(trails[1].name, 'Тестовый трек 1')
                self.assertEqual(trails[2].name, 'Тестовый трек 2')

    def test_top_trail_exists_on_relevant_pages_only(self):
        """
        Trail with highest rank is presented in top trails list
        on each page without region and with the trail region,
        but not exists on the pages with trails of other region.
        """
        trail = Trail.objects.create(
            name='Тестовый трек с высоким рейтингом',
            slug='test-trail-slug',
            region=self.region,
            main_image=uploaded,
            mobile_image=uploaded,
            card_image=uploaded,
            is_published=True,
        )
        other_region = Region.objects.create(
            name='Другой тестовый регион',
            slug='other-region-slug',
            main_image=uploaded,
            mobile_image=uploaded,
        )
        Comment.objects.create(
            trail=trail,
            author=self.user,
            ranking=5
        )
        urls = {
            reverse('trails:index'): 'top_trails',
            reverse(
                'trails:region_detail',
                kwargs={'slug_region': self.region.slug}
            ): 'top_trails',
            reverse(
                'trails:trail_detail',
                kwargs={'slug_trail': trail.slug}
            ): 'top_trails',
            reverse(
                'trails:comments_list',
                kwargs={'slug_trail': trail.slug}
            ): 'top_trails',
            reverse(
                'trails:region_trails_list',
                kwargs={'slug_region': self.region.slug}
            ): 'page_obj',
            reverse('trails:trails_list'): 'page_obj',
        }
        for url, context_key in urls.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                trails = response.context.get(context_key)
                self.assertEqual(
                    trails[0].name, 'Тестовый трек с высоким рейтингом')

        other_region_urls = {
            reverse(
                'trails:region_detail',
                kwargs={'slug_region': other_region.slug}
            ): 'top_trails',
            reverse(
                'trails:region_trails_list',
                kwargs={'slug_region': other_region.slug}
            ): 'page_obj',
        }
        for url, context_key in other_region_urls.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                trails = response.context.get(context_key)
                self.assertEqual(len(trails), 0)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PaginatorViewsTest(TestCase):
    """Paginator tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Test User')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.region = Region.objects.create(
            name='Тестовый регион',
            slug='test-region-slug',
            main_image=uploaded,
            mobile_image=uploaded,
        )
        cls.trails_qty = 15
        trails = [
            Trail(
                name=f'Тестовый трек {i}',
                slug=f'test-trail-{i}',
                region=cls.region,
                main_image=uploaded,
                mobile_image=uploaded,
                card_image=uploaded,
                is_published=True)
            for i in range(cls.trails_qty)
        ]
        Trail.objects.bulk_create(trails)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_pages_contains_correct_qty_of_trails(self):
        """
        Paginator shows correct trails split to pages.
        """
        objects_per_page = {
            reverse(
                'trails:region_trails_list',
                kwargs={'slug_region': self.region.slug}): 12,
            reverse('trails:trails_list'): 12,
        }
        for reverse_name, qty in objects_per_page.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), qty)
                response = self.authorized_client.get(f'{reverse_name}?page=2')
                self.assertEqual(
                    len(response.context['page_obj']), self.trails_qty - qty)

    def test_pages_contains_correct_qty_of_comments(self):
        """
        Paginator shows correct comments split to pages.
        """
        trail = Trail.objects.first()
        comments_qty = 8
        comments = [
            Comment(
                trail=trail,
                author=self.user,
                ranking=5)
            for _ in range(comments_qty)
        ]
        Comment.objects.bulk_create(comments)

        objects_per_page = {
            reverse(
                'trails:comments_list', kwargs={'slug_trail': trail.slug}): 5,
        }
        for reverse_name, qty in objects_per_page.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), qty)
                response = self.authorized_client.get(f'{reverse_name}?page=2')
                self.assertEqual(
                    len(response.context['page_obj']), comments_qty - qty)
