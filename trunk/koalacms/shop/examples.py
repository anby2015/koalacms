class Categories(models.Model):
    """
    Product's categories.
    """
    parent              = models.ForeignKey('self', blank=True, null=True, verbose_name=_('Parent'))
    path                = models.CharField(max_length=100, verbose_name = _('Path'))
    title               = models.CharField(max_length=100, verbose_name = _('Name'))
    description         = models.TextField(blank=True, verbose_name = _('Description'), help_text=_('Optional'))

    class Meta:
        ordering = ("-path", "id")
        verbose_name = _('Categories')
        verbose_name_plural = _('Categories')
        
    class Admin:
        list_display = ('title')
    """
    def __str__(self):
        title = len(self.path)/3*'-' + self.title
        return u"%s" % title
    """
    def __unicode__(self):
        title = len(self.path)/3*'-' + self.title
        return u"%s" % title
    """
    def get_absolute_url(self):
        if self.parent_id:
            return "/tag/%s/%s/" % (self.parent.description, self.description)
        else:
            return "/tag/%s/" % (self.description)
    
    def _recurse_for_parents(self, cat_obj):
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.parent
            p_list.append(p.title)
            more = self._recurse_for_parents(p)
            p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list
        
    def get_separator(self):
        return ' :: '
    
    def _parents_repr(self):
        p_list = self._recurse_for_parents(self)
        return self.get_separator().join(p_list)
    _parents_repr.description = "Tag parents"
    """
    def save(self, force_insert=False, force_update=False):
        obj = self
        path_list = []
        #path_list.append("%03d" % obj.pk)
        if self.parent_id:
            while obj.parent_id:
               path_list.append("%03d" % obj.parent_id)
               obj = obj.parent
            path_list.reverse()
            self.path = ''.join(path_list)
            #path=self.path
            #assert False
        if not self.pk:
            super(Categories, self).save(force_insert, force_update)
        if self.parent_id == self.pk:
            from django.core.exceptions import ValidationError
            raise ValidationError("You must not save a category in itself!")
        
        
def post_save_handler(sender, **kwargs):
    obj = kwargs['instance']
    path_list = []
    path_list.append("%03d" % obj.pk)
    if kwargs['instance'].parent_id:
        while obj.parent_id:
           path_list.append("%03d" % obj.parent_id)
           obj = obj.parent
    path_list.reverse()
    path = ''.join(path_list)
    obj = sender.objects.get(pk=kwargs['instance'].pk)
    obj.path = path
    obj.save()
    #kwargs['instance'].path = path
    #kwargs['instance'].save()
    #p = kwargs['instance'].path
    assert False

#post_save.connect(post_save_handler, sender=Categories)