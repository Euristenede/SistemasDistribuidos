import threading

class ContadorCentral:
    _numPessoas = 0

    def __init__(self):
        self.lock = threading.Lock()

    def _somarNumPessoas(self, n):
        self.lock.acquire()
        self._numPessoas += n
        self.lock.release()

class Roleta(threading.Thread):

    def __init__(self, incr, contadorCentral):
        threading.Thread.__init__(self)
        self.totPessoas = 0
        self.incr = incr
        self.contadorCentral = contadorCentral

    def run(self):
        for _ in range(4000000):
            self.totPessoas += self.incr
            self.contadorCentral._somarNumPessoas(self.incr)

def main():
    contador = ContadorCentral()

    e1 = Roleta(1, contador)
    e2 = Roleta(3, contador)

    e1.start()
    e2.start()

    e1.join()
    e2.join()

    print("\n*** FIM DA CONTAGEM ***")
    print(f"*** Entrada 1: {e1.totPessoas:,} pessoas")
    print(f"*** Entrada 2: {e2.totPessoas:,} pessoas")
    print(f"*** Total: {e1.totPessoas + e2.totPessoas:,} pessoas")
    print(f"*** Total CENTRALIZADO: {contador._numPessoas:,} pessoas")

if __name__ == "__main__":
    main()