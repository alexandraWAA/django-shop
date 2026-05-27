from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    """
    Кастомная команда для создания группы "Модератор продуктов"
    """
    help = 'Создает группу "Модератор продуктов" и назначает ей права'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Создание группы "Модератор продуктов"...'))

        # Получаем content type для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем или создаем права
        can_unpublish, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=content_type,
        )

        can_delete_product = Permission.objects.get(
            codename='delete_product',
            content_type=content_type,
        )

        # Создаем или получаем группу
        moderator_group, created = Group.objects.get_or_create(
            name='Модератор продуктов'
        )

        # Назначаем права группе
        moderator_group.permissions.add(can_unpublish, can_delete_product)

        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Группа "{moderator_group.name}" создана'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Группа "{moderator_group.name}" уже существует'))

        self.stdout.write(self.style.SUCCESS('📋 Назначены права:'))
        self.stdout.write(f'   - can_unpublish_product (отмена публикации)')
        self.stdout.write(f'   - delete_product (удаление продукта)')

        self.stdout.write(self.style.SUCCESS('\n✅ Команда выполнена успешно!'))