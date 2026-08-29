# Generator for comprehensive Notion-ready student workbooks

$workbooksDir = "d:\Projects\Infrastructure for Huawei\student_workbooks"

# 1. Master Syllabus
$syllabus = @"
# Huawei HCIA / HCIP Virtual Lab Guidebook: 32 Practical Hands-On Labs
**Platform:** EVE-NG (`http://208.8.8.135/`)  
**Target Devices:** Huawei AR1000v Router & NE40E Core Router  
**Converted From:** Standard Enterprise CCNA 32-Lab Simulation Suite  

---

## Course Structure & Learning Paths

```
Huawei 32-Lab Practical Curriculum
│
├── Module 1: Layer 2 Switching, VLANs & Link Aggregation (17 Labs)
│   ├── Access / Trunk / Hybrid Link Types
│   ├── Native VLAN (PVID) & 802.1Q Encapsulation
│   ├── Eth-Trunk Aggregation in Manual & Static LACP Mode
│   ├── Voice VLAN (OUI-Based & LLDP-MED Policy)
│   └── Layer 2 Defense: Port Security & DHCP Snooping
│
├── Module 2: IPv4 & IPv6 Addressing & Static Routing (12 Labs)
│   ├── Dual-Stack IPv4/IPv6 Interface Configuration
│   ├── Static Routes, Default Routes & Summary Routes
│   ├── Floating Static Routes (Preference-based Failover)
│   ├── Equal-Cost Multi-Path (ECMP) Load Balancing
│   └── Multi-Site Hierarchical WAN Address Planning
│
├── Module 3: Dynamic Routing Protocols (OSPFv2 & OSPFv3) (3 Labs)
│   ├── Single-Area & Multi-Area OSPFv2 Routing
│   ├── DR/BDR Election, Cost Metrics & Priority Tuning
│   └── OSPF Authentication & Path Optimization
│
└── Module 4: IP Infrastructure Services & Security (4 Labs)
    ├── Global & Interface DHCP Address Pools
    ├── DHCP Relay Agent Configuration
    ├── VRRP (Virtual Router Redundancy Protocol) High Availability
    └── Easy-IP Dynamic NAT & Advanced ACL Traffic Filtering
```

---

## EVE-NG Server Access
* **Web Portal:** `http://208.8.8.135/`
* **Default Login:** `admin` / `eve`
* **Lab Directory:** `/Huawei-CCNA-32-Labs/`
* **Console Access:** Click any device on the web canvas to launch in-browser HTML5 console or external Telnet.
"@

$syllabus | Out-File -FilePath "$workbooksDir\00-Master-Course-Syllabus.md" -Encoding utf8

# 2. Module 1: Layer 2 Switching
$mod1 = @"
# Module 1: Layer 2 Switching, VLANs & Link Aggregation
**Focus:** Huawei VRP Switching, 802.1Q Trunks, Eth-Trunk LACP, Voice VLANs, LLDP & L2 Security  

---

## Lab 05: LACP Static Eth-Trunk Aggregation
### Objective
Aggregate multiple physical GigabitEthernet links between two switches into a single logical Eth-Trunk interface using the standard LACP protocol.

### Topology
* **SW1** (`GE0/0/0`, `GE0/0/1`) $\longleftrightarrow$ **SW2** (`GE0/0/0`, `GE0/0/1`)

### Huawei VRP Configuration
```text
[SW1]
system-view
sysname SW1
interface Eth-Trunk 1
 mode lacp-static
 port link-type trunk
 port trunk allow-pass vlan 10 20
 quit
interface GigabitEthernet 0/0/0
 eth-trunk 1
 quit
interface GigabitEthernet 0/0/1
 eth-trunk 1
 quit

[SW2]
system-view
sysname SW2
interface Eth-Trunk 1
 mode lacp-static
 port link-type trunk
 port trunk allow-pass vlan 10 20
 quit
interface GigabitEthernet 0/0/0
 eth-trunk 1
 quit
interface GigabitEthernet 0/0/1
 eth-trunk 1
 quit
```
### Verification
```text
display eth-trunk 1
display interface Eth-Trunk 1
```

---

## Lab 07: VLAN Segmentation and 802.1Q Trunking
### Objective
Create VLANs 10, 20, and 30, assign access ports for host communication, and establish an 802.1Q trunk link between access switches.

### Huawei VRP Configuration
```text
[SW1]
system-view
sysname SW1
vlan batch 10 20 30
interface GigabitEthernet 0/0/2
 port link-type access
 port default vlan 10
 quit
interface GigabitEthernet 0/0/3
 port link-type access
 port default vlan 20
 quit
interface GigabitEthernet 0/0/0
 port link-type trunk
 port trunk allow-pass vlan 10 20 30
 quit
```

