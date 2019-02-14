from django.urls import reverse, resolve


class TestUrls:
    def test_order_create(self):
        path = reverse('orders:order_create')
        assert resolve(path).view_name == 'orders:order_create'

    def test_order_list(self):
        path = reverse('orders:order_list')
        assert resolve(path).view_name == 'orders:order_list'
