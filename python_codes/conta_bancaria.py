from threading import Thread
import threading

class Conta:
    saldo = 0

    def __init__(self):
        self.lock = threading.Lock()

    def funcao(self,op, vlr):
        self.lock.acquire()
        if(op == 1):
            Conta.saldo -= vlr
        elif(op == 2):
            Conta.saldo += vlr
        self.lock.release()

class Retirada(Thread):  
    def __init__(self, c):
        Thread.__init__(self)
        self.c = c

    def run(self):
        vlrs = [10, 20, 30, 40, 50, 60]
        for vlr in vlrs:
            self.c.funcao(1, vlr)
            print(f"Retirada: {vlr} - Saldo: {self.c.saldo}")

class Deposito(Thread):
    def __init__(self, c):
        Thread.__init__(self)
        self.c = c

    def run(self):
        vlrs = [40, 50, 60, 10, 20, 30]
        for vlr in vlrs:
            self.c.funcao(2, vlr)
            print(f"Deposito: {vlr} - Saldo: {self.c.saldo}")

c = Conta()

d = Deposito(c)
r = Retirada(c)

d.start()
r.start()

try:
    d.join()
    r.join()
except:
    pass

print(f"Saldo={c.saldo}")

