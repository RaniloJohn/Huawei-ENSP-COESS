# Huawei Enterprise Datacom Lab Infrastructure
## Comprehensive Architecture, Student Guide & Administrator Manual

**Co-Branded Edition:** Computer Engineering Students Society (COESS)  
**Author:** Ranilo John Delos Angeles  
**Infrastructure Version:** Huawei eNSP Lite 2026 Enterprise Edition  

---

## 📥 Virtual Machine Appliance (.OVA) Download

Students and instructors can download the complete, pre-configured **Huawei eNSP Lite Virtual Machine (`.ova` format)** using the official link below:

> ### 🚀 [**Click Here to Download Huawei eNSP Pro / Lite VM (.OVA)**](https://ueeduph-my.sharepoint.com/:f:/g/personal/delosangeles_ranilojohn_ue_edu_ph/IgDyUHenNnhOSJ1DYXTloOwSAYiUrdX7n8HbZy59GnxvU3I?e=WnXtss)
> * **Hosted on:** UE SharePoint / OneDrive Cloud Storage
> * **Included:** EulerOS Linux, Huawei eNSP Lite 2026 engine, All 33 Pre-Wired Practice Labs, and Local In-Memory Student Portal.
> * **Ready-to-Use:** Single-file import into VMware Workstation 17 Pro / Player.

---

## 1. Quick Access & Port Allocation Summary

Once the VM is imported and booted, access the services from your host machine's browser:

| Port | Service | Purpose | URL / Access Method |
| :--- | :--- | :--- | :--- |
| **`80`** | **Main Lab Portal** | **Main website for lab descriptions**, scenario objectives, interface/IP addressing tables, copyable VRP scripts, and line-by-line CCNA-style syntax breakdowns. | **`http://10.10.10.137/`** |
| **`8443`** | **eNSP Lite Console** | **Live simulation environment** containing the HTML5 topology canvas, interactive wiring, device power controls, and web CLI terminals. | **`https://10.10.10.137:8443/`** |
| **`22`** | **EulerOS Linux SSH** | Remote administrative shell access to the host virtual machine via PowerShell or terminal. | **`ssh root@10.10.10.137`** |

---

## 🛠️ 2. Detailed VMware Workstation Setup Guide (For New Users)

Follow this step-by-step setup guide to properly configure VMware Workstation, network adapters, and nested virtualization settings.

### Step 1: Host Computer Prerequisites (BIOS / UEFI)
Before creating or running any network simulation virtual machine, ensure that hardware virtualization is enabled on your host PC:
1. Restart your PC and press `F2`, `F10`, `Del`, or `Esc` to enter the **BIOS/UEFI Settings**.
2. Look for **Intel Virtualization Technology (Intel VT-x)** or **AMD SVM (Secure Virtual Machine) Mode**.
3. Set it to **Enabled**, save changes (`F10`), and boot into Windows.

---

### Step 2: Configure VMware Virtual Network Editor (`10.10.10.0/24`)
The VM is pre-configured with a static IP of **`10.10.10.137`**. Your VMware virtual switch must match this subnet.

```
 +---------------------------------------------------------+
 |                     Windows Host PC                     |
 |  VMware Network Adapter VMnet1: 10.10.10.1 / 24         |
 +----------------------------+----------------------------+
                              |
                     [ Host-Only VMnet1 ]
                              |
 +----------------------------v----------------------------+
 |                Huawei eNSP Lite Virtual Machine         |
 |                Static IP: 10.10.10.137 / 24             |
 +---------------------------------------------------------+
```

1. Open **VMware Workstation Pro**.
2. Go to the top menu: **Edit** $\rightarrow$ **Virtual Network Editor...**
3. Click **Change Settings** (bottom right, shield icon) to grant administrator privileges.
4. Select **`VMnet1` (Host-Only)**:
   * **Subnet IP:** `10.10.10.0`
   * **Subnet Mask:** `255.255.255.0`
   * Ensure `[x] Connect a host virtual adapter to this network` is **checked**.
   * Ensure `[x] Use local DHCP service to distribute IP address to VMs` is **checked**.
5. Click **Apply**, then click **OK**.

*(Alternative: If using **VMnet8 (NAT)**, set VMnet8 Subnet IP to `10.10.10.0` and Mask to `255.255.255.0`, with Gateway IP `10.10.10.2`)*.

---

