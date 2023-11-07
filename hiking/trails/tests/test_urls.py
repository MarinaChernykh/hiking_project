from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from trails.models import Region, Trail


User = get_user_model()


class TrailsURLTests(TestCase):
    fixtures = ['mysite_data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Test Guest User')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_urls_exist_at_desired_locations(self):
        regions = Region.objects.all()
        trails = Trail.objects.all()
        urls = {
            'index': ['/'],
            'regions': map(lambda region: f'/region/{region.slug}/', regions),
            'trails': map(lambda trail: f'/trails/{trail.slug}/', trails),
            'trails_list': ['/trails/'],
            'trails_list_by_reg': map(
                lambda region: f'/trails/{region.slug}/all/', regions
            ),
            'comments': map(lambda trail: f'/trails/{trail.slug}/comments/', trails),
            '/search/': ['/search/'],
        }
        for url_group in urls:
            for url in urls[url_group]:
                with self.subTest(url=url):
                    response = self.guest_client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        region = Region.objects.first()
        trail = Trail.objects.first()

        url_templates_names = {
            '/': 'trails/index.html',
            f'/region/{region.slug}/': 'trails/region_details.html',
            f'/trails/{trail.slug}/': 'trails/trail_details.html',
            f'/trails/{region.slug}/all/': 'trails/trails_list.html',
            '/trails/': 'trails/trails_list.html',
            f'/trails/{trail.slug}/comments/': 'trails/comments_list.html',
            '/search/': 'trails/search.html',
        }
        for address, template in url_templates_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_add_comment_url_redirect_anonimous_to_login(self):
        trail = Trail.objects.first()
        response = self.guest_client.get(f'/trails/{trail.slug}/comment/', follow=True)
        self.assertRedirects(
                    response, (f'/auth/login/?next=/trails/{trail.slug}/comment/')
                )

    def test_add_comment_url_trail_page_redirect_for_auth_user(self):
        trail = Trail.objects.first()
        response = self.authorized_client.get(f'/trails/{trail.slug}/comment/', follow=True)
        self.assertRedirects(response, (f'/trails/{trail.slug}/'))

    def test_incorrect_url_returns_404_and_use_correct_template(self):
        incorrect_url = '/some_url/'
        response = self.authorized_client.get(incorrect_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')
