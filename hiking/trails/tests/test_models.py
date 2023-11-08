from django.contrib.auth import get_user_model
from django.test import TestCase

from trails.models import Region, Trail, Comment


User = get_user_model()


class RegionModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.region = Region.objects.create(
            name="Тестовый регион",
            slug="test-region",
            description_intro="Отличный регион для тестов",
            description_seasons="Прекрасен в любой сезон",
            description_geo="Тест география",
            description_transport="Тест транспорт",
            description_accommodation="Тест размещение",
        )

    def test_object_absolute_url_is_correct(self):
        """Region object absolute url is correct."""
        region = self.region
        expected_object_url = f"/region/{region.slug}/"
        self.assertEqual(expected_object_url, region.get_absolute_url())

    def test_object_name_is_title_field(self):
        """__str__  for region is it's name."""
        region = self.region
        expected_object_name = region.name
        self.assertEqual(expected_object_name, str(region))


class TrailModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.region = Region.objects.create(
            name="Тестовый регион",
            slug="test-region",
        )
        cls.trail = Trail.objects.create(
            name="Тестовое имя",
            slug="test-slug",
            short_description="Тестовое описание маршрута",
            full_description="Полное тестовое описание маршрута",
            start_point="55.789923, 37.372381",
            region=cls.region,
            route_image="/google.com/",
        )

    def test_object_absolute_url_is_correct(self):
        """Trail object absolute url is correct."""
        trail = self.trail
        expected_object_url = f"/trails/{trail.slug}/"
        self.assertEqual(expected_object_url, trail.get_absolute_url())

    def test_object_name_is_title_field(self):
        """__str__  for trail is it's name."""
        trail = self.trail
        expected_object_name = trail.name
        self.assertEqual(expected_object_name, str(trail))


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.trail = Trail.objects.create(
            name="Тестовое имя",
            slug="test-slug",
        )
        cls.comment = Comment.objects.create(
                trail=cls.trail,
                author=cls.user,
                text='Тестовый комментарий',
                ranking=4
        )

    def test_object_name_is_correct(self):
        """
        __str__  for comment is it's author username and publication date.
        """
        comment = self.comment
        expected_object_name = (
            f'Автор: {comment.author.username}, дата: {comment.created}')
        self.assertEqual(expected_object_name, str(comment))
