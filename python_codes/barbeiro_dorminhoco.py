import threading
import time
import random
import argparse

class Cadeira():
    n_cadeiras = 0
    clientes = []

    @staticmethod
    def tem_lugar():
        return len(Cadeira.clientes) < Cadeira.n_cadeiras

    @staticmethod
    def tem_cliente():
        return len(Cadeira.clientes) > 0

    @staticmethod
    def sentar(cliente):
        Cadeira.clientes.append(cliente)

    @staticmethod
    def levantar():
        return Cadeira.clientes.pop(0)

class Cliente(threading.Thread):
    def __init__(self, nome, lock, barbeiro):
        threading.Thread.__init__(self)
        self.nome = nome
        self.lock = lock
        self.barbeiro = barbeiro
        self.e_esperar = threading.Event()

    def espera_atendimento(self):
        print(f"Cliente {self.nome} esperando")
        self.e_esperar.wait()
        self.e_esperar.clear()

    def continuar(self):
        print(f"\nCliente {self.nome} atendido")
        self.e_esperar.set()

    def sentar(self):
        self.lock.acquire()
        print(f"\nCliente {self.nome} sentou")
        Cadeira.sentar(self)
        self.lock.release()
        self.espera_atendimento()

    def run(self):
        self.lock.acquire()
        result = Cadeira.tem_lugar()
        self.lock.release()
        
        if result:
            self.lock.acquire()
            if self.barbeiro.dormindo:
                print(f"\nCliente {self.nome} acordou o barbeiro")
                self.barbeiro.acordar()
            self.lock.release()
            self.sentar()
        else:
            print(f"\nCliente {self.nome} foi embora porque não tem lugar")

class Barbeiro(threading.Thread):
    def __init__(self, nome, lock):
        threading.Thread.__init__(self)
        self.nome = nome
        self.lock = lock
        self.e_dormir = threading.Event()
        self.dormindo = False
        self.exit_event = threading.Event()

    def dormir(self):
        print("\nBarbeiro dormindo")
        self.lock.acquire()
        self.dormindo = True
        self.lock.release()
        self.e_dormir.wait()
        self.e_dormir.clear()

    def acordar(self):
        self.dormindo = False
        self.e_dormir.set()

    def trabalhar(self):
        if Cadeira.tem_cliente():
            self.lock.acquire()
            cliente = Cadeira.levantar()
            self.lock.release()
            print(f"\nAtendendo cliente {cliente.nome}")
            tempo = random.randint(1, 5)
            time.sleep(tempo)
            cliente.continuar()

    def run(self):
        while True:
            if not(Cadeira.tem_cliente()):
                self.dormir()
            self.trabalhar()
            time.sleep(0.5)

            if self.exit_event.is_set():
                break

class GerenciarClientes(threading.Thread):
    def __init__(self, lock, barbeiro):
        threading.Thread.__init__(self)
        self.lock = lock
        self.barbeiro = barbeiro
        self.exit_event = threading.Event()

    def run(self):
        i = 1
        while True:
            tempo = random.randint(1, 8)
            time.sleep(tempo)
            Cliente(i, self.lock, self.barbeiro).start()
            i += 1

            if self.exit_event.is_set():
                break
  
def main_task(n_cadeiras, tempo_aberto):
    Cadeira.n_cadeiras = n_cadeiras
  
    # creating a lock
    lock = threading.Lock()

    barbeiro = Barbeiro(1, lock)
    barbeiro.start()

    clientes = GerenciarClientes(lock, barbeiro)
    clientes.start()

    time.sleep(tempo_aberto)
    clientes.exit_event.set()
    
    while len(Cadeira.clientes) != 0:
        time.sleep(1)
    barbeiro.exit_event.set()

    # wait until threads finish their job
    clientes.join()
    barbeiro.join()

    print("\nBARBEARIA FECHOU!!!")

def parse_argumentos():
    """Faz o parse dos argumentos"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_cadeiras',
                        help='Numero de Cadeiras. [3]',
                        type=int,
                        default=3)
    parser.add_argument('--tempo_aberto',
                        help='Tempo que a barbearia fica aberta. [120]',
                        type=int,
                        default=120)
    return parser.parse_args()

def main():
    # faz o parse dos argumentos recebidos
    args = parse_argumentos()

    if args.n_cadeiras > 0 and args.tempo_aberto > 0:
        print(f"BARBEARIA ABERTA COM {args.n_cadeiras} CADEIRAS!!!")
        print(f"A barbearia fica aberta por {args.tempo_aberto} segundos!!!")
        main_task(args.n_cadeiras, args.tempo_aberto)
    else:
        print("Os valores dos argumentos devem ser maior que 0")

if __name__ == "__main__":
    main()