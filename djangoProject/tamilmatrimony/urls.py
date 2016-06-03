from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [

    url(r'^$', "tamilmatrimony.views.profile_list", name='list'),

    url(r'^search/$', "tamilmatrimony.views.profile_search_list", name='search1'),
    url(r'^search_by_id/$', "tamilmatrimony.views.profile_search_id", name='search2'),

    url(r'^create/$', "tamilmatrimony.views.profile_create", name='create'),
    url(r'^myprofile/$', "tamilmatrimony.views.my_profile", name='myprofile'),
    url(r'^all_profiles/$', "tamilmatrimony.views.profile_list_all", name='allprofiles'),

    url(r'^myprofile/edit/$', "tamilmatrimony.views.myprofile_update", name='myedit'),

    url(r'^(?P<slug>[\w.@+-]+)/$', "tamilmatrimony.views.profile_detail", name='detail'),
    url(r'^(?P<slug>[\w.@+-]+)/edit/$', "tamilmatrimony.views.profile_update", name='edit'),


    url(r'^(?P<slug>[\w.@+-]+)/delete/$', "tamilmatrimony.views.profile_delete"),

]
