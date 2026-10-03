# Current OpenWrt main — hardware verification log

This page preserves the first hardware-validation session of the CF-WR630AX port to current OpenWrt `main`.

> [!NOTE]
> Device-specific MAC addresses, client identifiers, transient build-host identifiers and similar unique values are intentionally anonymized. Public source revisions, image hashes, GPIO numbers, MMIO addresses and partition offsets are retained because they are needed for reproducibility.

## Test scope

- Device: COMFAST CF-WR630AX
- Test method: U-Boot TFTP → initramfs in RAM
- NAND write during this test: **none**
- OpenWrt source revision: `c759267c92b0697a6fd6f369164a5ed4c1a6a03c`
- Runtime revision: `r0+36743-c759267c92`
- Kernel: `6.18.52`
- Target: `mediatek/filogic`
- Current-main initramfs SHA256: `1866be3b8379e2b776db055141f97a258624f0e4ec563f188ff03311356b42b0`
- Image size: `9090776` bytes (`0x8ab6d8`)

The image was built successfully by GitHub Actions before being transferred to the router.

## TFTP transfer

```text
Using ethernet@15100000 device
TFTP from server 192.168.1.10; our IP address is 192.168.1.1
Filename 'openwrt-mediatek-filogic-comfast_cf-wr630ax-initramfs-kernel.bin'.
Load address: 0x46000000
...
done
Bytes transferred = 9090776 (8ab6d8 hex)
```

Before boot, U-Boot `iminfo` identified a valid FIT containing:

```text
Kernel: ARM64 OpenWrt Linux-6.18.52
Kernel load: 0x44000000
Kernel entry: 0x44000000
Initrd: ARM64 OpenWrt comfast_cf-wr630ax initrd
FDT: ARM64 OpenWrt comfast_cf-wr630ax device tree blob
FDT load: 0x43f00000

Hash(es) for kernel: crc32+ sha1+
Hash(es) for initrd: crc32+ sha1+
Hash(es) for FDT:    crc32+ sha1+
```

All FIT hash checks passed before `bootm`.

## Full sanitized boot log

