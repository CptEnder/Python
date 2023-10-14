"""
Created on Sat 10 Oct 21:07 2020
Finished on Sun 11 Oct 23:30 2020 ?
@author: Cpt.Ender

https://www.youtube.com/watch?v=kbwk1Tw3OhE
Given 2 people's calendars and the appointment time as
inputs (lists of strings of military time), find all the available
time spaces where they could have a meeting.

Sample Input:
cal1 = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
cal2 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
appTime = 30
bound1 = ['9:00', '20:00']
bound2 = ['10:00', '18:30']

Sample Output:
output = [['11:30', '12:30'], ['15:00', '16:00'], ['18:00', '18:30']]
                                                                                         """

""" INPUTS """
cal1 = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '16:45'], ['17:00', '17:30'], ['17:35', '18:00']]
cal2 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
appTime = 30
bound1 = ['9:00', '20:00']
bound2 = ['10:00', '18:30']


def time2Int(timetable: list):
    """ Convert a list of string military times to a list of integer times """
    new_lst = []
    for block in timetable:
        if type(block) == list:
            new_lst.append(time2Int(block))
        else:
            time1 = block.split(':')
            time1 = int(time1[0]) * 100 + int(time1[1])
            new_lst.append(time1)
    return new_lst


def int2Time(timetable: list):
    """ Convert a list of integer military times to a list o string times """
    new_lst = []
    for block in timetable:
        if type(block) == list:
            time1 = str(block[0] // 100) + ':' + str(block[0])[-2:]
            time2 = str(block[1] // 100) + ':' + str(block[1])[-2:]
            new_lst.append([time1, time2])
    return new_lst


def addBounds2Calendars(calendar: list, bound: list):
    """ Add the lower and upper time bounds for a calendar """
    calendar.insert(0, [0, bound[0]])
    calendar.append([bound[1], 2400])


def mergeAppointments(calendar: list):
    """ Merge the appointments of a calendar if the
    end time of one is the same as the start time of the next """
    i = 0
    while i < len(calendar) - 1:
        if calendar[i][1] == calendar[i + 1][0]:
            calendar[i][1] = calendar[i + 1][1]
            calendar.pop(i + 1)
            i -= 1
        i += 1


new_cal1 = time2Int(cal1)
new_cal2 = time2Int(cal2)
new_bound1 = time2Int(bound1)
new_bound2 = time2Int(bound2)

addBounds2Calendars(new_cal1, new_bound1)
addBounds2Calendars(new_cal2, new_bound2)
mergeAppointments(new_cal1)
mergeAppointments(new_cal2)


def mergeCalendars(calendar1: list, calendar2: list):
    """ Merge the 2 calendars together to form a
        new one with all the booked hours """
    pointer1 = 0
    pointer2 = 0
    _calendars = [calendar1, calendar2]
    _calendarsLengths = [len(calendar1), len(calendar2)]
    _calendarA = _calendars[_calendarsLengths.index(max(_calendarsLengths))]
    _calendarB = _calendars[_calendarsLengths.index(min(_calendarsLengths))]
    _bookedCal = [[time for time in block] for block in _calendarA]

    while pointer1 < len(_bookedCal):
        if pointer1 > 0:
            if _bookedCal[pointer1][1] < _bookedCal[pointer1 - 1][1]:
                _bookedCal.pop(pointer1)
        if _bookedCal[pointer1][1] >= _calendarB[pointer2][0]:
            if _bookedCal[pointer1][0] >= _calendarB[pointer2][0]:
                _bookedCal[pointer1][0] = _calendarB[pointer2][0]
            if _bookedCal[pointer1][1] <= _calendarB[pointer2][1]:
                _bookedCal[pointer1][1] = _calendarB[pointer2][1]
                pointer2 += 1
                pointer1 += 1
        else:
            pointer1 += 1
    return _bookedCal


def availableTimes(_bookedCal: list, _appTime: int):
    freeCal = []
    for i in range(len(_bookedCal) - 1):
        if _bookedCal[i + 1][0] - _bookedCal[i][1] >= _appTime:
            freeCal.append([_bookedCal[i][1], _bookedCal[i + 1][0]])
    freeCal = int2Time(freeCal)
    return freeCal


bookedCal = mergeCalendars(new_cal2, new_cal1)
mergeAppointments(bookedCal)

""" OUTPUT """
availableAppointments = availableTimes(bookedCal, appTime)
