from django.conf.urls import url

from design import views

urlpatterns = [
    url(r'^login/',views.login,name='login'),
    url(r'^register/',views.register,name='register'),
    url(r'^index/',views.index,name='index'),
    url(r'^search/',views.search,name='search'),
    url(r'^drawing/',views.drawing,name='drawing'),
    url(r'^clickImg/',views.clickImg,name='clickImg'),
    url(r'^user_base_info/',views.user_base_info,name='user_base_info'),
    url(r'^user_pic_info/',views.user_pic_info,name='user_pic_info'),
    url(r'^user_pass_info/',views.user_pass_info,name='user_pass_info'),
    url(r'^user_collection/',views.user_collection,name='user_collection'),
    url(r'^logout/',views.logout,name='logout'),
    url(r'^collection/',views.collection,name='colletcion'),
]