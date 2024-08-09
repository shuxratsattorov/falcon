from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db import models
from social_core.utils import slugify
from app.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'


class Profile(models.Model):
    first_name = models.CharField(max_length=55, null=True, blank=True)
    last_name = models.CharField(max_length=55, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profile'


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    amount = models.IntegerField(default=1)
    discount = models.IntegerField(null=True, blank=True, default=0)
    stock = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    users_like = models.ManyToManyField(User, related_name='users_like', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'

    def get_attributes(self) -> list:
        product_attributes = ProductAttribute.objects.filter(product=self)
        attributes = []
        for pa in product_attributes:
            attributes.append({
                'attribute_name': pa.attribute.attribute_name,
                'attribute_value': pa.attribute_value.attribute_value
            })
        return attributes

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + '-' + slugify(self.price)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'image'


class Attribute(models.Model):
    attribute_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'attribute_key'

    def __str__(self):
        return self.attribute_name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)

    class Meta:
        db_table = 'attribute_value'

    def __str__(self):
        return self.attribute_value


class ProductAttribute(models.Model):
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE)
    attribute = models.ForeignKey('app.Attribute', on_delete=models.CASCADE)
    attribute_value = models.ForeignKey('app.AttributeValue', on_delete=models.CASCADE)

    class Meta:
        db_table = 'attribute'


class Comment(models.Model):
    message = models.TextField(null=True, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'


class Rating(models.Model):
    rating = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = 'rating'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    # @property
    # def total_price(self):
    #     return self.total_cost * self.
