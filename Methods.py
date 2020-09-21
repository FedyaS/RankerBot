import Events
import datetime


def select_suffix(day):
    st = [1, 21, 31]
    nd = [2, 22]
    rd = [3, 23]
    if day in st:
        return "st"
    elif day in nd:
        return "nd"
    elif day in rd:
        return "rd"
    else:
        return "th"


def add_item(array, reminder: Events.Reminder = None, event: Events.Event = None):  # Adds an item to a dynamic array
    # Detect which case we are working with, this function is convenient because it provides the ability to add other
    # types of events and their lists
    if reminder is None and event is None:
        return False
    elif reminder is None:
        item = event
    elif event is None:
        item = reminder
    else:
        return False

    # Algorithm to add item to the first blank element or append it to the end
    blank_found = False
    for i in range(len(array)):
        if array[i] == 0:
            item.index = i
            array[i] = item.index
            blank_found = True
            break

    if not blank_found:
        item.index = len(array)
        array.append(item)


def remove_item(array, reminder: Events.Reminder = None, event: Events.Event = None):  # Removes an item from a dynamic array
    if reminder is None and event is None:
        return False
    elif reminder is None:
        item = event
    elif event is None:
        item = reminder
    else:
        return False

    if item.index == len(array) - 1:
        array.pop(item.index)
    else:
        array[item.index] = 0


def string_to_duration(st):  # Method to convert string of format 20:30:30 or 30:30 or 30s or 1h2m30s into a duration
    st = st.lower()
    time_split = st.find(':')
    timer = 0
    if time_split == -1:
        h_i = st.find("h")
        m_i = st.find("m")
        s_i = st.find("s")

        if h_i != -1:
            hour = st[0:h_i]
            if m_i != -1:
                minute = st[h_i + 1:m_i]
                if s_i != -1:
                    second = st[m_i + 1:s_i]
                else:
                    second = 0
            else:
                minute = 0
                if s_i != -1:
                    second = st[h_i + 1:s_i]
                else:
                    second = 0
        elif m_i != -1:
            hour = 0
            minute = st[0:m_i]
            if s_i != -1:
                second = st[m_i + 1:s_i]
            else:
                second = 0
        else:
            hour = 0
            minute = 0
            if s_i != -1:
                second = st[0:s_i]
            else:
                second = 0
        try:
            hour = int(hour)
            minute = int(minute)
            second = int(second)
        except ValueError:
            timer = -1
    else:
        quantity = st.count(":")
        if quantity == 1:
            second = 0
            hour = st[0:time_split]
            minute = st[time_split + 1:]
        elif quantity == 2:
            time_split_2 = st.find(":", time_split + 1)
            hour = st[0:time_split]
            minute = st[time_split + 1:time_split_2]
            second = st[time_split_2 + 1:]
        else:
            hour = 0
            minute = 0
            second = 0

        try:
            hour = int(hour)
            minute = int(minute)
            second = int(second)
        except ValueError:
            timer = -1

    if timer == -1:
        pass
    else:
        timer = (hour * 3600) + (minute * 60) + second

    if timer == 0:
        timer = -1

    return timer


def string_to_time(st1, st2):
    time_split = st1[2].find(':')
    if time_split is -1:
        try:
            # Always use try for this kind of bs so if it fails our bot doesn't crash
            hour = int(st1)
            try:
                minute = int(st2)
            except ValueError:
                minute = 0
            clock = datetime.time(hour, minute, 00)
        except ValueError:
            hour = -1
            minute = -1
            clock = -1

    else:
        try:
            hour = int(st1[0:time_split])
            try:
                minute = int(st1[time_split:])
            except IndexError:
                minute = 0
            try:
                clock = datetime.time(hour, minute, 00)
            except ValueError:
                clock = -1
        except ValueError:
            hour = -1
            minute = -1
            clock = -1

    return clock

# while True:
#     my = input("\n")
#     my = my.split()
#     print(string_to_time(input("\n")))