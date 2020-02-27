class Slack:
    def __init__(self):
        self.url = "incomming messageのurl"

    def update(self, kagi):
        if kagi.isOpen:
            msg = "開くました"
        else:
            msg = "閉めました"
        print("Kagi -> ", kagi.isOpen)