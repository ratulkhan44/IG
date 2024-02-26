from django.db import models
from apps.users.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Image(models.Model):
    name = models.CharField(
        verbose_name = _("image name"),
        max_length = 150,
        unique = True,
        error_messages = {
            "unique" : _("An image with that imagename already exists.")
        }
    )
    image_file = models.ImageField(upload_to = 'images/')
    view_count = models.IntegerField()
    created_by = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'image_creator')
    created_at = models.DateTimeField(auto_now_add = True,editable = False)
    updated_at = models.DateTimeField(auto_now = True,editable = False)

    def __str__(self) -> str:
        return self.name