from django.urls import path
from . import views

urlpatterns = [
    path('',views.welcome,name="home-page"),
    #facebook
    path('facebook/dashboard/',views.facebook_dashboard,name='fb-dashboard'),
    path('facebook/views/',views.facebook_view,name='fb-views'),
    path('facebook/post/',views.facebook_post,name='fb-post'),
    path('facebook/show/',views.face_make_post,name='fb-process-form'),
    #instagram
    path('instagram/dashboard/',views.instagram_dashboard,name='ig-dashboard'),
    path('instagram/views/',views.insta_views,name='ig-views'),
    path('instagram/post/',views.insta_post,name='ig-post'),
    path('instagram/show/',views.insta_make_post,name='ig-process-form'),
    #all
    path('all/post/',views.postAll,name='ig-post'),
    path('all/show/',views.all_make_post,name='all-process-form'),
    #set-up
    path('setup/',views.setup,name='set-up'),
    path('setup/process',views.setup_process,name='set-up-process')
]