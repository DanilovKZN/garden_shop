class TitleMixin:
    """Миксин для передачи титула в контексте,
    чтобы не заморачиваться с переопределением
    (get_context_data) в каждом контроллере."""
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
