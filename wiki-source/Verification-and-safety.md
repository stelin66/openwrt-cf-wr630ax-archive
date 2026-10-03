# Verification and safety

The working rule for this project is: **verify in RAM first, write flash last**.

That gate has now been completed successfully on one physical CF-WR630AX.

## What has been verified

### Boot path

- UART console works bidirectionally.
- U-Boot TFTP works.
- OpenWrt FIT metadata and hashes validate in U-Boot.
- Initramfs boots entirely from DRAM.
- Linux identifies the board as COMFAST CF-WR630AX.
- Permanent OpenWrt installation boots from NAND/UBI.
- A later cold boot with the enclosure assembled and UART disconnected also completed normally.

### Storage

The fixed partition layout remains:

```text
mtd0 00100000 "BL2"
mtd1 00080000 "u-boot-env"
mtd2 00200000 "Factory"
mtd3 00200000 "FIP"
mtd4 04000000 "ubi"
```

After sysupgrade, UBI contains three healthy dynamic volumes:

```text
kernel      36 LEBs   4571136 bytes
rootfs      36 LEBs   4571136 bytes
rootfs_data 415 LEBs 52695040 bytes
```

The post-install UBI state reported zero bad physical eraseblocks.

### Protected partitions

Independent pre-install backups were copied off-device and checksummed. After permanent sysupgrade, direct SHA256 reads from the four protected MTD partitions still matched those backups exactly:

```text
BL2
bfe6ef304f6a9b5e4f01f3e4ece18926ee9b1cb3f4a7f15c55fd24329176289f

u-boot-env
9d280971245e94e8508a56522b75076c3a6150468c7f290783c521df64de3057

Factory
bc1deae99f3509ec4f93eb45b65d970cef18f569efd22772ca58bfda26d4c545

FIP
852bbc73d48c9ce246846f45e61aba267a6aab88640ccd5dd6fc8ff9deaba7af
```

This verifies that the tested sysupgrade path changed the UBI system area without modifying BL2, u-boot-env, Factory or FIP.

### Network

- MT7531 switch initializes.
- LAN links work.
- WAN `eth1` works at 1 Gbit/s full duplex.
- LAN traffic to OpenWrt has been tested over SSH/ping.
- WAN was re-verified after permanent installation with `carrier=1`, `speed=1000`, `duplex=full`.

### Wi-Fi

- 2.4 GHz radio works.
- 5 GHz radio works.
- The board EEPROM/calibration area is readable from Factory.
- The primary and secondary Wi-Fi MAC locations have been verified directly.
- Per-band NVMEM MAC assignment is verified in initramfs and after permanent NAND installation.

Runtime result:

```text
phy0 <redacted-2.4ghz-mac>
phy1 <redacted-5ghz-mac>
```

Exact device MAC addresses are intentionally omitted from the public wiki; both runtime values matched their respective Factory NVMEM cells exactly.

### LEDs and buttons

Installed-image sysfs names:

```text
blue:mesh
blue:wan
blue:wlan-2ghz
blue:wlan-5ghz
mt76-phy0
mt76-phy1
```

GPIO state confirms:

```text
gpio-512 reset  input high IRQ ACTIVE LOW
gpio-513 wps    input high IRQ ACTIVE LOW
```

Physical LED mapping, WAN activity LED and WPS/Mesh button hotplug events have all been verified.

## Verified initramfs build #4

```text
openwrt-mediatek-filogic-comfast_cf-wr630ax-initramfs-kernel.bin
8746048 bytes (0x857440)
SHA256 9ceca37d2188f1e785d952a2cbb47d8e1b8d993469488b6c8fcd8bab4a18708b
```

U-Boot `iminfo` verified all FIT hashes before boot.

## Historical verified permanent full build

The image lists in this section record earlier hardware-validation builds.
They are retained for auditability and are not the current upstream image set.

```text
kernel.bin
4485820 bytes
SHA256 598499b5616eaa512d8be95f359661ee3edd4372f29e5638bfd941429e820338

sysupgrade.bin
9052439 bytes
SHA256 7ad1a79edf6d419594e837d900e16e00eed81d55e27dc583853759d693fc84be
```

The sysupgrade tar contained `CONTROL`, `kernel` and `root`; `sysupgrade -T` returned 0 before installation.

## Historical verified LuCI build #1

