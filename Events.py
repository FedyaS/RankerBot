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


class Reminder:
    # This is the reminder class and it represents a simple reminder (1 message)
    def __init__(self, clock, text, index, to_ping=None):  # We should decide if we need any other variables
        # Need to make it somehow so we can have both reminders that work as timers (go off in a set amount of time)
        # and as scheduled reminders (go off when the clock hits a certain time)
        self.time_till = clock
        self.text = text
        if to_ping is None:
            self.to_ping = []
        else:
            self.to_ping = to_ping
        self.index = index
        self.done = False

    def run_time(self, time):  # Running the timer down
        self.time_till -= time

    def check_if_time(self):  # Checking if it is time for the reminder to go off
        if self.done:
            return False
        elif self.time_till <= 0:
            return True
        else:
            return False

    def progress(self, time):  # Progressing the reminder, maybe should update self.done as well if time has come
        self.run_time(time)
        return self.check_if_time()


class Event:
    # This is the event class which represents an Event. This event can have attendance as well as reminders associated
    # with it.
    def __init__(self, time):
        pass
