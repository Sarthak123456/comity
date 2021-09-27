from django.shortcuts import  HttpResponse, render, redirect
# from comity.models import Services
from comity.models import *
import pytz
import uuid
# from django.db.models import Q
# from time import time
import datetime
import razorpay
import os
import json
from random import randint
import logging
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
import jwt


from django.core import serializers


# from django.core import serializers
# from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    users = User.objects.all()
    user = request.user
    # groups = group_info_table.objects.filter(created_by_user = user)
    grpNameByUser = group_table.objects.filter(u_id=user)
    # grpInfo = group_info_table.objects.filter(name = grpNameByUser)
    groupList = []
    # grp = []
    # //Find a better way later
    for grp in grpNameByUser:
        print("grp = {}".format(grp.g_id))
        grpInfo = group_info_table.objects.get(id=uuid.UUID(str(grp.g_id)))
        groupList.append(grpInfo)
    if (grpNameByUser.count() > 0):
        context = {"users": users, "groupList": groupList}
    else:
        context = {"users": users}
    # if grpInfo:
    #     print("grpInfo = " , grpInfo)
    return render(request, 'index.html', context)


def addGroup(request):
    milliseconds = getCurrentMilis()
    logger = getLogger()
    logger.debug("Added Group")

    # date = datetime.fromtimestamp(milliseconds/1000.0)
    if request.method == "POST":
        name = request.POST.get('name')
        amt = request.POST.get('amount')
        duration = request.POST.get('duration')
        # user = request.user
        user = User.objects.get(username=decryptToken(request.POST.get('token')))
        group = group_info_table(name=name, amount=amt, duration=duration, created_by_user=user,
                                 created_at=milliseconds, updated_at=milliseconds)
        group.save()
        # user = User.objects.get(id=ids)
        groupUuid = group_info_table.objects.get(id=group.id)
        # print("G_ID = " , groupUuid)
        u_id = user
        users = group_table(g_id=groupUuid, u_id=u_id)
        users.save()
        # messages.success(request, '"{}" saved!'.format(name))
        # groupUuid = group_info_table.objects.get(id=group.id)
        usersInGroup = group_table.objects.filter(g_id=group.id)

        users = []
        for user in usersInGroup:
            users.append({
                "name": user.u_id.username,
                "id": user.u_id.id,
                "first_name": user.u_id.first_name,
                "last_name": user.u_id.last_name,
                "email": user.u_id.email
            }
            )

        data= {
                "name": groupUuid.name,
                "amount": groupUuid.amount,
                "duration": groupUuid.duration,
                "g_id" : groupUuid.id,
                "usersInGroup": users,
                "admin" : groupUuid.created_by_user.username,
                "status": groupUuid.status
            }


        # qs_json = serializers.serialize('json', group)

        # To send the entire list as json
        # return HttpResponse(qs_json, content_type='application/json')

        return JsonResponse(data, safe=False)
        # SomeModel_json = serializers.serialize("json", groupUuid)
        # data = {"groups": SomeModel_json}
        # return JsonResponse(data)
        # return JsonResponse({'addedGroup': 'True'})
    return HttpResponse("Failed")


def about(request):
    return render(request, 'about.html')
    # return HttpResponse("About worked")


# def services(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         desc = request.POST.get('desc')
#         services = Services(name=name, email=email, phone=phone, desc=desc, date=datetime.datetime.now())
#         services.save()
#         messages.success(request, 'Services request saved!')
#         return redirect('/')
#     return render(request, 'services.html')
#     # return HttpResponse("Services worked")


# def getServices(request):
#     services = User.objects.all()
#     return HttpResponse(services.id)


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            user = User.objects.select_related().get(username=request.user)
            token = returnToken(user.username)
            return JsonResponse({'token': str(token) , "user" : user.username})
    return HttpResponse('Failed')


def returnToken(username):
    encoded_jwt = jwt.encode({"username": username}, "secret", algorithm="HS256")
    # key = "FLqz4-FWMT4M_0dihy5vqvG8rwvS6F7QQxFhI6lW1CU="
    # f = Fernet(key)
    # username = str(username)
    # encrypted_data = f.encrypt(str.encode(f'{username}'))
    return encoded_jwt

def decryptToken(encoded_jwt):
    # key = "FLqz4-FWMT4M_0dihy5vqvG8rwvS6F7QQxFhI6lW1CU="
    # f = Fernet(key)
    # decrypted_data = f.decrypt(str.encode(encrypted_data.split("'")[1]))
    decrypted_data = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    return decrypted_data.get('username')



def signUpUser(request):
    if request.method == "POST":
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            address_line_1 = request.POST.get('address_line_1')
            address_line_2 = request.POST.get('address_line_2')
            password = request.POST.get('password')

            print(password)

            user = User(username = username, first_name =first_name, last_name=last_name, email=email)
            user.password = make_password(password)
            user.save()
            user_info = UserInfo(u_id = user, mobile=mobile, address_line_1 = address_line_1, address_line_2 = address_line_2)
            user_info.save()
        except IntegrityError:
            print("Username has to be unique", username)
            return JsonResponse({"message": f'Username {username} already exists!'})

        return JsonResponse({"message" :'success'})
    return HttpResponse('failed')

    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/login')
    # else:
    #     form = UserCreationForm()
    # return render(request, 'signup.html', {"form": form})

