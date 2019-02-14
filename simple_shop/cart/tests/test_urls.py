from django.urls import reverse, resolve


class TestUrls:
    def test_cart_detail(self):
        path = reverse('cart:cart_detail')
        assert resolve(path).view_name == 'cart:cart_detail'

    def test_cart_add(self):
        path = reverse('cart:cart_add')
        assert resolve(path).view_name == 'cart:cart_add'

    def test_cart_remove(self):
        path = reverse('cart:cart_remove', kwargs={'pk': 1})
        assert resolve(path).view_name == 'cart:cart_remove'
