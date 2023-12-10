from django.urls import path, include
from . import views
from .views import MyPageView
from .views import search
from .views import SignInView, SignUpView, SignUpView2, SignUpView3, SignUpView4, SignUpView5
from .views import Update, SavePayment
from .views import mypage_detail_1, mypage_detail_2, check_password_mypage
from .views import change_password_mypage
from .views import review1, ReviewCreate


urlpatterns = [
    path('save_payment/', SavePayment.as_view(), name='save_payment'),
    path('update/<int:user_id>/', Update.as_view(), name='update'),
    path('order_payment/<int:store_id>/<int:menu_id>/', views.OrderPayment.as_view(), name='order_payment'),
    path('store_menu/<int:pk>/', views.StoreMenu.as_view(), name='store_menu'),
    path('store/', views.store, name='store'),
    path('search/', search, name='search'),
    path('', views.main, name='main'),
    path('mypage/', MyPageView.as_view(), name='mypage'),
    path('mypage_detail_1/', views.mypage_detail_1, name= 'mypage_detail_1'),
    path('mypage_detail_2/', views.mypage_detail_2, name= 'mypage_detail_2'),
    path('check_password_mypage/', check_password_mypage, name='check_password_mypage'),  # 비밀번호 확인
    path('change_password_mypage/', change_password_mypage, name='change_password_mypage'),
    path('my_logout/', views.my_logout, name='my_logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup2/', SignUpView2.as_view(), name='signup2'),
    path('signup3/', SignUpView3.as_view(), name='signup3'),
    path('signup4/', SignUpView4.as_view(), name='signup4'),
    path('signup_complete/', SignUpView5.as_view(), name='signup_complete'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('review1/', review1, name='review1'),
    path('create_post/', ReviewCreate.as_view(), name='create_post'),
    path('accounts/', include('django.contrib.auth.urls')),
]

