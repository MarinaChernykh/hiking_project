import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
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
            trail = cls.trail,
            author = cls.user,
            ranking = 5
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_reverse_name_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        url_templates_names = {
            reverse('trails:index'): 'trails/index.html',
            reverse('trails:region_detail', kwargs={'slug_region': self.region.slug}): 'trails/region_details.html',
            reverse('trails:trail_detail', kwargs={'slug_trail': self.trail.slug}): 'trails/trail_details.html',
            reverse('trails:region_trails_list', kwargs={'slug_region': self.region.slug}): 'trails/trails_list.html',
            reverse('trails:trails_list'): 'trails/trails_list.html',
            reverse('trails:comments_list', kwargs={'slug_trail': self.trail.slug}): 'trails/comments_list.html',
            reverse('trails:trails_search'): 'trails/search.html'
        }
        for reverse_name, template in url_templates_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_region_detail_page_show_correct_context(self):
        """Шаблон task_detail сформирован с правильным контекстом."""
        response = (self.guest_client.
            get(reverse('trails:region_detail', kwargs={'slug_region': 'test-region-slug'})))
        self.assertEqual(response.context.get('region').name, 'Тестовый регион')
        self.assertEqual(response.context.get('region').description_intro, 'Тестовое описание региона')

    def test_trail_detail_page_show_correct_context(self):
        """Шаблон trail_detail сформирован с правильным контекстом."""
        response = (self.guest_client.
            get(reverse('trails:trail_detail', kwargs={'slug_trail': 'test-trail-slug'})))
        self.assertEqual(response.context.get('trail').name, 'Тестовый трек')
        self.assertEqual(response.context.get('trail').short_description, 'Тестовое описание маршрута')
        self.assertEqual(response.context.get('average_rating'), 5.0)
        self.assertEqual(response.context.get('count'), 1)
        self.assertEqual(response.context.get('comments')[0], self.comment)
        self.assertIsInstance(response.context.get('form').fields['ranking'], forms.fields.TypedChoiceField)
        self.assertIsInstance(response.context.get('form').fields['text'], forms.fields.CharField)

    def test_region_trails_list_page_show_correct_context(self):
        """Шаблон region_trails_list сформирован с правильным контекстом."""
        response = (self.guest_client.
                    get(reverse('trails:region_trails_list', kwargs={'slug_region': 'test-region-slug'})))
        self.assertEqual(response.context.get('region').name, 'Тестовый регион')
        self.assertEqual(response.context.get('region').description_intro, 'Тестовое описание региона')

        first_trail = response.context.get('page_obj')[0]
        self.assertEqual(first_trail.name, 'Тестовый трек')
        self.assertEqual(first_trail.short_description, 'Тестовое описание маршрута')

    def test_trails_list_page_show_correct_context(self):
        """Шаблон trails_list сформирован с правильным контекстом."""
        response = (self.guest_client.
                    get(reverse('trails:trails_list')))
        first_trail = response.context.get('page_obj')[0]
        self.assertEqual(first_trail.name, 'Тестовый трек')
        self.assertEqual(first_trail.short_description, 'Тестовое описание маршрута')
        self.assertEqual(response.context.get('region'), None)

    def test_comments_list_page_show_correct_context(self):
        """Шаблон comments_list сформирован с правильным контекстом."""
        response = (self.guest_client.
                    get(reverse('trails:comments_list', kwargs={'slug_trail': self.trail.slug})))
        first_comment = response.context.get('page_obj')[0]
        self.assertEqual(first_comment.trail, self.trail)
        self.assertEqual(first_comment.author, self.user)
        self.assertEqual(first_comment.ranking, 5)
        self.assertEqual(response.context.get('trail'), self.trail)

    def test_trails_search_page_without_query_show_correct_context(self):
        """Шаблон trails_search сформирован с правильным контекстом."""
        response = (self.guest_client.
                    get(reverse('trails:trails_search')))
        self.assertEqual(response.context.get('query'), None)
        self.assertEqual(response.context.get('results'), [])
        self.assertIsInstance(response.context.get('form').fields['query'], forms.fields.CharField)

    def test_trails_search_page_with_query_show_correct_context(self):
        """Шаблон trails_search сформирован с правильным контекстом."""
        response = (self.guest_client.get(
            f"{reverse('trails:trails_search')}?query=трек"))
        self.assertEqual(response.context.get('query'), 'трек')
        search_result = response.context.get('results')
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0], self.trail)
        self.assertEqual(search_result[0].name, 'Тестовый трек')
        self.assertIsInstance(response.context.get('form').fields['query'], forms.fields.CharField)



# Проверяем работу паджинатора
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PaginatorViewsTest(TestCase):

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
        cls.trails_qty = 7
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
        Паджинатор отображает корректное кол-во треков
        на 1 и 2 страницах.
        """
        objects_per_page = {
            reverse('trails:region_trails_list', kwargs={'slug_region': self.region.slug}): 4,
            reverse('trails:trails_list'): 4,
        }
        for reverse_name, qty in objects_per_page.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), qty)
                response = self.authorized_client.get(f'{reverse_name}?page=2')
                self.assertEqual(len(response.context['page_obj']), self.trails_qty - qty)

    def test_pages_contains_correct_qty_of_comments(self):
        """
        Паджинатор отображает корректное кол-во комментариев
        на 1 и 2 страницах.
        """
        trail = Trail.objects.first()
        comments_qty = 8
        comments = [
            Comment(
                trail = trail,
                author = self.user,
                ranking = 5)
            for _ in range(comments_qty)
        ]
        Comment.objects.bulk_create(comments)

        objects_per_page = {
            reverse('trails:comments_list', kwargs={'slug_trail': trail.slug}): 5,
        }
        for reverse_name, qty in objects_per_page.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), qty)
                response = self.authorized_client.get(f'{reverse_name}?page=2')
                self.assertEqual(len(response.context['page_obj']), comments_qty - qty)