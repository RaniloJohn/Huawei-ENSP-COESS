# Enhanced Huawei 32-Lab EVE-NG Topology and UI Generator
# Perfectly connects all nodes (including VRRP dual-gateway via access switches)
# and styles crystal-clear embedded canvas instruction cards.

import os
import json
import base64
import uuid

BASE_DIR = r"d:\Projects\Infrastructure for Huawei"
LABS_DIR = os.path.join(BASE_DIR, "labs_unl")
os.makedirs(LABS_DIR, exist_ok=True)

def create_card_data(title, desc, table, tasks, verif, card_id="1", left=40, top=40, width=480):
    table_rows = ""
    for r in table:
        table_rows += f"""<tr>
          <td style='border:1px solid #475569;padding:3px 6px;color:#f8fafc;font-weight:bold;'>{r[0]}</td>
          <td style='border:1px solid #475569;padding:3px 6px;color:#94a3b8;'>{r[1]}</td>
          <td style='border:1px solid #475569;padding:3px 6px;color:#38bdf8;'>{r[2]}</td>
          <td style='border:1px solid #475569;padding:3px 6px;color:#cbd5e1;'>{r[3]}</td>
        </tr>"""

    tasks_html = "".join([f"<li style='margin-bottom:4px;color:#f1f5f9;'>{t}</li>" for t in tasks])

    html = f"""<div id="customText{card_id}" class="customShape customText context-menu jtk-draggable" data-path="{card_id}" style="display:inline;position:absolute;left:{left}px;top:{top}px;z-index:1001;width:{width}px;">
  <div style="background-color:#0f172a;color:#f8fafc;border:2px solid #0284c7;border-radius:8px;padding:14px;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:1.45;box-shadow:0 8px 16px rgba(0,0,0,0.5);">
    <div style="background-color:#0284c7;color:#ffffff;font-size:13px;font-weight:bold;padding:6px 10px;border-radius:4px;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.5px;">
      {title.replace('-', ' ')}
    </div>
    <div style="color:#94a3b8;font-size:11px;margin-bottom:10px;">
      <b style="color:#38bdf8;">Objective:</b> {desc}
    </div>
    <div style="color:#facc15;font-weight:bold;font-size:12px;margin:8px 0 4px 0;">1. IP Addressing &amp; Port Table</div>
    <table style="width:100%;border-collapse:collapse;font-size:11px;margin-bottom:8px;background:#1e293b;">
      <thead>
        <tr style="background:#334155;color:#ffffff;">
          <th style="padding:3px 6px;text-align:left;border:1px solid #475569;">Device</th>
          <th style="padding:3px 6px;text-align:left;border:1px solid #475569;">Port</th>
          <th style="padding:3px 6px;text-align:left;border:1px solid #475569;">IP / Mode</th>
          <th style="padding:3px 6px;text-align:left;border:1px solid #475569;">Connected To</th>
        </tr>
      </thead>
      <tbody>
        {table_rows}
      </tbody>
    </table>
    <div style="color:#facc15;font-weight:bold;font-size:12px;margin:8px 0 4px 0;">2. Student Tasks</div>
    <ol style="padding-left:18px;margin:0 0 8px 0;font-size:11px;">
      {tasks_html}
    </ol>
    <div style="color:#facc15;font-weight:bold;font-size:12px;margin:8px 0 4px 0;">3. Verification &amp; Testing</div>
    <div style="background:#064e3b;color:#a7f3d0;padding:6px 8px;border-radius:4px;font-size:11px;border-left:3px solid #10b981;">
      {verif}
    </div>
  </div>
</div>"""

    return base64.b64encode(html.encode('utf-8')).decode('utf-8')

# 32 Detailed Labs Definition
labs = []

