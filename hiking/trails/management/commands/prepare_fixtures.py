import json

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        initial_file_path = settings.BASE_DIR / 'data/trails_dump.json'
        result_file_path = settings.BASE_DIR / 'trails/fixtures/test_data.json'

        with open(initial_file_path, encoding="utf8") as file:
            data = json.load(file)
            for obj in data:
                if obj['model'] == 'trails.region':
                    obj['fields']['description_intro'] = (
                        f"Описание региона {obj['fields']['name']}"
                        )
                    obj['fields']['description_seasons'] = (
                        f"Когда ехать в {obj['fields']['name']}")
                    obj['fields']['description_geo'] = (
                        f"Где находится {obj['fields']['name']}")
                    obj['fields']['description_transport'] = (
                        f"Как добраться до региона {obj['fields']['name']}")
                    obj['fields']['description_accommodation'] = (
                        f"Проживание в регионе {obj['fields']['name']}")
                elif obj['model'] == 'trails.trail':
                    obj['fields']['short_description'] = (
                        f"Короткое описание трека {obj['fields']['name']}")
                    obj['fields']['full_description'] = (
                        f"Полное описание трека {obj['fields']['name']}")
                    obj['fields']['start_point_description'] = (
                        f"Где находится трек {obj['fields']['name']}")
                    obj['fields']['aqua'] = (
                        f"Что с водой на треке {obj['fields']['name']}")

            with open(result_file_path, 'w', encoding='utf8') as new_file:
                new_file.write(json.dumps(data, indent=3, ensure_ascii=False))
