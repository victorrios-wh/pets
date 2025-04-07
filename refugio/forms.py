from django.forms.utils import ErrorList
from django.utils.encoding import force_text
from django.utils.html import format_html, format_html_join

class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self:
            return ''
        return format_html(
            '<div class="errorlist">{}</div>',
            format_html_join('', '<div class="alert alert-danger">{}</div>', ((force_text(e),) for e in self))
        )