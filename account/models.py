import os
import string
import random
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CommonBase(models.Model):
    # is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # all_objects = models.Manager()

    class Meta:
        db_table = "common_base"
        abstract = True


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, CommonBase):
    username = None
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=255, blank=False, null=False)
    profile_picture = models.ImageField(upload_to='profile_images/', null=True)
    mobile_number = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=40,
                                  validators=[RegexValidator(
                                      r'^[a-zA-Z ]*$', 'Only characters are allowed.')],
                                  help_text='Enter name', blank=False, null=False)
    last_name = models.CharField(max_length=40,
                                 validators=[RegexValidator(
                                     r'^[a-zA-Z ]*$', 'Only characters are allowed.')],
                                 help_text='Enter name', blank=False, null=False)
    birthdate = models.DateField(auto_now=False, auto_now_add=False)
    id_cards = models.BigIntegerField(null=False, blank=False)
    is_subscribe_to_news = models.BooleanField(default=False)
    is_social_auth = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthdate', 'id_cards']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __int__(self) -> int:
        return self.id

def generate_unique_code():
    invite_code = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return invite_code

class ForgotPasswordInvite(CommonBase):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True,  null=False, blank=False)
    code = models.CharField(max_length=8, default=generate_unique_code, null=True, blank=True)

    class Meta:
        db_table = 'forgot_password_invite'

    def __int__(self) -> int:
        return self.id