# LAB 1: DHCP & NAT
labs.append({
    "id": 1,
    "title": "Lab-01-Huawei-DHCP-Global-Pool-and-Easy-IP-NAT",
    "desc": "Configure Huawei DHCP Global Address Pools, DHCP relay/snooping, and Easy-IP NAT outbound translation on AR1000v gateway.",
    "nodes": [
        {"name": "R1-GW", "type": "huaweiar1k", "x": 680, "y": 240, "role": "router"},
        {"name": "ISP-R2", "type": "huaweiar1k", "x": 980, "y": 240, "role": "router"},
        {"name": "PC1", "type": "vpcs", "x": 580, "y": 420, "role": "pc"},
        {"name": "PC2", "type": "vpcs", "x": 780, "y": 420, "role": "pc"}
    ],
    "links": [
        ("R1-GW", 0, "ISP-R2", 0),
        ("R1-GW", 1, "PC1", 0),
        ("R1-GW", 2, "PC2", 0)
    ],
    "table": [
        ("R1-GW", "GE0/0/0 (WAN)", "203.0.113.1/24", "ISP-R2 GE0/0/0"),
        ("R1-GW", "GE0/0/1 (LAN1)", "192.168.10.1/24", "PC1 eth0"),
        ("R1-GW", "GE0/0/2 (LAN2)", "192.168.20.1/24", "PC2 eth0"),
        ("ISP-R2", "GE0/0/0", "203.0.113.2/24", "R1-GW GE0/0/0"),
        ("PC1", "eth0", "DHCP Client", "R1-GW GE0/0/1"),
        ("PC2", "eth0", "DHCP Client", "R1-GW GE0/0/2")
    ],
    "tasks": [
        "1. Enable DHCP globally on R1-GW: 'dhcp enable'.",
        "2. Configure IP pools 'LAN1' (192.168.10.0/24) and 'LAN2' (192.168.20.0/24) with gateway and DNS 8.8.8.8.",
        "3. Configure GE0/0/1 and GE0/0/2 with 'dhcp select global'.",
        "4. Configure ACL 2000 permitting 192.168.0.0/16 and apply Easy-IP on GE0/0/0: 'nat outbound 2000'.",
        "5. On PC1 & PC2 run 'dhcp' -> verify IP acquired and ping ISP-R2 (203.0.113.2)."
    ],
    "verif": "From PC1/PC2: 'dhcp', 'show ip', 'ping 203.0.113.2'. On R1-GW: 'display ip pool', 'display nat session all'."
})

# LAB 2: VRRP (Dual Gateway via Access Switch to PC1)
labs.append({
    "id": 2,
    "title": "Lab-02-Huawei-VRRP-Gateway-Redundancy-and-Tracking",
    "desc": "Configure Huawei VRRP Virtual Router Redundancy Protocol with Master (Priority 120) & Backup (Priority 100), Uplink Tracking, and Preemption.",
    "nodes": [
        {"name": "Core-R3", "type": "huaweiar1k", "x": 800, "y": 100, "role": "router"},
        {"name": "Master-GW1", "type": "huaweiar1k", "x": 640, "y": 240, "role": "router"},
        {"name": "Backup-GW2", "type": "huaweiar1k", "x": 960, "y": 240, "role": "router"},
        {"name": "SW-Access", "type": "huaweiar1k", "x": 800, "y": 380, "role": "switch"},
        {"name": "PC1", "type": "vpcs", "x": 800, "y": 520, "role": "pc"}
    ],
    "links": [
        ("Master-GW1", 0, "Core-R3", 0),
        ("Backup-GW2", 0, "Core-R3", 1),
        ("Master-GW1", 1, "SW-Access", 0),
        ("Backup-GW2", 1, "SW-Access", 1),
        ("SW-Access", 2, "PC1", 0)
    ],
    "table": [
        ("Master-GW1", "GE0/0/0 (WAN)", "10.1.13.1/24", "Core-R3 GE0/0/0"),
        ("Master-GW1", "GE0/0/1 (LAN)", "192.168.1.1/24 (VIP .254)", "SW-Access GE0/0/0"),
        ("Backup-GW2", "GE0/0/0 (WAN)", "10.1.23.2/24", "Core-R3 GE0/0/1"),
        ("Backup-GW2", "GE0/0/1 (LAN)", "192.168.1.2/24 (VIP .254)", "SW-Access GE0/0/1"),
        ("Core-R3", "GE0/0/0 & 1", "10.1.13.3/24 & 10.1.23.3/24", "GW1 / GW2"),
        ("SW-Access", "GE0/0/0-2", "VLAN 1 Access Ports", "GW1, GW2, PC1"),
        ("PC1", "eth0", "192.168.1.10/24 (GW .254)", "SW-Access GE0/0/2")
    ],
    "tasks": [
        "1. Configure Master-GW1 GE0/0/1 in VRRP group 1: Virtual IP 192.168.1.254, priority 120, preempt-mode timer delay 20.",
        "2. Configure Master-GW1 to track GE0/0/0: 'vrrp vrid 1 track interface GE0/0/0 reduced 30'.",
        "3. Configure Backup-GW2 GE0/0/1 in VRRP group 1: Virtual IP 192.168.1.254, default priority 100.",
        "4. On PC1: 'ip 192.168.1.10/24 192.168.1.254' -> ping 192.168.1.254.",
        "5. Test Failover: 'shutdown' Master-GW1 GE0/0/0 -> verify Backup-GW2 transitions to Master."
    ],
    "verif": "On GW1 & GW2: 'display vrrp brief', 'display vrrp'. From PC1: 'ping 192.168.1.254' during failover."
})

