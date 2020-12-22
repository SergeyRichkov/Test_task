from django.db import models


class Sales(models.Model):  # Продажи

    customer = models.CharField(max_length=40, null=False )  # логин покупателя
    item = models.CharField(max_length=50, null=False)  # наименование товара
    total = models.FloatField(blank=False)  # сумма сделки
    quantity = models.IntegerField(null=False)  # количество товара, шт
    date = models.DateTimeField()  # дата и время регистрации сделки

    def __str__(self):
        return f"{self.id}: {self.customer}"




