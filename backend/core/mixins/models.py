import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models



class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey('chat.User', verbose_name=_('Created by'), on_delete=models.SET_NULL,
                                   editable=False, null=True, related_name="created_%(class)s_set")
    modified_by = models.ForeignKey('chat.User', verbose_name=_('Modified by'), on_delete=models.SET_NULL,
                                    editable=False, null=True, related_name="modified_%(class)s_set")
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), auto_now=True)

    class Meta:
        abstract = True