---

## Lab 27: Trunk, Native VLAN (PVID) & LACP Mode Sim
### Objective
Configure link aggregation between SW2 and SW3 where SW3 initiates LACP actively (system priority 100) and SW2 acts passively. Configure trunk links to allow VLAN 10 and forward untagged traffic over native VLAN 11 (PVID 11).

### Huawei VRP Configuration
```text
[SW2 - Passive Role]
system-view
sysname SW2
vlan batch 10 11
interface Eth-Trunk 23
 mode lacp-static
 port link-type trunk
 port trunk allow-pass vlan 10
 port trunk pvid vlan 11
 quit
interface range GigabitEthernet 0/0/0 to GigabitEthernet 0/0/1
 eth-trunk 23
 quit

[SW3 - Active Initiator]
system-view
sysname SW3
lacp priority 100
vlan batch 10 11
interface Eth-Trunk 23
 mode lacp-static
 port link-type trunk
 port trunk allow-pass vlan 10
 port trunk pvid vlan 11
 quit
interface range GigabitEthernet 0/0/0 to GigabitEthernet 0/0/1
 eth-trunk 23
 quit
```
### Verification
```text
display eth-trunk 23
display port vlan
```
"@

$mod1 | Out-File -FilePath "$workbooksDir\01-Module-1-Layer2-Switching.md" -Encoding utf8

# 3. Module 2: IPv4 & IPv6 Static Routing
$mod2 = @"
# Module 2: IPv4 & IPv6 Static & Default Routing
**Focus:** Dual-stack interface configuration, Static routes, Floating routes, ECMP & VLSM on Huawei VRP  

---

## Lab 03: IPv4 Static & Default Routing
### Objective
Configure static routing across three routers (R1, R2, R3) to enable end-to-end communication between loopback networks.

### Topology
* **R1** (`10.1.12.1/24`) $\longleftrightarrow$ **R2** (`10.1.12.2/24` & `10.1.23.2/24`) $\longleftrightarrow$ **R3** (`10.1.23.3/24`)

### Huawei VRP Configuration
```text
[R1]
system-view
sysname R1
interface LoopBack 0
 ip address 192.168.1.1 255.255.255.0
 quit
interface GigabitEthernet 0/0/0
 ip address 10.1.12.1 255.255.255.0
 undo shutdown
 quit
ip route-static 0.0.0.0 0.0.0.0 10.1.12.2

[R2]
system-view
sysname R2
interface GigabitEthernet 0/0/0
 ip address 10.1.12.2 255.255.255.0
 undo shutdown
 quit
interface GigabitEthernet 0/0/1
 ip address 10.1.23.2 255.255.255.0
 undo shutdown
 quit
ip route-static 192.168.1.0 255.255.255.0 10.1.12.1
ip route-static 192.168.3.0 255.255.255.0 10.1.23.3

[R3]
system-view
sysname R3
interface LoopBack 0
 ip address 192.168.3.1 255.255.255.0
 quit
interface GigabitEthernet 0/0/0
 ip address 10.1.23.3 255.255.255.0
 undo shutdown
 quit
ip route-static 0.0.0.0 0.0.0.0 10.1.23.2
```
### Verification
```text
display ip routing-table
ping -a 192.168.1.1 192.168.3.1
```

---

## Lab 13: Floating Static Route & Backup Path
### Objective
Deploy primary and backup static routes. The backup route must have a preference of 100 so it only appears in the routing table if the primary link goes down.

### Huawei VRP Configuration
```text
[R1]
system-view
! Primary link via Next-Hop 10.1.1.2 (Default Preference 60)
ip route-static 192.168.50.0 255.255.255.0 10.1.1.2
! Floating backup link via Next-Hop 10.2.2.2 (Preference 100)
ip route-static 192.168.50.0 255.255.255.0 10.2.2.2 preference 100
```

---

## Lab 17: IPv6 Static Routing
### Objective
Configure IPv6 global unicast addressing and static routes across dual-stack routers.

### Huawei VRP Configuration
```text
[R1]
system-view
sysname R1
ipv6
interface GigabitEthernet 0/0/0
 ipv6 enable
 ipv6 address 2001:DB8:12::1/64
 quit
ipv6 route-static 2001:DB8:3::/64 2001:DB8:12::2
```
### Verification
```text
display ipv6 routing-table
ping ipv6 2001:DB8:3::1
```
"@

