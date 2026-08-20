AVAILABLE = [3, 3, 2]
MAX_NEED = {"P0": [7, 5, 3], "P1": [3, 2, 2], "P2": [9, 0, 2], "P3": [2, 2, 2]}
ALLOCATION = {"P0": [0, 1, 0], "P1": [2, 0, 0], "P2": [3, 0, 2], "P3": [2, 1, 1]}

def calculate_need():
    need = {}
    for p in MAX_NEED:
        need[p] = [MAX_NEED[p][i] - ALLOCATION[p][i] for i in range(3)]
    return need

def is_safe(avail, alloc, need):
    work = avail[:]
    finish = {p: False for p in alloc}
    safe_seq = []
    while len(safe_seq) < len(alloc):
        found = False
        for p in alloc:
            if not finish[p] and all(need[p][i] <= work[i] for i in range(3)):
                for i in range(3):
                    work[i] += alloc[p][i]
                finish[p] = True
                safe_seq.append(p)
                found = True
                break
        if not found:
            return False, []
    return True, safe_seq

need = calculate_need()
print("Need matrix:", need)

safe, seq = is_safe(AVAILABLE, ALLOCATION, need)
print("Initial state safe?", safe)
print("Safe sequence:", seq)

# Request (a) P1 requests [1,0,2]
req = [1, 0, 2]
p = "P1"
if all(req[i] <= need[p][i] for i in range(3)) and all(req[i] <= AVAILABLE[i] for i in range(3)):
    new_avail = [AVAILABLE[i] - req[i] for i in range(3)]
    new_alloc = {k: v[:] for k, v in ALLOCATION.items()}
    new_need = {k: v[:] for k, v in need.items()}
    for i in range(3):
        new_alloc[p][i] += req[i]
        new_need[p][i] -= req[i]
    safe, seq = is_safe(new_avail, new_alloc, new_need)
    print(f"\nP1 request {req}: {'GRANTED' if safe else 'DENIED'} (safe sequence: {seq})")
else:
    print("P1 request exceeds Need or Available")

# Request (b) P0 requests [2,0,2]
req = [2, 0, 2]
p = "P0"
if all(req[i] <= need[p][i] for i in range(3)) and all(req[i] <= AVAILABLE[i] for i in range(3)):
    new_avail = [AVAILABLE[i] - req[i] for i in range(3)]
    new_alloc = {k: v[:] for k, v in ALLOCATION.items()}
    new_need = {k: v[:] for k, v in need.items()}
    for i in range(3):
        new_alloc[p][i] += req[i]
        new_need[p][i] -= req[i]
    safe, seq = is_safe(new_avail, new_alloc, new_need)
    if safe:
        print(f"P0 request {req}: GRANTED")
    else:
        print(f"P0 request {req}: DENIED — granting would leave the system in an UNSAFE state")
else:
    print("P0 request exceeds Need or Available")
