from django.db import models
from .search import PlaybookIndex

class Playbook(models.Model):
    """
    This model defines a general Playbook. Specific Playbooks extend this model.
    """
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True, default='')
    body = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='playbooks', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Playbook, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def indexing(self):
        obj = PlaybookIndex(
            meta={'id': self.id},
            owner=self.owner.username,
            created=self.created,
            title=self.title,
            body=self.body
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    # class Meta:
    #     ordering = ('created',)