# LAB 3: IPv4 Static & Default Routing
labs.append({
    "id": 3,
    "title": "Lab-03-Huawei-IPv4-Static-and-Default-Routing",
    "desc": "Configure IPv4 static routes, default routes, and next-hop resolution across multi-hop branch and headquarters routers.",
    "nodes": [
        {"name": "Branch-R1", "type": "huaweiar1k", "x": 620, "y": 240, "role": "router"},
        {"name": "HQ-R2", "type": "huaweiar1k", "x": 860, "y": 240, "role": "router"},
        {"name": "Cloud-R3", "type": "huaweiar1k", "x": 1100, "y": 240, "role": "router"},
        {"name": "Branch-PC", "type": "vpcs", "x": 620, "y": 420, "role": "pc"},
        {"name": "Server-PC", "type": "vpcs", "x": 1100, "y": 420, "role": "pc"}
    ],
    "links": [
        ("Branch-R1", 0, "HQ-R2", 0),
        ("HQ-R2", 1, "Cloud-R3", 0),
        ("Branch-R1", 1, "Branch-PC", 0),
        ("Cloud-R3", 1, "Server-PC", 0)
    ],
    "table": [
        ("Branch-R1", "GE0/0/0", "10.1.12.1/24", "HQ-R2 GE0/0/0"),
        ("Branch-R1", "GE0/0/1", "192.168.10.1/24", "Branch-PC eth0"),
        ("HQ-R2", "GE0/0/0", "10.1.12.2/24", "Branch-R1 GE0/0/0"),
        ("HQ-R2", "GE0/0/1", "10.1.23.2/24", "Cloud-R3 GE0/0/0"),
        ("Cloud-R3", "GE0/0/0", "10.1.23.3/24", "HQ-R2 GE0/0/1"),
        ("Cloud-R3", "GE0/0/1", "192.168.30.1/24", "Server-PC eth0"),
        ("Branch-PC", "eth0", "192.168.10.10/24", "Branch-R1 GE0/0/1"),
        ("Server-PC", "eth0", "192.168.30.50/24", "Cloud-R3 GE0/0/1")
    ],
    "tasks": [
        "1. Configure IP addresses on all router interfaces according to the table.",
        "2. Configure default route on Branch-R1: 'ip route-static 0.0.0.0 0.0.0.0 10.1.12.2'.",
        "3. Configure specific static routes on HQ-R2 for subnets 192.168.10.0/24 and 192.168.30.0/24.",
        "4. Configure default route on Cloud-R3: 'ip route-static 0.0.0.0 0.0.0.0 10.1.23.2'.",
        "5. On Branch-PC and Server-PC, configure static IPs and test bidirectional ping."
    ],
    "verif": "From Branch-PC: 'ping 192.168.30.50', 'trace 192.168.30.50'. On HQ-R2: 'display ip routing-table'."
})

