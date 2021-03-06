from django.shortcuts import render, HttpResponse, render, redirect
from comity.models import Services
from comity.models import group_info_table, group_table, UserInfo, bid
import pytz
import uuid
from django.db.models import Q
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
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    users = User.objects.all()
    user = request.user
    # groups = group_info_table.objects.filter(created_by_user = user)
    grpNameByUser = group_table.objects.filter(u_id = user)
    # grpInfo = group_info_table.objects.filter(name = grpNameByUser)
    groupList = []
    # grp = []
    print("grpNameByUser = " , grpNameByUser)
    # //Find a better way later
    for grp in grpNameByUser:
        print("grp = {}".format(grp.g_id))
        grpInfo = group_info_table.objects.get(id = uuid.UUID(str(grp.g_id)))
        groupList.append(grpInfo)
    # print("groupList = ", groupList[0].name)
        # otherGroupss.append(com)

    # print("grpNameByUser = " , grpNameByUser)                                                       
    
    # for gr in otherGroupss:
    #     print("gr = {}".format(gr))
    #     for h in gr:
    #         grp.append(h)
    #         print("h = {}".format(gr))

    if (grpNameByUser.count() > 0 ):
        context={"users" : users , "groupList" : groupList}
    else:
        context = {"users" : users}
    # if grpInfo:
    #     print("grpInfo = " , grpInfo)
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
        duration = request.POST.get('duration')
        print('Duration = ' , duration)
        # user = request.user
        user = User.objects.get(username = request.user)
        group = group_info_table(name = name , amount = amt, duration = duration, created_by_user = user, created_at= milliseconds, updated_at = milliseconds)
        group.save()
        # user = User.objects.get(id=ids)
        # print("ID = " , group.id)
        groupUuid = group_info_table.objects.get(id = group.id)
        # print("G_ID = " , groupUuid)
        u_id = user
        users = group_table(g_id = groupUuid , u_id = u_id)
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
        services = Services(name = name , email = email, phone = phone, desc = desc , date = datetime.datetime.now())
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

def addUserToGroups(request, id):
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

# def addUserToGroups(request):
#     if request.method == 'POST':
#         #gives list of id of inputs 
#         list_of_input_ids=request.POST.getlist('inputs')
#         id = request.get_full_path()
#         return HttpResponse(id)


