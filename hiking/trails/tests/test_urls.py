from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from trails.models import Region, Trail, Comment


User = get_user_model()


class TrailsURLTests(TestCase):
    """URLs tests."""
    fixtures = ['test_data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Test Guest User')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.trail = Trail.objects.first()
        cls.region = Region.objects.first()
        cls.comment = Comment.objects.create(
            trail=cls.trail,
            author=cls.user,
            ranking=5
        )
        cls.test_urls = {
            'trail_detail': f'/trails/{cls.trail.slug}/',
            'add_comment': f'/trails/{cls.trail.slug}/add_comment/',
            'edit_comment':
                f'/trails/{cls.trail.slug}/edit_comment/{cls.comment.pk}/',
            'delete_comment':
                f'/trails/{cls.trail.slug}/delete_comment/{cls.comment.pk}/',
            'favorite_list': '/trails/favorite/',
            'add_favorite': f'/trails/{cls.trail.slug}/add_favorite/',
            'delete_favorite': f'/trails/{cls.trail.slug}/delete_favorite/',
        }

    def test_urls_exist_at_desired_locations(self):
        """
        All urls, based on slugs from real db ficture data, are available.
        """
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
            'comments': map(
                lambda trail: f'/trails/{trail.slug}/comments/', trails),
            '/search/': ['/search/'],
        }
        for url_group in urls:
            for url in urls[url_group]:
                with self.subTest(url=url):
                    response = self.guest_client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """
        URLs uses correct templates.
        """
        url_templates_names = {
            '/': 'trails/index.html',
            f'/region/{self.region.slug}/': 'trails/region_details.html',
            f'/trails/{self.trail.slug}/': 'trails/trail_details.html',
            f'/trails/{self.region.slug}/all/': 'trails/trails_list.html',
            '/trails/': 'trails/trails_list.html',
            f'/trails/{self.trail.slug}/comments/':
                'trails/comments_list.html',
            '/search/': 'trails/search.html',
        }
        for address, template in url_templates_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_add_comment_url_redirect_anonimous_to_login(self):
        """
        Anonimous user is redirected to login when trying to post comment.
        """
        response = self.guest_client.get(
            self.test_urls['add_comment'], follow=True
        )
        self.assertRedirects(
                    response,
                    (f'/auth/login/?next={self.test_urls["add_comment"]}')
                )

    def test_add_comment_url_redirect_for_auth_user(self):
        """
        Authorized user is redirected to trail page with comment post form.
        """
        response = self.authorized_client.get(
            self.test_urls['add_comment'], follow=True
        )
        self.assertRedirects(response, self.test_urls['trail_detail'])

    def test_edit_and_delete_comment_url_redirect_anonimous_to_login(self):
        """
        Comment edit and delete URLs are available for authorized user
        and use correct template.
        """
        urls = [
            self.test_urls['edit_comment'],
            self.test_urls['delete_comment']
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(
                    response, (f'/auth/login/?next={url}'))

    def test_edit_and_delete_comment_url_available_for_author(self):
        """
        Comment edit and delete URLs are available for authorized user
        and use correct template.
        """
        urls = {
            self.test_urls['edit_comment']: 'trails/comment_edit.html',
            self.test_urls['delete_comment']: 'trails/comment_delete.html'
        }
        for url, template in urls.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_edit_and_delete_comment_url_redirect_for_nonauthor(self):
        not_author = User.objects.create_user(
            username='Some new user',
            email='some@mail.ru'
        )
        authorized_not_author = Client()
        authorized_not_author.force_login(not_author)
        urls = [
            self.test_urls['edit_comment'],
            self.test_urls['delete_comment']
        ]
        for url in urls:
            with self.subTest(url=url):
                response = authorized_not_author.get(url, follow=True)
                self.assertRedirects(response, self.test_urls['trail_detail'])

    def test_favorite_trails_urls_redirect_anonimous_to_login(self):
        """
        Anonimous user is redirected to login
        when trying to get favorite trails / add or remove favorite trail.
        """
        urls = [
            self.test_urls['favorite_list'],
            self.test_urls['add_favorite'],
            self.test_urls['delete_favorite'],
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, f'/auth/login/?next={url}')

    def test_favorite_trails_url_page_is_available_for_auth_user(self):
        """
        URL is available for authorized user and uses correct template.
        """
        response = self.authorized_client.get('/trails/favorite/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'trails/favorite.html')

    def test_add_remove_favorite_trails_urls_redirect_for_auth_user(self):
        """
        URLs redirect authorized user to favorite list page.
        """
        urls = [
            self.test_urls['add_favorite'],
            self.test_urls['delete_favorite'],
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url, follow=True)
                self.assertRedirects(response, self.test_urls['favorite_list'])

    def test_incorrect_url_returns_404_and_use_correct_template(self):
        """
        Incorrect URL returns 404 status code and uses custom template.
        """
        incorrect_url = '/some_url/'
        response = self.authorized_client.get(incorrect_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')