```text
bootm ${loadaddr}
## Loading kernel from FIT Image at 46000000 ...
   Using 'config-1' configuration
   Trying 'kernel-1' kernel subimage
     Description:  ARM64 OpenWrt Linux-6.18.52
     Type:         Kernel Image
     Compression:  lzma compressed
     Data Start:   0x460000e8
     Data Size:    4675437 Bytes = 4.5 MiB
     Architecture: AArch64
     OS:           Linux
     Load Address: 0x44000000
     Entry Point:  0x44000000
     Hash algo:    crc32
     Hash value:   b222a78c
     Hash algo:    sha1
     Hash value:   9fca7d4e1aede79898c096bda4717b45f20845ff
   Verifying Hash Integrity ... crc32+ sha1+ OK
## Loading ramdisk from FIT Image at 46000000 ...
   Using 'config-1' configuration
   Trying 'initrd-1' ramdisk subimage
     Description:  ARM64 OpenWrt comfast_cf-wr630ax initrd
     Type:         RAMDisk Image
     Compression:  uncompressed
     Data Start:   0x46475994
     Data Size:    4386392 Bytes = 4.2 MiB
     Architecture: AArch64
     OS:           Linux
     Load Address: unavailable
     Entry Point:  unavailable
     Hash algo:    crc32
     Hash value:   bfb5d418
     Hash algo:    sha1
     Hash value:   fb059e91167d4dbb3899994c00a86fd45fde6872
   Verifying Hash Integrity ... crc32+ sha1+ OK
## Loading fdt from FIT Image at 46000000 ...
   Using 'config-1' configuration
   Trying 'fdt-1' fdt subimage
     Description:  ARM64 OpenWrt comfast_cf-wr630ax device tree blob
     Type:         Flat Device Tree
     Compression:  uncompressed
     Data Start:   0x468a48fc
     Data Size:    27027 Bytes = 26.4 KiB
     Architecture: AArch64
     Load Address: 0x43f00000
     Hash algo:    crc32
     Hash value:   7486abd4
     Hash algo:    sha1
     Hash value:   d7c54297b58e2e82fa0ced9b36220e21fa64de03
   Verifying Hash Integrity ... crc32+ sha1+ OK
   Loading fdt from 0x468a48fc to 0x43f00000
   Booting using the fdt blob at 0x43f00000
Working FDT set to 43f00000
   Uncompressing Kernel Image
   Loading Ramdisk to 4f3ca000, end 4f7f8e58 ... OK
   Loading Device Tree to 000000004f3c0000, end 000000004f3c9992 ... OK
Working FDT set to 4f3c0000
Starting kernel ...
[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
[    0.000000] Linux version 6.18.52 (runner@build-host) (aarch64-openwrt-linux-musl-gcc (OpenWrt GCC 14.4.0 r0+36743-c759267c92) 14.4.0, GNU ld (GNU Binutils) 2.46.1) #0 SMP Wed Sep 30 14:32:02 2026
[    0.000000] KASLR disabled due to lack of seed
[    0.000000] Machine model: COMFAST CF-WR630AX
[    0.000000] OF: reserved mem: 0x0000000042ff0000..0x0000000042ffffff (64 KiB) map non-reusable ramoops@42ff0000
[    0.000000] OF: reserved mem: 0x0000000043000000..0x000000004302ffff (192 KiB) nomap non-reusable secmon@43000000
[    0.000000] OF: reserved mem: 0x0000000047c80000..0x0000000047d7ffff (1024 KiB) nomap non-reusable wmcpu-reserved@47c80000
[    0.000000] OF: reserved mem: 0x0000000047d80000..0x0000000047dbffff (256 KiB) nomap non-reusable wo-emi@47d80000
[    0.000000] OF: reserved mem: 0x0000000047dc0000..0x0000000047ffffff (2304 KiB) nomap non-reusable wo-data@47dc0000
[    0.000000] Zone ranges:
[    0.000000]   DMA      [mem 0x0000000040000000-0x000000004fffffff]
[    0.000000]   DMA32    empty
[    0.000000]   Normal   empty
[    0.000000] Movable zone start for each node
[    0.000000] Early memory node ranges
[    0.000000]   node   0: [mem 0x0000000040000000-0x0000000042ffffff]
[    0.000000]   node   0: [mem 0x0000000043000000-0x000000004302ffff]
[    0.000000]   node   0: [mem 0x0000000043030000-0x0000000047c7ffff]
[    0.000000]   node   0: [mem 0x0000000047c80000-0x0000000047ffffff]
[    0.000000]   node   0: [mem 0x0000000048000000-0x000000004fffffff]
[    0.000000] Initmem setup node 0 [mem 0x0000000040000000-0x000000004fffffff]
[    0.000000] psci: probing for conduit method from DT.
[    0.000000] psci: PSCIv1.1 detected in firmware.
[    0.000000] psci: Using standard PSCI v0.2 function IDs
[    0.000000] psci: MIGRATE_INFO_TYPE not supported.
[    0.000000] psci: SMC Calling Convention v1.4
[    0.000000] percpu: Embedded 20 pages/cpu s43416 r8192 d30312 u81920
[    0.000000] pcpu-alloc: s43416 r8192 d30312 u81920 alloc=20*4096
[    0.000000] pcpu-alloc: [0] 0 [0] 1 
[    0.000000] Detected VIPT I-cache on CPU0
[    0.000000] CPU features: detected: GICv3 CPU interface
[    0.000000] CPU features: kernel page table isolation disabled by kernel configuration
[    0.000000] alternatives: applying boot alternatives
[    0.000000] Kernel command line: console=ttyS0,115200n8
[    0.000000] printk: log buffer data + meta data: 131072 + 458752 = 589824 bytes
[    0.000000] Dentry cache hash table entries: 32768 (order: 6, 262144 bytes, linear)
[    0.000000] Inode-cache hash table entries: 16384 (order: 5, 131072 bytes, linear)
[    0.000000] software IO TLB: SWIOTLB bounce buffer size adjusted to 0MB
[    0.000000] software IO TLB: area num 2.
[    0.000000] software IO TLB: SWIOTLB bounce buffer size roundup to 0MB
[    0.000000] software IO TLB: mapped [mem 0x000000004fe4b000-0x000000004fecb000] (0MB)
[    0.000000] Built 1 zonelists, mobility grouping on.  Total pages: 65536
[    0.000000] mem auto-init: stack:off, heap alloc:off, heap free:off
[    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=2, Nodes=1
[    0.000000] rcu: Hierarchical RCU implementation.
[    0.000000] rcu: 	RCU restricting CPUs from NR_CPUS=4 to nr_cpu_ids=2.
[    0.000000] 	Tracing variant of Tasks RCU enabled.
[    0.000000] rcu: RCU calculated value of scheduler-enlistment delay is 10 jiffies.
[    0.000000] rcu: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=2
[    0.000000] RCU Tasks Trace: Setting shift to 1 and lim to 1 rcu_task_cb_adjust=1 rcu_task_cpu_ids=2.
[    0.000000] NR_IRQS: 64, nr_irqs: 64, preallocated irqs: 0
[    0.000000] GICv3: GIC: Using split EOI/Deactivate mode
[    0.000000] GICv3: 640 SPIs implemented
[    0.000000] GICv3: 0 Extended SPIs implemented
[    0.000000] Root IRQ handler: gic_handle_irq
[    0.000000] GICv3: GICv3 features: 16 PPIs
[    0.000000] GICv3: GICD_CTLR.DS=0, SCR_EL3.FIQ=0
[    0.000000] GICv3: CPU0: found redistributor 0 region 0:0x000000000c080000
[    0.000000] rcu: srcu_init: Setting srcu_struct sizes based on contention.
[    0.000000] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns
[    0.000000] arch_timer: cp15 timer running at 13.00MHz (phys).
[    0.000000] clocksource: arch_sys_counter: mask: 0xffffffffffffff max_cycles: 0x2ff89eacb, max_idle_ns: 440795202429 ns
[    0.000000] sched_clock: 56 bits at 13MHz, resolution 76ns, wraps every 4398046511101ns
[    0.000088] Calibrating delay loop (skipped), value calculated using timer frequency.. 26.00 BogoMIPS (lpj=130000)
[    0.000097] pid_max: default: 32768 minimum: 301
[    0.002526] Mount-cache hash table entries: 512 (order: 0, 4096 bytes, linear)
[    0.002535] Mountpoint-cache hash table entries: 512 (order: 0, 4096 bytes, linear)
[    0.008443] rcu: Hierarchical SRCU implementation.
[    0.008452] rcu: 	Max phase no-delay instances is 1000.
[    0.008678] Timer migration: 1 hierarchy levels; 8 children per group; 1 crossnode level
[    0.008898] smp: Bringing up secondary CPUs ...
[    0.009309] Detected VIPT I-cache on CPU1
[    0.009360] GICv3: CPU1: found redistributor 1 region 0:0x000000000c0a0000
[    0.009391] CPU1: Booted secondary processor 0x0000000001 [0x410fd034]
[    0.009475] smp: Brought up 1 node, 2 CPUs
[    0.009481] SMP: Total of 2 processors activated.
[    0.009483] CPU: All CPU(s) started at EL2
[    0.009486] CPU features: detected: 32-bit EL0 Support
[    0.009490] CPU features: detected: CRC32 instructions
[    0.009517] alternatives: applying system-wide alternatives
[    0.009661] CPU features: emulated: Privileged Access Never (PAN) using TTBR0_EL1 switching
[    0.009796] Memory: 231336K/262144K available (9728K kernel code, 948K rwdata, 2980K rodata, 960K init, 297K bss, 29100K reserved, 0K cma-reserved)
[    0.013159] posixtimers hash table entries: 1024 (order: 2, 16384 bytes, linear)
[    0.013201] futex hash table entries: 512 (32768 bytes on 1 NUMA nodes, total 32 KiB, linear).
[    0.013240] 28992 pages in range for non-PLT usage
[    0.013243] 520512 pages in range for PLT usage
[    0.014821] pinctrl core: initialized pinctrl subsystem
[    0.016057] NET: Registered PF_NETLINK/PF_ROUTE protocol family
[    0.016390] DMA: preallocated 128 KiB GFP_KERNEL pool for atomic allocations
[    0.016417] DMA: preallocated 128 KiB GFP_KERNEL|GFP_DMA pool for atomic allocations
[    0.016447] DMA: preallocated 128 KiB GFP_KERNEL|GFP_DMA32 pool for atomic allocations
[    0.016883] thermal_sys: Registered thermal governor 'fair_share'
[    0.016887] thermal_sys: Registered thermal governor 'bang_bang'
[    0.016890] thermal_sys: Registered thermal governor 'step_wise'
[    0.016893] thermal_sys: Registered thermal governor 'user_space'
[    0.016970] ASID allocator initialised with 65536 entries
[    0.017686] pstore: Using crash dump compression: deflate
[    0.017692] pstore: Registered ramoops as persistent store backend
[    0.017695] ramoops: using 0x10000@0x42ff0000, ecc: 0
[    0.019179] /soc/interrupt-controller@c000000: Fixed dependency cycle(s) with /soc/interrupt-controller@c000000
[    0.038103] SCSI subsystem initialized
[    0.038274] libata version 3.00 loaded.
[    0.040085] clocksource: Switched to clocksource arch_sys_counter
[    0.042596] NET: Registered PF_INET protocol family
[    0.042705] IP idents hash table entries: 4096 (order: 3, 32768 bytes, linear)
[    0.043769] tcp_listen_portaddr_hash hash table entries: 256 (order: 0, 4096 bytes, linear)
[    0.043783] Table-perturb hash table entries: 65536 (order: 6, 262144 bytes, linear)
[    0.043796] TCP established hash table entries: 2048 (order: 2, 16384 bytes, linear)
[    0.043816] TCP bind hash table entries: 2048 (order: 4, 65536 bytes, linear)
[    0.043868] TCP: Hash tables configured (established 2048 bind 2048)
[    0.044090] MPTCP token hash table entries: 256 (order: 1, 6144 bytes, linear)
[    0.044200] UDP hash table entries: 256 (order: 2, 16384 bytes, linear)
[    0.044221] UDP-Lite hash table entries: 256 (order: 2, 16384 bytes, linear)
[    0.044423] NET: Registered PF_UNIX/PF_LOCAL protocol family
[    0.044459] PCI: CLS 0 bytes, default 64
[    0.044677] Unpacking initramfs...
[    0.051419] workingset: timestamp_bits=46 max_order=16 bucket_order=0
[    0.056608] squashfs: version 4.0 (2009/01/31) Phillip Lougher
[    0.056619] jffs2: version 2.2 (NAND) (SUMMARY) (LZMA) (RTIME) (CMODE_PRIORITY) (c) 2001-2006 Red Hat, Inc.
[    0.060178] cryptd: max_cpu_qlen set to 1000
[    0.118653] Serial: 8250/16550 driver, 3 ports, IRQ sharing disabled
[    0.122544] printk: legacy console [ttyS0] disabled
[    0.142948] 11002000.serial: ttyS0 at MMIO 0x11002000 (irq = 72, base_baud = 2500000) is a ST16650V2
[    0.142997] printk: legacy console [ttyS0] enabled
[    0.927026] mtk_rng trng: registered RNG driver
[    0.931994] random: crng init done
[    0.939837] loop: module loaded
[    0.946524] spi-nand spi0.1: calibration result: 0x3
[    0.951770] spi-nand spi0.1: Winbond SPI NAND was found.
[    0.957090] spi-nand spi0.1: 128 MiB, block size: 128 KiB, page size: 2048, OOB size: 64
[    0.965746] Signature found at block 1023 [0x07fe0000]
[    0.970919] NMBM management region starts at block 960 [0x07800000]
[    0.978113] First info table with writecount 0 found in block 960
[    0.986812] Second info table with writecount 0 found in block 963
[    0.993050] NMBM has been successfully attached
[    1.267833] Freeing initrd memory: 4280K
[    1.277695] 5 fixed-partitions partitions found on MTD device spi0.1
[    1.284361] Creating 5 MTD partitions on "spi0.1":
[    1.289154] 0x000000000000-0x000000100000 : "BL2"
[    1.294962] 0x000000100000-0x000000180000 : "u-boot-env"
[    1.301031] 0x000000180000-0x000000380000 : "Factory"
[    1.307800] 0x000000380000-0x000000580000 : "FIP"
[    1.314099] 0x000000580000-0x000004580000 : "ubi"
[    1.351812] ubi0: default fastmap pool size: 25
[    1.356345] ubi0: default fastmap WL pool size: 12
[    1.361172] ubi0: attaching mtd4
[    1.592316] ubi0: scanning is finished
[    1.600831] ubi0: attached mtd4 (name "ubi", size 64 MiB)
[    1.606238] ubi0: PEB size: 131072 bytes (128 KiB), LEB size: 126976 bytes
[    1.613117] ubi0: min./max. I/O unit sizes: 2048/2048, sub-page size 2048
[    1.619893] ubi0: VID header offset: 2048 (aligned 2048), data offset: 4096
[    1.626847] ubi0: good PEBs: 512, bad PEBs: 0, corrupted PEBs: 0
[    1.632847] ubi0: user volume: 3, internal volumes: 1, max. volumes count: 128
[    1.640054] ubi0: max/mean erase counter: 8/4, WL threshold: 4096, image sequence number: <redacted>
[    1.649179] ubi0: available PEBs: 0, total reserved PEBs: 512, PEBs reserved for bad PEB handling: 19
[    1.658404] ubi0: background thread "ubi_bgt0d" started, PID 195
[    1.665129] block ubiblock0_1: created from ubi0:1(rootfs)
[    1.670636] ubiblock: device ubiblock0_1 (rootfs) set to be root filesystem
[    1.682746] mtk_soc_eth 15100000.ethernet: legacy DT: using hard-coded SRAM offset.
[    1.690702] mtk_soc_eth 15100000.ethernet: legacy DT: missing interrupt-names.
[    1.811811] i2c_dev: i2c /dev entries driver
[    1.817831] mtk-wdt 1001c000.watchdog: Watchdog enabled (timeout=31 sec, nowayout=0)
[    1.827017] NET: Registered PF_INET6 protocol family
[    1.832751] Segment Routing with IPv6
[    1.836437] In-situ OAM (IOAM) with IPv6
[    1.840423] NET: Registered PF_PACKET protocol family
[    1.845624] 8021q: 802.1Q VLAN Support v1.8
[    1.868580] mtk_soc_eth 15100000.ethernet: legacy DT: using hard-coded SRAM offset.
[    1.877386] mtk_soc_eth 15100000.ethernet: legacy DT: missing interrupt-names.
[    4.571007] mtk_soc_eth 15100000.ethernet eth0: mediatek frame engine at 0xffffffc081b80000, irq 75
[    4.581093] mtk_soc_eth 15100000.ethernet eth1: mediatek frame engine at 0xffffffc081b80000, irq 75
[    4.634271] mt7530-mdio mdio-bus:1f: no interrupt support
[    4.663809] mt7530-mdio mdio-bus:1f: configuring for fixed/2500base-x link mode
[    4.672801] mt7530-mdio mdio-bus:1f: Link is Up - 2.5Gbps/Full - flow control rx/tx
[    4.682880] mt7530-mdio mdio-bus:1f lan1 (uninitialized): PHY [mt7530-0:01] driver [MediaTek MT7531 PHY] (irq=POLL)
[    4.708647] mt7530-mdio mdio-bus:1f lan2 (uninitialized): PHY [mt7530-0:02] driver [MediaTek MT7531 PHY] (irq=POLL)
[    4.733980] mt7530-mdio mdio-bus:1f lan3 (uninitialized): PHY [mt7530-0:03] driver [MediaTek MT7531 PHY] (irq=POLL)
[    4.749716] mtk_soc_eth 15100000.ethernet eth0: entered promiscuous mode
[    4.756472] DSA: tree 0 setup
[    4.759774] clk: Disabling unused clocks
[    4.763997] PM: genpd: Disabling unused power domains
[    4.769669] Freeing unused kernel memory: 960K
[    4.774173] Run /init as init process
[    4.777826]   with arguments:
[    4.780791]     /init
[    4.783053]   with environment:
[    4.786182]     HOME=/
[    4.788530]     TERM=linux
[    4.932039] init: Console is alive
[    4.935565] init: - watchdog -
[    4.943329] kmodloader: loading kernel modules from /etc/modules-boot.d/*
[    4.950750] gpio_button_hotplug: loading out-of-tree module taints kernel.
[    4.980024] kmodloader: done loading kernel modules from /etc/modules-boot.d/*
[    4.997831] init: - preinit -
[    5.110706] mtk_soc_eth 15100000.ethernet eth0: configuring for fixed/2500base-x link mode
[    5.119159] mtk_soc_eth 15100000.ethernet eth0: Link is Up - 2.5Gbps/Full - flow control rx/tx
[    5.147018] mt7530-mdio mdio-bus:1f lan1: configuring for phy/gmii link mode
Press the [f] key and hit [enter] to enter failsafe mode
Press the [1], [2], [3] or [4] key and hit [enter] to select the debug level
\- generating board file -
[    9.641699] procd: - early -
[    9.644640] procd: - watchdog -
[   10.166992] procd: - watchdog -
[   10.170400] procd: - ubus -
[   10.224959] procd: - init -
Please press Enter to activate this console.
[   10.442456] kmodloader: loading kernel modules from /etc/modules.d/*
[   10.459982] crypto-safexcel 10320000.crypto: EIP97:230(0,1,4,4)-HIA:270(0,5,5),PE:150/433(alg:7fcdfc00)/0/0/0
[   10.493023] Loading modules backported from Linux version v7.2-0-g8d3ae59288f1
[   10.500284] Backport generated by backports.git v5.15.58-1-198-g2580fa90cb79
[   10.636752] urngd: v1.0.2 started.
[   10.840307] mt798x-wmac 18000000.wifi: HW/SW Version: 0x8a108a10, Build Time: 20260515121445a
[   10.860965] mt798x-wmac 18000000.wifi: WM Firmware Version: ____000000, Build Time: 20260515121504
[   10.901094] mt798x-wmac 18000000.wifi: WA Firmware Version: DEV_000000, Build Time: 20260515121859
[   11.000064] mt798x-wmac 18000000.wifi: registering led 'mt76-phy0'
[   11.092362] mt798x-wmac 18000000.wifi: registering led 'mt76-phy1'
[   11.208801] PPP generic driver version 2.4.2
[   11.214470] NET: Registered PF_PPPOX protocol family
[   11.227646] kmodloader: done loading kernel modules from /etc/modules.d/*
[   14.241885] mtk_soc_eth 15100000.ethernet eth0: Link is Down
[   14.267626] mtk_soc_eth 15100000.ethernet eth0: configuring for fixed/2500base-x link mode
[   14.277769] mtk_soc_eth 15100000.ethernet eth0: Link is Up - 2.5Gbps/Full - flow control rx/tx
[   14.290461] mt7530-mdio mdio-bus:1f lan1: configuring for phy/gmii link mode
[   14.314478] br-lan: port 1(lan1) entered blocking state
[   14.319722] br-lan: port 1(lan1) entered disabled state
[   14.325074] mt7530-mdio mdio-bus:1f lan1: entered allmulticast mode
[   14.331418] mtk_soc_eth 15100000.ethernet eth0: entered allmulticast mode
[   14.343028] mt7530-mdio mdio-bus:1f lan1: entered promiscuous mode
[   14.362988] mt7530-mdio mdio-bus:1f lan2: configuring for phy/gmii link mode
[   14.377267] br-lan: port 2(lan2) entered blocking state
[   14.382630] br-lan: port 2(lan2) entered disabled state
[   14.387895] mt7530-mdio mdio-bus:1f lan2: entered allmulticast mode
[   14.397735] mt7530-mdio mdio-bus:1f lan2: entered promiscuous mode
[   14.420400] mt7530-mdio mdio-bus:1f lan3: configuring for phy/gmii link mode
[   14.434609] br-lan: port 3(lan3) entered blocking state
[   14.439849] br-lan: port 3(lan3) entered disabled state
[   14.445137] mt7530-mdio mdio-bus:1f lan3: entered allmulticast mode
[   14.457437] mt7530-mdio mdio-bus:1f lan3: entered promiscuous mode
[   14.498149] mtk_soc_eth 15100000.ethernet eth1: PHY [mdio-bus:00] driver [MediaTek MT7981 PHY] (irq=POLL)
[   14.512110] mtk_soc_eth 15100000.ethernet eth1: configuring for phy/gmii link mode
[   18.710293] mtk_soc_eth 15100000.ethernet eth1: Link is Up - 1Gbps/Full - flow control rx/tx
```

