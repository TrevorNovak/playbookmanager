from django.db import models

class Playbook(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='playbooks', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Playbook, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)