def saveBankDetails(request):
    if request.method == "POST":
        account_number = request.POST.get('account_number')
        name = request.POST.get('name')
        ifsc = request.POST.get('ifsc')
        branch_address = request.POST.get('branch_address')
        gpay_qr = request.FILES.get("gpay_qr") if request.FILES.get("gpay_qr") else ''
        paytm_qr = request.FILES.get("paytm_qr") if request.FILES.get("paytm_qr") else ''
        phonepe_qr = request.FILES.get("phonepe_qr") if request.FILES.get("phonepe_qr") else ''

        print(ifsc , phonepe_qr, branch_address)

        user = User.objects.get(username = name)
        # user.password = make_password(password)
        # user.save()
        # user_info = UserInfo.objects.get_or_create(u_id = user)
        user_info = UserInfo.objects.get(u_id = user)
        user_info.account_number = account_number
        user_info.ifsc = ifsc
        user_info.branch_address = branch_address
        user_info.gpay_qr_code = gpay_qr
        user_info.phonepe_qr_code = phonepe_qr
        user_info.paytm_qr_code = paytm_qr
        user_info.save()

        return JsonResponse({"message" : "success"})
    return HttpResponse('failed')

def getBankDetails(request):
    if request.method == "POST":
        # account_number = request.POST.get('account_number')
        name = request.POST.get('name')
        # ifsc = request.POST.get('ifsc')
        # branch_address = request.POST.get('branch_address')
        # gpay_qr = request.FILES.get("gpay_qr") if request.FILES["gpay_qr"] else ''
        # paytm_qr = request.FILES["paytm_qr"] if request.FILES.get("paytm_qr") else ''
        # phonepe_qr = request.FILES["phonepe_qr"] if request.FILES.get("phonepe_qr") else ''
        #
        # print(ifsc , phonepe_qr, branch_address)

        user = User.objects.get(username = name)
        # user.password = make_password(password)
        # user.save()
        # user_info = UserInfo.objects.get_or_create(u_id = user)
        user_info = UserInfo.objects.get(u_id = user)
        data={

            "account_number" : user_info.account_number,
            "ifsc": user_info.ifsc,
            "branch_address": user_info.branch_address,
            "gpay_qr_code": user_info.gpay_qr_code.url if user_info.gpay_qr_code else None,
            "phonepe_qr_code": user_info.phonepe_qr_code.url if user_info.phonepe_qr_code else None,
            "paytm_qr_code": user_info.paytm_qr_code.url if user_info.paytm_qr_code else None,

        }
        # user_info.account_number = account_number
        # user_info.ifsc = ifsc
        # user_info.branch_address = branch_address
        # user_info.gpay_qr_code = gpay_qr
        # user_info.phonepe_qr_code = phonepe_qr
        # user_info.paytm_qr_code = paytm_qr
        # user_info.save()

        return JsonResponse(data, safe=False)
    return HttpResponse('failed')


def logoutUser(request):
    if request.method == "POST":
        user = User.objects.get(username = 'Sarthak')

        print("logout(request) = " , logout(request).encode())

        print("is_anonymous = " , user.is_anonymous)
        print("request.user = " , request.user.username)
        # user.session_set.all().delete()
        return JsonResponse({"message" : "Success"})

def addUserToGroups(request):
    print("addusrss")
    # people = group_table.objects.filter(g_id=id)
    # users = User.objects.exclude(username=request.user)
    # group = group_info_table.objects.get(id=id)
    # print("CreatedByUser = {} , User = {}".format(group.created_by_user , request.user) )
    # username = 'Sarthak'
    if request.method != None:
        if request.method == "POST":
            try:
                g_id = request.POST.get("g_id")
                username = request.POST.get("username")
                group = group_info_table.objects.get(id=g_id)
                u_id = User.objects.get(username=username)
                # print("addusrss" , group , u_id.username)

                # list_of_input_ids = request.POST.getlist('inputs')
                # if (list_of_input_ids):
                #     for ids in list_of_input_ids:
                #         user = User.objects.get(id=ids)
                #         g_id = group
                #         u_id = user
                group_table.objects.get_or_create(g_id=group, u_id=u_id)
                # group = group_info_table(name=name, amount=amt, duration=duration, created_by_user=user,
                #                          created_at=milliseconds, updated_at=milliseconds)
                # group.save()
                return JsonResponse({'user': str(u_id)})
            except AttributeError:
                print("Exception occurred while adding users to the Group")
            # return HttpResponse('Failed')

        # return redirect('/get/{}'.format(id))
    # context = {"people": people, "users": users, "id": id, "group": group, "request": request}
    # return render(request, 'groups.html', context)
    return HttpResponse('Failed')


