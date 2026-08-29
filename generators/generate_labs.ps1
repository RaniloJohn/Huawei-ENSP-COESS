# PowerShell Lab Generation and Deployment Engine for Huawei EVE-NG Labs
param(
    [string]$TargetServer = "208.8.8.135",
    [string]$WinScpPath = "C:\Program Files (x86)\WinSCP\WinSCP.com"
)

$baseDir = "d:\Projects\Infrastructure for Huawei"
$labsUnlDir = "$baseDir\labs_unl"
$workbooksDir = "$baseDir\student_workbooks"

if (!(Test-Path $labsUnlDir)) { New-Item -ItemType Directory -Path $labsUnlDir -Force }
if (!(Test-Path $workbooksDir)) { New-Item -ItemType Directory -Path $workbooksDir -Force }

# Helper to generate a new GUID
function New-EveGuid { return [guid]::NewGuid().ToString() }

# 32 Lab Metadata Definitions
$labs = @(
    @{ Id = 1;  Title = "Lab-01-IP-Services-DHCP-NAT"; Category = "04-IP-Services-Security"; Devices = @("R1", "R2", "PC1"); Desc = "Huawei IP Services: Global & Interface DHCP Pools and Easy-IP Dynamic NAT" },
    @{ Id = 2;  Title = "Lab-02-DHCP-Relay-and-VRRP"; Category = "04-IP-Services-Security"; Devices = @("GW1", "GW2", "CoreSW"); Desc = "Huawei IP Services: DHCP Relay and VRRP Gateway Redundancy" },
    @{ Id = 3;  Title = "Lab-03-IPv4-Static-and-Default-Routing"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("R1", "R2", "R3"); Desc = "Huawei IPv4 Static Routing, Default Routing, and Next-Hop Resolution" },
    @{ Id = 4;  Title = "Lab-04-OSPFv2-Single-and-Multi-Area"; Category = "03-Dynamic-Routing-OSPF"; Devices = @("R1", "R2", "R3"); Desc = "Huawei OSPFv2 Routing: Router-ID, Area 0, Area 1, and Route Propagation" },
    @{ Id = 5;  Title = "Lab-05-LACP-Static-Eth-Trunk-Aggregation"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2"); Desc = "Huawei Link Aggregation: Eth-Trunk Configuration in Static LACP Mode" },
    @{ Id = 6;  Title = "Lab-06-Voice-VLAN-and-QoS-Priority"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2"); Desc = "Huawei Voice VLAN: OUI-based Voice VLAN and CoS Priority Tagging" },
    @{ Id = 7;  Title = "Lab-07-VLAN-Segmentation-and-Trunking"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2"); Desc = "Huawei Layer 2 Fundamentals: Access Ports, 802.1Q Trunks, and Allowed VLANs" },
    @{ Id = 8;  Title = "Lab-08-IPv4-and-IPv6-Dual-Stack-Connectivity"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("R1", "R2"); Desc = "Huawei Dual-Stack Networking: IPv4 & IPv6 Global Unicast and Link-Local" },
    @{ Id = 9;  Title = "Lab-09-Advanced-ACL-and-Port-Security"; Category = "04-IP-Services-Security"; Devices = @("SW1", "SW2"); Desc = "Huawei Security: Advanced ACL 3000 Rules and Switch Port-Security Limits" },
    @{ Id = 10; Title = "Lab-10-DHCP-Snooping-and-Trusted-Ports"; Category = "04-IP-Services-Security"; Devices = @("R1", "SW1", "SW2"); Desc = "Huawei Layer 2 Defense: DHCP Snooping and DHCP Trusted Port Configuration" },
    @{ Id = 11; Title = "Lab-11-VLAN-Segmentation-and-LLDP-Discovery"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2"); Desc = "Huawei Campus Access: Multi-VLAN Tagging and LLDP Neighbor Discovery" },
    @{ Id = 12; Title = "Lab-12-IPv4-and-IPv6-Subnet-Deployment-1"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("R1", "R2"); Desc = "Huawei IP Deployment: Variable Length Subnet Masking (VLSM) and Dual-Stack" },
    @{ Id = 13; Title = "Lab-13-Floating-Static-Route-and-Path-Backup"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("R1", "R2", "R3"); Desc = "Huawei Route Redundancy: Primary Static Route vs Floating Route (Preference 100)" },
    @{ Id = 14; Title = "Lab-14-Route-Summarization-and-Null0-Route"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("R1", "R2", "R3"); Desc = "Huawei Routing Optimization: Summary Static Routes and Null0 Loop Prevention" },
    @{ Id = 15; Title = "Lab-15-Multi-Switch-LLDP-and-VLAN-Verification"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2", "SW3"); Desc = "Huawei Network Discovery: LLDP Neighbor Information and Multi-Switch Topologies" },
    @{ Id = 16; Title = "Lab-16-LLDP-TLV-Management-and-Port-Status"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2"); Desc = "Huawei Device Discovery: Fine-grained LLDP TLV Advertisement Control" },
    @{ Id = 17; Title = "Lab-17-IPv6-Static-and-Default-Routing"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("R1", "R2", "R3"); Desc = "Huawei IPv6 Routing: Global Next-Hop and Link-Local Static Route Deployments" },
    @{ Id = 18; Title = "Lab-18-Auto-Voice-VLAN-OUI-Mac-Matching"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2"); Desc = "Huawei Voice Infrastructure: Auto Voice VLAN Assignment via Telephony MAC OUI" },
    @{ Id = 19; Title = "Lab-19-Advanced-ACL-Traffic-Filtering"; Category = "04-IP-Services-Security"; Devices = @("R1", "SW1", "SW2"); Desc = "Huawei Access Control: Traffic-Filter Inbound/Outbound with ACL 3001" },
    @{ Id = 20; Title = "Lab-20-Voice-VLAN-and-LLDP-MED-Policies"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2"); Desc = "Huawei VoIP Integration: LLDP-MED Policy Advertisement for IP Phones" },
    @{ Id = 21; Title = "Lab-21-Allowed-VLANs-Native-PVID-and-LACP"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2", "SW3"); Desc = "Huawei Switching: Trunk Port PVID (Native VLAN), Allowed Lists, and LACP" },
    @{ Id = 22; Title = "Lab-22-VLAN-Trunk-Pruning-and-LLDP-Audit"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2", "SW3"); Desc = "Huawei Campus Audit: VLAN Port Trunks, Pruning, and LLDP Neighbor Table Verification" },
    @{ Id = 23; Title = "Lab-23-Equal-Cost-Multi-Path-Static-Routing"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("R1", "R2", "R3", "R4"); Desc = "Huawei Load Balancing: ECMP Static Routing across Dual High-Speed Links" },
    @{ Id = 24; Title = "Lab-24-IPv4-and-IPv6-Host-Address-Assignment"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("R1", "R2"); Desc = "Huawei Host Addressing: IPv4 Subnetting, IPv6 SLAAC, and Gateway Configuration" },
    @{ Id = 25; Title = "Lab-25-Standard-802.1Q-Trunk-and-Eth-Trunk"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2", "SW3"); Desc = "Huawei Enterprise Core: 802.1Q Encapsulation and Eth-Trunk Bundling" },
    @{ Id = 26; Title = "Lab-26-Multi-Site-Hierarchical-Subnet-Deployment"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("R1", "R2", "R3"); Desc = "Huawei Enterprise WAN: Multi-Site IPv4/IPv6 Hierarchical Addressing" },
    @{ Id = 27; Title = "Lab-27-LACP-Active-Passive-and-Native-PVID"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2", "SW3"); Desc = "Huawei Link Aggregation: Actor Priorities, LACP Modes, and Native PVID" },
    @{ Id = 28; Title = "Lab-28-Multi-Hop-Recursive-Static-Routing"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("R1", "R2", "R3", "R4"); Desc = "Huawei Backbone Routing: Multi-Hop Static Routing and Loopback Reachability" },
    @{ Id = 29; Title = "Lab-29-Dual-Stack-WAN-Core-and-Edge-Routing"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("AR1", "AR2", "NE40-Core"); Desc = "Huawei Core Infrastructure: Dual-Stack AR1000v and NE40E Interconnection" },
    @{ Id = 30; Title = "Lab-30-Enterprise-Campus-Static-Routing-Core"; Category = "02-IPv4-IPv6-Static-Routing"; Devices = @("Core1", "Core2", "Dist1", "Dist2"); Desc = "Huawei Campus Backbone: Dual-Core Redundant Static Routing" },
    @{ Id = 31; Title = "Lab-31-Multi-Tier-Voice-and-Data-VLAN-Isolation"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("CoreSW", "DistSW", "AccessSW"); Desc = "Huawei Multi-Tier Campus: End-to-End Voice & Data VLAN Separation" },
    @{ Id = 32; Title = "Lab-32-LACP-Link-Protection-and-VLAN-Control"; Category = "01-Layer2-Switching-and-VLANs"; Devices = @("SW1", "SW2", "SW3"); Desc = "Huawei L2 Hardening: Eth-Trunk Maximum Active Links and Strict VLAN Filters" }
)

Write-Output "Generating 32 Huawei EVE-NG .unl lab files..."

foreach ($lab in $labs) {
    $labId = $lab.Id
    $labTitle = $lab.Title
    $labDesc = $lab.Desc
    $guid = New-EveGuid
    $devs = $lab.Devices

    # Coordinates calculation
    $nodesXml = ""
    $networksXml = ""
    $nodeIndex = 1

    # Place nodes in a clean horizontal / triangular / square layout
    $xOffsets = @(350, 750, 1150, 750)
    $yOffsets = @(300, 300, 300, 550)

    for ($i = 0; $i -lt $devs.Count; $i++) {
        $devName = $devs[$i]
        $nodeId = $i + 1
        $nodeGuid = New-EveGuid
        $posX = $xOffsets[$i % $xOffsets.Count]
        $posY = $yOffsets[$i % $yOffsets.Count]

        # Use NE40 for core WAN or AR1000v for standard routers/switches
        $template = "huaweiar1k"
        $image = "huaweiar1k-5.170"
        $ram = 4096
        $cpu = 2
        $ethCount = 6
        $qemuOpts = "-machine type=pc,accel=kvm -vga std -usbdevice tablet -boot order=cd -cpu host"
        $icon = "Router.png"
        if ($devName -like "*SW*" -or $devName -like "*Switch*") {
            $icon = "Switch L32.png"
        }
        if ($devName -like "*NE40*") {
            $template = "huaweine40"
            $image = "huaweine40-ne40"
            $ram = 2048
            $cpu = 2
            $ethCount = 12
            $qemuOpts = "-cpu host -machine type=pc-1.0,accel=kvm -serial mon:stdio -nographic -nodefconfig -nodefaults -rtc base=utc"
            $icon = "Router.png"
        }

        # Interconnect interfaces
        $ifacesXml = ""
        if ($devs.Count -eq 2) {
            if ($nodeId -eq 1) {
                $ifacesXml = @"
        <interface id="0" name="GE0/0/0" type="ethernet" network_id="1"/>
        <interface id="1" name="GE0/0/1" type="ethernet" network_id="2"/>
"@
            } else {
                $ifacesXml = @"
        <interface id="0" name="GE0/0/0" type="ethernet" network_id="1"/>
        <interface id="1" name="GE0/0/1" type="ethernet" network_id="2"/>
"@
            }
        } elseif ($devs.Count -eq 3) {
            if ($nodeId -eq 1) {
                $ifacesXml = @"
        <interface id="0" name="GE0/0/0" type="ethernet" network_id="1"/>
        <interface id="1" name="GE0/0/1" type="ethernet" network_id="2"/>
"@
            } elseif ($nodeId -eq 2) {
                $ifacesXml = @"
        <interface id="0" name="GE0/0/0" type="ethernet" network_id="1"/>
        <interface id="1" name="GE0/0/1" type="ethernet" network_id="3"/>
"@
            } else {
                $ifacesXml = @"
        <interface id="0" name="GE0/0/0" type="ethernet" network_id="2"/>
        <interface id="1" name="GE0/0/1" type="ethernet" network_id="3"/>
"@
            }
        } else {
            $ifacesXml = @"
        <interface id="0" name="GE0/0/0" type="ethernet" network_id="$nodeId"/>
"@
        }

        $nodesXml += @"
      <node id="$nodeId" name="$devName" type="qemu" template="$template" image="$image" console="telnet" cpu="$cpu" cpulimit="0" ram="$ram" ethernet="$ethCount" uuid="$nodeGuid" qemu_options="$qemuOpts" qemu_version="2.12.0" qemu_arch="x86_64" qemu_nic="virtio-net-pci" delay="0" icon="$icon" config="0" left="$posX" top="$posY">
$ifacesXml
      </node>

"@
    }

    # Networks / Bridges
    if ($devs.Count -eq 2) {
        $networksXml = @"
      <network id="1" type="bridge" name="Link-1" left="550" top="280" visibility="0" icon="lan.png"/>
      <network id="2" type="bridge" name="Link-2" left="550" top="340" visibility="0" icon="lan.png"/>
"@
    } elseif ($devs.Count -ge 3) {
        $networksXml = @"
      <network id="1" type="bridge" name="Link-1-2" left="550" top="280" visibility="0" icon="lan.png"/>
      <network id="2" type="bridge" name="Link-1-3" left="750" top="420" visibility="0" icon="lan.png"/>
      <network id="3" type="bridge" name="Link-2-3" left="950" top="280" visibility="0" icon="lan.png"/>
"@
    }

    $unlContent = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<lab name="$labTitle" id="$guid" version="1" scripttimeout="300" lock="0" description="$labDesc">
  <topology>
    <nodes>
$nodesXml    </nodes>
    <networks>
$networksXml    </networks>
  </topology>
</lab>
"@
    $outFile = "$labsUnlDir\$labTitle.unl"
    $unlContent.Trim() | Out-File -FilePath $outFile -Encoding utf8
}

Write-Output "Successfully generated all 32 .unl files in $labsUnlDir."