## Board identity after boot

```json
{
  "kernel": "6.18.52",
  "hostname": "OpenWrt",
  "system": "ARMv8 Processor rev 4",
  "model": "COMFAST CF-WR630AX",
  "board_name": "comfast,cf-wr630ax",
  "rootfs_type": "initramfs",
  "release": {
    "distribution": "OpenWrt",
    "version": "SNAPSHOT",
    "revision": "r0+36743-c759267c92",
    "target": "mediatek/filogic",
    "description": "OpenWrt SNAPSHOT r0+36743-c759267c92"
  }
}
```

## NVMEM / Wi-Fi MAC verification

Exact device MAC addresses are redacted. The important result is that each radio received the address stored in its own Factory NVMEM cell:

```text
phy0 <redacted-2.4ghz-mac>   # Factory + 0x0004
phy1 <redacted-5ghz-mac>     # Factory + 0x8000
```

This confirms that the current-main DTS preserves the hardware-verified per-band NVMEM fix and does not use the old runtime MAC-increment workaround.

Radio mapping:

```text
Wiphy phy1
    Band 2:
Wiphy phy0
    Band 1:
```

Therefore:

```text
phy0 -> 2.4 GHz
phy1 -> 5 GHz
```

## WPS / Mesh button

GPIO debug state at rest:

```text
gpio-1   (                    |wps                 ) in  hi IRQ ACTIVE LOW
```

Fast press:

```text
gpio-1   (                    |wps                 ) in  hi IRQ ACTIVE LOW
gpio-1   (                    |wps                 ) in  lo IRQ ACTIVE LOW
gpio-1   (                    |wps                 ) in  hi IRQ ACTIVE LOW
```

Long press:

```text
gpio-1   (                    |wps                 ) in  hi IRQ ACTIVE LOW
gpio-1   (                    |wps                 ) in  lo IRQ ACTIVE LOW
gpio-1   (                    |wps                 ) in  lo IRQ ACTIVE LOW
gpio-1   (                    |wps                 ) in  lo IRQ ACTIVE LOW
gpio-1   (                    |wps                 ) in  lo IRQ ACTIVE LOW
gpio-1   (                    |wps                 ) in  lo IRQ ACTIVE LOW
gpio-1   (                    |wps                 ) in  hi IRQ ACTIVE LOW
```

Result: GPIO1 is active-low, fast presses are detected, and the input remains low for the duration of a long press.

## LEDs

Sysfs:

```text
blue:mesh
blue:wan
blue:wlan-2ghz
blue:wlan-5ghz
mt76-phy0
mt76-phy1
```

Each physical front-panel LED was driven manually and verified on the test unit:

| Sysfs LED | Physical function | Result |
|---|---|:---:|
| `blue:mesh` | Mesh | ✅ |
| `blue:wlan-5ghz` | 5 GHz | ✅ |
| `blue:wlan-2ghz` | 2.4 GHz | ✅ |
| `blue:wan` | WAN | ✅ |

## Ethernet port mapping

Physical LAN ports were tested one at a time using carrier state.

First LAN port:

```text
lan1: 1
lan2: 0
lan3: 0
```

Second LAN port:

```text
lan1: 0
lan2: 1
lan3: 0
```

Third LAN port:

```text
lan1: 0
lan2: 0
lan3: 1
```

This confirms the physical order maps directly to `lan1`, `lan2`, `lan3`.

WAN:

```text
cat /sys/class/net/eth1/carrier
1

cat /sys/class/net/eth1/speed /sys/class/net/eth1/duplex
1000
full
```

WAN LED configuration:

```text
system.led_wan=led
system.led_wan.name='WAN'
system.led_wan.sysfs='blue:wan'
system.led_wan.trigger='netdev'
system.led_wan.mode='link tx rx'
system.led_wan.dev='eth1'
```

Result: the physical WAN port is `eth1`, links at 1 Gbit/s full duplex, and the WAN LED follows `eth1`.

