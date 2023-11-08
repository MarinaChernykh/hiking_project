import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.conf import settings

from trails.models import Trail, Comment
from trails.forms import CommentForm

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
class CommentCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Test User')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.trail = Trail.objects.create(
            name='Тестовый трек',
            slug='test-trail-slug',
            short_description='Тестовое описание маршрута',
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
        cls.form = CommentForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_comment(self):
        """Валидная форма создает запись в Comment."""
        comments_count = Comment.objects.count()
        form_data = {
            'ranking': 5,
            'text': 'Тестовый комментарий'
        }
        response = self.authorized_client.post(
            reverse('trails:add_comment', kwargs={'slug_trail': self.trail.slug}),
            data=form_data,
            follow=True
        )
        last_comment = Comment.objects.latest('created')
        self.assertRedirects(response, reverse('trails:trail_detail', kwargs={'slug_trail': self.trail.slug}))
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertEqual(last_comment.ranking, 5)
        self.assertEqual(last_comment.text, 'Тестовый комментарий')

    def test_not_create_comment_with_both_fields_empty(self):
        """Комментарий, где оба поля пустые, не добавляется в базу."""
        comments_count = Comment.objects.count()
        form_data = {}
        response = self.authorized_client.post(
            reverse('trails:add_comment', kwargs={'slug_trail': self.trail.slug}),
            data=form_data,
            follow=True
        )
        last_comment = Comment.objects.latest('created')
        self.assertRedirects(response, reverse('trails:trail_detail', kwargs={'slug_trail': self.trail.slug}))
        self.assertEqual(Comment.objects.count(), comments_count)
        self.assertEqual(last_comment.ranking, 5)
        self.assertEqual(last_comment.text, '')
