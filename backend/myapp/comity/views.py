from django.shortcuts import render, HttpResponse, render, redirect
from comity.models import Services
from comity.models import group_info_table, group_table, UserInfo, bid
import pytz
import uuid
# from django.db.models import Q
# from time import time
import datetime
from  random import randint
import logging
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout,authenticate, login
# from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
# from django.core import serializers
# from django.core.exceptions import ObjectDoesNotExist


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
    if (grpNameByUser.count() > 0 ):
        context={"users" : users , "groupList" : groupList}
    else:
        context = {"users" : users}
    # if grpInfo:
    #     print("grpInfo = " , grpInfo)
    return render(request, 'index.html', context)

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

def sendNotficationToStartComity(request, id):

    logger = getLogger()
    milliseconds = getCurrentMilis()
    allWinners = group_table.objects.filter(g_id = id, winner = True)

    # If someone starts thrive make the start_comity flag true
    if request.method == "POST":
        group = group_info_table.objects.get(id = id)
        group.updated_at = milliseconds
        group.save()
        user = User.objects.get(username=request.user)
        admin = group_table.objects.get(g_id = group , u_id = user)
        admin.start_comity = True
        admin.save()
    
    # Check for users with pending invitations
    # groupId = group_info_table.objects.get(id = id)
    usersWithPendingInvitations = getUsersWithPendingInvitations(group)

    # If all users didn't accept the invitation to start the group, don't move forward
    if(usersWithPendingInvitations):
        logger.info("Getting users with pending invitations")
        for user in usersWithPendingInvitations:
            messages.warning(request , "usersWithPendingInvitations = {}" .format(user))
            logger.info('usersWithPendingInvitations = %s', user)

    # If no winners that is start of the group
    elif not allWinners: 

        # Set date of group based on duration, done one time when group is created
        if group.start_date == 0 or group.end_date == 0:
            setGroupStartDate(group , milliseconds)
            setGroupEndDate(group)
            logger.info("setGroupDates")

            # Check if winner already exists in the group otherwise choose a winner randomly
            winner = group_table.objects.filter(g_id = group, winner = True)
            logger.info("Getting winner at start")
            winner = startGroup(request , winner , logger, id, False)
            return redirect('/get/{}/winner/{}/{}'.format(id, winner, False))


    # Logic when group ends 
    elif (getCurrentDateInLocalTimezone().date() == convertMilisToDatetime(group.end_date).date()):
    # elif(getCurrentDateInLocalTimezone().date() == getCurrentDateInLocalTimezone().date()):
        
        bid.objects.filter(g_id = id).delete()
        logger.debug("allWinners = %s" , allWinners)


        winner = bid.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
        winner = startGroup(request , winner , logger, id, False)
        logger.debug("Logic when group ends %s" , winner)
        setGroupEndDate(group)

        return redirect('/get/{}/winner/{}/{}'.format(id, winner, False))


    # In last round select the remaining user 
    elif(len(allWinners) == len(group_table.objects.filter(g_id = group))):
        
        if (getCurrentDateInLocalTimezone().date() >= convertMilisToDatetime(group.end_date).date()):
        # if(getCurrentDateInLocalTimezone().date() >= getCurrentDateInLocalTimezone().date()):
 

            messages.success(request, "Finish")
            logger.debug("Finish")
            return redirect('/get/{}'.format(id))
             
        else:
            round = len(allWinners)
            winnerLeft = group_table.objects.get(g_id = id , winner = True, round=int(round))
            winner = winnerLeft
            logger.debug("allWinners = %s" , allWinners)
            logger.debug("round = %s" , round)
            messages.success(request, "winner left = {}" .format(winnerLeft))
            logger.debug("In last round select the remaining user  %s" , winner)

        return redirect('/get/{}/winner/{}/{}'.format(id, winner, True))

    # Logic for 2nd to n-1 rounds
    elif(len(allWinners) != len(group_table.objects.filter(g_id = group))):
        logger.info("Getting winner for 2nd to n-1 rounds")
        round = len(allWinners)
        logger.debug("allWinners = %s" , allWinners)
        logger.debug("round = %s" , round)
        finish = False

        messages.warning(request, "Round = {}".format(round))

        if round>0:
            lastWinner = group_table.objects.get(g_id = id , winner = True, round=int(round))
            logger.debug("lastWinner = %s" , lastWinner)
            lastWinnerUser = User.objects.get(username=lastWinner)
            logger.debug("lastWinnerUser for %s round = %s" , round , lastWinnerUser)


        # If winner exists by bidding, choose him, else choose the randomly selected winner
        if bid.objects.filter(g_id = id, bidAmount__gt = 0):
            winner = bid.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
            # If someone has already bid, don't show him the bid button
            logger.debug("highest bid winner for %s round = %s" , round , winner )

        
        # logger.debug("lastWinner for %s round = %s" , round, lastWinner )
        # logger.debug("allWinners = %s" , allWinners)
        # logger.debug("user = %s" , user)

        winner = startGroup(request , lastWinner , logger, id, finish)
        # If someone is the winner or if someone has bid should not be shown the bid form
        if str(winner) == str(user):
            finish = True
        logger.debug("winner for bid form = %s" , winner)

        for winners in allWinners:
            logger.debug("allWinners for bid form = %s" , winners)

            if str(winners) == str(user):
                finish = True

        return redirect('/get/{}/winner/{}/{}'.format(id, winner, finish))

    return redirect('/get/{}'.format(id))