def viewUsersInGroup(request):
    data = []
    if request.method == "POST":
        g_id = request.POST.get("g_id")
        grp = group_info_table.objects.get(id=g_id)
        # print("addusrss" , group , g_id)

        # list_of_input_ids = request.POST.getlist('inputs')
        # if (list_of_input_ids):
        #     for ids in list_of_input_ids:
        #         user = User.objects.get(id=ids)
        #         g_id = group
        #         u_id = user
        groups = group_table.objects.filter(g_id=grp).select_related()

        for group in groups:
            # print("bid_amount", group.bidAmount)
            data.append(
                {
                    "name": group.u_id.username,
                    "winner": group.winner,
                    "start_comity": group.start_comity,
                    "round": group.round,
                    "bid_amount": group.bidAmount,
                    "status": grp.status,
                    "group_name" : grp.name
                }
            )

        # qs_json = serializers.serialize('json', group)

        # To send the entire list as json
        # return HttpResponse(qs_json, content_type='application/json')

        return JsonResponse(data, safe=False)

    return HttpResponse('Failed')


def deleteUsersInGroup(request):
    # data = []
    if request.method == "POST":
        try:
            g_id = request.POST.get("g_id")
            username = request.POST.get("username")

            group = group_info_table.objects.get(id=g_id)
            u_id = User.objects.get(username=username)


            # list_of_input_ids = request.POST.getlist('inputs')
            # if (list_of_input_ids):
            #     for ids in list_of_input_ids:
            #         user = User.objects.get(id=ids)
            #         g_id = group
            #         u_id = user
            # group_table.objects.get(g_id=group, u_id=username)
            group_table.objects.get(g_id=group, u_id=u_id).delete()
        # groups = group_table.objects.filter(g_id=group)

        # print("del_user = " , groups , g_id, username)

        #
        # for group in groups:
        #     print("group", group)
        #     data.append(
        #         {
        #             "name": group.u_id.username,
        #             "winner": group.winner,
        #             "start_comity": group.start_comity,
        #             "round": group.round,
        #             "bid_amount": group.bidAmount
        #         }
        #     )

        # qs_json = serializers.serialize('json', group)

        # To send the entire list as json
        # return HttpResponse(qs_json, content_type='application/json')

            return JsonResponse({"delete" : "success"}, safe=False)

        except:
            return JsonResponse({"delete" : "failed"}, safe=False)


def getUser(request):
    username = request.POST.get("user")
    if username and username is not None:
        try:
            user = User.objects.filter(username__iexact=username)
        except User.DoesNotExist:
            return HttpResponse('Failed')

        if user:
            return JsonResponse(
                                {'userName': str(user[0].username),
                                'first_name': str(user[0].first_name),
                                'last_name': str(user[0].last_name),
                                'user_id': str(user[0].id),
                                'email': str(user[0].email)}
                            )
    return JsonResponse({'message' : 'user not found'}, safe=False)

def getAllGroups(request):
    if request.method == 'POST':
        data = []
        # Just to check the token, don't delete
        user = User.objects.get(username=decryptToken(request.POST.get('token')))
        groups = group_info_table.objects.select_related().all()

        for group in groups:
            id = group.id
            winner = ''
            usersInGroup = group_table.objects.filter(g_id=id)
            currentGroup = group_info_table.objects.select_related().get(id=id)
            dateAfterOneDays = convertMilisToDatetime(currentGroup.updated_at) + relativedelta(days=+1)
            totalAmount = int(len(usersInGroup)) * int(currentGroup.amount)
            minBidAmount = totalAmount / 100
            allWinners = group_table.objects.filter(g_id=id, winner=True)
            if currentGroup.status == 'active':
                winner = group_table.objects.select_related().get(g_id=id, winner=True, round=len(allWinners)) if len(allWinners)-1 == 0 else group_table.objects.select_related().get(g_id=id, winner=True, round=len(allWinners)-1),
                print('winner = ' , winner[0])
                # data.append({"winner": winner[0].u_id.username})
                # print('round = ' , len(allWinners))
            user_id = currentGroup.created_by_user.id
            # user_details = User.objects.get(id = user_id)
            # profile_details = Profile.objects.all()
            # print("user_details = " , user_details)
            # print("profile_details = " , profile_details)
            # print("user" , user_id)
            minBidAmountUser = ''
            user_info = UserInfo.objects.get(u_id=user_id) if UserInfo.objects.filter(
                u_id=user_id).exists() else None
            if len(bid.objects.all()) > 0:
                minBidAmountUser = bid.objects.select_related().filter(g_id=id, bidAmount__gt=0).order_by('bidAmount').last()

            users = []
            for user in usersInGroup:
                user_info = UserInfo.objects.get(u_id=user.u_id.id) if UserInfo.objects.filter(
                    u_id=user.u_id.id).exists() else None
                users.append({
                    "username" : user.u_id.username,
                    "id" : user.u_id.id,
                    "first_name" : user.u_id.first_name,
                    "last_name" : user.u_id.last_name,
                    "email" : user.u_id.email,
                    "account_number" : user_info.account_number if user_info else None,
                    "ifsc" : user_info.ifsc if user_info else None,
                    "superuser": user_info.superuser if user_info else None,
                    }
                )


            data.append(
                {

                    "minBidAmountUser": minBidAmountUser.u_id.username if minBidAmountUser else None,
                    "bid_amount": minBidAmountUser.bidAmount if minBidAmountUser else None,
                    "updated_date": convertMilisToDatetime(minBidAmountUser.g_id.updated_at).date() if minBidAmountUser else None,
                    "updated_time": convertMilisToDatetime(minBidAmountUser.g_id.updated_at).time() if minBidAmountUser else None,
                    "totalAmount": totalAmount,
                    "usersInGroup": users,
                    "minBidAmount": minBidAmount,
                    # "dateAfterOneDays_date": convertMilisToDatetime(currentGroup.bid_date).date() if currentGroup.bid_date else None,
                    # "dateAfterOneDays_time": dateAfterOneDays.time(),
                    "bidEndDate": convertMilisToDatetime(currentGroup.bid_date).date() if currentGroup.bid_date else None,
                    "bidEndDateInMilis": currentGroup.bid_date if currentGroup.bid_date else None,
                    "admin" : currentGroup.created_by_user.username,
                    "name" : currentGroup.name,
                    "duration" : currentGroup.duration,
                    "amount" : currentGroup.amount,
                    "g_id" : currentGroup.id,
                    "status" : currentGroup.status,
                    "end_date" : convertMilisToDatetime(currentGroup.end_date).date() if currentGroup.end_date else None,
                    "round" : len(allWinners),
                    "winner": winner[0].u_id.username if winner else None

                }
            )

        # SomeModel_json = serializers.serialize("json", group_info_table.objects.all())
        # data = {"groups": SomeModel_json}
        return JsonResponse(data, safe=False)
        # return HttpResponse("Not Authenticated")
    # return JsonResponse(group_info_table.objects.all())