GitHub Actions run **36767167724** completed successfully with the same pinned OpenWrt base, feeds and hardware-fix patch, plus `CONFIG_PACKAGE_luci=y`.

```text
kernel.bin
4485308 bytes
SHA256 6b9ef0a625f27f3abc35319cba6b09f853525d71b598576bef6aae33a9c2b539

sysupgrade.bin
9502999 bytes
SHA256 0ccb08a90c756ed10df3ba317233e69fafb4203d11a1e7afabb062fb093ea1aa
```

The sysupgrade image passed `sysupgrade -T`, was installed successfully, and LuCI was verified operational on the physical router.

## Current OpenWrt main RAM and NAND verification

A separate port to current OpenWrt `main` was first built and booted by TFTP/initramfs without writing NAND. The hardware session verified kernel 6.18.52, board identity, NAND/NMBM/UBI attach, all three LAN ports, WAN at 1 Gbit/s full duplex, both Wi-Fi radios with real associated clients, per-band NVMEM MAC assignment, all front-panel LEDs, and the WPS/Mesh button.

The historical full validation build from OpenWrt `main` commit `c759267c92b0697a6fd6f369164a5ed4c1a6a03c` produced:

```text
kernel.bin
4703880 bytes
SHA256 ecdba4eee1e69647a96faf300aae60929ecd7d9d92652c7701b1f5ee68ee879f

sysupgrade.bin
9369879 bytes
SHA256 610ae53e659a4c5a82308d6a01c2851751e372a53861f12b8087e0c1641b61b7
```

On the router, `sysupgrade -T` returned 0 and the sysupgrade image SHA256 matched again before installation. The image was installed with `sysupgrade -n` and rebooted as OpenWrt SNAPSHOT `r0+36743-c759267c92`, kernel 6.18.52, target `mediatek/filogic`, with `rootfs_type=squashfs`.

After this current-main installation, direct reads of BL2, u-boot-env, Factory and FIP still produced exactly the same SHA256 values listed in the protected-partition section above.

The full sanitized console/test record is preserved at [[Current-main-verification]].

## Completed installation gate

- [x] UART recovery path verified
- [x] U-Boot TFTP boot verified
- [x] Historical support builds reproducibly
- [x] Ethernet verified
- [x] Both Wi-Fi radios verified
- [x] LED mapping verified
- [x] WPS/Mesh button verified
- [x] Factory Wi-Fi MAC offsets verified
- [x] NVMEM MAC fix verified in fresh initramfs
- [x] Full kernel/sysupgrade validation completed with all fixes
- [x] BL2 backup copied off-device and checksummed
- [x] u-boot-env backup copied off-device and checksummed
- [x] Factory backup copied off-device and checksummed twice
- [x] FIP backup copied off-device and checksummed
- [x] OEM UBI backup copied off-device and checksummed
- [x] Exact platform/nand install behavior reviewed
- [x] `sysupgrade -T` passed
- [x] Permanent NAND installation completed
- [x] Protected MTD partitions verified byte-identical afterward
- [x] Normal reboot verified
- [x] Cold boot without UART verified
- [x] LuCI image verified
- [x] Current-main initramfs hardware validation completed
- [x] Current-main kernel/sysupgrade validation completed and inspected
- [x] Current-main `sysupgrade -T` passed with exit status 0
- [x] Current-main permanent NAND installation completed
- [x] Current-main boot verified as `rootfs_type=squashfs`
- [x] Protected MTD hashes re-verified unchanged after current-main flash

## Package ABI warning

The project contains pinned OpenWrt snapshot builds. Snapshot package repositories are rolling, so repository packages can move to newer userspace or kernel ABIs after a firmware image was built.

On the historical image, an attempted `apk add luci` correctly stopped with dependency conflicts before changing the system. The same general snapshot rule still applies to the current-main installation: do not use `apk --force` to cross an ABI mismatch, and build `kmod-*` packages against the exact installed source revision.

## Recovery assets

The stock bootloader provides:

- interactive UART console
- TFTP image loading
- direct FIT `bootm`
- U-Boot boot menu
- Web failsafe entry

The OEM backups provide an additional recovery reference, including two identical independent reads of the unique Factory partition.

## Factory partition safety

The NAND **Factory** partition contains device-specific calibration and MAC
data. Preserve it exactly: do not erase it, format it, or write an OpenWrt
image to it.
