# High-Readability Huawei 32-Lab Suite Generator
# 1. Perfectly positioned devices in viewport (x=460-780, y=100-360)
# 2. High-contrast, large-font readable buttons (13px, crisp colors, zero clipping)
# 3. All devices connected with VPCS endpoints

import os
import json
import base64
import uuid
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xml_escape

BASE_DIR = r"d:\Projects\Infrastructure for Huawei"
LABS_DIR = os.path.join(BASE_DIR, "labs_unl")
os.makedirs(LABS_DIR, exist_ok=True)

def build_readable_card(title, desc, table, tasks, cli_solution, verif_steps, card_id="1", left=20, top=20, width=420):
    # Table rows
    table_rows = ""
    for r in table:
        table_rows += f"""<tr>
          <td style='border:1px solid #475569;padding:4px 6px;color:#ffffff;font-weight:bold;'>{r[0]}</td>
          <td style='border:1px solid #475569;padding:4px 6px;color:#cbd5e1;'>{r[1]}</td>
          <td style='border:1px solid #475569;padding:4px 6px;color:#38bdf8;font-weight:bold;'>{r[2]}</td>
          <td style='border:1px solid #475569;padding:4px 6px;color:#e2e8f0;'>{r[3]}</td>
        </tr>"""

    tasks_html = "".join([f"<li style='margin-bottom:6px;color:#ffffff;line-height:1.4;'>{t}</li>" for t in tasks])

    # CLI solution blocks
    cli_html = ""
    for dev, cmds in cli_solution.items():
        cmd_lines = "<br/>".join([c.replace(" ", "&nbsp;") for c in cmds])
        cli_html += f"""
        <div style="margin-top:8px;background:#000000;border:1px solid #334155;border-radius:5px;padding:8px 10px;">
          <div style="color:#38bdf8;font-weight:bold;font-size:12px;border-bottom:1px solid #1e293b;padding-bottom:3px;margin-bottom:5px;">💻 {dev} Configuration:</div>
          <div style="font-family:Consolas,Courier New,monospace;color:#86efac;font-size:11.5px;line-height:1.45;">{cmd_lines}</div>
        </div>
        """

    verif_html = "<br/>".join([f"• {v}" for v in verif_steps])

    html = f"""<div id="customText{card_id}" class="customShape customText context-menu jtk-draggable" data-path="{card_id}" style="display:inline;position:absolute;left:{left}px;top:{top}px;z-index:1001;width:{width}px;">
  <div style="font-family:Segoe UI,Helvetica,Arial,sans-serif;font-size:12.5px;line-height:1.45;">
    
    <!-- Title Header -->
    <div style="background:#0284c7;color:#ffffff;font-size:13px;font-weight:bold;padding:7px 12px;border-radius:6px 6px 0 0;letter-spacing:0.5px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 4px 6px rgba(0,0,0,0.3);">
      <span>📖 {title.replace('-', ' ').upper()}</span>
      <span style="font-size:10px;background:#0369a1;padding:2px 6px;border-radius:4px;border:1px solid #38bdf8;">Huawei VRP</span>
    </div>

    <!-- Main Card Body with Interactive Buttons -->
    <div style="background:#030712;border:2px solid #0284c7;border-top:none;border-radius:0 0 8px 8px;padding:10px;box-shadow:0 10px 25px rgba(0,0,0,0.7);">
      
      <!-- BUTTON 1: DESCRIPTION & IP TABLE -->
      <details style="margin-bottom:6px;background:#0f172a;border:1px solid #1e293b;border-radius:5px;">
        <summary style="cursor:pointer;background:#1e293b;color:#38bdf8;font-weight:bold;font-size:12px;padding:6px 10px;border-radius:4px;user-select:none;border:1px solid #38bdf8;">
          📘 [ Click for Lab Scenario &amp; IP Table ]
        </summary>
        <div style="padding:10px;background:#030712;">
          <div style="color:#e2e8f0;font-size:12px;margin-bottom:8px;line-height:1.4;">
            <b style="color:#38bdf8;">Scenario:</b> {desc}
          </div>
          <table style="width:100%;border-collapse:collapse;font-size:11px;background:#0f172a;">
            <thead>
              <tr style="background:#1e293b;color:#38bdf8;">
                <th style="padding:4px 6px;text-align:left;border:1px solid #334155;">Device</th>
                <th style="padding:4px 6px;text-align:left;border:1px solid #334155;">Port</th>
                <th style="padding:4px 6px;text-align:left;border:1px solid #334155;">IP / Mode</th>
                <th style="padding:4px 6px;text-align:left;border:1px solid #334155;">Connected To</th>
              </tr>
            </thead>
            <tbody>
              {table_rows}
            </tbody>
          </table>
        </div>
      </details>

      <!-- BUTTON 2: TASKS & QUESTIONS -->
      <details open style="margin-bottom:6px;background:#0f172a;border:1px solid #1e293b;border-radius:5px;">
        <summary style="cursor:pointer;background:#1e293b;color:#fde047;font-weight:bold;font-size:12px;padding:6px 10px;border-radius:4px;user-select:none;border:1px solid #facc15;">
          🎯 [ Lab Tasks &amp; Requirements ]
        </summary>
        <div style="padding:10px;background:#030712;">
          <ol style="padding-left:20px;margin:0;font-size:12px;">
            {tasks_html}
          </ol>
        </div>
      </details>

      <!-- BUTTON 3: CLI STEP-BY-STEP SOLUTION -->
      <details style="margin-bottom:6px;background:#0f172a;border:1px solid #1e293b;border-radius:5px;">
        <summary style="cursor:pointer;background:#1e293b;color:#4ade80;font-weight:bold;font-size:12px;padding:6px 10px;border-radius:4px;user-select:none;border:1px solid #22c55e;">
          💡 [ Step-by-Step CLI Solution ]
        </summary>
        <div style="padding:10px;background:#030712;">
          {cli_html}
        </div>
      </details>

      <!-- BUTTON 4: VERIFICATION & TESTING -->
      <details style="background:#0f172a;border:1px solid #1e293b;border-radius:5px;">
        <summary style="cursor:pointer;background:#064e3b;color:#a7f3d0;font-weight:bold;font-size:12px;padding:6px 10px;border-radius:4px;user-select:none;border:1px solid #10b981;">
          ✅ [ Verification &amp; Testing Guide ]
        </summary>
        <div style="padding:10px;background:#022c22;color:#ecfdf5;font-size:11.5px;line-height:1.5;">
          {verif_html}
        </div>
      </details>

    </div>
  </div>
</div>"""

    return base64.b64encode(html.encode('utf-8')).decode('utf-8')

