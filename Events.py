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
