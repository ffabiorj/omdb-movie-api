from django.db.models import Manager


class FilterManager(Manager):

    def filter_ignoring_none(self, *args, **kwargs):
        """Remove None parameters, then filter"""
        updated_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return super().filter(*args, **updated_kwargs)