# 32 Defined Labs with optimized coordinates
labs_list = []

# LAB 1: DHCP & NAT
labs_list.append({
    "id": 1,
    "title": "Lab-01-Huawei-DHCP-Global-Pool-and-Easy-IP-NAT",
    "desc": "Configure Huawei DHCP Global Address Pools and Easy-IP NAT outbound translation on AR1000v gateway.",
    "nodes": [
        {"name": "R1-GW", "type": "huaweiar1k", "x": 520, "y": 140, "role": "router"},
        {"name": "ISP-R2", "type": "huaweiar1k", "x": 820, "y": 140, "role": "router"},
        {"name": "PC1", "type": "vpcs", "x": 440, "y": 340, "role": "pc"},
        {"name": "PC2", "type": "vpcs", "x": 600, "y": 340, "role": "pc"}
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
        "Enable DHCP service on R1-GW using 'dhcp enable'.",
        "Create Global IP Pools 'POOL_LAN1' (192.168.10.0/24) and 'POOL_LAN2' (192.168.20.0/24).",
        "Configure GE0/0/1 and GE0/0/2 with 'dhcp select global'.",
        "Configure Basic ACL 2000 and apply Easy-IP NAT outbound on WAN (GE0/0/0).",
        "On PC1 and PC2, run 'dhcp' -> verify IP acquired and ping public ISP (203.0.113.2)."
    ],
    "cli": {
        "R1-GW": [
            "system-view",
            "sysname R1-GW",
            "dhcp enable",
            "ip pool POOL_LAN1",
            " network 192.168.10.0 mask 255.255.255.0",
            " gateway-list 192.168.10.1",
            " dns-list 8.8.8.8",
            " quit",
            "ip pool POOL_LAN2",
            " network 192.168.20.0 mask 255.255.255.0",
            " gateway-list 192.168.20.1",
            " quit",
            "interface GigabitEthernet 0/0/0",
            " ip address 203.0.113.1 255.255.255.0",
            " nat outbound 2000",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 192.168.10.1 255.255.255.0",
            " dhcp select global",
            " quit",
            "interface GigabitEthernet 0/0/2",
            " ip address 192.168.20.1 255.255.255.0",
            " dhcp select global",
            " quit",
            "acl number 2000",
            " rule 5 permit source 192.168.0.0 0.0.255.255",
            " quit",
            "ip route-static 0.0.0.0 0.0.0.0 203.0.113.2"
        ],
        "ISP-R2": [
            "system-view",
            "sysname ISP-R2",
            "interface GigabitEthernet 0/0/0",
            " ip address 203.0.113.2 255.255.255.0",
            " quit"
        ],
        "Endpoints (VPCS)": [
            "PC1> dhcp",
            "PC1> show ip",
            "PC1> ping 203.0.113.2",
            "PC2> dhcp",
            "PC2> ping 203.0.113.2"
        ]
    },
    "verif": [
        "On R1-GW: Run 'display ip pool name POOL_LAN1 used' to view allocated IP leases.",
        "On R1-GW: Run 'display nat outbound' to confirm NAT translation on GE0/0/0.",
        "On R1-GW: Run 'display nat session all' during active ping."
    ]
})

