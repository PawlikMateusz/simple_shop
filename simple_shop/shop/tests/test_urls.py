from django.urls import reverse, resolve


class TestUrls:
    def test_home_view(self):
        path = reverse('shop:home_view')
        assert resolve(path).view_name == 'shop:home_view'

    def test_manage_view(self):
        path = reverse('shop:manage_view')
        assert resolve(path).view_name == 'shop:manage_view'

    def test_product_add_view(self):
        path = reverse('shop:product_add_view')
        assert resolve(path).view_name == 'shop:product_add_view'

    def test_product_detail_view(self):
        path = reverse('shop:product_detail_view',
                       kwargs={'slug': 'random-shoes'})
        assert resolve(path).view_name == 'shop:product_detail_view'

    def test_category_add_view(self):
        path = reverse('shop:category_add_view')
        assert resolve(path).view_name == 'shop:category_add_view'

    def test_category_products(self):
        path = reverse('shop:category_products', kwargs={'slug': 'Sneakers'})
        assert resolve(path).view_name == 'shop:category_products'
