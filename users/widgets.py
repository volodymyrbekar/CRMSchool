from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.safestring import mark_safe


class CenterSelectWidget(FilteredSelectMultiple):
    def __init__(self, verbose_name, is_stacked=False, attrs=None):
        super().__init__(verbose_name, is_stacked, attrs)

    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        return mark_safe(output)