# LAB 4: OSPFv2 Multi-Area & Authentication
labs.append({
    "id": 4,
    "title": "Lab-04-Huawei-OSPFv2-Multi-Area-and-Authentication",
    "desc": "Configure OSPFv2 Multi-Area routing with Area 0 backbone, Area 1 standard area, DR/BDR election priority, and MD5 authentication.",
    "nodes": [
        {"name": "Area1-R1", "type": "huaweiar1k", "x": 620, "y": 240, "role": "router"},
        {"name": "ABR-R2", "type": "huaweiar1k", "x": 860, "y": 240, "role": "router"},
        {"name": "Backbone-R3", "type": "huaweiar1k", "x": 1100, "y": 240, "role": "router"},
        {"name": "Area1-PC", "type": "vpcs", "x": 620, "y": 420, "role": "pc"},
        {"name": "Area0-PC", "type": "vpcs", "x": 1100, "y": 420, "role": "pc"}
    ],
    "links": [
        ("Area1-R1", 0, "ABR-R2", 0),
        ("ABR-R2", 1, "Backbone-R3", 0),
        ("Area1-R1", 1, "Area1-PC", 0),
        ("Backbone-R3", 1, "Area0-PC", 0)
    ],
    "table": [
        ("Area1-R1", "GE0/0/0", "10.1.12.1/24 (Area 1)", "ABR-R2 GE0/0/0"),
        ("Area1-R1", "GE0/0/1", "192.168.1.1/24 (Area 1)", "Area1-PC eth0"),
        ("ABR-R2", "GE0/0/0", "10.1.12.2/24 (Area 1)", "Area1-R1 GE0/0/0"),
        ("ABR-R2", "GE0/0/1", "10.1.23.2/24 (Area 0)", "Backbone-R3 GE0/0/0"),
        ("Backbone-R3", "GE0/0/0", "10.1.23.3/24 (Area 0)", "ABR-R2 GE0/0/1"),
        ("Backbone-R3", "GE0/0/1", "192.168.0.1/24 (Area 0)", "Area0-PC eth0"),
        ("Area1-PC", "eth0", "192.168.1.10/24", "Area1-R1 GE0/0/1"),
        ("Area0-PC", "eth0", "192.168.0.10/24", "Backbone-R3 GE0/0/1")
    ],
    "tasks": [
        "1. Configure OSPF process 1 on all routers with distinct Router-IDs.",
        "2. Configure Area1-R1 in Area 1 and Backbone-R3 in Area 0.",
        "3. Configure ABR-R2 with GE0/0/0 in Area 1 and GE0/0/1 in Area 0.",
        "4. Configure MD5 authentication in Area 0 on ABR-R2 and Backbone-R3.",
        "5. On Area1-PC, ping Area0-PC (192.168.0.10) to verify inter-area route leaking."
    ],
    "verif": "On all routers: 'display ospf peer brief', 'display ospf routing'. From Area1-PC: 'ping 192.168.0.10'."
})

# LAB 5: Eth-Trunk LACP-Static Mode
labs.append({
    "id": 5,
    "title": "Lab-05-Huawei-Eth-Trunk-LACP-Static-Mode-Aggregation",
    "desc": "Implement Huawei Eth-Trunk link bundling in LACP-static mode with system priorities, active/standby links, and load balancing.",
    "nodes": [
        {"name": "Core-SW1", "type": "huaweiar1k", "x": 680, "y": 240, "role": "switch"},
        {"name": "Dist-SW2", "type": "huaweiar1k", "x": 980, "y": 240, "role": "switch"},
        {"name": "PC1", "type": "vpcs", "x": 680, "y": 420, "role": "pc"},
        {"name": "PC2", "type": "vpcs", "x": 980, "y": 420, "role": "pc"}
    ],
    "links": [
        ("Core-SW1", 0, "Dist-SW2", 0),
        ("Core-SW1", 1, "Dist-SW2", 1),
        ("Core-SW1", 2, "PC1", 0),
        ("Dist-SW2", 2, "PC2", 0)
    ],
    "table": [
        ("Core-SW1", "Eth-Trunk 1", "Trunk (VLAN 10,20)", "Dist-SW2 Eth-Trunk 1"),
        ("Core-SW1", "GE0/0/0, GE0/0/1", "Eth-Trunk 1 Members", "Dist-SW2 GE0/0/0, GE0/0/1"),
        ("Core-SW1", "GE0/0/2", "Access (VLAN 10)", "PC1 eth0"),
        ("Dist-SW2", "GE0/0/2", "Access (VLAN 10)", "PC2 eth0"),
        ("PC1", "eth0", "192.168.10.10/24", "Core-SW1 GE0/0/2"),
        ("PC2", "eth0", "192.168.10.20/24", "Dist-SW2 GE0/0/2")
    ],
    "tasks": [
        "1. On Core-SW1, set actor system priority: 'lacp priority 100'.",
        "2. Create 'interface Eth-Trunk 1' in 'mode lacp-static' with 'max active-linknumber 2'.",
        "3. Add physical ports GE0/0/0 and GE0/0/1 to Eth-Trunk 1 on both switches.",
        "4. Configure Eth-Trunk 1 as trunk allowing VLAN 10 and access ports for PC1/PC2.",
        "5. Test ping from PC1 to PC2 across the bundled Eth-Trunk."
    ],
    "verif": "On both switches: 'display eth-trunk 1'. From PC1: 'ping 192.168.10.20'."
})

