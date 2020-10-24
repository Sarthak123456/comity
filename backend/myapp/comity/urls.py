from django.contrib import admin
from django.urls import path
from comity import views

urlpatterns = [
    # path('', views.login, name='login'),
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('login', views.loginUser, name='loginUser'),
    path('logout', views.logoutUser, name='logoutUser'),
    path('signup', views.signUpUser, name='signup'),
    path('addGroup', views.addGroup, name='addGroup'),
    path('getServices', views.getServices, name='getServices'),
    # path('getGroups', views.getGroups, name='getGroups'),
    path('get/<str:id>',views.get,name="get"),
    path('get/<str:id>/start',views.sendNotficationToStartComity,name="sendNotficationToStartComity"),
    path('get/<str:id>/winner/<str:name>',views.returnWinner,name="returnWinner"),
    path('get/<str:id>/bid',views.bidMoney,name="bidMoney"),
    path('get/<str:id>/transfer/<str:name>',views.transferMoney,name="transferMoney"),
    path('addUserToGroups' , views.addUserToGroups , name = 'addUserToGroups'),
    path('profile' , views.profile, name = 'profile'),
    path('viewProfile' , views.viewProfile, name = 'viewProfile')

]