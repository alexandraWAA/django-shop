from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product
from catalog.constants import FORBIDDEN_WORDS


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования товаров
    """

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select',
                'style': 'border-radius: 8px; padding: 10px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Стилизация полей
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'TextInput':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'style': 'border-radius: 8px; padding: 10px;'
                })
            elif field.widget.__class__.__name__ == 'Textarea':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'rows': 5,
                    'style': 'border-radius: 8px; padding: 10px;'
                })
            elif field.widget.__class__.__name__ == 'Select':
                field.widget.attrs.update({
                    'class': 'form-select',
                    'style': 'border-radius: 8px; padding: 10px;'
                })
            elif field.widget.__class__.__name__ == 'ClearableFileInput':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'style': 'border-radius: 8px; padding: 5px;'
                })
            elif field.widget.__class__.__name__ == 'NumberInput':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0',
                    'style': 'border-radius: 8px; padding: 10px;'
                })

    def _check_forbidden_words(self, value, field_name):
        """Проверка наличия запрещенных слов"""
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
                f'Поле "{field_name}" содержит запрещенные слова: {words_str}.'
            )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name) < 3:
            raise ValidationError('Название должно содержать минимум 3 символа.')
        self._check_forbidden_words(name, 'название')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) < 10:
            raise ValidationError('Описание должно содержать минимум 10 символов.')
        self._check_forbidden_words(description, 'описание')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise ValidationError('Цена обязательна для заполнения.')
        if price < 0:
            raise ValidationError(f'Цена не может быть отрицательной. Вы ввели: {price}.')
        if price == 0:
            raise ValidationError('Цена не может быть равна 0.')
        return price