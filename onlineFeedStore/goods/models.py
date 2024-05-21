from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Categories(MPTTModel):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
        verbose_name="Родительская категория",
    )
    image = models.ImageField(
        upload_to="categories_images", blank=True, null=True, verbose_name="Изображение"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        unique_together = [["parent", "slug"]]
        db_table = "category"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    category = TreeForeignKey(
        "Categories",
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="Категория",
    )
    image_small = models.ImageField(
        upload_to="goods_images",
        blank=True,
        null=True,
        verbose_name="Изображение для католога",
    )
    image_big = models.ImageField(
        upload_to="goods_images",
        blank=True,
        null=True,
        verbose_name="Изображение для карточки товара",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание для товара в каталоге"
    )
    price = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    advantages = models.TextField(
        blank=True, null=True, verbose_name="Преимущества (ENTER)"
    )
    release_form = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Форма выпуска"
    )
    packing = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Упаковка"
    )
    nutritional_info = models.TextField(
        blank=True, null=True, verbose_name="Питательность хар-ки (; ENTER)"
    )
    composition = models.TextField(blank=True, null=True, verbose_name="Состав (ENTER)")
    feeding_standards = models.TextField(
        blank=True, null=True, verbose_name="Нормы кормления (ENTER) для комбикорма/(; ENTER) для БМВД"
    )
    recommendations = models.TextField(
        blank=True, null=True, verbose_name="Рекомендации (ENTER)"
    )

    class Meta:
        db_table = "product"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("id",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})

    def sell_price(self):
        return self.price
