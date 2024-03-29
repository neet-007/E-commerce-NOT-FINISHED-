from django.db.models import Sum, Max, Min
from rest_framework.serializers import ModelSerializer
from django.core.paginator import Paginator, EmptyPage
from rest_framework import serializers
from .models import *

class User_serializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'bio', 'items_count', 'cash', 'is_verified', 'is_staff']

class Gender_serializers(ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'


class Categories_serializers(ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class Sub_Categories_serializers(ModelSerializer):
    class Meta:
        model = SubCategories
        fields = '__all__'


class Items_serializers(ModelSerializer):
    user = User_serializer(read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    gender = Gender_serializers(read_only=True)
    category = Categories_serializers(read_only=True)
    sub_category = Sub_Categories_serializers(read_only=True)
    class Meta:
        model = Items
        fields = '__all__'


class getItemsFinalSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField(method_name='get_name')
    details = serializers.SerializerMethodField(method_name='get_details')

    field = ['name', 'details']
    def get_name(self, obj):
        return self.context.get('name')

    def get_details(self, obj):
        context = self.context
        shoe_size_filter = context.get('shoe-size')
        clothing_size_filter = context.get('clothing-size')
        colors_filter = context.get('colors')
        category_filter = context.get('cat-filter')
        sub_category_filter = context.get('sub-cat-filter')
        if category_filter and sub_category_filter:
            qs = obj.items_set.filter(category__name=category_filter, sub_category__name=sub_category_filter).order_by(context.get('sort'))
        elif category_filter:
            qs = obj.items_set.filter(category__name=category_filter).order_by(context.get('sort'))
        elif sub_category_filter:
            qs = obj.items_set.filter(sub_category__name=sub_category_filter).order_by(context.get('sort'))
        else:
            qs = obj.items_set.all().order_by(context.get('sort'))

        page_num = self.context.get('page_num')
        paginator = Paginator(qs, 2)
        try:
            data = paginator.page(page_num)
        except EmptyPage:
            data = Items.objects.none()
        items = Items_serializers(data, many=True).data
        shoe_size = qs.values_list('shoe_size', flat=True).distinct()
        clothing_size = qs.values_list('clothing_size', flat=True).distinct()
        colors = qs.values_list('color', flat=True).distinct()
        max_price = qs.aggregate(Max('price'))['price__max']
        min_price = qs.aggregate(Min('price'))['price__min']
        c_ids = qs.values_list('category', flat=True).distinct()
        sc_ids = qs.values_list('sub_category', flat=True).distinct()
        categories = Categories.objects.filter(id__in=c_ids).values_list('name', flat=True).distinct()
        sub_categories = SubCategories.objects.filter(id__in=sc_ids).values_list('name', flat=True).distinct()
        return {'items':items, 'shoe_size':shoe_size, "clothing_size":clothing_size, 'colors':colors, 'max_price':max_price, "min_price":min_price, "categories":categories, "sub_categories":sub_categories, "next_page":paginator.page(page_num).has_next(), "shoe_size_filter":shoe_size_filter, "clothing_size_filter":clothing_size_filter, "colors_filter":colors_filter}

class GenderWithItemsSerializer(serializers.ModelSerializer):
    #items = serializers.SerializerMethodField(method_name='get_items')
    #categories = serializers.SerializerMethodField(method_name='get_categories')
    #sub_categories = serializers.SerializerMethodField(method_name='get_sub_categories')
    #colours = serializers.SerializerMethodField(method_name='get_colours')
    #min_max_price = serializers.SerializerMethodField(method_name='get_min_max_price')
    details = serializers.SerializerMethodField(method_name='get_details')
    class Meta:
        model = Gender
        fields = ['id', 'name', 'details']

    """def get_items(self, obj):
        items = obj.items_set.all()
        response = Items_serializers(items, many=True).data
        return response

    def get_categories(self, obj):
        distinct_item_ids = Items.objects.filter(gender=obj).values_list('id', flat=True).distinct()
        categories = Categories.objects.filter(
            items__id__in=distinct_item_ids
        ).values_list('name', flat=True).distinct()
        return categories

    def get_sub_categories(self, obj):
        #distinct_item_ids = Items.objects.filter(gender=obj).values_list('id', flat=True).distinct()
        #sub_categories = SubCategories.objects.filter(items__id__in=distinct_item_ids).values_list('name', flat=True).distinct()
        qs = obj.items_set.all()
        sc = qs.values_list('category', flat=True).distinct()
        return sc

    def get_colours(self, obj):
        pass

    def get_min_max_price(self, obj):
        qs = obj.items_set.all()
        max_price = qs.aggregate(Max('price'))['price__max']
        min_price = qs.aggregate(Min('price'))['price__min']
        return {'max_price':max_price, 'min_price':min_price}"""

    def get_details(self, obj):
        qs = obj.items_set.all().order_by('-created_at')
        page_num = self.context.get('page_num')
        paginator = Paginator(qs, 2)
        try:
            data = paginator.page(page_num)
        except EmptyPage:
            data = Items.objects.none()
        items = Items_serializers(data, many=True).data
        shoe_size = qs.values_list('shoe_size', flat=True).distinct()
        clothing_size = qs.values_list('clothing_size', flat=True).distinct()
        colors = qs.values_list('color', flat=True).distinct()
        max_price = qs.aggregate(Max('price'))['price__max']
        min_price = qs.aggregate(Min('price'))['price__min']
        c_ids = qs.values_list('category', flat=True).distinct()
        sc_ids = qs.values_list('sub_category', flat=True).distinct()
        categories = Categories.objects.filter(id__in=c_ids).values_list('name', flat=True).distinct()
        sub_categories = SubCategories.objects.filter(id__in=sc_ids).values_list('name', flat=True).distinct()
        return {'items':items, 'shoe_size':shoe_size, "clothing_size":clothing_size, 'colors':colors, 'max_price':max_price, "min_price":min_price, "categories":categories, "sub_categories":sub_categories}

class CategoriesWithItemsSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(method_name='get_items')

    class Meta:
        model = Categories
        fields = ['id', 'name', 'items']

    def get_items(self, obj):
        items = obj.items_set.all()
        response = Items_serializers(items, many=True).data
        return response


class SubCategoriesWithItemsSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(method_name='get_items')

    class Meta:
        model = SubCategories
        fields = ['id', 'name', 'items']

    def get_items(self, obj):
        items = obj.items_set.all()
        response = Items_serializers(items, many=True).data
        return response


class Ratings_serializers(ModelSerializer):
    user = User_serializer(read_only=True)
    item = Items_serializers(read_only=True)
    class Meta:
        model = Ratings
        fields = '__all__'

class Comments_serializers(ModelSerializer):
    user = User_serializer(read_only=True)
    item = Items_serializers(read_only=True)
    class Meta:
        model = Comments
        fields = '__all__'

class Up_votes_serializers(ModelSerializer):
    user = User_serializer(read_only=True)
    Comment = Comments_serializers(read_only=True)
    class Meta:
        model = Up_votes
        fields = '__all__'

class WishList_serializers(ModelSerializer):
    user = User_serializer(read_only=True)
    items = Items_serializers(read_only=True, many=True)
    price = serializers.SerializerMethodField(method_name='calculate_price')
    count = serializers.SerializerMethodField(method_name='items_count')
    class Meta:
        model = WishList
        fields = '__all__'

    def calculate_price(self, product:WishList):
        total_price = product.items.aggregate(total_price=Sum('price'))['total_price']
        return total_price or 0

    def items_count(self, product:WishList):
        return product.items.all().count()

class Cart_item_serializers(ModelSerializer):
    item = Items_serializers(read_only=True, required=False)
    price = serializers.SerializerMethodField(method_name='calculate_price')
    class Meta:
        model = CartItem
        fields = '__all__'

    def calculate_price(self, item:CartItem):
        return item.item.price * item.quantity

class items_id_quantity(serializers.Serializer):
    items = serializers.ListField()
    quantity = serializers.ListField()
    def validate(self, attrs):
        items = attrs['items']
        quantity = attrs['quantity']

        if items and quantity and len(items) == len(quantity):
            for i in range(len(items)):
                if not int(items[i]):
                    raise serializers.ValidationError('items must be integer ids')

                if not int(quantity[i]) or quantity[i] == 0:
                    raise serializers.ValidationError('quantity is 0 or not integer')
                if Items.objects.filter(id__in=items).exists:
                     return attrs

        raise serializers.ValidationError('invalid data')

class Cart_serializers(ModelSerializer):
    user = User_serializer(read_only=True)
    cart_items = Cart_item_serializers(source='cart_cartitem', many=True)
    price = serializers.SerializerMethodField(method_name='calculate_price')
    count = serializers.SerializerMethodField(method_name='cart_items_count')
    class Meta:
        model = Cart
        fields = '__all__'

    def calculate_price(self, product:Cart):
        total = 0
        for cart_item in product.cart_cartitem.all():
            total += cart_item.quantity * cart_item.item.price

        return total

    def cart_items_count(self, product:Cart):
        return product.cart_cartitem.all().count()

class Order_item_serializers(ModelSerializer):
    item = Items_serializers()
    price = serializers.SerializerMethodField(method_name='calculate_price')
    class Meta:
        model = OrderItem
        fields = '__all__'

    def calculate_price(self, product:OrderItem):
        return product.quantity * product.item.price

class Order_serializers(ModelSerializer):
    user = User_serializer(read_only=True)
    order_items = Order_item_serializers(source='order_orderitem',read_only=True, many=True)
    price = serializers.SerializerMethodField(method_name='calculate_price')
    count = serializers.SerializerMethodField(method_name='order_item_count')
    class Meta:
        model = Order
        fields = '__all__'

    def calculate_price(self, product:Order):
        total = 0
        for order_item in product.order_orderitem.all():
            total += order_item.quantity * order_item.item.price

        return total

    def order_item_count(self, product:Order):
        return product.order_orderitem.all().count()

class UserComplateSerializers(ModelSerializer):
    order = serializers.SerializerMethodField(method_name='get_order')
    cart = serializers.SerializerMethodField(method_name='get_cart')
    class Meta:
        model = User
        fields = ['id', 'username', 'is_verified', 'cash', 'is_staff', 'order', 'cart']

    def get_order(self, obj):
        order = obj.user_order.all()
        serializered_order = Order_serializers(order, many=True).data
        return serializered_order

    def get_cart(self, obj):
        cart = obj.user_cart.all()
        serializered_cart = Cart_serializers(cart, many=True).data
        return serializered_cart


class HomePageSerializers(serializers.Serializer):
    sub_categoies = Categories_serializers(many=True)
    trending_items = Items_serializers(many=True)
    main_categories = Categories_serializers(many=True)
    shoe_categories = Items_serializers(many=True)
    sport_categories = Categories_serializers(many=True)
