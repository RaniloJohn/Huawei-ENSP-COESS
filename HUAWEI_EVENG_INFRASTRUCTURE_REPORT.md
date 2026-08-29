# Infrastructure Audit & Huawei EVE-NG Migration Report

**Date:** August 29, 2026  
**Target Environment:** VMware Workstation / ESXi  
**Scope:** Network Lab Infrastructure Audit, Huawei Virtual Appliance Deployment, and CCNA-to-Huawei Lab Blueprint  

---

## 1. Executive Summary

This report documents the architectural audit of existing Cisco IOU-Web lab virtual machines (`208.8.8.129` and `208.8.8.159`), the installation and configuration of Huawei virtual routing appliances (**AR1000v** and **NE40E**) on the EVE-NG platform, device cleanups, and network reconfiguration of the EVE-NG server from `208.8.8.131` to `208.8.8.135`.

---

## 2. Source Environments Audit

### A. Cisco IOU-Web Server (`http://208.8.8.129/`)
* **Operating System / Stack:** Linux / Apache 2.2 / PHP 5.3.3
* **Application Platform:** `iou-web-1.2.2-23`
* **Underlying Emulation Engine:** Cisco IOU (IOS on UNIX / Cisco IOL - IOS on Linux) 32-bit ELF user-space binaries
* **Interconnect Mechanism:** Linux domain sockets / `NETMAP` point-to-point virtual wiring
* **Console Access:** HTML image maps with direct Telnet port redirects (`telnet://208.8.8.129:2001-2016`)
* **Loaded Topologies:**
  1. `00 RSTvX`: RouteSwitchTshoot Hayup Lab (Multi-protocol enterprise mesh)
  2. `01 MPLSCloud`: MPLS, VRF, and mBGP Lab
  3. `02 WAN`: MultiSite Enterprise Lab
  4. `03 Tier Architecture`: Enterprise Campus Lab
  5. `04 NetAuto`: Python, Ansible, and EEM Lab
  6. `05 InfraNet`: CCIE InterNetwork

### B. Cisco CCNA Practice Lab Server (`http://208.8.8.159/`)
* **Application Platform:** `iou-web-1.2.2-23`
* **Lab Library:** 32 modular simulation scenarios covering fundamental to advanced routing & switching:
  * **Switching:** VLAN segmentation, 802.1Q encapsulation, Native VLAN (PVID), LACP EtherChannels, Voice VLANs.
  * **IP Addressing & Routing:** IPv4 & IPv6 assignment, Static & floating routes, Subnetting.
  * **Inter-VLAN & Dynamic Routing:** Sub-interfaces (Router-on-a-stick), OSPF single/multi-area.
* **Pedagogical Structure:** Each lab contains a dedicated topology visual, port connection table, task objectives, and structured solution syntax.

---

## 3. Operations Log on EVE-NG Server

### Phase 1: Huawei NE40E Image Deployment
1. **Source Assets (`E:\huaweine40-ne40`):**
   * Disk Image: `hda.qcow2` (~549 MB)
   * Template: `huaweine40.yml`
2. **Transfer & Installation on EVE-NG:**
   * Created destination directory: `/opt/unetlab/addons/qemu/huaweine40-ne40/`
   * Uploaded `hda.qcow2` to `/opt/unetlab/addons/qemu/huaweine40-ne40/hda.qcow2`
   * Installed template configurations across EVE-NG template directories:
     * `/opt/unetlab/html/templates/huaweine40.yml`
     * `/opt/unetlab/html/templates/intel/huaweine40.yml`
     * `/opt/unetlab/html/templates/amd/huaweine40.yml`
   * Repaired filesystem permissions:
     ```bash
     /opt/unetlab/wrappers/unl_wrapper -a fixpermissions
     ```

### Phase 2: Removal of Cisco & FortiGate Images
To streamline the environment and reclaim storage, non-Huawei vendor appliances were purged:
* **FortiGate QEMU Appliances Purged:**
  * `/opt/unetlab/addons/qemu/fortinet-FAZ-v7.2.0-build1124`
  * `/opt/unetlab/addons/qemu/fortinet-FAZ-v7.2.1-build1215`
  * `/opt/unetlab/addons/qemu/fortinet-FGT-v7.0.9-build0444`
  * `/opt/unetlab/addons/qemu/fortinet-FMG-v7.2.0-build1124`
* **Cisco Binaries Purged:**
  * Purged all Cisco IOL binaries (`.bin`) from `/opt/unetlab/addons/iol/bin/`
  * Purged all Cisco Dynamips IOS images (`.image`) from `/opt/unetlab/addons/dynamips/`
* **Storage Optimization:** Disk utilization decreased from **74% down to 53%** (Available space increased to **13 GB free**).

### Phase 3: Network Configuration Migration (`208.8.8.131` &rarr; `208.8.8.135`)
* Reconfigured `/etc/network/interfaces` from DHCP to a persistent static binding on `pnet0`:
  ```text
  # The primary network interface
  iface eth0 inet manual
  auto pnet0
  iface pnet0 inet static
      address 208.8.8.135
      netmask 255.255.255.0
      gateway 208.8.8.2
      dns-nameservers 8.8.8.8 1.1.1.1
      pre-up ip link set dev eth0 up
      bridge_hw eth0
      bridge_ports eth0
      bridge_stp off
  ```
