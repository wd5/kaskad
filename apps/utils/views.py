# -*- coding: utf-8 -*-

class CreateViewMixin():
    def get_success_url(self):
        if self.success_url:
            url = self.success_url
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to. Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url