def deleteAllGroups(request):
    group_info_table.objects.all().delete()
    return JsonResponse({"groupsDelete": "True"})

def activateSubscription(request):
    logger = getLogger()
    if request.method == 'POST':
        username = decryptToken(request.POST.get('token'))
        user = User.objects.get(username=username)
        logger.info("Activating subscription for user = " + user.username)
        user_info = UserInfo.objects.get(u_id=user.id) if UserInfo.objects.filter(
            u_id=user.id).exists() else None
        if user_info:
            user_info.superuser = True
            user_info.superuser_start_date = getCurrentMilis()
            dateAfterOneMonth = getCurrentDateInLocalTimezone() + relativedelta(days=+30)
            user_info.superuser_end_date = dateAfterOneMonth.timestamp() * 1000
            user_info.save()
            logger.info("Activating subscription successful for user = " +  user.username)
            return JsonResponse({"activate_subscription": "True"})
    return HttpResponse("activate_subscription : False")

def deactivateSubscription(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        user_info = UserInfo.objects.get(u_id=user.id) if UserInfo.objects.filter(
            u_id=user.id).exists() else None
        if user_info:
            user_info.superuser = False
            user_info.superuser_start_date = 0
            user_info.superuser_end_date = 0
            user_info.save()
            return JsonResponse({"deactivate_subscription": "True"})
    return HttpResponse("deactivate_subscription : False")


def createRazorPayOrderId(request):
    if request.method == 'POST':
        secret_id= 'rzp_live_sioclijuytb3Mp'
        secret_key = 'jKpz9OPR9taxWTHhWFX3Feyh'

        client = razorpay.Client(auth=(secret_id, secret_key))
        order_amount = request.POST.get('order_amount')
        order_currency = 'INR'
        order_receipt = request.POST.get('group_id')

        order_id = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt))
        print("order_id = " , order_id.get('id'))
        if order_id:
            user = User.objects.get(username=decryptToken(request.POST.get('token')))
            user_info = UserInfo.objects.get(u_id=user.id)
            user_info.order_id = order_id.get('id')
            user_info.save()


        return JsonResponse({"createRazorPayOrderId": "True" , "order_id" : order_id})
    return JsonResponse({"createRazorPayOrderId": "False"})

def verifyAndSavePayment(request):
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_signature = request.POST.get('razorpay_signature')

    secret_id = 'rzp_test_nu9LsvfHJHqHQx'
    secret_key = 'vqt4RvJIR5NeyWfMAcWcGuPY'

    client = razorpay.Client(auth=(secret_id, secret_key))

    params_dict = {
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_signature': razorpay_signature
    }

    try:
        client.utility.verify_payment_signature(params_dict)

        user = User.objects.get(username=decryptToken(request.POST.get('token')))
        user_info = UserInfo.objects.get(u_id=user.id)
        user_info.razorpay_order_id = razorpay_order_id
        user_info.razorpay_payment_id = razorpay_payment_id
        user_info.razorpay_signature = razorpay_signature
        user_info.superuser = True
        user_info.superuser_start_date = getCurrentMilis()
        dateAfterOneMonth = getCurrentDateInLocalTimezone() + relativedelta(days=+30)
        user_info.superuser_end_date = dateAfterOneMonth.timestamp() * 1000
        user_info.save()
        return JsonResponse({"Razorpay_payment": "success"})

    except:
        return JsonResponse({"Razorpay_payment": "failed"})



def deleteGroup(request, id):
    group_info_table.objects.get(id=id).delete()
    return JsonResponse({"groupDelete": "True"})