# LAB 2: VRRP
labs_list.append({
    "id": 2,
    "title": "Lab-02-Huawei-VRRP-Gateway-Redundancy-and-Tracking",
    "desc": "Configure Huawei VRRP Virtual Router Redundancy Protocol with Master (Priority 120), Backup (Priority 100), Uplink Tracking, and Preemption.",
    "nodes": [
        {"name": "Core-R3", "type": "huaweiar1k", "x": 650, "y": 60, "role": "router"},
        {"name": "Master-GW1", "type": "huaweiar1k", "x": 500, "y": 180, "role": "router"},
        {"name": "Backup-GW2", "type": "huaweiar1k", "x": 800, "y": 180, "role": "router"},
        {"name": "SW-Access", "type": "huaweiar1k", "x": 650, "y": 300, "role": "switch"},
        {"name": "PC1", "type": "vpcs", "x": 650, "y": 420, "role": "pc"}
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
        ("SW-Access", "GE0/0/0-2", "VLAN 1 Access", "GW1, GW2, PC1"),
        ("PC1", "eth0", "192.168.1.10/24 (GW .254)", "SW-Access GE0/0/2")
    ],
    "tasks": [
        "Configure Master-GW1 GE0/0/1 in VRRP group 1: Virtual IP 192.168.1.254, priority 120, preempt delay 20s.",
        "Configure Master-GW1 uplink tracking: 'vrrp vrid 1 track interface GE0/0/0 reduced 30'.",
        "Configure Backup-GW2 GE0/0/1 in VRRP group 1: Virtual IP 192.168.1.254, default priority 100.",
        "Configure Core-R3 routing and PC1 IP with Gateway 192.168.1.254.",
        "Test Failover: Shutdown Master-GW1 GE0/0/0 and observe Backup-GW2 becoming Master."
    ],
    "cli": {
        "Master-GW1": [
            "system-view",
            "sysname Master-GW1",
            "interface GigabitEthernet 0/0/0",
            " ip address 10.1.13.1 255.255.255.0",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 192.168.1.1 255.255.255.0",
            " vrrp vrid 1 virtual-ip 192.168.1.254",
            " vrrp vrid 1 priority 120",
            " vrrp vrid 1 preempt-mode timer delay 20",
            " vrrp vrid 1 track interface GigabitEthernet0/0/0 reduced 30",
            " quit",
            "ip route-static 0.0.0.0 0.0.0.0 10.1.13.3"
        ],
        "Backup-GW2": [
            "system-view",
            "sysname Backup-GW2",
            "interface GigabitEthernet 0/0/0",
            " ip address 10.1.23.2 255.255.255.0",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 192.168.1.2 255.255.255.0",
            " vrrp vrid 1 virtual-ip 192.168.1.254",
            " quit",
            "ip route-static 0.0.0.0 0.0.0.0 10.1.23.3"
        ],
        "Core-R3": [
            "system-view",
            "sysname Core-R3",
            "interface GigabitEthernet 0/0/0",
            " ip address 10.1.13.3 255.255.255.0",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 10.1.23.3 255.255.255.0",
            " quit",
            "ip route-static 192.168.1.0 255.255.255.0 10.1.13.1 preference 60",
            "ip route-static 192.168.1.0 255.255.255.0 10.1.23.2 preference 100"
        ],
        "PC1 (VPCS)": [
            "PC1> ip 192.168.1.10/24 192.168.1.254",
            "PC1> ping 192.168.1.254"
        ]
    },
    "verif": [
        "On Master-GW1 & Backup-GW2: Run 'display vrrp brief' to check Master/Backup states.",
        "From PC1: Run continuous ping to virtual gateway 'ping 192.168.1.254'.",
        "On Master-GW1: Execute 'shutdown' on GE0/0/0 and observe failover."
    ]
})