def sendNotficationToStartComity(request, id):
    # resetComity(id)
    milliseconds =  getCurrentMilis()
    currentGroup = group_info_table.objects.get(id = id)
    showBidInputBox = True
    finish = False
    if milliseconds:
        currentGroup.updated_at = milliseconds
        currentGroup.save()
    currentDate = getCurrentDateInLocalTimezone()
    usersInGroup = group_table.objects.filter(g_id=id)
    # dateAfterOneMonth = currentDate + relativedelta(months=+1)
    # print("dateAfterOneMonth = " , dateAfterOneMonth.date())
    # print('getCurrentDateInLocalTimezone = ', getCurrentDateInLocalTimezone().date())
    winners = ''
    highestBidUser = bid.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
    allWinners = group_table.objects.filter(g_id = id , winner = True)
    lastWinner = group_table.objects.filter(g_id = id , winner = True).first()

    print(len(allWinners) ,len(usersInGroup))

    if len(allWinners) > 1:
        lastWinner = group_table.objects.filter(g_id = id , winner = True, bidAmount=0).last()
        if( len(allWinners) == len(usersInGroup)):
            finish = True
            # lastWinner = group_table.objects.get(g_id = id , winner = True, bidAmount=0)
            highestBidUser = lastWinner
            print("lastWinner indfskasd= " , lastWinner)

    #     lastWinnerQuery = group_table.objects.filter(g_id = id , winner = True).order_by('winner')[:len(allWinners)]
    #     lastWinner  = lastWinnerQuery[len(allWinners) - 1].u_id
        # print("lastWinner indfs= " , lastWinner)

    # else:
    #     # pass
    #     lastWinner = group_table.objects.filter(g_id = id , winner = True).last()

    #     print("lastWinner indfslkl= " , lastWinner)

    # lastWinnersBidAmount = []
    # if(len(allWinners) > 1 and type(lastWinner) == list):
    #     for l in lastWinner:
    #         print("l.bidmt = " , l)
    #         lastWinnersBidAmount.append(l.bidAmount)
    #     print("group_table.objects.filter(~Q(bidAmount__in=lastWinnersBidAmount)) = ", group_table.objects.exclude(bidAmount__in=lastWinnersBidAmount))
    #     highestBidUser = group_table.objects.exclude(g_id = id, bidAmount__in=lastWinnersBidAmount).filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()


    #     print("highestBidUser = ", highestBidUser)

    # else:
    #     highestBidUser = group_table.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
    #     print("highestBidUser else= ", highestBidUser)


    # print("highestBidUser 2= " , highestBidUser)

    if(highestBidUser):
        if highestBidUser != lastWinner:
            lastWinner.winner = False
            lastWinner.save()
        winners  = highestBidUser
        messages.success(request, "{} highestBidUser".format(highestBidUser))
    else:
        # winner = get_random(group, request)
        winners = allWinners

    if highestBidUser:
        winner = highestBidUser
    else:
        if lastWinner:
            # print("left = " , convertMilisToDatetime(currentGroup.end_date)-convertMilisToDatetime(currentGroup.created_at).months())
            print("lastWinner elif = ", lastWinner)
            winner = lastWinner
            # winner = ''


        # highestBidUser = group_table.objects.exclude(bidAmount=lastWinner.bidAmount).filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
        # abc = group_table.objects.filter(bidAmount=lastWinner.bidAmount)
        # print("abc = " , abc, highestBidUser)
        else:
            winner = group_table.objects.filter(g_id = id , winner = True).last()

        # highestBidUser = group_table.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
        # print("highestBidUser = ", highestBidUser)

        # winner = group_table.objects.exclude(bidAmount=lastWinner.bidAmount).filter(g_id = id , winner = True).last()
            print("winner = ", winner)
    if not winners:
        messages.success(request, 'no winners')
        return startComity(request, id, highestBidUser, finish)
        
# TODO : Check for better check since for the whole day "Start comity" will increment members.toUpperCase()
    elif (getCurrentDateInLocalTimezone().date() == convertMilisToDatetime(currentGroup.end_date).date()):
    # elif(getCurrentDateInLocalTimezone().date() == getCurrentDateInLocalTimezone().date()):
        # lastWinner = group_table.objects.filter(g_id = id , winner = True).last()
        # print("lastWinner = " , lastWinner)
        highestBidUser = None
        try:
            highestBidUser = bid.objects.get(g_id=id)
            print("highestBidUser in try= " ,  highestBidUser)
        except ObjectDoesNotExist:
            print("highestBidUser DoesNotExist")
    
        if highestBidUser != None:
            usersInGroup = group_table.objects.get(g_id = id, u_id=highestBidUser.u_id)    
            print("usersInGroup = " ,  usersInGroup)
            print("lastWinner b4 delete= " ,  lastWinner)
            print("finish b4 delete= " ,  finish)

            if highestBidUser != lastWinner and finish == False:
                winner.winner = False
                winner.save()

            if usersInGroup:
                usersInGroup.winner = True
                usersInGroup.bidAmount = highestBidUser.bidAmount or 0
                usersInGroup.save()
            showBidInputBox =True
            if highestBidUser:
                print("highestBidUser b4 delete = " ,  highestBidUser)
                highestBidUser.delete()
                print("highestBidUser after delete = " ,  highestBidUser)

            # resetComity(id)
    
            # for u in highestBidUser:
            #     print('u.uid =' , u.u_id)
            #     u.delete()
                # u.save()

        # else:
        #     if len(usersInGroup)>0 and lastWinner:
        #         for u in usersInGroup:
        #             # for l in lastWinner:
        #             if (u != lastWinner):
        #                 print('u.uid =' , u)
        #                 print('lw uid =' ,lastWinner)
        #                 u.bidAmount = 0
        #                 u.save()

        # if lastWinner:
        #     abc = group_table.objects.filter(bidAmount=lastWinner.bidAmount)
        #     print("abc = " , abc, highestBidUser)
        return startComity(request, id, None, finish)
        
    else :
        messages.success(request, "Please transfer money to {}.".format(winner))
        print("finish = ", finish)

        if currentGroup.end_date > 0:
            messages.success(request, "{}  days remaining for the next cycle...".format(str(convertMilisToDatetime(currentGroup.end_date) - currentDate).split('.')[0]))
        return redirect('/get/{}/winner/{}/{}'.format(id, winner, finish))
    return redirect('/')

