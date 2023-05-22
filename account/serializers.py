from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from collections import defaultdict
from django.db import transaction
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import razorpay

from account.models import *


'''
Address Serializer
'''

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model=Address
        fields=['id', 'full_name', 'mobile_number', 'pincode', 'address_line1', 
                'address_line2', 'landmark', 'town', 'state', 'country']
        

class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields=['full_name', 'mobile_number', 'pincode', 'address_line1', 
                'address_line2', 'landmark', 'town', 'state', 'country','user']
        read_only_fields = ['user']
        
    def create(self, validated_data):
        instance = self.Meta.model.objects.create(**validated_data,user=self.context['request'].user)
        instance.save()
        return instance
        
'''
User Serializer
'''

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user and not user.is_active:
            raise serializers.ValidationError(
                "Account has been deactivated. \n Please contact your company's admin to restore your account."
            )

        if not user:
            raise serializers.ValidationError("Email or Password is wrong.")

        refresh = RefreshToken.for_user(user)
        data = {"access": str(refresh.access_token), "refresh": str(refresh)}

        return data
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','email','profile_picture','first_name','last_name','mobile_number','birthdate','is_subscribe_to_news','is_social_auth']


class UserGetSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','email','profile_picture','first_name','last_name','birthdate','mobile_number','addresses','is_subscribe_to_news','is_social_auth']

    def get_addresses(self, obj):
        addresses = obj.addresses.all()
        serializer = AddressSerializer(addresses, many=True)
        return serializer.data


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'birthdate', 'mobile_number', 'id_cards', 'is_subscribe_to_news','is_social_auth']
        write_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance
    

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthdate', 'mobile_number', 'id_cards', "is_subscribe_to_news"]
        write_only_fields = ['id']

class ForgotPasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ForgotPasswordInvite
        fields = ['email', 'code']
        read_only_fields = ['code']

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data['email']).first()
        if not user:
            raise serializers.ValidationError("account doesn't exist.",code="invalid")
        if user.is_social_auth == True:
            raise serializers.ValidationError("Can't reset password. account linked to other social account",code="invalid")
        instnace = self.Meta.model.objects.create(**validated_data)
        instnace.save()
        return instnace
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    password = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()
        

'''
category serializers
'''
class CategoryAllSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'label', 'icon', 'has_children', 'children']

    def get_children(self):
        obj = self.Meta.model.get(name="main_menu")
        children = obj.sub_categories.all()
        serializer = self.__class__(children, many=True)
        return serializer.data
    # def validate(self, validated_data):
    #     category = self.Meta.model.objects.get()
    #     Categories = self.Meta.model.get_childrens(validated_data)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name','color','label','icon','has_children','parent','sub_categories']
        depth=1


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name','color','label','icon','has_children']

'''
specification serializer
'''
class SpecificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSpecification
        fields = ['id','name','details']


'''
Image Serizlizer
'''

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','image','product']

    
'''
specification serializer
'''
class SpecificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSpecification
        fields = ['id','name','details']


'''
size chart serializers
'''

class SizechartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductDimension
        fields = ['id','name','dimension_image','size_chart']

    depth = 1


'''
review serializer
'''

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id','grade','title','review']

class ReviewProductSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['id','grade','title','review','user']
        depth = 1 
    
    def get_user(self, obj):
        serializer = UserSerializer(obj.user)
        return serializer.data
class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id','grade','title','review','product']

    def create(self, validated_data):
        # print("validated_data",validated_data)
        instance = self.Meta.model.objects.create(**validated_data,user=self.context['request'].user)
        instance.save()
        return instance
    


class ServiceRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceRequest
        fields = ['id', 'topic', 'email', 'name', 'message']

    

'''
product serializer
'''

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','product_name','description','brand','status','original_price','publish_price','images']
        depth = 1


class ProductRetrieveSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    variations = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()
    size_chart = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','product_name','description','long_description','SKU','brand','condition','condition_notes',
                    'model','prouduct_identifier','prouduct_identifier_type','status','msrp','original_price',
                    'net_price','publish_price','weight','weight_unit','package_length','package_width',
                    'package_heigth','dimension_type','variations','images','specifications','size_chart',
                    'attributes', 'options', 'reviews']
        # depth = 1
    
    def get_images(self, obj):
        images = obj.images.all()
        serializer = ImageSerializer(images, many=True)
        return serializer.data

    def get_reviews(self, obj):
        reviwes = obj.reviews.all()
        # print(reviwes)
        serializer = ReviewProductSerializer(reviwes, many=True)
        return serializer.data

    def get_size_chart(self, obj):
        serializer = SizechartSerializer(obj.size_chart)
        return serializer.data


    def get_variations(self, obj):
        variations = obj.variations.all()
        serializer = self.__class__(variations, many=True)
        return serializer.data
    
    def get_specifications(self, obj):
        specifications = obj.specifications.all()
        serializer = SpecificationSerializer(specifications, many=True)
        return serializer.data

    def get_options(self, obj):

        attributes_dict = defaultdict(list)
        for attribute in obj.attributes.all():
            attributes_dict[attribute.name].append(attribute.value)
        for variation in obj.variations.all():
            for attribute in variation.attributes.all():
                attributes_dict[attribute.name].append(attribute.value)
        attributes_list = []
        for name, values in attributes_dict.items():
            attribute_data = {
                'name': name,
                'values': list(set(values)) # remove duplicates
            }
            attributes_list.append(attribute_data)
        return attributes_list

    def get_attributes(self, obj):
        attributes_dict = defaultdict(list)
        for attribute in obj.attributes.all():
            attributes_dict[attribute.name].append(attribute.value)
        attributes_list = []
        for name, values in attributes_dict.items():
            attribute_data = {
                'name': name,
                'values': list(values) # remove duplicates
            }
            attributes_list.append(attribute_data)
        return attributes_list


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = ['name','value']


class ProductCreateSerializer(serializers.ModelSerializer):
    upload_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )
    # specification = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id','product_name','upload_images','description','long_description','SKU','brand',
                  'condition','condition_notes','model','prouduct_identifier','prouduct_identifier_type',
                  'status','msrp','original_price','net_price','publish_price','weight','weight_unit','package_length',
                  'package_width','package_heigth','dimension_type']
        
    def create(self, validated_data):
        files = validated_data.pop('upload_images')
        instance = self.Meta.model(**validated_data)
        instance.status = True
        instance.save()
        if len(files)>1:
            for img in files:
                ProductImage.objects.create(image=img,product=instance)
        else:
            ProductImage.objects.create(image=files[0],product=instance)
        return instance
    

class ProductUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','product_name','description','long_description','SKU','brand',
                  'condition','condition_notes','model','prouduct_identifier','prouduct_identifier_type',
                  'status','msrp','original_price','net_price','publish_price','weight','weight_unit','package_length',
                  'package_width','package_heigth','dimension_type']
        
class RecommendationSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = UserPreference
        fields = ['products']
        
    def get_products(self, obj):
        # Get the user's preferences
        userpre = UserPreference.objects.get(user=self.context['request'].user.id)
        user_preferences = userpre.products.all()

        # Calculate the cosine similarity between the user's preferences and the preferences of other users
        similar_users = UserPreference.objects.exclude(user=self.context['request'].user).filter(products__in=user_preferences)
        similar_users_products = similar_users.values_list("products", flat=True).distinct()
        recommendation_scores = {}
        for product_id in similar_users_products:
            product = Product.objects.get(id=product_id)
            similarity_sum = 0
            for similar_user in similar_users.filter(products=product):
                similarity_sum += similar_user.products.count()
            recommendation_scores[product_id] = similarity_sum / similar_users.count()

        # Sort the products by their recommendation score and return the top 10
        recommended_products = Product.objects.filter(id__in=recommendation_scores.keys()).order_by("-id")
        recommended_products = sorted(recommended_products, key=lambda p: recommendation_scores[p.id], reverse=True)[:10]

        # Serialize and return the recommended products
        serializer = ProductSerializer(recommended_products, many=True)
        return serializer.data
    
class AddPreferenceSerializer(serializers.ModelSerializer):
    product = serializers.ListField(
        child=serializers.IntegerField(),
        write_only = True
    )
    class Meta:
        model = UserPreference
        fields = ['id', 'user', 'product', 'products']
        read_only_fields = ['id', 'user', 'products']

    def create(self, validated_data):
        instnace = self.Meta.model.objects.create(user=self.context['request'].user)
        instnace.products.add(*validated_data['product'])
        instnace.save()
        return instnace
        


    