def sendNotficationToStartComity(request):
    logger = getLogger()
    milliseconds = getCurrentMilis()
    id = request.POST.get('g_id')
    print("group_id" , id)
    allWinners = group_table.objects.filter(g_id=id, winner=True)
    print("allWinners" , allWinners)

    # If someone starts thrive make the start_comity flag true
    if request.method == "POST":
        group = group_info_table.objects.get(id=id)
        group.updated_at = milliseconds
        group.save()
        user = User.objects.get(username=decryptToken(request.POST.get('token')))
        admin = group_table.objects.get(g_id=group, u_id=user)
        admin.start_comity = True
        admin.save()

    # Check for users with pending invitations
    # groupId = group_info_table.objects.get(id = id)
    usersWithPendingInvitations = getUsersWithPendingInvitations(group)

    # If all users didn't accept the invitation to start the group, don't move forward
    if (usersWithPendingInvitations):
        data = []
        logger.info("Getting users with pending invitations")

        for user in usersWithPendingInvitations:
            data.append(
                {
                "name" : user.u_id.username,
                "winner": user.winner,
                "start_comity": user.start_comity,
                "round": user.round,
                "bid_amount" : user.bidAmount
                }
            )

            # messages.warning(request, "usersWithPendingInvitations = {}".format(user))
            # logger.info('userPendingInvitations = %s', data)
        # qs_json = serializers.serialize('json', data)

        return JsonResponse(data, safe=False)

    # If no winners that is start of the group
    elif not allWinners:

        # Set date of group based on duration, done one time when group is created
        if group.start_date == 0 or group.end_date == 0:
            group.status = 'active'
            group.save()
            setGroupStartDate(group, milliseconds)
            setGroupEndDate(group)
            logger.info("setGroupDates")

            # Check if winner already exists in the group otherwise choose a winner randomly
            winner = group_table.objects.filter(g_id=group, winner=True)
            logger.info("Getting winner at start")
            winner = startGroup(request, winner, logger, id, False)
            print("Winner" , winner)
            data = {
                "name": winner.u_id.username,
                "winner": winner.winner,
                "start_comity": winner.start_comity,
                "round": winner.round,
                "bid_amount": winner.bidAmount
            }
            return JsonResponse(data, safe=False)
            # return JsonResponse({"winner" : winner.u_id.username}, safe=False)
            # return redirect('/get/{}/winner/{}/{}'.format(id, winner, False))


    # In last round select the remaining user 
    elif (len(allWinners) == len(group_table.objects.filter(g_id=group))):
            round = len(allWinners)
            winnerLeft = group_table.objects.get(g_id=id, winner=True, round=int(round))
            winner = winnerLeft
            logger.debug("allWinners = %s", allWinners)
            logger.debug("round = %s", round)
            messages.success(request, "winner left = {}".format(winnerLeft))
            logger.debug("In last round select the remaining user  %s", winner)

            data = {
                "name": winner.u_id.username,
                "winner": winner.winner,
                "start_comity": winner.start_comity,
                "round": winner.round,
                "bid_amount": winner.bidAmount
            }
            # qs_json = serializers.serialize('json', lastWinner)
            return JsonResponse(data, safe=False)

        # return redirect('/get/{}/winner/{}/{}'.format(id, winner, True))

    # Logic for 2nd to n-1 rounds
    elif (len(allWinners) != len(group_table.objects.filter(g_id=group))):
        count = 0
        logger.info("Getting winner for 2nd to n-1 rounds")
        print('Getting winner for 2nd to n-1 rounds = ' ,  count)
        count += count + 1
        round = len(allWinners)
        finish = False
        lastWinner = ''

        if round > 0:
            lastWinner = group_table.objects.select_related().get(g_id=id, winner=True, round=int(round))
            # logger.debug("lastWinner = %s", lastWinner)
            # lastWinnerUser = User.objects.get(username=lastWinner)
            # logger.debug("lastWinnerUser for %s round = %s", round, lastWinnerUser)
            data={
                    "name": lastWinner.u_id.username,
                    "winner": lastWinner.winner,
                    "start_comity": lastWinner.start_comity,
                    "round": lastWinner.round,
                    "bid_amount": lastWinner.bidAmount
                }
            # qs_json = serializers.serialize('json', lastWinner)
            return JsonResponse(data, safe=False)

        # If winner exists by bidding, choose him, else choose the randomly selected winner
        if bid.objects.filter(g_id=id, bidAmount__gt=0):
            winner = bid.objects.filter(g_id=id, bidAmount__gt=0).order_by('bidAmount').last()
            # If someone has already bid, don't show him the bid button
            logger.debug("highest bid winner for %s round = %s", round, winner)

        # logger.debug("lastWinner for %s round = %s" , round, lastWinner )
        # logger.debug("allWinners = %s" , allWinners)
        # logger.debug("user = %s" , user)

        winner = startGroup(request, lastWinner, logger, id, finish)
        # If someone is the winner or if someone has bid should not be shown the bid form
        if str(winner) == str(user):
            finish = True
        logger.debug("winner for bid form = %s", winner)

        for winners in allWinners:
            logger.debug("allWinners for bid form = %s", winners)

            if str(winners) == str(user):
                finish = True

        return redirect('/get/{}/winner/{}/{}'.format(id, winner, finish))

    return redirect('/get/{}'.format(id))


