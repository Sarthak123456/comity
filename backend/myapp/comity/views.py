from django.shortcuts import render, HttpResponse, render, redirect
from comity.models import Services
from comity.models import group_info_table
from comity.models import group_table
from comity.models import UserInfo
import pytz
from time import time
import datetime
from  random import randint
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout,authenticate, login
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
from django.core import serializers


# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    users = User.objects.all()
    user = request.user
    groups = group_info_table.objects.filter(created_by_user = user)
    otherGroups = group_table.objects.filter(u_id = user)
    otherGroupss = []
    grp = []
    # //Find a better way later
    for g in otherGroups:
        com = group_info_table.objects.filter(name = g.g_id)
        otherGroupss.append(com)
    
    for gr in otherGroupss:
        for h in gr:
            grp.append(h)
            print("h = {}".format(h.id))
    context={"users" : users ,"groups": groups , "otherGroups" : grp}
    return render(request, 'index.html', context)

    # data = {}
    # if request.user.is_anonymous:
    #     return redirect('/login')
    # data['phone_number'] = request.user
    # userList =User.objects.all()
    # posts_serialized = serializers.serialize('json', userList)
    # return JsonResponse(posts_serialized, safe=False)

def addGroup(request):
    milliseconds = getCurrentMilis()
    # date = datetime.fromtimestamp(milliseconds/1000.0)
    if request.method == "POST":
        name = request.POST.get('name')
        amt = request.POST.get('amt')
        user = request.user
        group = group_info_table(name = name , amount = amt, created_by_user = user, created_at= milliseconds, updated_at = milliseconds)
        group.save()
        # user = User.objects.get(id=ids)
        g_id = group_info_table.objects.get(id = group.id)
        u_id = user
        users = group_table(g_id = g_id , u_id = u_id)
        users.save()
        messages.success(request, '"{}" saved!'.format(name))
        return redirect('/')
    return render(request, 'services.html')

# def getGroups(request):
#     user = request.user
#     groups = group_info_table.objects.filter(created_by_user = user)
#     return HttpResponse(groups)

def about(request):
    return render(request, 'about.html')
    # return HttpResponse("About worked")