def startComity(request, id, highestBidUser, finish):
    adm =''
    milliseconds = getCurrentMilis()
    print("getDateAfterSometime = " , getDateAfterSometime("months" , 1))
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
            # if(lastWinner):
            #     return get_random(group, request)


            if(highestBidUser):
                winner = highestBidUser
                # messages.success(request, "{} highestBidUser".format(highestBidUser))
            else:
                winner = get_random(group, request)
                messages.success(request, "{} chosen at random".format(winner))
                # messages.success(request, winner)
            if winner:
                userss = User.objects.get(username=winner)
                # messages.success(request, userss)
                admins = group_table.objects.get(g_id= group , u_id = userss)

                if group.start_date == 0 or getCurrentDateInLocalTimezone().date() == convertMilisToDatetime(group.end_date).date():
                    duration={"1m" : "month 1" , "2w" : "weeks 2", "1w" : "weeks 1" , "3d" : "days 3"}
                    print("iuhibhkbk" , duration.get(group.duration).split(' ')[0])
                    print("time = " , getDateAfterSometime(duration.get(group.duration).split(' ')[0], int(duration.get(group.duration).split(' ')[1])))
                    # duration={"1m" : "month 1" }
                    # print("group duration = " , )
                    # getDateAfterSometime(weeks,2)
                    dateAfterOneMonth= convertMilisToDatetime(getCurrentMilis()) + relativedelta(months=+1)
                    yr =  dateAfterOneMonth.year
                    mn = dateAfterOneMonth.month
                    dy = dateAfterOneMonth.day
                    dt = datetime.datetime(yr, mn, dy)
                    print("dateAfterOneMonth milis =", unix_time_millis(dt))  
                    group.end_date = unix_time_millis(dt)
                    group.start_date = milliseconds
                    group.save()
                # if  not finish:
                admins.winner = True
                admins.save()
                adm = admins
                
    if adm != '':
        return redirect('/get/{}/winner/{}/{}'.format(id,adm, finish))
    else:
        return redirect('/get/{}'.format(id))
    return redirect('/')


def returnWinner(request, id, name, finish):
    context = {"id" : id ,"winner": name , "finish" : finish}
    return render(request, 'about.html', context)


def get_random(id, request):
    usersInGroup = []
    # users = group_table.objects.filter(g_id = id, winner = false)
    allWinners = group_table.objects.filter(g_id = id , winner = True, bidAmount__gt=0)
    notWinners = group_table.objects.filter(g_id = id , winner = False)
    # if notWinners and (len(allWinners) != (len(group_table.objects.filter(g_id = id)) -1)):
    if notWinners:
        for u in notWinners:
            usersInGroup.append(u)
            # messages.success(request , u)
        count = len(usersInGroup)
        i = randint(0, (count - 1))
        return usersInGroup[i]
    else:
        return messages.success(request , "Commitee finished")



