# Zone Job-Scheduler & Deadlock-Safety Engine

## Production Choice (Task 8)

**Chosen family: Round Robin**

- FCFS produces the highest average waiting time on this job list → unsuitable for time-sensitive sensor jobs.
- SJF/SRTF family can starve longer jobs (observed higher variance in waiting times) → unacceptable for zone fairness.
- Priority scheduling without aging left Z3-J02 with the longest wait; even with aging the priority numbers still create unfairness under continuous high-priority arrivals → less suitable than RR for mixed sensor workloads.
- Round Robin (especially quantum=6) balances fairness and overhead (only 10 context switches vs 16 at quantum 3) while keeping average waiting time reasonable for this exact workload.
