"""zeta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from users.views import *
from games.views import *

urlpatterns = [
	url(r'^$', home, name="home"),
    url(r'^login', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout', auth_views.logout, name='logout'),
    url(r'^create_user', create_user),
    url(r'^change_password', change_password),
    url(r'^change_pin', change_pin),
    url(r'^lock', lock),
    url(r'^send_money', send_money),
    url(r'^history', history),
    url(r'^make_bet', make_bet),
    url(r'^results', view_results),
    url(r'^view_games', view_games),
    url(r'^generate_result', generate_result),
    url(r'^latest_tiles_game', latest_tiles_game),
    url(r'^latest_cards_game', latest_cards_game),
    url(r'^account_details', account_details),
]