def startGroup(request , winner , logger, id, finish):
     # If someone bid or bid more than the last, then random winner will not matter and the higest bid user will be the winner
    highestBidUser = bid.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()
    # logger.debug("highestBidUser = %s" , highestBidUser)
    # logger.debug("winner = %s" , winner)

    if highestBidUser and not finish:
        logger.debug("highestBidUser in startGroup = %s" , highestBidUser)
        winner = highestBidUser
        messages.warning(request , "highestBidUser = {}" .format(highestBidUser))
        return highestBidUser

    elif(winner):
        # logger.debug("highestBidUser = %s" , highestBidUser)
        messages.warning(request , "Winner = {}" .format(winner))
        return winner


    # No winner exists, select one winner randomly
    else:
        randomlySelectedWinner = getRandom(id, request, logger)
        if randomlySelectedWinner:
            user = User.objects.get(username=randomlySelectedWinner)
            winner = group_table.objects.get(g_id = id, u_id = user)
            winner.winner = True
            winner.save()
            allWinners = group_table.objects.filter(g_id = id, winner = True)
            # logger.debug("allWinners = %s" , allWinners)
            # logger.debug("len(allWinners) = %s" , len(allWinners))

            winner.round = len(allWinners)
            winner.save()
            messages.success(request , "randomlySelectedWinner = " , randomlySelectedWinner)
            logger.debug("randomlySelectedWinner = %s" , winner)
            return winner
    

def setGroupStartDate(group, milliseconds):
    #   if group.start_date == 0 or getCurrentDateInLocalTimezone().date() == convertMilisToDatetime(group.end_date).date():
    group.start_date = milliseconds
    group.save()

def setGroupEndDate(group):
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
    print("dateAfterOneMonth milis =", unixTimeMillis(dt))  
    group.end_date = unixTimeMillis(dt)
    group.save()


def returnWinner(request, id, winner, finish):
    context = {"id" : id ,"winner": winner , "finish" : str(finish)}
    return render(request, 'winner.html', context)

def getUsersWithPendingInvitations(groupId):
     return group_table.objects.filter(g_id = groupId , start_comity = False)

def getLogger():
    # create logger
    logger = logging.getLogger('Thrive')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    return logger