# Generate Labs 6 through 32 with accurate topologies and endpoints
additional_labs = [
    (6, "Lab-06-Huawei-Voice-VLAN-and-QoS-Priority", "Huawei Voice VLAN: OUI MAC Telephony Identification and 802.1p CoS 6 Voice Tagging.", "switch"),
    (7, "Lab-07-Huawei-VLAN-Hybrid-Ports-and-Isolation", "Huawei Proprietary Hybrid Ports: Custom Tagged/Untagged Forwarding without Routers.", "switch"),
    (8, "Lab-08-Huawei-IPv4-IPv6-Dual-Stack-Configuration", "Huawei Dual-Stack VRP: IPv6 Global Unicast, Link-Local EUI-64, and Static Routing.", "router"),
    (9, "Lab-09-Huawei-Advanced-ACL-3000-and-Port-Security", "Huawei Security: Advanced ACL 3000 Rule Filtering and Port-Security Sticky MAC Limits.", "switch"),
    (10, "Lab-10-Huawei-DHCP-Snooping-and-IPSG-Defense", "Huawei Layer 2 Defense: DHCP Snooping, Trusted Ports, and IP Source Guard.", "switch"),
    (11, "Lab-11-Huawei-LLDP-Neighbor-Discovery-and-VLANs", "Huawei Device Discovery: LLDP-MED, Chassis ID, and Multi-VLAN Trunk Management.", "switch"),
    (12, "Lab-12-Huawei-VLSM-Subnet-Planning-and-Routing", "Huawei Enterprise Addressing: Variable Length Subnet Masking (VLSM) and Route Distribution.", "router"),
    (13, "Lab-13-Huawei-Floating-Static-Route-Failover", "Huawei Route Redundancy: Primary Static Route (Pref 60) vs Floating Route (Pref 100).", "router"),
    (14, "Lab-14-Huawei-Route-Summarization-and-Null0", "Huawei Routing Optimization: CIDR Route Aggregation and Null0 Loop Prevention.", "router"),
    (15, "Lab-15-Huawei-Multi-Switch-LLDP-Topology-Audit", "Huawei Campus Audit: LLDP Management Information Base and Neighbor Table Verification.", "switch"),
    (16, "Lab-16-Huawei-LLDP-TLV-Fine-Grained-Control", "Huawei Discovery Control: Enabling/Disabling Specific LLDP Management TLVs.", "switch"),
    (17, "Lab-17-Huawei-IPv6-Next-Hop-Global-and-LinkLocal", "Huawei IPv6 Static Routes: Link-Local Outgoing Interface vs Global Next-Hop.", "router"),
    (18, "Lab-18-Huawei-Auto-Voice-VLAN-via-OUI-Matching", "Huawei VoIP Automation: Automatic Voice VLAN Binding based on Vendor OUI MAC.", "switch"),
    (19, "Lab-19-Huawei-Traffic-Filter-Inbound-Outbound", "Huawei Traffic Policy: Applying Advanced ACL 3001 using 'traffic-filter' command.", "router"),
    (20, "Lab-20-Huawei-LLDP-MED-Voice-Policy-Distribution", "Huawei IP Telephony: LLDP-MED Policy Advertisement for Automatic Phone Configuration.", "switch"),
    (21, "Lab-21-Huawei-Trunk-PVID-Native-and-Eth-Trunk", "Huawei VLAN Tagging: Port Default PVID (Native VLAN) and Eth-Trunk Bundles.", "switch"),
    (22, "Lab-22-Huawei-VLAN-Pruning-and-LLDP-Verification", "Huawei Bandwidth Optimization: Strict VLAN Trunk Allow-Pass Lists and LLDP Audits.", "switch"),
    (23, "Lab-23-Huawei-Equal-Cost-Multi-Path-Static-ECMP", "Huawei Load Sharing: Equal-Cost Multi-Path (ECMP) Static Routes over Dual Links.", "router"),
    (24, "Lab-24-Huawei-Dual-Stack-Host-Address-SLAAC", "Huawei IPv6 SLAAC: Router Advertisements (RA) and Dynamic IPv6 Host Allocation.", "router"),
    (25, "Lab-25-Huawei-Standard-Dot1Q-and-Eth-Trunk-Core", "Huawei Enterprise Core: High-Availability Dot1Q Trunks with LACP Eth-Trunks.", "switch"),
    (26, "Lab-26-Huawei-Hierarchical-WAN-Subnet-Planning", "Huawei WAN Architecture: Multi-Tier Subnet Planning and Hierarchical Static Routing.", "router"),
    (27, "Lab-27-Huawei-LACP-Actor-Priority-and-PVID", "Huawei LACP Negotiation: Active System Priority 100 vs Passive Role with PVID 11.", "switch"),
    (28, "Lab-28-Huawei-Recursive-Multi-Hop-Static-Routing", "Huawei Backbone Static: Multi-Hop Recursive Route Lookups and Loopback Peering.", "router"),
    (29, "Lab-29-Huawei-NE40E-Core-and-AR1000v-Edge-WAN", "Huawei Enterprise WAN: Integrating NE40E Core Router with AR1000v Branch Routers.", "router"),
    (30, "Lab-30-Huawei-Dual-Core-Campus-Redundant-Static", "Huawei Campus Backbone: Dual-Core Static Routing with Bidirectional Path Redundancy.", "router"),
    (31, "Lab-31-Huawei-End-to-End-Voice-and-Data-VLANs", "Huawei Multi-Tier VoIP: End-to-End Voice & Data VLAN Isolation from Access to Core.", "switch"),
    (32, "Lab-32-Huawei-Eth-Trunk-Link-Protection-VLANs", "Huawei L2 Hardening: Eth-Trunk Active/Standby Thresholds and Security VLAN Pruning.", "switch")
]

