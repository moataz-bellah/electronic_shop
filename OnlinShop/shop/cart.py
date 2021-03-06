#from decimal import Decimal
from django.conf import settings
from .models import Product
#from coupons.models import Coupons


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False,comment=''):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = int(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price),
                                      'comment':comment,
                                      }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['comment']=comment
        else:
            self.cart[product_id]['quantity'] += int(quantity)
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def update(self,product):
        product_id = str(product.id)


    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = item['price']
            item['total_price'] = item['price'] * item['quantity']
            yield item
    def getQuantity(self,product_id):
        product_ids = self.cart.keys()
        print(product_ids)
        for x in self.cart:
            if str(x) == str(product_id):
                print(x)
                quan = self.cart[str(x)]['quantity']
                return quan
        return 0

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):

        return sum(int(item['price']) * int(item['quantity']) for item in self.cart.values())+5