* Rebooted the VM to apply network stack changes.
* **Post-Migration Verification:**
  * **ARP Confirmation:** `208.8.8.135` bound to physical MAC `00:0c:29:8e:fa:a1`
  * **HTTP Web Interface:** `http://208.8.8.135/` &rarr; HTTP 200 OK (EVE-NG v6.2.0-4)
  * **SSH Daemon:** `208.8.8.135:22` &rarr; Operational (TCP Test Succeeded)
  * **REST API Authentication:** Authenticated with status code `200 Success`

---

## 4. Current EVE-NG Inventory

| Device Type | Model / Version | QEMU Image Path | Template | Recommended Specs |
| :--- | :--- | :--- | :--- | :--- |
| **Enterprise Router** | Huawei AR1000v (v5.170) | `/opt/unetlab/addons/qemu/huaweiar1k-5.170` | `huaweiar1k` | 2 vCPU, 4096 MB RAM, 6 GE Ports |
| **Edge / Core Router** | Huawei NE40E | `/opt/unetlab/addons/qemu/huaweine40-ne40` | `huaweine40` | 2 vCPU, 2048 MB RAM, 12 GE Ports |
| **Linux Client** | Slax Linux 9.11.0 | `/opt/unetlab/addons/qemu/linux-slax-9.11.0` | `linux` | 1 vCPU, 512 MB RAM |

---

## 5. Cisco IOS to Huawei VRP Command Translation Guide

Use this cheat sheet to translate existing CCNA labs into Huawei VRP configuration syntax:

| Feature / Objective | Cisco IOS Command | Huawei VRP Command |
| :--- | :--- | :--- |
| **System Configuration Mode** | `enable` &rarr; `configure terminal` | `system-view` (or `sys`) |
| **Exit Mode / Return to User** | `exit` / `end` | `quit` / `return` |
| **Save Configuration** | `write memory` / `copy run start` | `save` |
| **View Active Configuration** | `show running-config` | `display current-configuration` |
| **Interface Status** | `show ip interface brief` | `display ip interface brief` |
| **Routing Table** | `show ip route` | `display ip routing-table` |
| **Create VLAN** | `vlan 10` &rarr; `name Management` | `vlan 10` &rarr; `description Management` |
| **Access Port Assignment** | `switchport mode access`<br>`switchport access vlan 10` | `port link-type access`<br>`port default vlan 10` |
| **Trunk Port Configuration** | `switchport mode trunk`<br>`switchport trunk allowed vlan 10,20` | `port link-type trunk`<br>`port trunk allow-pass vlan 10 20` |
| **Native VLAN (PVID)** | `switchport trunk native vlan 11` | `port trunk pvid vlan 11` |
| **Link Aggregation (LACP)** | `interface range e0/2-3`<br>`channel-group 23 mode active` | `interface Eth-Trunk 23`<br>`mode lacp-static`<br>`interface GigabitEthernet 0/0/2`<br>`eth-trunk 23` |
| **Static Routing** | `ip route 192.168.2.0 255.255.255.0 10.1.1.2` | `ip route-static 192.168.2.0 24 10.1.1.2` |
| **Router-on-a-Stick** | `int g0/0.10`<br>`encapsulation dot1Q 10`<br>`ip address 192.168.10.1 255.255.255.0` | `interface GigabitEthernet 0/0/0.10`<br>`dot1q termination vid 10`<br>`ip address 192.168.10.1 24`<br>`arp broadcast enable` *(Required)* |
| **OSPF Routing** | `router ospf 1`<br>`network 10.1.1.0 0.0.0.3 area 0` | `ospf 1 router-id 1.1.1.1`<br>`area 0`<br>`network 10.1.1.0 0.0.0.3` |

---

## 6. Blueprint for Huawei Labs on EVE-NG

To replicate the 32 CCNA labs, organize them into structured curriculum folders within EVE-NG:

### Track 1: Switching & Link Layer Protocols
* **Lab 01:** VLAN Creation, Access, Trunk & Hybrid Port Modes
* **Lab 02:** Port PVID (Native VLAN) & Voice VLAN Tagging
* **Lab 03:** Eth-Trunk Aggregation (Manual vs. LACP-Static Mode)
* **Lab 04:** Spanning Tree Protocols (STP, RSTP, and MSTP on VRP)

### Track 2: IPv4 & IPv6 Network Routing
* **Lab 05:** Dual-Stack IPv4/IPv6 Interface Configuration on AR1000v & NE40E
* **Lab 06:** Static Routes, Summary Routes, and Floating Default Routes
* **Lab 07:** Inter-VLAN Routing via Sub-interfaces (`dot1q termination`) and `VLANIF` (Layer 3 Switch)

### Track 3: Dynamic Routing Protocols
* **Lab 08:** Single-Area & Multi-Area OSPFv2 Configuration
* **Lab 09:** OSPF DR/BDR Election, Cost Tuning & MD5/Keychain Authentication
* **Lab 10:** OSPFv3 for IPv6 Routing & BGP Peering on NE40E

### Track 4: Network Services & Device Hardening
* **Lab 11:** DHCP Server (Global & Interface Pools) and DHCP Relay
* **Lab 12:** Basic ACLs (2000–2999) & Advanced ACLs (3000–3999)
* **Lab 13:** Network Address Translation (Easy-IP & NAT Server for Port Redirection)
* **Lab 14:** AAA Authentication, Local Users, and STelnet (SSH) Access

---

## 7. Access Information

* **EVE-NG Web Portal:** `http://208.8.8.135/`
* **Default Web Credentials:**
  * **Username:** `admin`
  * **Password:** `eve`
* **SSH Server Access:**
  * **Host:** `208.8.8.135`
  * **Port:** `22`
  * **User:** `root`
  * **Password:** `eve`