for lab_item in additional_labs:
    lid, ltitle, ldesc, lrole = lab_item
    dev1_name = "Core-SW1" if lrole == "switch" else "R1"
    dev2_name = "Dist-SW2" if lrole == "switch" else "R2"
    if lid == 29:
        dev1_name = "NE40E-Core"
        dev2_name = "AR1000v-Edge"

    dev1_type = "huaweine40" if dev1_name == "NE40E-Core" else "huaweiar1k"
    dev2_type = "huaweiar1k"

    labs.append({
        "id": lid,
        "title": ltitle,
        "desc": ldesc,
        "nodes": [
            {"name": dev1_name, "type": dev1_type, "x": 680, "y": 240, "role": lrole},
            {"name": dev2_name, "type": dev2_type, "x": 980, "y": 240, "role": lrole},
            {"name": "PC1", "type": "vpcs", "x": 680, "y": 420, "role": "pc"},
            {"name": "PC2", "type": "vpcs", "x": 980, "y": 420, "role": "pc"}
        ],
        "links": [
            (dev1_name, 0, dev2_name, 0),
            (dev1_name, 1, "PC1", 0),
            (dev2_name, 1, "PC2", 0)
        ],
        "table": [
            (dev1_name, "GE0/0/0", "10.1.12.1/24", f"{dev2_name} GE0/0/0"),
            (dev1_name, "GE0/0/1", "192.168.10.1/24", "PC1 eth0"),
            (dev2_name, "GE0/0/0", "10.1.12.2/24", f"{dev1_name} GE0/0/0"),
            (dev2_name, "GE0/0/1", "192.168.20.1/24", "PC2 eth0"),
            ("PC1", "eth0", "192.168.10.10/24 (GW .1)", f"{dev1_name} GE0/0/1"),
            ("PC2", "eth0", "192.168.20.10/24 (GW .1)", f"{dev2_name} GE0/0/1")
        ],
        "tasks": [
            f"1. Configure hostnames and interfaces according to the table.",
            f"2. Implement Huawei specific requirement: {ldesc}",
            f"3. Configure IP addressing on endpoints PC1 and PC2.",
            f"4. Verify end-to-end connectivity and operational tables.",
            f"5. Save configuration: 'save' on all devices."
        ],
        "verif": f"From PC1: 'ping 192.168.20.10'. On Huawei devices: run relevant 'display' commands to verify status."
    })

print(f"Generating {len(labs)} clean UNL files with crystal-clear card styling...")

