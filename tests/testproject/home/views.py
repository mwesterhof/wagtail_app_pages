from django.views.generic import TemplateView


class TestViewA(TemplateView):
    template_name = 'home/test_a.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['parent'] = self.parent_page
        return ctx


class TestViewB(TemplateView):
    template_name = 'home/test_b.html'