class Address(CommonBase):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=255, null=False, blank=False)
    mobile_number = models.CharField(max_length=255, null=False, blank=False)
    pincode = models.CharField(max_length=255, null=False, blank=False)
    address_line1 = models.TextField(null=False, blank=False)
    address_line2 = models.TextField(null=False, blank=False)
    landmark = models.TextField(null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey("account.User", null=False, blank=False,
                             related_name='addresses', on_delete=models.CASCADE)

    class Meta:
        db_table = 'address'

    def __int__(self) -> int:
        return self.id


CURRENCY_OPTIONS = {('AED', 'AED'), ('GEL', 'GEL'), ('MDL', 'MDL'), ('RON', 'RON'), 
                    ('NZD', 'NZD'), ('BDT', 'BDT'), ('ETB', 'ETB'), ('SBD', 'SBD'), 
                    ('VND', 'VND'), ('NIO', 'NIO'), ('CVE', 'CVE'), ('UAH', 'UAH'), 
                    ('AOA', 'AOA'), ('BYN', 'BYN'), ('BIF', 'BIF'), ('UGX', 'UGX'), 
                    ('BTN', 'BTN'), ('HUF', 'HUF'), ('AUD', 'AUD'), ('LVL', 'LVL'), 
                    ('AWG', 'AWG'), ('PYG', 'PYG'), ('WST', 'WST'), ('XPF', 'XPF'), 
                    ('MGA', 'MGA'), ('EGP', 'EGP'), ('KRW', 'KRW'), ('HRK', 'HRK'), 
                    ('GYD', 'GYD'), ('PKR', 'PKR'), ('USD', 'USD'), ('TRY', 'TRY'), 
                    ('PGK', 'PGK'), ('BND', 'BND'), ('THB', 'THB'), ('TWD', 'TWD'), 
                    ('BSD', 'BSD'), ('AMD', 'AMD'), ('CDF', 'CDF'), ('JOD', 'JOD'), 
                    ('BHD', 'BHD'), ('YER', 'YER'), ('ZAR', 'ZAR'), ('OMR', 'OMR'), 
                    ('DOP', 'DOP'), ('LKR', 'LKR'), ('SHP', 'SHP'), ('UZS', 'UZS'), 
                    ('ARS', 'ARS'), ('GNF', 'GNF'), ('GTQ', 'GTQ'), ('SRD', 'SRD'), 
                    ('RUB', 'RUB'), ('RWF', 'RWF'), ('BMD', 'BMD'), ('BBD', 'BBD'), 
                    ('CNY', 'CNY'), ('SLE', 'SLE'), ('STD', 'STD'), ('PAB', 'PAB'), 
                    ('PLN', 'PLN'), ('GBP', 'GBP'), ('SZL', 'SZL'), ('LTL', 'LTL'), 
                    ('CLP', 'CLP'), ('CZK', 'CZK'), ('FJD', 'FJD'), ('MRO', 'MRO'), 
                    ('MZN', 'MZN'), ('MAD', 'MAD'), ('ISK', 'ISK'), ('LSL', 'LSL'), 
                    ('SCR', 'SCR'), ('DKK', 'DKK'), ('VEF', 'VEF'),('GMD', 'GMD'), 
                    ('EEK', 'EEK'), ('BZD', 'BZD'), ('UYU', 'UYU'), ('XCD', 'XCD'), 
                    ('LAK', 'LAK'), ('SLL', 'SLL'), ('BOB', 'BOB'), ('MKD', 'MKD'), 
                    ('FKP', 'FKP'), ('RSD', 'RSD'), ('TZS', 'TZS'), ('PEN', 'PEN'), 
                    ('USDC', 'USDC'), ('KES', 'KES'), ('KHR', 'KHR'), ('ANG', 'ANG'), 
                    ('GIP', 'GIP'), ('KYD', 'KYD'), ('SOS', 'SOS'), ('TOP', 'TOP'), 
                    ('ILS', 'ILS'), ('KGS', 'KGS'), ('HKD', 'HKD'), ('QAR', 'QAR'), 
                    ('MOP', 'MOP'), ('AZN', 'AZN'), ('SAR', 'SAR'), ('DZD', 'DZD'), 
                    ('HNL', 'HNL'), ('BAM', 'BAM'), ('KMF', 'KMF'), ('BWP', 'BWP'), 
                    ('JPY', 'JPY'), ('KZT', 'KZT'), ('CHF', 'CHF'), ('HTG', 'HTG'), 
                    ('IDR', 'IDR'), ('LBP', 'LBP'), ('GHS', 'GHS'), ('VUV', 'VUV'), 
                    ('NPR', 'NPR'), ('BRL', 'BRL'), ('ZMW', 'ZMW'), ('LRD', 'LRD'), 
                    ('MYR', 'MYR'), ('NOK', 'NOK'), ('ALL', 'ALL'), ('TJS', 'TJS'), 
                    ('MMK', 'MMK'), ('SVC', 'SVC'), ('CRC', 'CRC'), ('BGN', 'BGN'), 
                    ('MWK', 'MWK'), ('TTD', 'TTD'), ('SGD', 'SGD'), ('MVR', 'MVR'), 
                    ('KWD', 'KWD'), ('DJF', 'DJF'), ('XOF', 'XOF'), ('MUR', 'MUR'), 
                    ('COP', 'COP'), ('TND', 'TND'), ('JMD', 'JMD'), ('SEK', 'SEK'), 
                    ('MNT', 'MNT'), ('AFN', 'AFN'), ('INR', 'INR'), ('PHP', 'PHP'), 
                    ('NAD', 'NAD'), ('NGN', 'NGN'), ('CAD', 'CAD'), ('MXN', 'MXN'), 
                    ('EUR', 'EUR'), ('XAF', 'XAF')}

PAYMENT_STATUS = {
    ('pending','pending'),
    ('succeeded','succeeded'),
    ('failed','failed')
}

class Order(CommonBase):
    id = models.BigAutoField(primary_key=True)
    cart = models.ManyToManyField("account.Cart", related_name='orders')
    billing_address = models.ForeignKey("account.Address", related_name='bill_orders', null=False,
                                        blank=False, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey("account.Address", related_name='ship_orders', null=False,
                                         blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey("account.User", related_name='orders', null=False,
                             blank=False, on_delete=models.CASCADE)
    order_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(
        max_length=255, null=True, blank=True, choices=CURRENCY_OPTIONS)
    order_payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS,default="pending")
    order_payment_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'order'

    def __int__(self) -> int:
        return self.id


def validate_file_extension(value):

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.PNG', '.jpg', '.JPG',
                        '.JPEG', '.jpeg', '.webp', '.svg', '.SVG']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Category(CommonBase):
    id = models.AutoField(primary_key=True)
    icon = models.FileField(upload_to='category_icons/', blank=True, null=True)
    name = models.CharField(max_length=255, null=False,
                            blank=False, unique=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    position = models.BigIntegerField(null=False, blank=False)
    has_children = models.BooleanField(default=False)
    parent = models.ForeignKey("self", related_name="sub_categories",
                               null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'category'

    def __str__(self) -> str:
        return str(self.label)

    def get_children_and_self(self):
        descendants = set()

        def _get_children_recursive(category):
            children = category.sub_categories.all()
            if children:
                for child in children:
                    descendants.add(child)
                    _get_children_recursive(child)

        _get_children_recursive(self)
        descendants.add(self)

        return list(descendants)


CONDITION_CHOICE = {
    ('new', 'new'),
    ('used', 'used'),
}

PI_TYPE = {
    ('UPC', 'UPC'),
    ('EAN', 'EAN'),
    ('ISBN', 'ISBN'),
    ('ASIN', 'ASIN'),
    ('GCID', 'GCID')
}

WEIGHT_UNITS = {
    ('pounds', 'pounds'),
    ('kilograms', 'kilograms'),
    ('Oz', 'Oz')
}

DIMENSIONS_UNIT = {
    ('inches', 'inches'),
    ('centimeters', 'centimeters')
}


class Product(CommonBase):
    id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    long_description = models.TextField(null=True, blank=True)
    SKU = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(
        max_length=255, choices=CONDITION_CHOICE, default='new')
    condition_notes = models.TextField(null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    prouduct_identifier = models.CharField(
        max_length=255, null=True, blank=True)
    prouduct_identifier_type = models.CharField(
        max_length=255, null=True, blank=True, choices=PI_TYPE)
    brand = models.CharField(max_length=255, null=True, blank=True)
    msrp = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    original_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False)
    net_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False)
    publish_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False)
    weight = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    weight_unit = models.CharField(
        max_length=255, choices=WEIGHT_UNITS, null=True, blank=True)
    package_length = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    package_width = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    package_heigth = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    dimension_type = models.CharField(
        max_length=255, choices=DIMENSIONS_UNIT, null=True, blank=True)
    status = models.BooleanField(default=True)
    parent = models.ForeignKey(
        "self", related_name="variations", null=True, blank=True, on_delete=models.CASCADE)
    category = models.ManyToManyField(
        "account.Category", related_name='products', blank=True)
    size_chart = models.ForeignKey("account.ProductDimension", related_name='products', null=True, blank=True,
                                   on_delete=models.SET_NULL)

    class Meta:
        db_table = 'product'

    def __str__(self) -> str:
        return self.product_name


def upload_image_to(instance, filename):
    upload_to = 'product_images'
    # name, ext = os.path.splitext(filename)

    return f'{upload_to}/{filename}'


class ProductImage(CommonBase):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        upload_to=upload_image_to, null=False, blank=False)
    product = models.ForeignKey("account.Product", related_name="images", null=True,
                                blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_image'

    def __str__(self) -> str:
        return self.image.path


class ProductAttribute(CommonBase):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    value = models.CharField(max_length=255, null=False, blank=False)
    product = models.ForeignKey("account.Product", related_name="attributes", null=False,
                                blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_attribute'

    def __str__(self):
        return self.name


class ProductSpecification(CommonBase):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    details = models.CharField(max_length=255, null=False, blank=False)
    product = models.ForeignKey("account.Product", related_name="specifications", null=False,
                                blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_specification'

    def __str__(self) -> str:
        return self.name


class ProductDimension(CommonBase):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    dimension_image = models.ImageField(
        upload_to='product_diamension_images', null=True)
    size_chart = models.JSONField()

    class Meta:
        db_table = 'product_dimension'

    def __int__(self) -> int:
        return self.id


class UserPreference(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField("account.Product", related_name="user_preferences")

    class Meta:
        db_table = 'user_preference'

    def __int__(self):
        return self.id

class Review(CommonBase):
    id = models.BigAutoField(primary_key=True)
    grade = models.DecimalField(
        max_digits=4, decimal_places=1, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    review = models.TextField(null=False, blank=False)
    product = models.ForeignKey("account.Product", related_name="reviews", null=False, blank=False,
                                on_delete=models.CASCADE)
    user = models.ForeignKey("account.User", related_name="user_reviews", null=False, blank=False,
                             on_delete=models.CASCADE)

    class Meta:
        db_table = 'review'

    def __int__(self):
        return self.id


class ServiceRequest(CommonBase):
    id = models.BigAutoField(primary_key=True)
    topic = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    message = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'service_request'

    def __int__(self):
        return self.id


class Cart(CommonBase):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey("account.Product", related_name="product_cart", null=False, blank=False,
                                on_delete=models.CASCADE)
    user = models.ForeignKey("account.User", related_name="user_cart", null=False, blank=False,
                             on_delete=models.CASCADE)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    is_visible = models.BooleanField(default=True)

    class Meta:
        db_table = 'cart'

    def __int__(self):
        return self.id


class Favourite(CommonBase):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey("account.Product", related_name="product_fav", null=False, blank=False,
                                on_delete=models.CASCADE)
    user = models.ForeignKey("account.User", related_name="user_fav", null=False, blank=False,
                             on_delete=models.CASCADE)

    class Meta:
        db_table = 'favourite'
        unique_together = ('product', 'user')

    def __int__(self):
        return self.id


class GlobleSize(CommonBase):
    id = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=255, null=False, blank=False)
    subcategory = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    details = models.CharField(max_length=255, null=True, blank=True)
    size = models.JSONField(null=False, blank=False)

    class Meta:
        db_table = 'globle_size'

    def __int__(self):
        return self.id
    

class SiteReview(CommonBase):
    id = models.BigAutoField(primary_key=True)
    grade = models.DecimalField(
        max_digits=4, decimal_places=1, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    review = models.TextField(null=False, blank=False)
    user = models.ForeignKey("account.User", related_name="user_site_reviews", null=False, blank=False,
                             on_delete=models.CASCADE)

    class Meta:
        db_table = 'site_review'

    def __int__(self):
        return self.id
    
class Alerts(CommonBase):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField(null=False, blank=False)
    subject = models.CharField(max_length=255, null=False, blank=False)
    created_by = models.ForeignKey("account.User", related_name='user_alerts', null=False, 
                             blank=False, on_delete=models.CASCADE)
    user = models.ManyToManyField("account.User", related_name='alert_users')
    class Meta:
        db_table = 'alerts'

    def __int__(self):
        return self.id

DISCOUNT_TYPES = {
    ('currency','currency'),
    ('percentage','percentage')
}

class Coupon(CommonBase):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    valid_from = models.DateTimeField(null=True)
    valid_to = models.DateTimeField(null=True)
    discount_value = models.FloatField(validators=[MinValueValidator(0)], null=False, blank=False)
    discount_type = models.CharField(max_length=255, choices=DISCOUNT_TYPES, null=False, blank=False)
    active = models.BooleanField(default=True)
    one_time_only = models.BooleanField(default=False)
    created_by = models.ForeignKey("account.User", related_name='user_coupons', null=False, 
                             blank=False, on_delete=models.CASCADE)
    user = models.ManyToManyField("account.User", related_name="coupons_user", through='account.CouponUser')
    class Meta:
        db_table = 'coupon'

    def __int__(self) -> int:
        return self.id
    
class CouponUser(CommonBase):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("account.User",on_delete=models.CASCADE)
    coupon = models.ForeignKey("account.Coupon",on_delete=models.CASCADE)

    class Meta:
        db_table = 'coupon_user'

    def __int__(self) -> int:
        return self.id
    
class Offer(CommonBase):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    banner = models.ImageField(upload_to="offer_images", null=True)
    discount_value = models.FloatField(validators=[MinValueValidator(0)], null=False, blank=False)
    discount_type = models.CharField(max_length=255, choices=DISCOUNT_TYPES, null=False, blank=False)
    active = models.BooleanField(default=True)
    product = models.ManyToManyField("account.Product", related_name='offer_products')
    created_by = models.ForeignKey("account.User", related_name='user_offers', null=False, 
                             blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'offer'

    def __int__(self) -> int:
        return self.id    