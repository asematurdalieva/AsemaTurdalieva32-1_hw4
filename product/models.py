from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title


@property
def rating(self):
    len_ = len(self.reviews.all())
    sum_ = [i.stars for i in self.reviews.all()]
    if len_ > 0:
        return sum_ / len_
    return 0


STARS = (
    (1, '*'),
    (2, '*' * 2),
    (3, '*' * 3),
    (4, '*' * 4),
    (5, '*' * 5),
)


class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=STARS, default=5)

    def __str__(self):
        return self.text