## 5 GHz AP test

The default OpenWrt AP is disabled in the initramfs configuration. A temporary 5 GHz test AP was enabled only for validation and then shut down.

```text
Interface phy1-ap0
    addr <redacted-5ghz-mac>
    ssid WR630AX-main-test
    type AP
    channel 36 (5180 MHz), width: 80 MHz, center1: 5210 MHz
    txpower 20.00 dBm
```

Associated client, sanitized:

```text
Station <redacted-client-mac> (on phy1-ap0)
    authorized: yes
    authenticated: yes
    associated: yes
    signal:      -36 dBm
    tx bitrate:  960.7 MBit/s 80MHz HE-MCS 9 HE-NSS 2
    rx bitrate: 1200.9 MBit/s 80MHz HE-MCS 11 HE-NSS 2
    tx retries: 0
    tx failed:  0
    expected throughput: 795.781Mbps
```

Result: 5 GHz 802.11ax/HE, 80 MHz and 2 spatial streams were verified with a real associated client.

## 2.4 GHz AP test

A temporary WPA2-protected 2.4 GHz test AP was enabled and tested. The temporary initramfs configuration did not persist into the later clean NAND installation.

```text
Interface phy0-ap0
    addr <redacted-2.4ghz-mac>
    ssid WR630AX-main-24G
    type AP
    channel 1 (2412 MHz), width: 20 MHz
    txpower 20.00 dBm
```