$mod2 | Out-File -FilePath "$workbooksDir\02-Module-2-IPv4-and-IPv6-Routing.md" -Encoding utf8

# 4. Module 3: Dynamic Routing (OSPF)
$mod3 = @"
# Module 3: Dynamic Routing Protocols (OSPFv2 & OSPFv3)
**Focus:** OSPF Single-Area, Multi-Area, DR/BDR Election, Cost Tuning & Authentication on Huawei VRP  

---

## Lab 04: OSPFv2 Single-Area and Multi-Area Configuration
### Objective
Configure OSPF process 1 across routers R1, R2, and R3. Establish Area 0 on core backbone links and Area 1 for branch subnets.

### Topology
* **R1** (Area 1 & Area 0 ABR) $\longleftrightarrow$ **R2** (Backbone Area 0) $\longleftrightarrow$ **R3** (Area 0)

### Huawei VRP Configuration
```text
[R1]
system-view
sysname R1
router id 1.1.1.1
ospf 1 router-id 1.1.1.1
 area 0.0.0.0
  network 10.1.12.0 0.0.0.255
 quit
 area 0.0.0.1
  network 192.168.1.0 0.0.0.255
 quit
quit

[R2]
system-view
sysname R2
router id 2.2.2.2
ospf 1 router-id 2.2.2.2
 area 0.0.0.0
  network 10.1.12.0 0.0.0.255
  network 10.1.23.0 0.0.0.255
 quit
quit

[R3]
system-view
sysname R3
router id 3.3.3.3
ospf 1 router-id 3.3.3.3
 area 0.0.0.0
  network 10.1.23.0 0.0.0.255
  network 192.168.3.0 0.0.0.255
 quit
quit
```
### Verification
```text
display ospf peer brief
display ospf routing
display ip routing-table protocol ospf
```
"@

$mod3 | Out-File -FilePath "$workbooksDir\03-Module-3-OSPF-Routing.md" -Encoding utf8

# 5. Module 4: IP Services & Security
$mod4 = @"
# Module 4: IP Infrastructure Services & Security
**Focus:** DHCP Pools, DHCP Relay, Easy-IP NAT, VRRP High Availability & Advanced ACLs  

---

## Lab 01: IP Services - DHCP Server & Easy-IP NAT
### Objective
Configure R1 as a DHCP server delivering IP addresses to LAN clients, and configure Easy-IP NAT on the WAN interface to allow internal users to access simulated internet addresses.

### Huawei VRP Configuration
```text
[R1 - DHCP & NAT Gateway]
system-view
sysname R1
dhcp enable

! 1. Global DHCP Pool Configuration
ip pool LAN_POOL
 network 192.168.10.0 mask 255.255.255.0
 gateway-list 192.168.10.1
 dns-list 8.8.8.8 1.1.1.1
 lease day 3
 quit

interface GigabitEthernet 0/0/1
 ip address 192.168.10.1 255.255.255.0
 dhcp select global
 quit

! 2. Easy-IP Dynamic NAT
acl number 2000
 rule 5 permit source 192.168.10.0 0.0.0.255
 quit

interface GigabitEthernet 0/0/0
 ip address 203.0.113.2 255.255.255.0
 nat outbound 2000
 quit
```
### Verification
```text
display ip pool name LAN_POOL used
display nat outbound
display nat session all
```

---

## Lab 02: Gateway Redundancy via VRRP
### Objective
Configure VRRP Virtual Router Redundancy Protocol between GW1 (Master) and GW2 (Backup) to provide a virtual gateway IP `192.168.1.254` for LAN users.

### Huawei VRP Configuration
```text
[GW1 - Master Router]
system-view
sysname GW1
interface GigabitEthernet 0/0/1
 ip address 192.168.1.1 255.255.255.0
 vrrp vrid 1 virtual-ip 192.168.1.254
 vrrp vrid 1 priority 120
 vrrp vrid 1 preempt-mode timer delay 20
 quit

[GW2 - Backup Router]
system-view
sysname GW2
interface GigabitEthernet 0/0/1
 ip address 192.168.1.2 255.255.255.0
 vrrp vrid 1 virtual-ip 192.168.1.254
 vrrp vrid 1 priority 100
 quit
```
### Verification
```text
display vrrp brief
display vrrp
```
"@

$mod4 | Out-File -FilePath "$workbooksDir\04-Module-4-IP-Services-Security.md" -Encoding utf8

Write-Output "Successfully generated all 5 student workbooks in $workbooksDir."
