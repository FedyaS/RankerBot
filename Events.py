class Reminder:
    def __init__(self, clock, text, index, to_ping=None):
        self.time_till = clock
        self.text = text
        if to_ping is None:
            self.to_ping = []
        else:
            self.to_ping = to_ping
        self.index = index
        self.done = False

    def run_time(self, time):
        self.time_till -= time

    def check_if_time(self):
        if self.done:
            return False
        elif self.time_till <= 0:
            return True
        else:
            return False

    def progress(self, time):
        self.run_time(time)
        return self.check_if_time()


class Event:
    def __init__(self, time):
        pass
