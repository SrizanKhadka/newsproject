from django.db import models

# Create your models here.


class Article(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    main_text = models.TextField()
    published_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(
        auto_now_add=True
    )  # When this option is set, the field will be set to the current date and time when an object is created for the first time.
    # Once set during the creation, it won't change subsequently when the object is updated.

    updated_date = models.DateTimeField(
        auto_now=True
    )  # When this option is set, the field will be updated to the current date and time every time the object is saved
    # This means that every time you call save() on the model instance, the updated_date field will be updated.

    def __str__(self):
        return self.title
