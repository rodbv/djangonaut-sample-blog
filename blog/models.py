import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def _unique_slug(model_class, source, slug_field="slug", max_length=50):
    base = slugify(source)[:max_length]
    slug = base
    counter = 1
    qs = model_class.objects
    while qs.filter(**{slug_field: slug}).exists():
        slug = f"{base}-{counter}"
        counter += 1
    return slug


class TimestampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Blog(TimestampedModel):
    name = models.CharField(max_length=120)
    description = models.TextField()
    slug = models.SlugField(unique=True, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blogs",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(Blog, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(TimestampedModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(Post, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(TimestampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    def __str__(self):
        return f"Comment by {self.created_by} on {self.post}"


class Organization(TimestampedModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Invoice(TimestampedModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="invoices",
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateField()

    def __str__(self):
        return f"Invoice {self.id} for {self.organization}"


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name="books")
    published_date = models.DateField()

    def __str__(self):
        return f"{self.title}"