def startGroup(request, winner, logger, id, finish):
    # If someone bid or bid more than the last, then random winner will not matter and the higest bid user will be the winner
    highestBidUser = bid.objects.filter(g_id=id, bidAmount__gt=0).order_by('bidAmount').last()
    # logger.debug("highestBidUser = %s" , highestBidUser)
    # logger.debug("winner = %s" , winner)

    if highestBidUser and not finish:
        logger.debug("highestBidUser in startGroup = %s", highestBidUser)
        winner = highestBidUser
        messages.warning(request, "highestBidUser = {}".format(highestBidUser))
        return highestBidUser

    elif (winner):
        logger.debug("winner = %s" , winner)
        messages.warning(request, "Winner = {}".format(winner))
        return winner


    # No winner exists, select one winner randomly
    else:
        randomlySelectedWinner = getRandom(id, request, logger)
        if randomlySelectedWinner:
            user = User.objects.get(username=randomlySelectedWinner)
            winner = group_table.objects.get(g_id=id, u_id=user)
            winner.winner = True
            winner.save()
            allWinners = group_table.objects.filter(g_id=id, winner=True)
            # logger.debug("allWinners = %s" , allWinners)
            # logger.debug("len(allWinners) = %s" , len(allWinners))

            winner.round = len(allWinners)
            winner.save()
            messages.success(request, "randomlySelectedWinner = ", randomlySelectedWinner)
            logger.debug("randomlySelectedWinner = %s", winner)
            return winner


def setGroupStartDate(group, milliseconds):
    #   if group.start_date == 0 or getCurrentDateInLocalTimezone().date() == convertMilisToDatetime(group.end_date).date():
    group.start_date = milliseconds
    group.save()


def setGroupEndDate(group):
    duration = {"1m": "month 1", "2w": "weeks 2", "1w": "weeks 1", "3d": "days 3"}
    print("iuhibhkbk", duration.get(group.duration).split(' ')[0])
    print("time = ", getDateAfterSometime(duration.get(group.duration).split(' ')[0],
                                          int(duration.get(group.duration).split(' ')[1])))
    # duration={"1m" : "month 1" }
    # print("group duration = " , )
    # getDateAfterSometime(weeks,2)
    dateAfterOneMonth = convertMilisToDatetime(getCurrentMilis()) + relativedelta(months=+1)
    yr = dateAfterOneMonth.year
    mn = dateAfterOneMonth.month
    dy = dateAfterOneMonth.day
    dt = datetime.datetime(yr, mn, dy)
    print("dateAfterOneMonth milis =", unixTimeMillis(dt))
    group.end_date = unixTimeMillis(dt)
    group.save()


def returnWinner(request, id, winner, finish):
    context = {"id": id, "winner": winner, "finish": str(finish)}
    return render(request, 'winner.html', context)


def getUsersWithPendingInvitations(groupId):
    return group_table.objects.filter(g_id=groupId, start_comity=False).select_related()


def getLogger():
    # create logger
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_FILENAME = os.path.join(BASE_DIR, "mylog.log")
    logger = logging.getLogger('Thrive')
    logger.setLevel(logging.INFO)
    if logger.handlers:
        logger.handlers = []

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # add formatter to ch
    ch.setFormatter(formatter)

    # create file handler and set level to debug
    fh = logging.FileHandler(LOG_FILENAME)

    # add formatter to fh
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # LOG_FILENAME = os.path.join(BASE_DIR, "mylog.log")
    # FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # logger = logging.getLogger("Thrive")
    # logger.setLevel(logging.INFO)
    # # Reset the logger.handlers if it already exists.
    # if logger.handlers:
    #     logger.handlers = []
    # fh = logging.FileHandler(LOG_FILENAME)
    # formatter = logging.Formatter(FORMAT)
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    # return logger


def getRandom(id, request, logger):
    usersInGroup = []
    # users = group_table.objects.filter(g_id = id, winner = false)
    # allWinners = group_table.objects.filter(g_id = id , winner = True, bidAmount__gt=0)
    notWinners = group_table.objects.filter(g_id=id, winner=False)
    logger.debug("notWinners = %s", notWinners)
    # if notWinners and (len(allWinners) != (len(group_table.objects.filter(g_id = id)) -1)):
    if notWinners:
        for u in notWinners:
            usersInGroup.append(u)
            # messages.success(request , u)
        count = len(usersInGroup)
        i = randint(0, (count - 1))
        return usersInGroup[i]
    else:
        messages.success(request, "Commitee finished")
        return redirect('/get/{}'.format(id))


