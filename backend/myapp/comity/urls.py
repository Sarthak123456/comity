from django.contrib import admin
from django.urls import path
from comity import views
from django.conf import  settings
from django.conf.urls.static import  static
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # path('', views.login, name='login'),
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('login', csrf_exempt(views.loginUser)),
    path('logout', csrf_exempt(views.logoutUser)),
    path('signup', csrf_exempt(views.signUpUser)),
    path('act_sub', csrf_exempt(views.activateSubscription)),
    path('deact_sub', csrf_exempt(views.deactivateSubscription)),
    path('bank_details', csrf_exempt(views.saveBankDetails)),
    path('get/bank_details', csrf_exempt(views.getBankDetails)),
    path('addGroup', csrf_exempt(views.addGroup)),
    path('get/groups', csrf_exempt(views.getAllGroups)),
    path('add/user/', csrf_exempt(views.addUserToGroups)),
    path('group/start/', csrf_exempt(views.sendNotficationToStartComity)),
    path('get/<str:id>/winner/<str:winner>/<str:finish>', views.returnWinner, name="returnWinner"),
    path('submit/bid', csrf_exempt(views.bidMoney)),
    # path('get/bid', csrf_exempt(views.getBidDetails)),
    path('get/<str:id>/transfer/<str:name>', views.transferMoney, name="transferMoney"),
    # path('addUserToGroups' , views.addUserToGroups , name = 'addUserToGroups'),
    path('profile', views.profile, name='profile'),
    path('viewProfile', views.viewProfile, name='viewProfile'),
    path('delete/groups', csrf_exempt(views.deleteAllGroups)),
    path('delete/group/<str:id>', csrf_exempt(views.deleteGroup)),
    path('get/user/', csrf_exempt(views.getUser)),
    path('get/group/users/', csrf_exempt(views.viewUsersInGroup)),
    path('delete/group/user/', csrf_exempt(views.deleteUsersInGroup)),
    path('get/razorpay/order_id/', csrf_exempt(views.createRazorPayOrderId)),
    path('get/razorpay/save/', csrf_exempt(views.verifyAndSavePayment)),





]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
