from rest_framework import serializers
from .models import Category, Product, Order, OrderItem
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','slug','image')

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('id','name','slug','description','price','stock','category','image')

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    class Meta:
        model = OrderItem
        fields = ('id','product','product_id','price','quantity')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    class Meta:
        model = Order
        fields = ('id','user','name','email','phone','address','total_price','status','date','items')
        read_only_fields = ('id','user','total_price','status','date')

    def create(self, validated_data):
        items_data = self.initial_data.get('items', [])
        # create order
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None
        order = Order.objects.create(
            user=user,
            name=validated_data.get('name'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            address=validated_data.get('address'),
            total_price=0
        )
        total = 0
        for item in items_data:
            pid = item.get('product_id')
            quantity = int(item.get('quantity', 1))
            product = Product.objects.get(id=pid)
            price = product.price
            OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
            total += float(price) * quantity
        order.total_price = total
        order.save()
        return order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')