def services(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        services = Services(name = name , email = email, phone = phone, desc = desc , date = datetime.today())
        services.save()
        messages.success(request, 'Services request saved!')
        return redirect('/')
    return render(request, 'services.html')
    # return HttpResponse("Services worked")

def getServices(request):
    services = User.objects.all()
    return HttpResponse(services.id)

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('/')
    return render(request, 'login.html')

def signUpUser(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {"form":form})


def logoutUser(request):
    logout(request)
    return redirect('/login')

def get(request, id):
    people = group_table.objects.filter(g_id = id)
    users = User.objects.exclude(username = request.user)
    group = group_info_table.objects.get(id = id)
    # print("CreatedByUser = {} , User = {}".format(group.created_by_user , request.user) )
    if request.method == "POST":
        list_of_input_ids=request.POST.getlist('inputs')
        if(list_of_input_ids):
            for ids in list_of_input_ids:
                user = User.objects.get(id=ids)
                g_id = group
                u_id = user
                users = group_table.objects.get_or_create(g_id = g_id , u_id = u_id)
            return redirect('/get/{}'.format(id))
    context = {"people" : people, "users" : users, "id" : id , "group" : group, "request" : request}
    return render(request, 'groups.html', context)

def addUserToGroups(request):
    if request.method == 'POST':
        #gives list of id of inputs 
        list_of_input_ids=request.POST.getlist('inputs')
        id = request.get_full_path()
        return HttpResponse(id)


def sendNotficationToStartComity(request, id):
    # milliseconds =  datetime.now(timezone.utc)
    milliseconds = getCurrentMilis()
    print("milliseconds = " , milliseconds)
    group = group_info_table.objects.get(id = id)
    group.updated_at = milliseconds
    group.save()
    currentDate = convertMilisToDatetime(group.updated_at)
    dateAfterOneMonth = currentDate + relativedelta(days=+0)
    print("dateAfterOneMonth = " , dateAfterOneMonth.date())
    print('getCurrentDateInLocalTimezone = ', getCurrentDateInLocalTimezone().date())
    winners = group_table.objects.filter(g_id = id , winner = True)
    if winners:
        winner = group_table.objects.filter(g_id = id , winner = True).latest('winner')
        print("winner = ", winner)
    print("winners = " , winners)

    # 
    # s = milliseconds / 1000
    # 
    # int(time() * 1000)
    # print("date = " , three_mon_rel)
    if not winners:
        messages.success(request, 'no winners')
        return startComity(request, id)
    elif (getCurrentDateInLocalTimezone().date() == dateAfterOneMonth.date()):
        return startComity(request, id)
        # if request.method == "POST":
        #     group.updated_at = milliseconds
        #     group.save()
        #     user = User.objects.get(username=request.user)
        #     admin = group_table.objects.get(g_id = group , u_id = user)
        #     admin.start_comity = True
        #     admin.save()
        #     adm =''
        #     defaulters = group_table.objects.filter(g_id = group , start_comity = False)
        #     if(defaulters):
        #         for d in defaulters:
        #             messages.success(request, 'defaulters = {}'.format(d))
        #     else:
        #         # messages.success(request, 'Choose user at random')
        #         # notWinners = group_table.objects.filter(g_id = group , winner = False)
        #         # messages.success(request, notWinners)
        #         # messages.success(request, get_random(group))
        #         winner = get_random(group, request)
        #         # messages.success(request, winner)
        #         if winner:
        #             userss = User.objects.get(username=winner)
        #             # messages.success(request, userss)
        #             admins = group_table.objects.get(g_id= group , u_id = userss)
        #             # DON'T DELETE BELOW LINES, USED FOR selectedUser--
        #             admins.winner = True
        #             admins.save()
        #             adm = admins
        #             messages.success(request, "{} chosen at random".format(admins))
        # if adm != '':
        #     return redirect('/get/{}/winner/{}'.format(id,adm))
        # else:
        #     return redirect('/get/{}'.format(id))
    else :
        messages.success(request, "Please transfer money to {}.".format(winner))
        messages.success(request, "{}  days remaining for the next cycle...".format((dateAfterOneMonth - currentDate).days))
        return redirect('/get/{}'.format(id))


def returnWinner(request, id, name):
    context = {"id" : id ,"winner": name}
    return render(request, 'about.html', context)


def get_random(id, request):
    usersInGroup = []
    # users = group_table.objects.filter(g_id = id, winner = false)
    notWinners = group_table.objects.filter(g_id = id , winner = False)
    if notWinners:
        for u in notWinners:
            usersInGroup.append(u)
            # messages.success(request , u)
        count = len(usersInGroup)
        i = randint(0, (count - 1))
        return usersInGroup[i]
    else:
        messages.success(request , "Commitee finished")



def bidMoney(request, id):
    bidAmount = 0
    user = User.objects.get(username=request.user)
    userInGroup = group_table.objects.get(g_id = id, u_id = user)
    usersInGroup = group_table.objects.filter(g_id = id)
    currentGroup = group_info_table.objects.get(id = id)
    totalAmount = int(len(usersInGroup)) * int(currentGroup.amount)
    minBidAmount = totalAmount / 100
    if request.method == "POST":
        bidAmount = request.POST.get("bidAmt")
        if int(minBidAmount) > int(bidAmount):
            messages.success(request, "BidAmt should be atleast 1 percent of total amount")
        elif (int(bidAmount) > totalAmount):
            messages.success(request, "BidAmt should be less than total amount")
        else:
            minBidAmountUser = group_table.objects.filter(g_id = id, bidAmount__gt = 0 ).order_by('bidAmount').first()
            higgestBidderUser = minBidAmountUser = group_table.objects.filter(g_id = id, bidAmount__gt = 0 ).order_by('bidAmount').last()
            if minBidAmountUser:
                if int(bidAmount) <=  int(minBidAmountUser.bidAmount):
                    messages.success(request, "Bid more than {}".format(minBidAmountUser.bidAmount))
                    print("minBidAmount = " , minBidAmountUser.bidAmount)
                    print("bidAmount = " , bidAmount)
                else:
                    userInGroup.bidAmount = int(bidAmount)
                    userInGroup.save()
            else:
                userInGroup.bidAmount = int(bidAmount)
                userInGroup.save()
                messages.success(request, "{} bidAmt".format(bidAmount))
                returnToUser = int(bidAmount) / int(len(usersInGroup))
                messages.success(request, "{} returnToUser".format(returnToUser))
    # checkSuperuser = usersInGroup.objects.all()
    # messages.success(request, "{} usersInGroup".format(len(usersInGroup)))
        messages.success(request, "{} higgestBidderUser with bid {}".format(higgestBidderUser, higgestBidderUser.bidAmount))
    context = {"name" : user, "userInGroup" : userInGroup, "totalAmt" : totalAmount , "id" : id, "usersInGroup" : usersInGroup}
    return render(request, 'bid.html', context)


def transferMoney(request, id, name):
    user = User.objects.get(username=name)
    user_info = UserInfo.objects.filter(u_id = user)
    context = {"winner" : name, "user_info" : user_info}
    return render(request, 'transfer.html', context)

def profile(request):
    user = request.user
    if request.method == 'POST':
        u_id = user
        acnum = request.POST.get('acnum')
        ifsc = request.POST.get('ifsc')
        messages.success(request, "ifsc = {}".format(ifsc))
        userInfo = UserInfo(u_id = u_id, account_number = acnum , ifsc = ifsc)
        if acnum != '' and ifsc != '' and user:
            userInfo.save()
            messages.success(request, 'User Info Saved!')
            # redirect('/profile')
            return redirect('/viewProfile')
    return render(request, "profile.html")

def viewProfile(request):
    user = request.user
    user_info = UserInfo.objects.filter(u_id = user)
    context = {"userInfo" : user_info}
    return render(request, "viewProfile.html" , context)


def convertMilisToDatetime(milis):
    if milis:
        s = milis / 1000
        print('s = ' , s)
        print('DATE = ', datetime.datetime.fromtimestamp(s, pytz.timezone('Asia/Kolkata')))
        return datetime.datetime.fromtimestamp(s, pytz.timezone('Asia/Kolkata'))

def getCurrentMilis():
    print('milis = ', datetime.datetime.now(pytz.timezone('Asia/Kolkata')).timestamp() * 1000)
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata')).timestamp() * 1000

def getCurrentDateInLocalTimezone():
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

def startComity(request, id):
    adm =''
    milliseconds = getCurrentMilis()
    if request.method == "POST":
        group = group_info_table.objects.get(id = id)
        group.updated_at = milliseconds
        group.save()
        user = User.objects.get(username=request.user)
        admin = group_table.objects.get(g_id = group , u_id = user)
        admin.start_comity = True
        admin.save()
        defaulters = group_table.objects.filter(g_id = group , start_comity = False)
        if(defaulters):
            for d in defaulters:
                messages.success(request, 'defaulters = {}'.format(d))
        else:
            # messages.success(request, 'Choose user at random')
            # notWinners = group_table.objects.filter(g_id = group , winner = False)
            # messages.success(request, notWinners)
            # messages.success(request, get_random(group))
            winner = get_random(group, request)
            # messages.success(request, winner)
            if winner:
                userss = User.objects.get(username=winner)
                # messages.success(request, userss)
                admins = group_table.objects.get(g_id= group , u_id = userss)
                # DON'T DELETE BELOW LINES, USED FOR selectedUser--
                # admins.winner = True
                # admins.save()
                adm = admins
                messages.success(request, "{} chosen at random".format(admins))
    if adm != '':
        return redirect('/get/{}/winner/{}'.format(id,adm))
    else:
        return redirect('/get/{}'.format(id))