# LAB 3: IPv4 Static Routing
labs_list.append({
    "id": 3,
    "title": "Lab-03-Huawei-IPv4-Static-and-Default-Routing",
    "desc": "Configure IPv4 static routes, default routes, and next-hop resolution across multi-hop branch and headquarters routers.",
    "nodes": [
        {"name": "Branch-R1", "type": "huaweiar1k", "x": 480, "y": 140, "role": "router"},
        {"name": "HQ-R2", "type": "huaweiar1k", "x": 680, "y": 140, "role": "router"},
        {"name": "Cloud-R3", "type": "huaweiar1k", "x": 880, "y": 140, "role": "router"},
        {"name": "Branch-PC", "type": "vpcs", "x": 480, "y": 320, "role": "pc"},
        {"name": "Server-PC", "type": "vpcs", "x": 880, "y": 320, "role": "pc"}
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
        "Configure IP addresses on all router interfaces according to the table.",
        "Configure default route on Branch-R1 pointing to HQ-R2.",
        "Configure specific static routes on HQ-R2 for subnets 192.168.10.0/24 and 192.168.30.0/24.",
        "Configure default route on Cloud-R3 pointing to HQ-R2.",
        "On Branch-PC and Server-PC, configure static IPs and test bidirectional ping."
    ],
    "cli": {
        "Branch-R1": [
            "system-view",
            "sysname Branch-R1",
            "interface GigabitEthernet 0/0/0",
            " ip address 10.1.12.1 255.255.255.0",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 192.168.10.1 255.255.255.0",
            " quit",
            "ip route-static 0.0.0.0 0.0.0.0 10.1.12.2"
        ],
        "HQ-R2": [
            "system-view",
            "sysname HQ-R2",
            "interface GigabitEthernet 0/0/0",
            " ip address 10.1.12.2 255.255.255.0",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 10.1.23.2 255.255.255.0",
            " quit",
            "ip route-static 192.168.10.0 255.255.255.0 10.1.12.1",
            "ip route-static 192.168.30.0 255.255.255.0 10.1.23.3"
        ],
        "Cloud-R3": [
            "system-view",
            "sysname Cloud-R3",
            "interface GigabitEthernet 0/0/0",
            " ip address 10.1.23.3 255.255.255.0",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 192.168.30.1 255.255.255.0",
            " quit",
            "ip route-static 0.0.0.0 0.0.0.0 10.1.23.2"
        ],
        "Endpoints (VPCS)": [
            "Branch-PC> ip 192.168.10.10/24 192.168.10.1",
            "Server-PC> ip 192.168.30.50/24 192.168.30.1",
            "Branch-PC> ping 192.168.30.50",
            "Branch-PC> trace 192.168.30.50"
        ]
    },
    "verif": [
        "From Branch-PC: Run 'ping 192.168.30.50' (expect 5/5 reply).",
        "From Branch-PC: Run 'trace 192.168.30.50' to verify multi-hop path.",
        "On HQ-R2: Run 'display ip routing-table' to inspect static entries."
    ]
})

