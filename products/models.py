from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Comment(models.Model):
    user = models.ForeignKey("users.Profile", on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=100)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    def __str__(self) -> str:
        return (
            f"user: {self.user}\n" f"rating: {self.rating}\n" f"content: {self.content}"
        )


class Product(models.Model):
    name = models.TextField(max_length=25)
    description = models.TextField(max_length=100, default=None)
    price = models.FloatField(default=5)
    comments = models.ManyToManyField(
        Comment,
        blank=True,
        related_name="product_comments",
    )
