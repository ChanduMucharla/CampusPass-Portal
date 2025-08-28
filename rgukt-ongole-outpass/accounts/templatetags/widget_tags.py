from django import template
register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    try:
        return field.as_widget(attrs={'class': css})
    except Exception:
        return field