def bidMoney(request):
    # bidAmount = 0
    logger = getLogger()
    if request.method == "POST":
        id = request.POST.get('g_id')
        username = request.POST.get('username')
        bid_amount = request.POST.get('bid_amount')

    user = User.objects.get(username=username)

    allWinners = group_table.objects.filter(g_id=id, winner=True)
    # userInGroup = group_table.objects.get(g_id=id, u_id=user)
    nonWinnerUsersInGroup = group_table.objects.filter(g_id=id, bidAmount=0)
    usersInGroup = group_table.objects.filter(g_id=id)
    # user_info = UserInfo.objects.get(u_id=user)
    currentGroup = group_info_table.objects.get(id=id)
    dateAfterOneDays = convertMilisToDatetime(currentGroup.start_date) + relativedelta(days=+1)

    # milis = date_to_unix_time_millis(dateAfterOneDays.date())
    milliseconds_since_one_day = dateAfterOneDays.timestamp() * 1000
    print("date = " , dateAfterOneDays.date())
    print("milis = " , milliseconds_since_one_day)
    currentGroup.bid_date = milliseconds_since_one_day
    currentGroup.save()
    highestBidUser = bid.objects.filter(g_id=id, bidAmount__gt=0).order_by('bidAmount').last()
    print("highestBidUser in bid = " , highestBidUser)

    showBidInputBox = True
    totalAmount = int(len(usersInGroup)) * int(currentGroup.amount)
    print("getCurrentDateInLocalTimezone().date()" , getCurrentDateInLocalTimezone().date())
    print("dateAfterOneDays.date()" , dateAfterOneDays.date())
    # if (getCurrentDateInLocalTimezone().date() >= dateAfterOneDays.date()):
    # # if(getCurrentDateInLocalTimezone().date() == getCurrentDateInLocalTimezone().date()):
    #     showBidInputBox = False
    #     if highestBidUser:
    #         round = len(allWinners)
    #         lastWinner = group_table.objects.get(g_id=id, winner=True, round=int(round))
    #         logger.debug('lastWinner in  bid =  %s', lastWinner)
    #
    #         if lastWinner and highestBidUser != lastWinner:
    #             lastWinner.winner = False
    #             lastWinner.round = 0
    #             lastWinner.save()
    #         user = User.objects.get(username=highestBidUser)
    #         highestBidWinner = group_table.objects.get(g_id=id, u_id=user)
    #         logger.debug('highestBidWinner in  bid =  %s', highestBidWinner.u_id.username)


    if highestBidUser:
        logger.debug('highestBidUser =  %s' , highestBidUser)
        highestBidUser.winner = True
        highestBidUser.bidAmount = highestBidUser.bidAmount
        highestBidUser.save()
        highestBidUser.round = len(allWinners)
        highestBidUser.save()

        logger.debug('round while bidding =  %s', len(allWinners))

        return checkBidForm(request, bid_amount, totalAmount, id, nonWinnerUsersInGroup, user)

                # messages.success(request,
                #                  "{} highestBidUser with bid {}".format(highestBidUser, highestBidUser.bidAmount))


    else:
        # lastWinner = group_table.objects.filter(g_id = id , winner = True).last()
        if highestBidUser:

            messages.success(request, "{} highestBidUser3 with bid {}".format(highestBidUser, highestBidUser.bidAmount))

        messages.success(request, "Bids open till {} for {}. Please bid!".format(dateAfterOneDays.date(), str(
            dateAfterOneDays - getCurrentDateInLocalTimezone()).split('.')[0]))
        logger.debug('highestBidUser =  %s', highestBidUser)
        return checkBidForm(request, bid_amount, totalAmount, id, nonWinnerUsersInGroup, user)

    # context = {"name": str(user), "userInGroup": userInGroup, "highestBidUser": str(highestBidUser),
    #            "usersInGroup": usersInGroup, "showBidInputBox": showBidInputBox, "totalAmt": totalAmount, "id": id,
    #            "user_info": user_info}
    return HttpResponse("Pass1")


def checkBidForm(request, bidAmount, totalAmount, id, nonWinnerUsersInGroup, user):
    minBidAmount = totalAmount / 100
    # bidUser = bid.objects.all()
    grp = group_info_table.objects.get(id=id)
    print("bidUser id= ", id)
    print("bidUser user= ", user)
    print("bidUser amt= ", bidAmount)
    print("bidUser = ", grp.id)
    if request.method == "POST":
            # bidAmount = request.POST.get("bidAmt")
        if int(minBidAmount) > int(bidAmount):
            messages.success(request, "BidAmt should be atleast 1 percent of total amount")
            print("minBidAmountUser 1", bidAmount)

        elif (int(bidAmount) > totalAmount):
            messages.success(request, "BidAmt should be less than total amount")
            print("minBidAmountUser 2", totalAmount)

        else:
            minBidAmountUser = bid.objects.select_related().filter(g_id=id, bidAmount__gt=0).order_by('bidAmount').last()

            if minBidAmountUser:
                print("minBidAmountUser 3" , minBidAmountUser)
                if int(bidAmount) <= int(minBidAmountUser.bidAmount):
                    # bids = bid.objects.all()
                    # print("bids = ", bids)
                    messages.success(request, "Bid more than {}".format(minBidAmountUser.bidAmount))
                    print("minBidAmount = ", minBidAmountUser)
                    print("minBidAmount = ", minBidAmountUser.bidAmount)
                    print("bidAmount = ", bidAmount)
                else:
                    # bids = bid.objects.all()
                    # print("bids = " , bids)
                    bid.objects.update_or_create(u_id=user, g_id=grp,  defaults={'bidAmount': bidAmount})
                    # bidUser.save()
                    # minBidAmountUser.bidAmount = int(bidAmount)
                    # minBidAmountUser.g_id = id
                    # minBidAmountUser.u_id = user
                    # minBidAmountUser.save()
                print("minBidAmountUser 4 ", minBidAmountUser)
                # return HttpResponse("pass")
                minBidAmountUser = bid.objects.select_related().filter(g_id=id, bidAmount__gt=0).order_by(
                    'bidAmount').last()

                data = {
                    "usernmame": minBidAmountUser.u_id.username,
                    "g_id": minBidAmountUser.g_id.id,
                    "bid_amount": minBidAmountUser.bidAmount,
                    "admin": minBidAmountUser.g_id.created_by_user.username,
                    "updated" : convertMilisToDatetime(minBidAmountUser.g_id.updated_at)
                }
                # # qs_json = serializers.serialize('json', lastWinner)
                return JsonResponse(data, safe=False)


            else:
                print("fdsfdsf")
                bidUser = bid(u_id=user, bidAmount=bidAmount, g_id=grp)
                bidUser.save()
                messages.success(request, "{} bidAmt".format(bidAmount))
                returnToUser = int(bidAmount) / int(len(nonWinnerUsersInGroup))
                messages.success(request, "{} returnToUser".format(returnToUser))
                minBidAmountUser = bid.objects.select_related().filter(g_id=id, bidAmount__gt=0).order_by(
                    'bidAmount').last()

                data = {
                    "usernmame": minBidAmountUser.u_id.username,
                    "g_id": minBidAmountUser.g_id.id,
                    "bid_amount": minBidAmountUser.bidAmount,
                    "admin": minBidAmountUser.g_id.created_by_user.username,
                    "updated": convertMilisToDatetime(minBidAmountUser.g_id.updated_at)
                }
                # # qs_json = serializers.serialize('json', lastWinner)
                return JsonResponse(data, safe=False)
                # return HttpResponse("Pass2")