Associated client, sanitized:

```text
Station <redacted-client-mac> (on phy0-ap0)
    authorized: yes
    authenticated: yes
    associated: yes
    signal:      -31 dBm
    tx bitrate: 229.4 MBit/s HE-MCS 9 HE-NSS 2
    rx bitrate: 258.0 MBit/s HE-MCS 10 HE-NSS 2
    expected throughput: 197.640Mbps
```

Result: 2.4 GHz 802.11ax/HE and 2 spatial streams were verified with a real associated client.

## Permanent current-main installation

After the RAM-only validation, full current-main images were built by GitHub Actions run **36863399195** from the same pinned OpenWrt source revision.

Build result:

```text
openwrt-mediatek-filogic-comfast_cf-wr630ax-squashfs-factory.bin
10747904 bytes
SHA256 b58d3593a5bb991f8555dde4986f7e7cb88ead5cbe2909d23480b635b117107a

openwrt-mediatek-filogic-comfast_cf-wr630ax-squashfs-sysupgrade.bin
9369879 bytes
SHA256 610ae53e659a4c5a82308d6a01c2851751e372a53861f12b8087e0c1641b61b7
```

The workflow verified that the factory image begins with UBI magic and that the sysupgrade archive contains WR630AX control data, kernel and root entries. On the router, the sysupgrade image was copied to `/tmp`, re-hashed and matched the build artifact exactly.

```text
sysupgrade -T /tmp/openwrt-mediatek-filogic-comfast_cf-wr630ax-squashfs-sysupgrade.bin
verifying sysupgrade tar file integrity

exit status: 0

SHA256 on router:
610ae53e659a4c5a82308d6a01c2851751e372a53861f12b8087e0c1641b61b7
```

The image was then installed with a clean `sysupgrade -n`. After reboot, OpenWrt reported:

```json
{
    "kernel": "6.18.52",
    "model": "COMFAST CF-WR630AX",
    "board_name": "comfast,cf-wr630ax",
    "rootfs_type": "squashfs",
    "release": {
        "distribution": "OpenWrt",
        "version": "SNAPSHOT",
        "revision": "r0+36743-c759267c92",
        "target": "mediatek/filogic"
    }
}
```

The `squashfs` root confirms that this boot is from the installed NAND image, not initramfs.

Post-install MTD layout:

```text
mtd0: 00100000 00020000 "BL2"
mtd1: 00080000 00020000 "u-boot-env"
mtd2: 00200000 00020000 "Factory"
mtd3: 00200000 00020000 "FIP"
mtd4: 04000000 00020000 "ubi"
```

The four protected partitions were read directly again after the current-main flash. Their SHA256 values remained identical to the previously verified backups:

```text
BL2       bfe6ef304f6a9b5e4f01f3e4ece18926ee9b1cb3f4a7f15c55fd24329176289f
u-boot-env 9d280971245e94e8508a56522b75076c3a6150468c7f290783c521df64de3057
Factory   bc1deae99f3509ec4f93eb45b65d970cef18f569efd22772ca58bfda26d4c545
FIP       852bbc73d48c9ce246846f45e61aba267a6aab88640ccd5dd6fc8ff9deaba7af
```

Result: the tested current-main sysupgrade path replaced the OpenWrt UBI system while preserving BL2, u-boot-env, Factory calibration data and FIP byte-for-byte.

## Current-main verification status

