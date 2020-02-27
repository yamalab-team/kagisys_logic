import servo
import led

class Observer:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except:
            pass

    def notify(self):
        for ob in self._observers:
            ob.update(self)

class Slack():
    def update(self, kagi):
        print(kagi.isOpen)

class Kagi(Observer):
    def __init__(self):
        super().__init__()
        self.isOpen = False
        # 鍵の状態が変わったときに通知する
        self.attach(Slack())
        self.attach(servo())
        self.attach(led())

    def open(self):
        if self.isOpen:
            return
        self.isOpen = True
        self.notify()
        
    
    def close(self):
        if not self.isOpen:
            return
        self.isOpen = False
        self.notify()

if __name__ == "__main__":
    k = Kagi()
    k.open()
    k.close()