'''
Cart Serializers
'''
class CartSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'product', 'attributes', 'quantity', 'total', 'orders']
        # depth = 1
    
    def get_product(self, obj):
        serializer = ProductSerializer(obj.product)
        return serializer.data

    def get_attributes(self, obj):
        attributes_dict = defaultdict(list)
        for attribute in obj.product.attributes.all():
            attributes_dict[attribute.name].append(attribute.value)
        attributes_list = []
        for name, values in attributes_dict.items():
            attribute_data = {
                'name': name,
                'values': list(values) # remove duplicates
            }
            attributes_list.append(attribute_data)
        return attributes_list

class CartCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['product','user','quantity','total']
        read_only_fields = ['user','total']

    def create(self, validated_data):
        # product = Product.objects.get(id=validated_data['product'])
        total = float(validated_data['quantity'])*float(validated_data['product'].publish_price)
        instance = self.Meta.model.objects.create(product=validated_data['product'],
                                                quantity=validated_data['quantity'],
                                                user=self.context['request'].user,
                                                total=total)
        instance.save()

        
        return instance


'''
favorite serilizer
'''
class FavSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ['id','product']
        depth = 1


class FavCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = ['product','user']
        read_only_fields = ['user']

    def create(self, validated_data):
        fav = self.Meta.model.objects.filter(product=validated_data['product'],
                                             user=self.context['request'].user)
        if fav:
            raise serializers.ValidationError("Product already in favourites",409)


        instance = self.Meta.model.objects.create(product=validated_data['product'],
                                                  user=self.context['request'].user)
        instance.save()
        return instance
    

'''
Order Serializer
'''
class OrderSerializer(serializers.ModelSerializer):

    cart = serializers.SerializerMethodField()
    billing_address = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'cart', 'billing_address', 'shipping_address',
                  'order_amount', 'currency', 'order_payment_status', 'order_payment_id','created_date']

    def get_cart(self, obj):
        carts = obj.cart.all()
        serializer = CartSerializer(carts, many=True)
        return serializer.data
    
    def get_billing_address(self, obj):
        serializer = AddressSerializer(obj.billing_address)
        return serializer.data
    
    def get_shipping_address(self, obj):
        serializer = AddressSerializer(obj.shipping_address)
        return serializer.data

class OrderListSerializer(serializers.Serializer):
    cart = serializers.SerializerMethodField()

    def get_cart(self, obj):
        carts = Cart.objects.filter(is_visible=False)
        serializer = CartSerializer(carts, many=True)

        return serializer.data

class OrderCreateSerializer(serializers.ModelSerializer):
    cart_list = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    payment = serializers.DictField(read_only=True)
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'cart_list', 'billing_address', 'shipping_address','user',
                  'order_amount', 'currency', 'order_payment_status', 'order_payment_id','payment']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        # cart = validated_data.pop('cart_list')
        # instance = self.Meta.model.objects.create(**validated_data,
        #                                           user=self.context['request'].user)
        # instance.cart.add(*cart)
        # instance.save()
        # with transaction.atomic():
        #     for id in cart:
        #         Cart.objects.filter(id=id).update(is_visible=False)
        cart = validated_data.pop('cart_list')
        instance = self.Meta.model.objects.create(**validated_data,
                                                  user=self.context['request'].user)
        # order = self.Meta.model.objects.create(**validated_data)      
        razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY, settings.RAZOR_SECRET))
        payment = razorpay_client.order.create({'amount': float(validated_data['order_amount']), 'currency': validated_data['currency']})
        instance.cart.add(*cart)
        instance.order_payment_id = payment["id"]
        instance.save()
        
        with transaction.atomic():
            for id in cart:
                Cart.objects.filter(id=id).update(is_visible=False)
        data = {
            'id':instance.id, 
            'billing_address':instance.billing_address, 
            'shipping_address':instance.shipping_address,
            'user':instance.user,
            'order_amount':instance.order_amount, 
            'currency':instance.currency,
            'order_payment_status':instance.order_payment_status, 
            'order_payment_id':instance.order_payment_id,
            # 'payment':payment
        }
        return data
    
