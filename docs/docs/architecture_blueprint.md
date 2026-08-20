# Architecture Blueprint — Zone Job-Scheduler Deployment

All references below use the scheduler, Banker's Algorithm engine, and memory translator from Part 1 as the fixed compute core.

## 9. Distributed Architecture & Communication

**Chosen Architecture: Client-Server**

- Transparency: Zone controllers act as clients; dashboard is the central server.
- Fault tolerance: Dashboard can be made highly available; zone controllers continue local scheduling.
- Scalability: New zones can be added as clients without changing other zones.
- Single point of failure: Mitigated by redundant dashboard instances.

**Data Flows:**
- (a) Real-time public-safety alert → **Asynchronous MQTT** (low latency, publish-subscribe suitable for alerts).
- (b) Full day's sensor log → **Synchronous HTTPS** (reliable delivery and integrity for archival).

## 10. VPC Design

Use **one VPC with three private subnets** (one per Zone).  
Logical isolation is provided by subnet boundaries + route tables.  
Customizability allows different security groups per zone.

**Enforcing control:** A Security Group rule on Zone-A's subnet that denies all inbound traffic from Zone-B's CIDR range.

## 11. Network-Security Objectives

| Objective              | Control                          | How it defends this platform                                      |
|------------------------|----------------------------------|-------------------------------------------------------------------|
| Protect sensitive data | AES-256 encryption at rest       | Encrypts JOBS list and sensor logs on zone controllers            |
| Authentication         | Mutual TLS + certificates        | Ensures only authorized zone controllers connect to dashboard     |
| Authorization          | Role-based IAM policies          | Limits operators to their own zone resources                      |
| Prevent cyber attacks  | WAF + rate limiting              | Blocks DDoS and injection attempts against the dashboard API      |
| Secure communication   | TLS 1.3                          | Encrypts all data in transit between zones and dashboard          |
| Ensure availability    | Multi-AZ deployment + auto-scale | Keeps the scheduler engine running even if one AZ fails           |

## 12. IAM Table & Data-Protection Map

**IAM Roles**
- Zone Operator: Read/write only their zone's jobs and sensors
- City Dashboard Admin: Full access to all zones + Banker's safety checks
- Auditor: Read-only access to logs and scheduling metrics

**Data States**
- At rest: AES-256 encryption of the JOBS list on zone controller disks
- In transit: TLS 1.3 for public-safety alerts to the dashboard
- In use: Memory encryption / secure enclave for Banker's Algorithm safety checks running in RAM

## 13. IoT Connectivity & Architecture Layers

**Devices & Technologies**
- Traffic camera trigger → 5G (high bandwidth, low latency)
- Environmental sensor → LoRaWAN (long range, low power)
- Wearable public-safety device → NB-IoT (good coverage, low power)

**IoT Layers**
- Physical Environment: City streets, junctions, air quality
- Perception/Device: Sensors listed above
- Gateway: Zone edge gateways
- Network Communication: 5G / LoRaWAN / NB-IoT
- Cloud Platform: **Part 1's scheduler + Banker's Algorithm engine**
- Application: Smart City Operations dashboard

## 14. Threats & Mitigations

1. Compromised zone controller → Mutual TLS + certificate pinning
2. Man-in-the-middle on alert messages → End-to-end encryption + MQTT over TLS
3. Resource exhaustion attack on Banker's engine → Rate limiting + request quotas