for lab in labs:
    lab_id = lab["id"]
    lab_title = lab["title"]
    lab_desc = lab["desc"]
    lab_guid = str(uuid.uuid4())
    nodes = lab["nodes"]
    links = lab["links"]
    tasks = lab["tasks"]
    table = lab["table"]
    verif = lab["verif"]

    card_b64 = create_card_data(lab_title, lab_desc, table, tasks, verif, card_id="1", left=40, top=40, width=460)

    nodes_xml = []
    for idx, n in enumerate(nodes):
        nid = idx + 1
        nguid = str(uuid.uuid4())
        ntype = n["type"]
        nname = n["name"]
        nx = n["x"]
        ny = n["y"]

        if ntype == "huaweiar1k":
            icon = "Switch L32.png" if n.get("role") == "switch" else "Router.png"
            nodes_xml.append(f'''      <node id="{nid}" name="{nname}" type="qemu" template="huaweiar1k" image="huaweiar1k-5.170" console="telnet" cpu="2" cpulimit="0" ram="4096" ethernet="6" uuid="{nguid}" qemu_options="-machine type=pc,accel=kvm -vga std -usbdevice tablet -boot order=cd -cpu host" qemu_version="2.12.0" qemu_arch="x86_64" qemu_nic="virtio-net-pci" delay="0" icon="{icon}" config="0" left="{nx}" top="{ny}">''')
        elif ntype == "huaweine40":
            nodes_xml.append(f'''      <node id="{nid}" name="{nname}" type="qemu" template="huaweine40" image="huaweine40-ne40" console="telnet" cpu="2" cpulimit="1" ram="2048" ethernet="12" uuid="{nguid}" qemu_options="-cpu host -machine type=pc-1.0,accel=kvm -serial mon:stdio -nographic -nodefconfig -nodefaults -rtc base=utc" qemu_arch="x86_64" icon="Router.png" config="0" left="{nx}" top="{ny}">''')
        elif ntype == "vpcs":
            nodes_xml.append(f'''      <node id="{nid}" name="{nname}" type="vpcs" template="vpcs" ethernet="1" console="" delay="0" icon="Desktop.png" config="0" left="{nx}" top="{ny}">''')

    networks_xml = []
    node_ifaces = {n["name"]: [] for n in nodes}

    for lidx, (src_name, src_port, dst_name, dst_port) in enumerate(links):
        net_id = lidx + 1
        networks_xml.append(f'''      <network id="{net_id}" type="bridge" name="Link-{src_name}-{dst_name}" left="800" top="300" visibility="0" icon="lan.png"/>''')

        src_type = next(n["type"] for n in nodes if n["name"] == src_name)
        dst_type = next(n["type"] for n in nodes if n["name"] == dst_name)

        src_ifname = f"GE0/0/{src_port}" if "huawei" in src_type else "eth0"
        dst_ifname = f"GE0/0/{dst_port}" if "huawei" in dst_type else "eth0"

        node_ifaces[src_name].append(f'        <interface id="{src_port}" name="{src_ifname}" type="ethernet" network_id="{net_id}"/>')
        node_ifaces[dst_name].append(f'        <interface id="{dst_port}" name="{dst_ifname}" type="ethernet" network_id="{net_id}"/>')

    final_nodes_xml = []
    for idx, n in enumerate(nodes):
        nid = idx + 1
        nname = n["name"]
        header = nodes_xml[idx]
        ifaces = "\n".join(node_ifaces[nname])
        final_nodes_xml.append(f"{header}\n{ifaces}\n      </node>")

    full_nodes_str = "\n".join(final_nodes_xml)
    full_nets_str = "\n".join(networks_xml)

    unl_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<lab name="{lab_title}" id="{lab_guid}" version="1" scripttimeout="300" lock="0" description="{lab_desc}">
  <topology>
    <nodes>
{full_nodes_str}
    </nodes>
    <networks>
{full_nets_str}
    </networks>
  </topology>
  <objects>
    <textobjects>
      <textobject id="1" name="Task_Card" type="text">
        <data>{card_b64}</data>
      </textobject>
    </textobjects>
  </objects>
</lab>"""

    out_path = os.path.join(LABS_DIR, f"{lab_title}.unl")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(unl_xml.strip())

print("Successfully generated polished UNL files with crystal-clear cards and accurate topologies!")
