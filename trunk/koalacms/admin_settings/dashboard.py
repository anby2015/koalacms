from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard

class CustomIndexDashboard(Dashboard):

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.children.append(modules.ModelList(
            title = _('Shop'),
                models=(
                    'shop.models.Order',
                    'shop.models.Product',
                    'shop.models.Category',
                    'shop.models.Delivery',
                    'django.contrib.auth.models.User',
                ),
        ))
        self.children.append(modules.ModelList(
                title = _('Users'),
                models=(
                    'django.contrib.auth.models.User',
                    #'users.models.UserProfile',
                ),
        ))
        self.children.append(modules.ModelList(
            title = _('Payment modules'),
                models=(
                    'webmoney.models.PaymentSettings',
                    'prochange.models.PaymentSettings',
                ),
        ))
        

        self.children.append(modules.LinkList(
            layout='stacked',
            children=(
                {
                    'title': _('Koala documentation'),
                    'url': 'http://koala.deeper4k.ru/',
                    'external': True,
                },
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list') ,
                    'url': 'http://groups.google.ru/group/django-russian',
                    'external': True,
                },
            )
        ))
        """
        self.children.append(modules.Group(
                title= _('Statistics'),
                display="tabs",
                children=[
                    nadovmeste_modules.Overview(),
                    nadovmeste_modules.Subscribers(),
                    nadovmeste_modules.Finances(),
                    nadovmeste_modules.Users(),
                ]
            ))
        """