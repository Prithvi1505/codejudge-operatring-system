from jobs import JOBS
from copy import deepcopy

def print_table(results, title):
    print(f"\n=== {title} ===")
    print(f"{'Job ID':<10} {'Waiting':<10} {'Turnaround':<12}")
    for r in results:
        print(f"{r['job_id']:<10} {r['waiting']:<10} {r['turnaround']:<12}")
    avg_wait = sum(r['waiting'] for r in results) / len(results)
    avg_tat = sum(r['turnaround'] for r in results) / len(results)
    print(f"Average Waiting Time: {avg_wait:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")
    return avg_wait, avg_tat

# ---------------- FCFS ----------------
def fcfs(jobs):
    jobs = sorted(jobs, key=lambda x: (x['arrival_time'], x['job_id']))
    time = 0
    results = []
    for j in jobs:
        if time < j['arrival_time']:
            time = j['arrival_time']
        wait = time - j['arrival_time']
        time += j['burst_time']
        tat = time - j['arrival_time']
        results.append({'job_id': j['job_id'], 'waiting': wait, 'turnaround': tat})
    return results

# ---------------- Non-preemptive SJF ----------------
def sjf(jobs):
    jobs = deepcopy(jobs)
    time = 0
    results = []
    completed = set()
    while len(completed) < len(jobs):
        ready = [j for j in jobs if j['arrival_time'] <= time and j['job_id'] not in completed]
        if not ready:
            time += 1
            continue
        # Select shortest burst, then earlier arrival, then lower job_id
        ready.sort(key=lambda x: (x['burst_time'], x['arrival_time'], x['job_id']))
        j = ready[0]
        wait = time - j['arrival_time']
        time += j['burst_time']
        tat = time - j['arrival_time']
        results.append({'job_id': j['job_id'], 'waiting': wait, 'turnaround': tat})
        completed.add(j['job_id'])
    return results

# ---------------- SRTF (preemptive) ----------------
def srtf(jobs):
    jobs = deepcopy(jobs)
    n = len(jobs)
    remaining = {j['job_id']: j['burst_time'] for j in jobs}
    arrival = {j['job_id']: j['arrival_time'] for j in jobs}
    burst = {j['job_id']: j['burst_time'] for j in jobs}
    completed = set()
    time = 0
    results = {}
    last_job = None
    while len(completed) < n:
        ready = [j for j in jobs if j['arrival_time'] <= time and j['job_id'] not in completed]
        if not ready:
            time += 1
            continue
        ready.sort(key=lambda x: (remaining[x['job_id']], x['arrival_time'], x['job_id']))
        current = ready[0]
        remaining[current['job_id']] -= 1
        time += 1
        if remaining[current['job_id']] == 0:
            completed.add(current['job_id'])
            tat = time - arrival[current['job_id']]
            wait = tat - burst[current['job_id']]
            results[current['job_id']] = {'job_id': current['job_id'], 'waiting': wait, 'turnaround': tat}
    return list(results.values())

# ---------------- Round Robin ----------------
def round_robin(jobs, quantum):
    from collections import deque
    jobs = deepcopy(jobs)
    jobs.sort(key=lambda x: (x['arrival_time'], x['job_id']))
    remaining = {j['job_id']: j['burst_time'] for j in jobs}
    arrival = {j['job_id']: j['arrival_time'] for j in jobs}
    burst = {j['job_id']: j['burst_time'] for j in jobs}
    queue = deque()
    time = 0
    i = 0
    completed = set()
    results = {}
    context_switches = 0
    last_running = None

    while len(completed) < len(jobs):
        # Add newly arrived jobs
        while i < len(jobs) and jobs[i]['arrival_time'] <= time:
            queue.append(jobs[i]['job_id'])
            i += 1

        if not queue:
            time += 1
            continue

        current = queue.popleft()
        if last_running is not None and last_running != current:
            context_switches += 1
        last_running = current

        run_time = min(quantum, remaining[current])
        remaining[current] -= run_time
        time += run_time

        # Add jobs that arrived during this quantum
        while i < len(jobs) and jobs[i]['arrival_time'] <= time:
            queue.append(jobs[i]['job_id'])
            i += 1

        if remaining[current] > 0:
            queue.append(current)
        else:
            completed.add(current)
            tat = time - arrival[current]
            wait = tat - burst[current]
            results[current] = {'job_id': current, 'waiting': wait, 'turnaround': tat}

    return list(results.values()), context_switches

# ---------------- Priority (with / without aging) ----------------
def priority_scheduling(jobs, aging=False):
    jobs = deepcopy(jobs)
    time = 0
    results = []
    completed = set()
    ready_since = {}

    while len(completed) < len(jobs):
        for j in jobs:
            if j['arrival_time'] <= time and j['job_id'] not in completed and j['job_id'] not in ready_since:
                ready_since[j['job_id']] = time

        ready = [j for j in jobs if j['arrival_time'] <= time and j['job_id'] not in completed]
        if not ready:
            time += 1
            continue

        if aging:
            for j in ready:
                waited = time - ready_since[j['job_id']]
                j['effective'] = max(1, j['priority'] - (waited // 3))
        else:
            for j in ready:
                j['effective'] = j['priority']

        ready.sort(key=lambda x: (x['effective'], x['arrival_time'], x['job_id']))
        j = ready[0]
        wait = time - j['arrival_time']
        time += j['burst_time']
        tat = time - j['arrival_time']
        results.append({'job_id': j['job_id'], 'waiting': wait, 'turnaround': tat})
        completed.add(j['job_id'])

    return results

if __name__ == "__main__":
    print_table(fcfs(JOBS), "FCFS")
    print_table(sjf(JOBS), "Non-preemptive SJF")
    print_table(srtf(JOBS), "SRTF")

    rr3, switches3 = round_robin(JOBS, 3)
    avg_w3, avg_t3 = print_table(rr3, "Round Robin (quantum=3)")
    print(f"Context switches (quantum=3): {switches3}")

    rr6, switches6 = round_robin(JOBS, 6)
    avg_w6, avg_t6 = print_table(rr6, "Round Robin (quantum=6)")
    print(f"Context switches (quantum=6): {switches6}")

    print("\nTheory: Quantum 3 causes more overhead in a real OS because it produces more context switches "
          f"({switches3} vs {switches6}), and each switch has a non-zero cost.")

    no_aging = priority_scheduling(JOBS, aging=False)
    print_table(no_aging, "Priority (No Aging)")
    longest_no = max(no_aging, key=lambda x: x['waiting'])
    print(f"Longest waiting job (no aging): {longest_no['job_id']} with wait {longest_no['waiting']}")

    with_aging = priority_scheduling(JOBS, aging=True)
    print_table(with_aging, "Priority (With Aging)")
    longest_yes = max(with_aging, key=lambda x: x['waiting'])
    print(f"Longest waiting job (with aging): {longest_yes['job_id']} with wait {longest_yes['waiting']}")
