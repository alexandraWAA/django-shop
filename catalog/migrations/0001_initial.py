from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введите заголовок статьи', max_length=200, verbose_name='заголовок')),
                ('content', models.TextField(help_text='Введите текст статьи', verbose_name='содержимое')),
                ('preview', models.ImageField(blank=True, help_text='Загрузите изображение для превью', null=True, upload_to='blog_previews/', verbose_name='превью')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('is_published', models.BooleanField(default=True, help_text='Отметьте, чтобы опубликовать статью', verbose_name='признак публикации')),
                ('views_count', models.PositiveIntegerField(default=0, help_text='Счетчик просмотров статьи', verbose_name='количество просмотров')),
            ],
            options={
                'verbose_name': 'блоговая запись',
                'verbose_name_plural': 'блоговые записи',
                'ordering': ['-created_at'],
            },
        ),
    ]