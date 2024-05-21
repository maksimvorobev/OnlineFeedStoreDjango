from django.db import models

class Feedback(models.Model):

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(max_length=255, verbose_name='Электронный адрес (email)')
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Содержимое письма')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    ip_address = models.GenericIPAddressField(verbose_name='IP отправителя',  blank=True, null=True)

    class Meta:
        db_table = 'feedback'
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-time_create']

    def __str__(self):
        return f'Вам письмо от {self.email}'