def bidMoney(request, id):
    # bidAmount = 0
    user = User.objects.get(username=request.user)
    userInGroup = group_table.objects.get(g_id = id, u_id = user)
    nonWinnerUsersInGroup = group_table.objects.filter(g_id = id, bidAmount=0)
    usersInGroup = group_table.objects.filter(g_id = id)
    user_info = UserInfo.objects.get(u_id = user)
    # print("nonWinnerUsersInGroup" , nonWinnerUsersInGroup)
    # print("usersInGroup" , usersInGroup)
    currentGroup = group_info_table.objects.get(id = id)
    dateAfterThreeDays= convertMilisToDatetime(currentGroup.start_date) + relativedelta(days=+3)

    # lastWinner = ''
    lastWinner = group_table.objects.filter(g_id = id , winner = True, bidAmount__gt=0).last()
    allWinners = group_table.objects.filter(g_id = id , winner = True, bidAmount__gt=0)

    highestBidUser = None
    try:
        highestBidUser = bid.objects.get(g_id=id)
    except:
        print("DoesNotExist")

    # if (lastWinner and int(lastWinner.bidAmount) > 0):
    # print("highestBidUser bidMoney" , highestBidUser)
    # print("user bidMoney" , user)
    # print("user bidMoney" , str(lastWinner) == str(user))

    #     highestBidUser = group_table.objects.exclude(bidAmount=lastWinner.bidAmount).filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
    # else:

    # if (getCurrentDateInLocalTimezone().date() == dateAfterThreeDays.date()): 



    # if (len(allWinners) > 1):
    #     highestBidUser = group_table.objects.exclude(bidAmount=lastWinner.bidAmount).filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
    #     print("highestBidUser init if " , highestBidUser)
    # else:
    #     highestBidUser = group_table.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
    #     print("highestBidUser init" , highestBidUser)

    # lastWinnersBidAmount = []
    # if(len(allWinners) > 1 and type(lastWinner) == list):
    #     for l in lastWinner:
    #         print("l.bidmt = " , l)
    #         lastWinnersBidAmount.append(l.bidAmount)
    #     print("group_table.objects.filter(~Q(bidAmount__in=lastWinnersBidAmount)) = ", group_table.objects.exclude(bidAmount__in=lastWinnersBidAmount))
    #     highestBidUser = group_table.objects.exclude(g_id = id, bidAmount__in=lastWinnersBidAmount).filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()


    #     print("highestBidUser = ", highestBidUser)

    # else:
    #     highestBidUser = group_table.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
    #     print("highestBidUser else= ", highestBidUser)


    # if highestBidUser:
    #     print("highestBidUser 2= " , highestBidUser)

    # highestBidUser = group_table.objects.exclude(bidAmount=lastWinner.bidAmount).filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()


    showBidInputBox = True
    totalAmount = int(len(usersInGroup)) * int(currentGroup.amount)
    if (getCurrentDateInLocalTimezone().date() == dateAfterThreeDays.date()):
    # if(getCurrentDateInLocalTimezone().date() == getCurrentDateInLocalTimezone().date()):
        showBidInputBox = False
        # if highestBidUser:
        #     winners = group_table.objects.filter(g_id = id , winner = True).first()
        #     if winners:
        #         winners.winner = False
        #         winners.save()
        #     highestBidUser.winner = True
        #     highestBidUser.save()
            # lastWinner = group_table.objects.filter(g_id = id , winner = True).first()
        messages.success(request, "{} highestBidUser with bid {}".format(highestBidUser, highestBidUser.bidAmount))
    else:
        # lastWinner = group_table.objects.filter(g_id = id , winner = True).last()
        if highestBidUser:
            messages.success(request, "{} highestBidUser3 with bid {}".format(highestBidUser, highestBidUser.bidAmount))
            # messages.success(request, "{} highestBidUser3 with bid {}".format(lastWinner, lastWinner.bidAmount))
        messages.success(request, "Bids open till {} for {}. Please bid!".format(dateAfterThreeDays.date() , str(dateAfterThreeDays - getCurrentDateInLocalTimezone()).split('.')[0]))
        checkBidForm(request, totalAmount, lastWinner , id , userInGroup, nonWinnerUsersInGroup)
    # checkSuperuser = usersInGroup.objects.all()
    # messages.success(request, "{} usersInGroup".format(len(usersInGroup)))
    context = {"name" : str(user), "userInGroup" : userInGroup,"lastWinner" : str(lastWinner), "highestBidUser" : str(highestBidUser), "usersInGroup" : usersInGroup, "showBidInputBox": showBidInputBox, "totalAmt" : totalAmount , "id" : id,"user_info" : user_info}
    return render(request, 'bid.html', context)