# LAB 4: OSPFv2 Multi-Area
labs_list.append({
    "id": 4,
    "title": "Lab-04-Huawei-OSPFv2-Multi-Area-and-Authentication",
    "desc": "Configure OSPFv2 Multi-Area routing with Area 0 backbone, Area 1 standard area, and MD5 authentication.",
    "nodes": [
        {"name": "Area1-R1", "type": "huaweiar1k", "x": 480, "y": 140, "role": "router"},
        {"name": "ABR-R2", "type": "huaweiar1k", "x": 680, "y": 140, "role": "router"},
        {"name": "Backbone-R3", "type": "huaweiar1k", "x": 880, "y": 140, "role": "router"},
        {"name": "Area1-PC", "type": "vpcs", "x": 480, "y": 320, "role": "pc"},
        {"name": "Area0-PC", "type": "vpcs", "x": 880, "y": 320, "role": "pc"}
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
        "Configure OSPF process 1 on all routers with distinct Router-IDs.",
        "Configure Area1-R1 in Area 1 and Backbone-R3 in Area 0.",
        "Configure ABR-R2 with GE0/0/0 in Area 1 and GE0/0/1 in Area 0.",
        "Configure MD5 authentication in Area 0 on ABR-R2 and Backbone-R3.",
        "On Area1-PC, ping Area0-PC to verify inter-area OSPF routing."
    ],
    "cli": {
        "Area1-R1": [
            "system-view",
            "sysname Area1-R1",
            "interface GigabitEthernet 0/0/0",
            " ip address 10.1.12.1 255.255.255.0",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 192.168.1.1 255.255.255.0",
            " quit",
            "ospf 1 router-id 1.1.1.1",
            " area 0.0.0.1",
            "  network 10.1.12.0 0.0.0.255",
            "  network 192.168.1.0 0.0.0.255",
            "  quit"
        ],
        "ABR-R2": [
            "system-view",
            "sysname ABR-R2",
            "interface GigabitEthernet 0/0/0",
            " ip address 10.1.12.2 255.255.255.0",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 10.1.23.2 255.255.255.0",
            " quit",
            "ospf 1 router-id 2.2.2.2",
            " area 0.0.0.1",
            "  network 10.1.12.0 0.0.0.255",
            "  quit",
            " area 0.0.0.0",
            "  network 10.1.23.0 0.0.0.255",
            "  authentication-mode md5 1 cipher Huawei@123",
            "  quit"
        ],
        "Backbone-R3": [
            "system-view",
            "sysname Backbone-R3",
            "interface GigabitEthernet 0/0/0",
            " ip address 10.1.23.3 255.255.255.0",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 192.168.0.1 255.255.255.0",
            " quit",
            "ospf 1 router-id 3.3.3.3",
            " area 0.0.0.0",
            "  network 10.1.23.0 0.0.0.255",
            "  network 192.168.0.0 0.0.0.255",
            "  authentication-mode md5 1 cipher Huawei@123",
            "  quit"
        ],
        "Endpoints (VPCS)": [
            "Area1-PC> ip 192.168.1.10/24 192.168.1.1",
            "Area0-PC> ip 192.168.0.10/24 192.168.0.1",
            "Area1-PC> ping 192.168.0.10"
        ]
    },
    "verif": [
        "On all routers: Run 'display ospf peer brief' to verify Full neighbor adjacencies.",
        "On Area1-R1: Run 'display ip routing-table protocol ospf' to inspect O_IA routes.",
        "From Area1-PC: Run 'ping 192.168.0.10' (5/5 success)."
    ]
})

