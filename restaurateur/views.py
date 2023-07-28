import os
import requests
from django import forms, setup
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import views as auth_views, authenticate, login
from django.db.models import F, Q
from environs import Env
from sql_util.utils import SubquerySum
from geopy import distance

from foodcartapp.models import Product, Restaurant, Order
from geo_data.models import GeoData


os.environ['DJANGO_SETTINGS_MODULE'] = 'star_burger.settings'
setup()

env = Env()
env.read_env()


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def fetch_coordinates(apikey, address):
    try:
        geo_data = GeoData.objects.get(address=address)
        lon = geo_data.longitude
        lat = geo_data.latitude
    except GeoData.DoesNotExist:
        base_url = "https://geocode-maps.yandex.ru/1.x"
        response = requests.get(
            base_url, params={
                'geocode': address,
                'apikey': apikey,
                'format': "json",
            },
            timeout=10,
        )
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection']['featureMember']

        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        GeoData.objects.create(
            address=address,
            latitude=lat,
            longitude=lon,
        )
    return lon, lat


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    yandex_api_key = env('YANDEX_API_KEY')

    orders = Order.objects.filter(~Q(status='CL'))\
        .prefetch_related('products__item__menu_items__restaurant')\
        .annotate(
            cost=SubquerySum(
                F('products__previous_price')*F('products__count')
            ),
        )



    viewed_restaurants = dict()  # key = name, value = object

    for order in orders:
        try:
            viewed_restaurants_names = set()

            order_items = order.products.all()
            for iters, order_item in enumerate(order_items):
                items_viewed_restaurants_names = set()
                for menu_item in order_item.item.menu_items.all():
                    if menu_item.restaurant.name not in items_viewed_restaurants_names:
                        viewed_restaurants[menu_item.restaurant.name] = menu_item.restaurant
                        items_viewed_restaurants_names.add(
                            menu_item.restaurant.name
                        )
                viewed_restaurants_names = viewed_restaurants_names\
                    .intersection(items_viewed_restaurants_names)\
                    if iters > 0 else items_viewed_restaurants_names

            order_coordinates = fetch_coordinates(
                yandex_api_key,
                order.address,
            )
            order_restaurants = []
            for restaurant_name in viewed_restaurants_names:
                restaurant = viewed_restaurants[restaurant_name]
                restaurant_coordinates = fetch_coordinates(
                    yandex_api_key, restaurant.address
                )
                print(restaurant_coordinates)
                distance_restaurant_order = 0
                if order_coordinates and restaurant_coordinates:
                    if order_coordinates[0] and order_coordinates[1]\
                       and restaurant_coordinates[0]\
                       and restaurant_coordinates[1]:
                        distance_restaurant_order = -1
                        if restaurant_coordinates != order_coordinates:
                            distance_restaurant_order = distance.distance(
                                restaurant_coordinates[::-1],
                                order_coordinates[::-1],
                            )
                order_restaurants.append((
                    restaurant,
                    distance_restaurant_order,
                ))
            order.restaurants = order_restaurants
        except Exception:
            pass


    return render(request, template_name='order_items.html', context={
        'order_items': orders,
    })
