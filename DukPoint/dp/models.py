from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.CharField(max_length=300, unique=True)
    password = models.CharField(max_length=400)
    points = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=150, default='')

    # last_login 필드 추가
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True)
    username = None

    objects = CustomUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'


class Store(models.Model):  # 가게 정보
    name = models.CharField(max_length=200)  # 가게 이름
    location = models.CharField(max_length=400)  # 위치
    phone = models.CharField(max_length=30, blank=True, null=True)  # 전화번호
    is_cafe = models.BooleanField()  # True -> 카페, False -> 레스토랑
    image = models.ImageField(upload_to='dp/store_images/%Y/%m/%d', blank=True, null=True)  # 가게 이미지, pip install pillow 필수
    discount = models.PositiveIntegerField(default=0)  # 할인 정보
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Menu(models.Model):  # 가게의 메뉴 정보
    store = models.ForeignKey('Store', on_delete=models.CASCADE)  # 가게가 삭제되면 메뉴들도 함께 삭제
    name = models.CharField(max_length=200)  # 메뉴 이름
    image = models.ImageField(upload_to='dp/menu_images/%Y/%m/%d', blank=True, null=True)  # 메뉴 이미지, pip install pillow 필수
    price = models.PositiveIntegerField(default=0)  # 메뉴 가격

    def __str__(self):
        return f'{self.name} - {self.price}'


class Review(models.Model):  # 후기
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, verbose_name='가게 이름')
    comment = models.TextField(verbose_name='후기')
    created_at = models.DateTimeField(auto_now_add=True)  # 후기 생성 날짜 자동 저장
    image = models.ImageField(upload_to='dp/review1/%Y/%m/%d', null=True, blank=True, verbose_name='이미지')

    def __str__(self):
        return f'Review by {self.user.email} for {self.store.name}'


class Payment(models.Model):  # 결제 정보
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 결제한 사용자
    store = models.ForeignKey('Store', on_delete=models.CASCADE)  # 구매한 가게 정보와 가게의 discount 가져오기
    menu_item = models.ForeignKey('Menu', on_delete=models.CASCADE)  # 구매한 상품
    user_points = models.PositiveIntegerField(default=0)  # 보유한 포인트
    points_used = models.PositiveIntegerField(default=0)  # 사용한 포인트
    total_amount = models.PositiveIntegerField(default=0)  # 총 결제 금액
    payment_date = models.DateTimeField(auto_now_add=True)  # 결제한 날짜 자동 저장

    """
    def save(self, *args, **kwargs):
        self.points_used = min(self.points_used, self.user_points)

        # Calculate total_amount based on menu_item's price, points_used, and store's discount.
        if not self.total_amount:
            menu_price = self.menu_item.price
            discount = self.store.discount  # Assuming 'discount' is a field in the Store model
            self.total_amount = max(0, menu_price - self.points_used - discount)

        super().save(*args, **kwargs)
    """

