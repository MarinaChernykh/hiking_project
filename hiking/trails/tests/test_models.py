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

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        region = self.region
        field_verboses = {
            "name": "Название региона",
            "slug": "Слаг",
            "description_intro": "Общая информация",
            "description_seasons": "Когда лучше ехать",
            "description_geo": "География региона",
            "description_transport": "Как добраться",
            "description_accommodation": "Где остановиться",
            "main_image": "Главный баннер",
            "mobile_image": "Главный баннер для мобильных",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    region._meta.get_field(field).verbose_name, expected_value
                )

    def test_object_absolute_url_is_correct(self):
        """url объекта region соответствует ожидаемому."""
        region = self.region
        expected_object_url = f"/region/{region.slug}/"
        self.assertEqual(expected_object_url, region.get_absolute_url())

    def test_object_name_is_title_field(self):
        """__str__  region - это строчка с содержимым region.name."""
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
            start_point_description="Тестовое описание дороги до начала маршрута",
            start_point="55.789923, 37.372381",
            region=cls.region,
            level="easy",
            distance=12,
            time="2-3 часа",
            elevation_gain=1200,
            aqua="На всем маршруте",
            route_type="loop",
            route_image="/google.com/",
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        trail = self.trail
        field_verboses = {
            "name": "Название трека",
            "slug": "Слаг",
            "short_description": "Короткое описание маршрута",
            "full_description": "Полное описание маршрута",
            "start_point_description": "Описание дороги до начала маршрута",
            "start_point": "Координаты начала маршрута",
            "region": "Регион",
            "level": "Сложность",
            "distance": "Длина, км",
            "time": "Время",
            "elevation_gain": "Набор высоты, м",
            "aqua": "Вода на маршруте",
            "route_type": "Вид маршрута",
            "route_image": "Карта маршрута",
            "main_image": "Главный баннер",
            "mobile_image": "Главный баннер для мобильных",
            "card_image": "Фото для карточки маршрута",
            "previous_trail": "Предыдущий маршрут",
            "next_trail": "Следующий маршрут",
            "created": "Дата создания статьи",
            "is_published": "Статус публикации",
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    trail._meta.get_field(field).verbose_name, expected_value
                )

    def test_object_absolute_url_is_correct(self):
        """url объекта trail соответствует ожидаемому."""
        trail = self.trail
        expected_object_url = f"/trails/{trail.slug}/"
        self.assertEqual(expected_object_url, trail.get_absolute_url())

    def test_object_name_is_title_field(self):
        """__str__  trail - это строчка с содержимым trail.name."""
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
                trail = cls.trail,
                author = cls.user,
                text = 'Тестовый комментарий',
                ranking = 4
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        comment = self.comment
        field_verboses = {
            'trail': 'Маршрут',
            'author': 'Автор',
            'text': 'Комментарий',
            'ranking': 'Оценка',
            'created': 'Дата публикации',
            'is_active': 'Статус публикации'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).verbose_name, expected_value
                )

    def test_object_name_is_correct(self):
        """__str__  comment - это строчка с именем автора и датой."""
        comment = self.comment
        expected_object_name = (
            f'Автор: {comment.author.username}, дата: {comment.created}')
        self.assertEqual(expected_object_name, str(comment))
