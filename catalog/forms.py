from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from PIL import Image
import io
from catalog.models import Product, Category
from catalog.constants import FORBIDDEN_WORDS, MAX_IMAGE_SIZE_BYTES, ALLOWED_IMAGE_FORMATS


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования товаров
    С валидацией:
    - запрещенных слов в названии и описании
    - отрицательной цены
    - формата и размера изображения (доп. задание)
    """

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        """
        Стилизация формы через метод __init__
        Добавляем CSS-классы ко всем полям
        """
        super().__init__(*args, **kwargs)

        # Стили для всех полей
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название товара',
            'style': 'border-radius: 8px; padding: 10px;'
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Введите описание товара',
            'style': 'border-radius: 8px; padding: 10px;'
        })

        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/jpeg,image/png',
            'style': 'border-radius: 8px; padding: 5px;'
        })

        self.fields['category'].widget.attrs.update({
            'class': 'form-select',
            'style': 'border-radius: 8px; padding: 10px;'
        })

        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите цену товара',
            'step': '0.01',
            'min': '0',
            'style': 'border-radius: 8px; padding: 10px;'
        })

        # Чекбоксы и другие поля
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-check-input',
                    'style': 'width: 20px; height: 20px;'
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'form-select',
                    'style': 'border-radius: 8px; padding: 10px;'
                })

    def _check_forbidden_words(self, value, field_name):
        """
        Проверка наличия запрещенных слов в тексте
        Регистр игнорируется
        """
        if not value:
            return

        value_lower = value.lower()
        found_words = []

        for forbidden in FORBIDDEN_WORDS:
            if forbidden in value_lower:
                found_words.append(forbidden)

        if found_words:
            words_str = ', '.join(found_words)
            raise ValidationError(
                f'Поле "{field_name}" содержит запрещенные слова: {words_str}. '
                f'Пожалуйста, удалите их.'
            )

    def clean_name(self):
        """
        Валидация названия продукта
        Проверка на запрещенные слова
        """
        name = self.cleaned_data.get('name')

        if name and len(name) < 3:
            raise ValidationError('Название должно содержать минимум 3 символа.')

        self._check_forbidden_words(name, 'название')

        return name

    def clean_description(self):
        """
        Валидация описания продукта
        Проверка на запрещенные слова
        """
        description = self.cleaned_data.get('description')

        if description and len(description) < 10:
            raise ValidationError('Описание должно содержать минимум 10 символов.')

        self._check_forbidden_words(description, 'описание')

        return description

    def clean_price(self):
        """
        Кастомная валидация для поля price
        Проверяет, что цена не может быть отрицательной
        """
        price = self.cleaned_data.get('price')

        if price is None:
            raise ValidationError('Цена обязательна для заполнения.')

        if price < 0:
            raise ValidationError(
                'Цена не может быть отрицательной. '
                f'Вы ввели: {price}. Пожалуйста, введите корректную цену.'
            )

        if price == 0:
            raise ValidationError(
                'Цена не может быть равна 0. '
                'Пожалуйста, укажите цену больше 0.'
            )

        if price > 1000000:
            raise ValidationError(
                'Цена не может превышать 1 000 000. '
                'Пожалуйста, введите корректную цену.'
            )

        return price

    def clean_image(self):
        """
        * ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ
        Валидация изображения:
        - проверка формата (JPEG или PNG)
        - проверка размера (не более 5 МБ)
        """
        image = self.cleaned_data.get('image')

        if not image:
            return image

        # Проверка размера файла
        if image.size > MAX_IMAGE_SIZE_BYTES:
            raise ValidationError(
                f'Размер изображения не должен превышать {MAX_IMAGE_SIZE_BYTES / (1024 * 1024)} МБ. '
                f'Ваш файл: {image.size / (1024 * 1024):.2f} МБ.'
            )

        # Проверка формата файла
        try:
            # Открываем изображение с помощью Pillow
            img = Image.open(image)
            format_name = img.format

            if format_name not in ALLOWED_IMAGE_FORMATS:
                raise ValidationError(
                    f'Неподдерживаемый формат изображения. '
                    f'Разрешены: {", ".join(ALLOWED_IMAGE_FORMATS)}. '
                    f'Ваш формат: {format_name}'
                )

            # Проверка размеров изображения (опционально)
            width, height = img.size
            if width < 100 or height < 100:
                raise ValidationError(
                    f'Изображение слишком маленькое. '
                    f'Минимальный размер: 100x100 пикселей. '
                    f'Ваше изображение: {width}x{height}'
                )

            if width > 4000 or height > 4000:
                raise ValidationError(
                    f'Изображение слишком большое. '
                    f'Максимальный размер: 4000x4000 пикселей. '
                    f'Ваше изображение: {width}x{height}'
                )

        except Exception as e:
            raise ValidationError(f'Ошибка при обработке изображения: {str(e)}')

        return image