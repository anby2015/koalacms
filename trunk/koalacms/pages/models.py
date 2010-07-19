from django.db import models
from django.utils.translation import ugettext_lazy as _

class Page(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s' % self.title
    class Meta:
        ordering = ["-id"]