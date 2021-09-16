import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")
django.setup()

from django.http import request
from comity.models import *
import datetime
from random import randint
import pytz
from dateutil.relativedelta import relativedelta

def my_cron_job():
    print('sample cron job')
    groups = group_info_table.objects.all()
    users = User.objects.all()
    for user in users:
        print('collecting user details for ' + user.username)
        user_info = UserInfo.objects.get(u_id = user.id) if UserInfo.objects.filter(u_id = user.id).exists() else None
        # -------------- Deactivate Subscription -------------------
        if user_info:
            if (getCurrentDateInLocalTimezone().date() == convertMilisToDatetime(user_info.superuser_end_date)):
                print("Deactivating subscription for user =" , user.username)
            # deactivateSubscription(user.username)

                user_info.superuser = False
                user_info.superuser_start_date = 0
                user_info.superuser_end_date = 0
                user_info.save()
                print("Deactivating subscription successful for user =" , user.username)



    for group in groups:
        if group.status == 'active':
            print("Active group: ",  group.id)
            id = group.id
            currentGroup = group_info_table.objects.get(id=id)
            # Getting 2 days after the end_date since at midnight the date changes
            dateAfterOneDays = convertMilisToDatetime(currentGroup.end_date) + relativedelta(days=+2)
            allWinners = group_table.objects.filter(g_id=id, winner=True)


            # -------------- Bid money logic -------------------
            if (getCurrentDateInLocalTimezone().date() == convertMilisToDatetime(currentGroup.bid_date)):
                # # dateAfterOneDays = convertMilisToDatetime(currentGroup.start_date) + relativedelta(days=+3)
                highestBidUser = bid.objects.filter(g_id=id, bidAmount__gt=0).order_by('bidAmount').last()
                if highestBidUser:
                    round = len(allWinners)
                    lastWinner = group_table.objects.get(g_id=id, winner=True, round=int(round))
                    print('lastWinner in  bid =  %s', lastWinner)

                    if lastWinner and highestBidUser != lastWinner:
                        lastWinner.winner = False
                        lastWinner.round = 0
                        lastWinner.save()
                    user = User.objects.get(username=highestBidUser)
                    highestBidWinner = group_table.objects.get(g_id=id, u_id=user)
                    print('highestBidWinner in  bid =  %s', highestBidWinner.u_id.username)

                    if highestBidWinner:
                        print('highestBidWinner =  %s', highestBidWinner)
                        highestBidWinner.winner = True
                        highestBidWinner.bidAmount = highestBidUser.bidAmount
                        highestBidWinner.save()
                        highestBidWinner.round = len(allWinners)
                        highestBidWinner.save()

                # When bidding ends for a round, set bid date to a day after group end_date
                currentGroup.bid_date = dateAfterOneDays.timestamp() * 1000
                currentGroup.final_bid_time = getCurrentDateInLocalTimezone().date()
                currentGroup.save()
                print("updated currentGroup.bid_date")


                    # ----------------- sendNotficationToStartComity ---------------------------

            if (getCurrentDateInLocalTimezone().date() == convertMilisToDatetime(group.end_date).date()):
            # if (getCurrentDateInLocalTimezone().date() == convertMilisToDatetime(currentGroup.bid_date)):
                print("allWinners = %s", allWinners)
                bid.objects.filter(g_id=id).delete()
                winner = bid.objects.select_related().filter(g_id=id, bidAmount__gt=0).order_by('bidAmount').last()

                # import pdb;
                # pdb.set_trace()
                winner = startGroup(request, winner, id, False)

                data = {
                    "name": winner.u_id.username,
                    "winner": winner.winner,
                    "start_comity": winner.start_comity,
                    "round": winner.round,
                    "bid_amount": winner.bidAmount
                }
                print("end date winner", data)

                print("Logic when group ends %s", winner)
                setGroupEndDate(group)

            if (len(allWinners) == len(group_table.objects.filter(g_id=id))):

                if (getCurrentDateInLocalTimezone().date() >= convertMilisToDatetime(group.end_date).date()):
                    # if(getCurrentDateInLocalTimezone().date() >= getCurrentDateInLocalTimezone().date()):

                    group.status = 'completed'
                    group.save()
                    print("Group Finished " , id)
        else:
            print("Group not active" , group.id)

def startGroup(request, winner, id, finish):
    # If someone bid or bid more than the last, then random winner will not matter and the higest bid user will be the winner
    highestBidUser = bid.objects.filter(g_id=id, bidAmount__gt=0).order_by('bidAmount').last()
    # logger.debug("highestBidUser = %s" , highestBidUser)
    # logger.debug("winner = %s" , winner)

    if highestBidUser and not finish:
        print("highestBidUser in startGroup = %s", highestBidUser)
        winner = highestBidUser
        print("highestBidUser = {}".format(highestBidUser))
        return highestBidUser

    elif (winner):
        print("winner = %s" , winner)
        return winner


    # No winner exists, select one winner randomly
    else:
        randomlySelectedWinner = getRandom(id, request)
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
            print("randomlySelectedWinner = ", randomlySelectedWinner)
            print("randomlySelectedWinner = %s", winner)
            return winner

def deactivateSubscription(username):
    username = username
    user = User.objects.get(username=username)
    user_info = UserInfo.objects.get(u_id=user.id) if UserInfo.objects.filter(
        u_id=user.id).exists() else None
    if user_info:
        user_info.superuser = False
        user_info.superuser_start_date = 0
        user_info.superuser_end_date = 0
        user_info.save()
        return True
    return False


def getRandom(id, request):
    usersInGroup = []
    # users = group_table.objects.filter(g_id = id, winner = false)
    # allWinners = group_table.objects.filter(g_id = id , winner = True, bidAmount__gt=0)
    notWinners = group_table.objects.filter(g_id=id, winner=False)
    print("notWinners = %s", notWinners)
    # if notWinners and (len(allWinners) != (len(group_table.objects.filter(g_id = id)) -1)):
    if notWinners:
        for u in notWinners:
            usersInGroup.append(u)
            # messages.success(request , u)
        count = len(usersInGroup)
        i = randint(0, (count - 1))
        return usersInGroup[i]
    else:
        print(request, "Commitee finished")
        # return redirect('/get/{}'.format(id))


def setGroupEndDate(group):
    duration = {"1m": "month 1", "2w": "weeks 2", "1w": "weeks 1", "3d": "days 3"}
    print("iuhibhkbk", duration.get(group.duration).split(' ')[0])
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


def convertMilisToDatetime(milis):
    if milis:
        s = milis / 1000
        return datetime.datetime.fromtimestamp(s, pytz.timezone('Asia/Kolkata'))


def getCurrentMilis():
    print('milis = ', datetime.datetime.now(pytz.timezone('Asia/Kolkata')).timestamp() * 1000)
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata')).timestamp() * 1000


def getCurrentDateInLocalTimezone():
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

def unixTimeMillis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

if __name__ == "__main__":
    my_cron_job()