def checkBidForm(request, totalAmount, lastWinner, id , userInGroup, nonWinnerUsersInGroup):
    minBidAmount = totalAmount / 100
    # bidUser = bid.objects.all()
    grp = group_info_table.objects.get(id = id)
    print("bidUser = " , grp.id)
    if request.method == "POST":
        bidAmount = request.POST.get("bidAmt")
        if int(minBidAmount) > int(bidAmount):
            messages.success(request, "BidAmt should be atleast 1 percent of total amount")
        elif (int(bidAmount) > totalAmount):
            messages.success(request, "BidAmt should be less than total amount")
        else:
            # if (lastWinner and int(lastWinner.bidAmount) > 0):
            #     print("lastWinner checkBidForm if " , lastWinner)
            #     minBidAmountUser = group_table.objects.exclude(g_id = id, bidAmount=lastWinner.bidAmount).filter(g_id = id, bidAmount__gt = 0 ).order_by('bidAmount').last()

            #     # highestBidUser = group_table.objects.exclude(bidAmount=lastWinner.bidAmount).filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
            # else:
            #     print("lastWinner checkBidForm else " , lastWinner)
            minBidAmountUser = bid.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()

                # highestBidUser = group_table.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()

            if minBidAmountUser:
                if int(bidAmount) <=  int(minBidAmountUser.bidAmount):
                    messages.success(request, "Bid more than {}".format(minBidAmountUser.bidAmount))
                    print("minBidAmount = " , minBidAmountUser)
                    print("minBidAmount = " , minBidAmountUser.bidAmount)
                    print("bidAmount = " , bidAmount)
                else: 
                    minBidAmountUser.bidAmount = int(bidAmount)
                    minBidAmountUser.g_id = grp
                    minBidAmountUser.u_id = request.user
                    # winners = group_table.objects.filter(g_id = id , winner = True).first()
                    # winners.winner = False
                    # winners.save()
                    # userInGroup.winner = True
                    minBidAmountUser.save()
            else:
                bidUser = bid(u_id = request.user, bidAmount = bidAmount, g_id= grp)
                # bidUser.bidAmount = int(bidAmount)
                # bidUser.g_id = id
                # bidUser.u_id = request.user
                # winners = group_table.objects.filter(g_id = id , winner = True).first()
                # winners.winner = False
                # winners.save()
                # userInGroup.winner = True
                bidUser.save()
                messages.success(request, "{} bidAmt".format(bidAmount))
                returnToUser = int(bidAmount) / int(len(nonWinnerUsersInGroup))
                messages.success(request, "{} returnToUser".format(returnToUser))

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
    user_info = UserInfo.objects.get(u_id = user)
    # print(user, user_info.ifsc)
    context = {"user_info" : user_info}
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

def getDateAfterSometime(durationType: str, duration: int):
    milliseconds = getCurrentMilis()
    currentDate = convertMilisToDatetime(milliseconds)
    dy = durationType
    tm = duration
    print(dy , tm , exec('dy=+tm'))
    print("getDateAfterSometime= ", (currentDate + relativedelta(exec('dy=+tm'))))
    return (currentDate + relativedelta(exec('durationType=+duration')))

def resetComity(id):
    usersInGroup = group_table.objects.filter(g_id = id)
    if usersInGroup:
        for u in usersInGroup:
            print(u.u_id)
            u.winner = False
            u.bidAmount = 0
            print(u.winner)



def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

