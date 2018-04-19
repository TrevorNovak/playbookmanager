from django.db import models
from .STIX import create_stix

class Playbook(models.Model):
    """
    This model defines a general Playbook. Specific Playbooks extend this model.
    """
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='attack-pattern--')
    body = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='playbooks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
    	return self.title

    def save(self, *args, **kwargs):
    	# when you create a new playbook, user inputs are sent to STIX.py to convert the data
    	if (self.created_at == self.updated_at):
    		stix_obj_bundle = create_stix(self)
    		self.title = stix_obj_bundle.id
    		self.body = stix_obj_bundle
    	super(Playbook, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)