# def getBidDetails(request):
#     pass
    # id = request.POST.get('g_id')
    # print("id" , id)
    # usersInGroup = group_table.objects.filter(g_id=id)
    # currentGroup = group_info_table.objects.get(id=id)
    # dateAfterOneDays = convertMilisToDatetime(currentGroup.updated_at) + relativedelta(days=+1)
    # totalAmount = int(len(usersInGroup)) * int(currentGroup.amount)
    # minBidAmount = totalAmount / 100
    # minBidAmountUser = bid.objects.select_related().filter(g_id=id, bidAmount__gt=0).order_by('bidAmount').last()
    #
    # data = {
    #     "minBidAmountUser": minBidAmountUser.u_id.username,
    #     "g_id": minBidAmountUser.g_id.id,
    #     "bid_amount": minBidAmountUser.bidAmount,
    #     "admin": minBidAmountUser.g_id.created_by_user.username,
    #     "updated_date": convertMilisToDatetime(minBidAmountUser.g_id.updated_at).date(),
    #     "updated_time": convertMilisToDatetime(minBidAmountUser.g_id.updated_at).time(),
    #     "totalAmount" : totalAmount,
    #     "usersInGroup" : len(usersInGroup),
    #     "minBidAmount" : minBidAmount,
    #     "dateAfterOneDays_date": dateAfterOneDays.date(),
    #     "dateAfterOneDays_time": dateAfterOneDays.time()
    # }
    # # # qs_json = serializers.serialize('json', lastWinner)
    # return JsonResponse(data, safe=False)


def transferMoney(request, id, name):
    user = User.objects.get(username=name)
    user_info = UserInfo.objects.filter(u_id=user)
    context = {"winner": name, "user_info": user_info}
    return render(request, 'transfer.html', context)


def profile(request):
    user = request.user
    if request.method == 'POST':
        u_id = user
        acnum = request.POST.get('acnum')
        ifsc = request.POST.get('ifsc')
        messages.success(request, "ifsc = {}".format(ifsc))
        userInfo = UserInfo(u_id=u_id, account_number=acnum, ifsc=ifsc)
        if acnum != '' and ifsc != '' and user:
            userInfo.save()
            messages.success(request, 'User Info Saved!')
            # redirect('/profile')
            return redirect('/viewProfile')
    return render(request, "profile.html")


def viewProfile(request):
    user = request.user
    user_info = UserInfo.objects.get(u_id=user)
    # print(user, user_info.ifsc)
    context = {"user_info": user_info}
    return render(request, "viewProfile.html", context)


def convertMilisToDatetime(milis):
    if milis:
        s = milis / 1000
        return datetime.datetime.fromtimestamp(s, pytz.timezone('Asia/Kolkata'))


def getCurrentMilis():
    print('milis = ', datetime.datetime.now(pytz.timezone('Asia/Kolkata')).timestamp() * 1000)
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata')).timestamp() * 1000


def getCurrentDateInLocalTimezone():
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata'))


def getDateAfterSometime(durationType: str, duration: int):
    milliseconds = getCurrentMilis()
    currentDate = convertMilisToDatetime(milliseconds)
    dy = durationType
    tm = duration
    print(dy, tm, exec('dy=+tm'))
    print("getDateAfterSometime= ", (currentDate + relativedelta(exec('dy=+tm'))))
    return (currentDate + relativedelta(exec('durationType=+duration')))


def resetComity(id):
    usersInGroup = group_table.objects.filter(g_id=id)
    if usersInGroup:
        for u in usersInGroup:
            print(u.u_id)
            u.winner = False
            u.bidAmount = 0
            print(u.winner)


def date_to_unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


def unixTimeMillis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0