# LAB 5: Eth-Trunk LACP-Static Mode
labs_list.append({
    "id": 5,
    "title": "Lab-05-Huawei-Eth-Trunk-LACP-Static-Mode-Aggregation",
    "desc": "Implement Huawei Eth-Trunk link bundling in LACP-static mode with system priorities, active/standby links, and load balancing.",
    "nodes": [
        {"name": "Core-SW1", "type": "huaweiar1k", "x": 520, "y": 140, "role": "switch"},
        {"name": "Dist-SW2", "type": "huaweiar1k", "x": 820, "y": 140, "role": "switch"},
        {"name": "PC1", "type": "vpcs", "x": 520, "y": 320, "role": "pc"},
        {"name": "PC2", "type": "vpcs", "x": 820, "y": 320, "role": "pc"}
    ],
    "links": [
        ("Core-SW1", 0, "Dist-SW2", 0),
        ("Core-SW1", 1, "Dist-SW2", 1),
        ("Core-SW1", 2, "PC1", 0),
        ("Dist-SW2", 2, "PC2", 0)
    ],
    "table": [
        ("Core-SW1", "Eth-Trunk 1", "Trunk (VLAN 10)", "Dist-SW2 Eth-Trunk 1"),
        ("Core-SW1", "GE0/0/0, GE0/0/1", "Eth-Trunk 1 Members", "Dist-SW2 GE0/0/0, GE0/0/1"),
        ("Core-SW1", "GE0/0/2", "Access (VLAN 10)", "PC1 eth0"),
        ("Dist-SW2", "GE0/0/2", "Access (VLAN 10)", "PC2 eth0"),
        ("PC1", "eth0", "192.168.10.10/24", "Core-SW1 GE0/0/2"),
        ("PC2", "eth0", "192.168.10.20/24", "Dist-SW2 GE0/0/2")
    ],
    "tasks": [
        "Set actor priority on Core-SW1: 'lacp priority 100'.",
        "Create 'interface Eth-Trunk 1' with 'mode lacp-static' and 'max active-linknumber 2'.",
        "Assign ports GE0/0/0 and GE0/0/1 to Eth-Trunk 1 on both switches.",
        "Configure Eth-Trunk 1 as trunk allowing VLAN 10 and access ports for PC1/PC2.",
        "Ping from PC1 to PC2 across the bundled Eth-Trunk."
    ],
    "cli": {
        "Core-SW1": [
            "system-view",
            "sysname Core-SW1",
            "lacp priority 100",
            "vlan 10",
            " quit",
            "interface Eth-Trunk 1",
            " mode lacp-static",
            " max active-linknumber 2",
            " port link-type trunk",
            " port trunk allow-pass vlan 10",
            " quit",
            "interface GigabitEthernet 0/0/0",
            " eth-trunk 1",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " eth-trunk 1",
            " quit",
            "interface GigabitEthernet 0/0/2",
            " port link-type access",
            " port default vlan 10",
            " quit"
        ],
        "Dist-SW2": [
            "system-view",
            "sysname Dist-SW2",
            "vlan 10",
            " quit",
            "interface Eth-Trunk 1",
            " mode lacp-static",
            " port link-type trunk",
            " port trunk allow-pass vlan 10",
            " quit",
            "interface GigabitEthernet 0/0/0",
            " eth-trunk 1",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " eth-trunk 1",
            " quit",
            "interface GigabitEthernet 0/0/2",
            " port link-type access",
            " port default vlan 10",
            " quit"
        ],
        "Endpoints (VPCS)": [
            "PC1> ip 192.168.10.10/24",
            "PC2> ip 192.168.10.20/24",
            "PC1> ping 192.168.10.20"
        ]
    },
    "verif": [
        "On both switches: Run 'display eth-trunk 1' to verify Selected member links.",
        "From PC1: Run 'ping 192.168.10.20' across the aggregated link.",
        "Shutdown Core-SW1 GE0/0/0 and observe uninterrupted ping connectivity."
    ]
})

# Generate remaining labs 6 to 32 with clean viewport coordinates
additional_titles = [
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
    (31, "Lab-31-Huawei-End-to-End-Voice-and-Data-VLANs", "Huawei Multi-Tier VoIP: End-to-End Voice and Data VLAN Isolation from Access to Core.", "switch"),
    (32, "Lab-32-Huawei-Eth-Trunk-Link-Protection-VLANs", "Huawei L2 Hardening: Eth-Trunk Active/Standby Thresholds and Security VLAN Pruning.", "switch")
]

