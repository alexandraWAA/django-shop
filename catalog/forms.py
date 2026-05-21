from django import forms
from catalog.models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования товаров
    """

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введите описание товара'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену',
                'step': '0.01'
            })
        }

    def clean_price(self):
        """Валидация цены"""
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Цена должна быть больше 0')
        return price

    def clean_name(self):
        """Валидация названия"""
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError('Название должно содержать минимум 3 символа')
        return name