### Step 3: Import the `.ova` File into VMware
1. Download the `eNSP_Pro_EulerOS.ova` file from the [SharePoint link](https://ueeduph-my.sharepoint.com/:f:/g/personal/delosangeles_ranilojohn_ue_edu_ph/IgDyUHenNnhOSJ1DYXTloOwSAYiUrdX7n8HbZy59GnxvU3I?e=WnXtss).
2. In VMware Workstation, click **File** $\rightarrow$ **Open...** (or press `Ctrl + O`).
3. Browse and select the `.ova` file.
4. Set a name for your virtual machine (e.g., `Huawei-eNSP-COESS`).
5. Choose a storage path on an SSD with at least **50 GB** of free disk space.
6. Click **Import** and wait for the virtual disk extraction to finish (approx. 1–2 minutes).

---

### Step 4: Configure Virtual Machine Hardware Settings (CRITICAL)
Before powering on the VM, click **Edit virtual machine settings** (`Ctrl + D`) and verify these exact settings:

```
+-------------------------------------------------------------------------------+
|  HARDWARE COMPONENT      |  RECOMMENDED VALUE      |  MANDATORY FLAGS         |
+--------------------------+-------------------------+--------------------------+
|  Processors (vCPUs)      |  8 Cores (or 4 Cores)   |  [x] Virtualize VT-x/AMD |
|  Memory (RAM)            |  16 GB (min. 12 GB)     |  Dedicated allocation    |
|  Hard Disk               |  100 GB (Thin Provision)|  SCSI / NVMe             |
|  Network Adapter         |  Custom: VMnet1         |  Host-Only (10.10.10.0)  |
+-------------------------------------------------------------------------------+
```

#### A. Processors & Nested Virtualization (MANDATORY):
* **Number of processors:** `1`
* **Number of cores per processor:** `4` to `8` (Total: `8 vCPUs` recommended).
* **Virtualization Engine Checkboxes:**
  * ✅ **`[x] Virtualize Intel VT-x/EPT or AMD-V/RVI`** $\leftarrow$ **CRITICAL / MANDATORY!**  
    *(If this is not checked, Huawei AR routers, NE40E carrier nodes, and USG firewalls will fail to launch in QEMU/KVM).*
  * ✅ `[x] Virtualize CPU performance counters` *(Optional)*.
  * ✅ `[x] Virtualize IOMMU (IO virtualization)` *(Optional)*.

#### B. Memory (RAM):
* Allocate **`16384 MB` (16 GB)** for smooth multi-node topologies.
* Absolute minimum: `8192 MB` (8 GB) for lightweight single-switch labs.

#### C. Network Adapter:
* Select **`Custom: Specific virtual network`** $\rightarrow$ Choose **`VMnet1 (Host-only)`** (or `VMnet8` if configured in Step 2).

Click **OK** to save the settings.

---

### Step 5: Power On & First Boot
1. Click **Power on this virtual machine** (Green Play button).
2. Allow **60 to 90 seconds** for EulerOS Linux to boot and automatically initialize:
   * ETCD distributed state database.
   * Container runtime & eNSP Lite node services.
   * `huawei-lab-portal.service` (Port 80).
   * `ensp-service` Spring Boot engine (Port 8443).
3. The EulerOS console login screen will display `10.10.10.137`.

---

### Step 6: Test Host Connectivity
Open Windows PowerShell (`Win + X` $\rightarrow$ *Terminal*) and ping the VM:

```powershell
ping 10.10.10.137
```

You should receive instant replies:
```text
Pinging 10.10.10.137 with 32 bytes of data:
Reply from 10.10.10.137: bytes=32 time<1ms TTL=64
Reply from 10.10.10.137: bytes=32 time<1ms TTL=64
```

---

## 3. How to SSH via Windows PowerShell

Students and instructors can access the backend EulerOS Linux environment directly from Windows PowerShell:

```powershell
ssh root@10.10.10.137
```

* **Default Username:** `root`
* **Default Password:** `ensp2026@ensp`  
*(Note: Characters will not display on screen while typing the password in PowerShell).*

---

## 4. System Credentials & Reference Summary

| Component | Endpoint | Username | Password | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Lab Portal (Port 80)** | `http://10.10.10.137/` | *(None)* | *(None)* | Open access for all students |
| **Console Env (Port 8443)** | `https://10.10.10.137:8443/` | *(No auth patch)* | *(None)* | Direct simulation canvas access |
| **VM OS Root SSH (Port 22)** | `10.10.10.137:22` | **`root`** | **`ensp2026@ensp`** | Host administrative shell |
| **VRP Device AAA** | Console / Telnet / SSH | **`admin`** | **`admin`** | Privilege Level 15 (Manager) |
| **VRP Super Password** | Privilege Elevation | **`super`** | **`super`** | Privilege Level 15 Elevation |

---

## 5. Student User Guide: Step-by-Step Workflow

```
 +------------------------+      +---------------------------+      +---------------------------+
 |   1. OPEN LAB PORTAL   | ===> |   2. STUDY BLUEPRINT &    | ===> |   3. LAUNCH SIMULATION    |
 |  http://10.10.10.137/  |      |   SYNTAX BREAKDOWN TABLE  |      | https://10.10.10.137:8443 |
 +------------------------+      +---------------------------+      +---------------------------+
                                                                                  |
                                 +---------------------------+                    v
                                 |  5. SAVE & STOP TOPOLOGY  | <=== +---------------------------+
                                 |   <Huawei> save           |      |   4. POWER ON NODES &     |
                                 |   Free up CPU & RAM       |      |   APPLY VRP CONFIGURATION |
                                 +---------------------------+      +---------------------------+
```

### Step 1: Open the Lab Portal (`http://10.10.10.137/`)
* Use the **Theme Switcher** (Sun/Moon icon in top right) to toggle between Huawei Light and Dark modes.
* Use the **Search Bar** in the left sidebar to quickly filter labs by topic (e.g., `OSPF`, `VLAN`, `VRRP`, `NAT`, `ACL`, `Eth-Trunk`, `IPv6`).

### Step 2: Study the 6 Structured Tabs
Before touching the CLI, review the 6 tabs for your active lab:
1. **`1. Overview & Setup`:** Problem context, topology scope, and default credentials.
2. **`2. Interface & IP Matrix`:** Cabling matrix, IP addresses, subnets, and VLAN memberships.
3. **`3. Task Objectives`:** Interactive checklist of lab requirements.
4. **`4. Step-by-Step Solution (CCNA Standard)`:** Detailed pedagogical breakdown with problem context $\rightarrow$ isolated `@Device` CLI blocks $\rightarrow$ command rationale $\rightarrow$ `VERIFY:` commands.
5. **`5. Command Syntax Breakdown Table`:** Complete reference table explaining every command line-by-line with parameter mechanisms, Cisco IOS equivalents, and single-click copy buttons.
6. **`6. Verification Runbook`:** Live `display` check commands, ping testing, and failover validation steps.

### Step 3: Launch eNSP Lite Console (`https://10.10.10.137:8443/`)
1. Click **"Open Simulation Console"** in the top bar or navigate to `https://10.10.10.137:8443/`.
2. Find your lab sandbox (e.g., `Lab 01 Huawei DHCP Global Pool and Easy IP NAT` or `Enterprise HQ and WAN Figure 4-7`).
3. Click to open the topology canvas.

### Step 4: Power On Nodes & Configure
1. Click the **Start / Power On** button on the devices needed for your active lab.
2. Double-click any device (or right-click $\rightarrow$ *CLI*) to open the web terminal.
3. Apply configurations, test ping connectivity, and execute verification commands.
4. Before finishing, save your work in VRP User View:
   ```text
   <Huawei> save
   Are you sure to continue? (y/n)[n]: y
   ```

---

## 6. Critical Resource Hygiene: Stopping Labs When Finished

> [!CAUTION]
> **Avoid Running Multiple Heavy Labs Concurrently!**
> Huawei VRP router containers (especially NE40E, AR routers, and USG Firewalls) consume dedicated CPU cycles and RAM.
> * Always click **Stop / Power Off** on devices in an old lab before starting a new one.
> * If the web console becomes slow or unresponsive, restart the background services via SSH:
>   ```bash
>   systemctl restart huawei-lab-portal.service
>   ```

---

## 7. Troubleshooting Guide (FAQ)

### Q1: "The host supports Intel VT-x, but Intel VT-x is disabled."
* **Cause:** CPU Virtualization is disabled in your host computer's motherboard BIOS.
* **Fix:** Reboot your computer $\rightarrow$ Enter BIOS/UEFI (`F2`/`Del`) $\rightarrow$ Enable **Intel Virtualization Technology** or **AMD SVM Mode** $\rightarrow$ Save & Reboot.

### Q2: "Cannot access `http://10.10.10.137/` from browser."
* **Cause:** The host virtual network adapter `VMnet1` is not on subnet `10.10.10.0/24`.
* **Fix:** Open VMware $\rightarrow$ `Edit` $\rightarrow$ `Virtual Network Editor...` $\rightarrow$ Select `VMnet1` $\rightarrow$ Set Subnet IP to `10.10.10.0` and Mask to `255.255.255.0` $\rightarrow$ Click Apply.

### Q3: "Device nodes fail to start or give QEMU errors on canvas."
* **Cause:** Nested virtualization is not enabled on the VM processor.
* **Fix:** Power off VM $\rightarrow$ `Edit virtual machine settings` $\rightarrow$ `Processors` $\rightarrow$ Check **`[x] Virtualize Intel VT-x/EPT or AMD-V/RVI`** $\rightarrow$ Click OK $\rightarrow$ Power on.

### Q4: "Browser shows SSL certificate warning on `https://10.10.10.137:8443/`."
* **Cause:** eNSP Lite uses a self-signed HTTPS certificate for local simulation security.
* **Fix:** Click **Advanced** $\rightarrow$ **Proceed to 10.10.10.137 (unsafe)** in Chrome/Edge.

---

**Computer Engineering Students Society (COESS)**  
*Empowering Future Network & Systems Engineers with Modern Hands-on Infrastructure.*
