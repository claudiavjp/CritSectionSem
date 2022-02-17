from multiprocessing import Process, Manager, BoundedSemaphore
from multiprocessing import current_process
from multiprocessing import Value, Array

N = 8

def task(common, tid, semaph):
    a = 0
    for i in range(100):
        print(f'{tid}−{i}: Non−critical Section')
        a += 1
        print(f'{tid}−{i}: End of non−critical Section')
        
        semaph.acquire()
        try:
            print(f'{tid}−{i}: Critical section')
            v = common.value + 1
            print(f'{tid}−{i}: Inside critical section')
            common.value = v
            print(f'{tid}−{i}: End of critical section')
        finally:
            semaph.release()

def main():
    lp = []
    common = Value('i', 0)
    semaph = BoundedSemaphore(1)
    for tid in range(N):
        lp.append(Process(target=task, args=(common, tid, semaph)))
    print (f"Valor inicial del contador {common.value}")
    for p in lp:
        p.start() #para abrir nuevas hebras de ejecución a raiz del hilo de ejecución principal
    for p in lp:
        p.join() #espera que los procesos p abiertos por el bucle anterior acaben y los cierra, de forma que nos queda un único hilo de ejecición
    print (f"Valor final del contador {common.value}")
    print ("fin")

if __name__ == "__main__":
    main()