| Area | Result |
|---|:---:|
| Build from pinned current `main` | ✅ |
| TFTP transfer | ✅ |
| FIT hashes | ✅ |
| Kernel boot | ✅ |
| Correct board identity | ✅ |
| SPI-NAND detection | ✅ |
| NMBM attach | ✅ |
| Fixed partition layout | ✅ |
| Existing UBI attach | ✅ |
| MT7531 / DSA | ✅ |
| LAN1 / LAN2 / LAN3 physical mapping | ✅ |
| WAN / `eth1` 1 Gbit/s full duplex | ✅ |
| Per-band NVMEM MAC assignment | ✅ |
| WPS/Mesh GPIO1 active-low | ✅ |
| Mesh LED | ✅ |
| 2.4 GHz LED | ✅ |
| 5 GHz LED | ✅ |
| WAN LED | ✅ |
| 2.4 GHz AP + real client | ✅ |
| 5 GHz AP + real client | ✅ |
| Permanent current-main flash | ✅ |

## Upstream-submission validation — 2026-10-03

A separate upstream-candidate branch in Stefan's OpenWrt fork was validated with a dedicated GitHub Actions workflow before any pull request was opened.

The first three validation attempts did not produce a usable artifact. The decisive failure in attempt 3 was not a DTS compilation failure: the WR630AX DTB was built successfully, but the later FIT step received an empty DTS filename and tried to open `image-.dtb`.

The cause was premature Make expansion in the WR630AX `Device/...` image definition. The broken form was:

```make
fit lzma $(KDIR)/image-$(firstword $(DEVICE_DTS)).dtb
```

The corrected OpenWrt-style deferred expansion is:

```make
fit lzma $$(KDIR)/image-$$(firstword $$(DEVICE_DTS)).dtb
```

The factory-image size check was normalized at the same time:

```make
IMAGE/factory.bin := append-ubi | check-size $$$$(IMAGE_SIZE)
```

Two earlier commits whose messages claimed to fix the expansion were later verified to contain no file changes. The first commit that actually changed the file as intended was:

```text
c548953863d231ff83394078681aff40cb1618ad
```

GitHub Actions run **36947965104**, attempt 4, then completed successfully. The build, image-verification and artifact-upload steps all passed.

Validation artifact:

```text
Artifact name: cf-wr630ax-upstream-validation-1
Artifact ID:   11260965989
ZIP SHA256:    9bbe04c0ad7318a5b11b614ce559663a8b771e319a4d65393fa8ae134e4725e5
```

The uploaded images were independently inspected after the workflow completed:

```text
factory.bin
10747904 bytes
SHA256 5ada98a0b0980f41a34f761fe826dd0d1723af08cfdd746234fe71cce2d7db71
first four bytes: 55 42 49 23 ("UBI#")

sysupgrade.bin
9380117 bytes
SHA256 ab79d2ab7145f6947212e6e9aa31eabf6146be0baf5740d40ba58eaaaf57b2c6
```

The sysupgrade tar was valid and contained `CONTROL`, `kernel` and `root`. Its control data contained:

```text
BOARD=comfast_cf-wr630ax
```

Extracted sysupgrade members:

```text
kernel
4707012 bytes
SHA256 3c981770218444644bc87633ddff23879e8a33a19d4a0b19076447af40f38d22

root
4661248 bytes
SHA256 6d0a0b4a94d344f88856609885cf7011c8b8bec1534c595fb896efa6c33fa043
```

The validation build used Linux **6.18.54**.

After this successful validation, upstream OpenWrt `main` was re-checked at:

```text
9b95be917b2804cf877ca05c078175b37a3a95bf
```

The candidate was 16 upstream commits behind that revision, and none of those 16 commits touched the five WR630AX support files. A clean rebased validation commit was therefore created directly on that upstream revision:

```text
75cc41b4fac56a27cb54a724b8bf13fb02d26d70
```

It is a single commit ahead of `9b95be917...` and changes exactly the five WR630AX support files. It is currently carried on the temporary branch:

```text
mediatek-filogic-cf-wr630ax-rebased-validation
```

This rebased candidate must complete a fresh validation build before the temporary/WIP history is replaced by the final DCO-correct upstream commit. No OpenWrt pull request has been opened yet.

## Known non-fatal warnings

The current-main kernel prints:

```text
mtk_soc_eth 15100000.ethernet: legacy DT: using hard-coded SRAM offset.
mtk_soc_eth 15100000.ethernet: legacy DT: missing interrupt-names.
```

Ethernet nevertheless initializes, the MT7531 CPU link comes up at 2.5 Gbit/s, all three LAN ports work, and WAN links at 1 Gbit/s full duplex. These warnings are retained here because they are useful cleanup targets for the upstream-quality DTS.

## Safety boundary

The first current-main validation was intentionally performed from initramfs in RAM without writing NAND. Only after that hardware session passed were separate full factory/sysupgrade images built and inspected.

The current-main sysupgrade image has now passed `sysupgrade -T`, been installed to NAND, booted as a `squashfs` root filesystem, and the four protected MTD partitions have been re-verified byte-identical afterward. A later cold-power-cycle test can be recorded separately; it is not implied by the checks above.