class VerifyPaymentSerializer(serializers.Serializer):
    razorpay_payment_id = serializers.CharField()
    razorpay_order_id = serializers.CharField()
    # razorpay_signature = serializers.CharField()
    order_id = serializers.IntegerField()

'''
globlesize serializer
'''
class GlobleSizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GlobleSize
        fields = ["id", "category", "subcategory", "title", "details", "size"]

'''
site review serializer
'''
class SiteReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = SiteReview
        fields = ['id','grade','title','review',]
    
class SiteReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SiteReview
        fields = ['id','grade','title','review',]

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(**validated_data,user=self.context['request'].user)
        instance.save()
        return instance
    

'''
Alerts Serializer
'''
class AlertSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    class Meta:
        model = Alerts
        fields = ['id','content','created_by','users'] 

    def get_users(self, obj):
        serializer = UserSerializer(obj.user, many=True)
        return serializer.data
    

class AlertCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerts
        fields = ['content','subject','created_by']
        read_only_fields = ['created_by'] 
    
    def create(self, validated_data):
        # users = validated_data.pop(users)
        users = [ user.id for user in User.objects.filter(is_subscribe_to_news=True)]
        insatnce = self.Meta.model.objects.create(content=validated_data['content'],
                                                  subject=validated_data['subject'],
                                                  created_by=self.context['request'].user)
        insatnce.user.add(*users)
        send_mail(
                from_email="bhagyesh@samcomtechnobrains.com",
                message=validated_data['content'],
                subject=validated_data['subject'],
                recipient_list= [user.email for user in User.objects.filter(is_subscribe_to_news=True)],
                fail_silently=True
                )
        insatnce.save()
        return insatnce
    
'''
coupon serializer
'''
class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ['id', 'code', 'valid_from', 'valid_to', 'discount_value', 'created_by','discount_type', 'active','one_time_only']

class CouponCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ['code', 'valid_from', 'valid_to', 'discount_value','discount_type', 'active','one_time_only']

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(**validated_data,
                                                  created_by = self.context['request'].user)
        instance.save()
        return instance
    
class ApplyCouponSerializer(serializers.Serializer):
    # user = serializers.IntegerField(write_only=True)
    cost = serializers.FloatField()
    code = serializers.CharField()

    def validate(self, validated_data):

        try:
            coupon = Coupon.objects.get(code=validated_data['code'])

        except Coupon.DoesNotExist:
            raise serializers.ValidationError({"code":"Invalid Coupon Code"})
        
        # if coupon.expiry_date < timezone.now():
        #     raise serializers.ValidationError("Coupon has expired")
        
        if coupon.valid_from > timezone.now() or coupon.valid_to < timezone.now():
            raise serializers.ValidationError({"code":"Coupon has expired"})
        
        if coupon.active == False:
            raise serializers.ValidationError({"code":"Coupon is not active"})
        
        if coupon.one_time_only == True:
            couponuser = CouponUser.objects.filter(coupon_id=coupon.id,user_id=self.context['request'].user).first()
            if couponuser:
                raise serializers.ValidationError({"code":"Coupon already used"}) 
        
        if coupon.discount_type == "percentage":
            cost = validated_data['cost'] - (validated_data['cost']*coupon.discount_value)/100
            
        elif coupon.discount_type == "currency":
            cost = validated_data['cost'] - coupon.discount_value

        coupon.user.add(self.context['request'].user)
        coupon.save()
        
        return {"cost":cost, "code":validated_data["code"]}
         
'''
offer serializer
'''
class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['id', 'name', 'banner', 'discount_value', 'discount_type', 'created_by', 'active']

class OfferGetSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = Offer
        fields = ['id', 'name', 'banner', 'discount_value', 'discount_type', 'created_by', 'active','product']
        # depth = 1
    
    def get_product(self, obj):
        products = obj.product.all()
        serializer = ProductSerializer(products, many=True)
        return serializer.data

class OfferCreateSerializer(serializers.ModelSerializer):
    products = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    class Meta:
        model = Offer
        fields = ['name', 'banner', 'discount_value', 'discount_type', 'active', 'products']

    def create(self, validated_data):
        products = validated_data.pop("products")
        instnace = self.Meta.model.objects.create(**validated_data, created_by=self.context['request'].user)
        instnace.product.add(*products)
        instnace.save()
        return instnace