def getRandom(id, request, logger):
    usersInGroup = []
    # users = group_table.objects.filter(g_id = id, winner = false)
    # allWinners = group_table.objects.filter(g_id = id , winner = True, bidAmount__gt=0)
    notWinners = group_table.objects.filter(g_id = id , winner = False)
    logger.debug("notWinners = %s" , notWinners)
    # if notWinners and (len(allWinners) != (len(group_table.objects.filter(g_id = id)) -1)):
    if notWinners:
        for u in notWinners:
            usersInGroup.append(u)
            # messages.success(request , u)
        count = len(usersInGroup)
        i = randint(0, (count - 1))
        return usersInGroup[i]
    else:
        messages.success(request , "Commitee finished")
        return redirect('/get/{}'.format(id))



def bidMoney(request, id):
    # bidAmount = 0
    logger = getLogger()
    user = User.objects.get(username=request.user)
    allWinners = group_table.objects.filter(g_id = id, winner = True)
    userInGroup = group_table.objects.get(g_id = id, u_id = user)
    nonWinnerUsersInGroup = group_table.objects.filter(g_id = id, bidAmount=0)
    usersInGroup = group_table.objects.filter(g_id = id)
    user_info = UserInfo.objects.get(u_id = user)
    currentGroup = group_info_table.objects.get(id = id)
    dateAfterOneDays= convertMilisToDatetime(currentGroup.start_date) + relativedelta(days=+1)
    highestBidUser = bid.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()

    showBidInputBox = True
    totalAmount = int(len(usersInGroup)) * int(currentGroup.amount)
    if (getCurrentDateInLocalTimezone().date() >= dateAfterOneDays.date()):
    # if(getCurrentDateInLocalTimezone().date() >= getCurrentDateInLocalTimezone().date()):
        showBidInputBox = False
        if highestBidUser:
            round = len(allWinners)
            lastWinner = group_table.objects.get(g_id = id , winner = True, round=int(round))
            logger.debug('lastWinner in  bid =  %s' , lastWinner)

            if lastWinner and  highestBidUser != lastWinner:
                lastWinner.winner = False
                lastWinner.round = 0
                lastWinner.save()
            user = User.objects.get(username=highestBidUser)
            highestBidWinner = group_table.objects.get(g_id = id , u_id = user)
            
            if highestBidWinner:
                # logger.debug('highestBidWinner =  %s' , highestBidWinner)
                highestBidWinner.winner = True
                highestBidWinner.bidAmount = highestBidUser.bidAmount
                highestBidWinner.save()
                highestBidWinner.round = len(allWinners)
                highestBidWinner.save()


                logger.debug('round while bidding =  %s' , len(allWinners))

                messages.success(request, "{} highestBidUser with bid {}".format(highestBidUser, highestBidUser.bidAmount))
        
        
    else:
        # lastWinner = group_table.objects.filter(g_id = id , winner = True).last()
        if highestBidUser:
            messages.success(request, "{} highestBidUser3 with bid {}".format(highestBidUser, highestBidUser.bidAmount))

        messages.success(request, "Bids open till {} for {}. Please bid!".format(dateAfterOneDays.date() , str(dateAfterOneDays - getCurrentDateInLocalTimezone()).split('.')[0]))
        checkBidForm(request, totalAmount , id , userInGroup, nonWinnerUsersInGroup)
        
    context = {"name" : str(user), "userInGroup" : userInGroup, "highestBidUser" : str(highestBidUser), "usersInGroup" : usersInGroup, "showBidInputBox": showBidInputBox, "totalAmt" : totalAmount , "id" : id,"user_info" : user_info}
    return render(request, 'bid.html', context)

def checkBidForm(request, totalAmount, id , userInGroup, nonWinnerUsersInGroup):
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
            minBidAmountUser = bid.objects.filter(g_id = id, bidAmount__gt = 0).order_by('bidAmount').last()

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
                    minBidAmountUser.save()
            else:
                bidUser = bid(u_id = request.user, bidAmount = bidAmount, g_id= grp)
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



def unixTimeMillis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

