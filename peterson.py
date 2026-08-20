import threading
import time

counter = 100
flag = [False, False]
turn = 0

def unsafe_worker(delta, name):
    global counter
    for _ in range(5):  # multiple runs to show race
        local = counter
        time.sleep(0.001)  # force interleaving
        counter = local + delta
        print(f"{name} saw {local}, wrote {counter}")

def peterson_enter(id):
    other = 1 - id
    flag[id] = True
    turn = other
    while flag[other] and turn == other:
        pass

def peterson_exit(id):
    flag[id] = False

def safe_worker(delta, id, name):
    global counter
    for _ in range(5):
        peterson_enter(id)
        local = counter
        counter = local + delta
        print(f"{name} (safe) saw {local}, wrote {counter}")
        peterson_exit(id)

print("=== UNSAFE RUNS ===")
for i in range(5):
    counter = 100
    t1 = threading.Thread(target=unsafe_worker, args=(-40, "Debit"))
    t2 = threading.Thread(target=unsafe_worker, args=(25, "Credit"))
    t1.start(); t2.start()
    t1.join(); t2.join()
    print(f"Run {i+1} final counter = {counter}")

print("\n=== PETERSON'S ALGORITHM (SAFE) ===")
for i in range(5):
    counter = 100
    flag[0] = flag[1] = False
    t1 = threading.Thread(target=safe_worker, args=(-40, 0, "Debit"))
    t2 = threading.Thread(target=safe_worker, args=(25, 1, "Credit"))
    t1.start(); t2.start()
    t1.join(); t2.join()
    print(f"Safe Run {i+1} final counter = {counter}")
