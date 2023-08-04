from django.db import models


class Products(models.Model):
    code = models.IntegerField('Код товара', unique=True)
    link = models.CharField('Ссылка', unique=True, max_length=600)
    title = models.CharField('Название', max_length=1000, blank=True, null=True)
    price = models.FloatField('Цена', blank=True, null=True)
    description = models.CharField('Описание', max_length=3000, blank=True, null=True)
    image_url = models.CharField('Ссылка на фото', max_length=500, blank=True, null=True)
    discount = models.CharField('Скидка', max_length=30, blank=True, null=True)
    date = models.DateTimeField('Обновлено', auto_now=True,
                                help_text="Дата и время добавления либо последнего обновления записи")

    def __str__(self):
        return self.link

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("-date",)
