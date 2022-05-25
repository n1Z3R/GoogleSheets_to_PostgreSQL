from django.db import models


class GoogleSheetsModel(models.Model):
    number_order = models.IntegerField(db_column="заказ №")
    price = models.IntegerField(db_column="стоимость,$")
    date_delivery = models.DateField(db_column="срок поставки")
    price_rub = models.FloatField(db_column="стоимость в руб.")