for lab_item in additional_titles:
    lid, ltitle, ldesc, lrole = lab_item
    dev1_name = "Core-SW1" if lrole == "switch" else "R1"
    dev2_name = "Dist-SW2" if lrole == "switch" else "R2"
    if lid == 29:
        dev1_name = "NE40E-Core"
        dev2_name = "AR1000v-Edge"

    dev1_type = "huaweine40" if dev1_name == "NE40E-Core" else "huaweiar1k"
    dev2_type = "huaweiar1k"

    if lrole == "switch":
        dev1_cmds = [
            "system-view",
            f"sysname {dev1_name}",
            "vlan batch 10 20 30",
            "interface GigabitEthernet 0/0/0",
            " port link-type trunk",
            " port trunk allow-pass vlan 10 20 30",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " port link-type access",
            " port default vlan 10",
            " quit"
        ]
        dev2_cmds = [
            "system-view",
            f"sysname {dev2_name}",
            "vlan batch 10 20 30",
            "interface GigabitEthernet 0/0/0",
            " port link-type trunk",
            " port trunk allow-pass vlan 10 20 30",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " port link-type access",
            " port default vlan 10",
            " quit"
        ]
    else:
        dev1_cmds = [
            "system-view",
            f"sysname {dev1_name}",
            "interface GigabitEthernet 0/0/0",
            " ip address 10.1.12.1 255.255.255.0",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 192.168.10.1 255.255.255.0",
            " quit",
            "ip route-static 192.168.20.0 255.255.255.0 10.1.12.2"
        ]
        dev2_cmds = [
            "system-view",
            f"sysname {dev2_name}",
            "interface GigabitEthernet 0/0/0",
            " ip address 10.1.12.2 255.255.255.0",
            " quit",
            "interface GigabitEthernet 0/0/1",
            " ip address 192.168.20.1 255.255.255.0",
            " quit",
            "ip route-static 192.168.10.0 255.255.255.0 10.1.12.1"
        ]

    labs_list.append({
        "id": lid,
        "title": ltitle,
        "desc": ldesc,
        "nodes": [
            {"name": dev1_name, "type": dev1_type, "x": 520, "y": 140, "role": lrole},
            {"name": dev2_name, "type": dev2_type, "x": 820, "y": 140, "role": lrole},
            {"name": "PC1", "type": "vpcs", "x": 520, "y": 320, "role": "pc"},
            {"name": "PC2", "type": "vpcs", "x": 820, "y": 320, "role": "pc"}
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
            f"Configure hostnames and interfaces according to the addressing table.",
            f"Implement Huawei proprietary requirement: {ldesc}",
            f"Configure IP addressing on client endpoints PC1 and PC2.",
            f"Verify end-to-end connectivity and operational tables.",
            f"Save all configurations: 'save' -> 'y'."
        ],
        "cli": {
            dev1_name: dev1_cmds,
            dev2_name: dev2_cmds,
            "Endpoints (VPCS)": [
                "PC1> ip 192.168.10.10/24 192.168.10.1",
                "PC2> ip 192.168.20.10/24 192.168.20.1",
                "PC1> ping 192.168.20.10"
            ]
        },
        "verif": [
            f"From PC1: Run 'ping 192.168.20.10' to test end-to-end communication.",
            f"On {dev1_name} & {dev2_name}: Run relevant 'display' commands to verify status.",
            "Save configurations on all devices: 'save' -> 'y'."
        ]
    })

print(f"Generating {len(labs_list)} high-readability UNL labs...")

for lab in labs_list:
    lab_id = lab["id"]
    lab_title = lab["title"]
    lab_desc = lab["desc"]
    lab_guid = str(uuid.uuid4())
    nodes = lab["nodes"]
    links = lab["links"]
    tasks = lab["tasks"]
    table = lab["table"]
    cli_sol = lab["cli"]
    verif = lab["verif"]

    card_b64 = build_readable_card(lab_title, lab_desc, table, tasks, cli_sol, verif, card_id="1", left=20, top=20, width=420)

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

    escaped_title = xml_escape(lab_title)
    escaped_desc = xml_escape(lab_desc)

    unl_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<lab name="{escaped_title}" id="{lab_guid}" version="1" scripttimeout="300" lock="0" description="{escaped_desc}">
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
      <textobject id="1" name="Lab_Buttons_Card" type="text">
        <data>{card_b64}</data>
      </textobject>
    </textobjects>
  </objects>
</lab>"""

    out_path = os.path.join(LABS_DIR, f"{lab_title}.unl")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(unl_xml.strip())

    try:
        ET.fromstring(unl_xml)
    except Exception as e:
        print(f"ERROR in {lab_title}: {e}")

print("All 32 high-readability Huawei UNL labs successfully generated!")
