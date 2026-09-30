# Verification and safety

The working rule for this project is: **verify in RAM first, write flash last**.

## What has been verified

### Boot path

- UART console works bidirectionally.
- U-Boot TFTP works.
- OpenWrt FIT metadata and hashes validate in U-Boot.
- Initramfs boots entirely from DRAM.
- Linux identifies the board as COMFAST CF-WR630AX.

### Storage

- SPI-NAND is detected.
- NMBM attaches.
- UBI attaches.
- No permanent write is required for the current test cycle.

### Network

- MT7531 switch initializes.
- LAN links work.
- WAN `eth1` link works at 1 Gbit/s full duplex.
- LAN traffic to OpenWrt has been tested over SSH/ping.

### Wi-Fi

- 2.4 GHz radio works.
- 5 GHz radio works.
- The board EEPROM/calibration area is readable from Factory.
- The primary and secondary Wi-Fi MAC locations have been verified directly.
- Per-band NVMEM MAC assignment is verified in a fresh initramfs boot.
- Runtime result is `phy0 = 40:a5:ef:45:cb:41` and `phy1 = 40:a5:ef:45:cb:42`.

### LEDs and buttons

- Physical LED GPIO mapping is verified.
- WAN link/activity LED works.
- GPIO1 is physically the WPS/Mesh button.
- `KEY_WPS_BUTTON` produces correct OpenWrt pressed/released hotplug events.

## Verified initramfs build #4

```text
openwrt-mediatek-filogic-comfast_cf-wr630ax-initramfs-kernel.bin
8746048 bytes (0x857440)
SHA256 9ceca37d2188f1e785d952a2cbb47d8e1b8d993469488b6c8fcd8bab4a18708b
```

U-Boot `iminfo` verified all FIT hashes before boot.

This image contains the hardware-fix patch with:

- corrected LED definitions
- WPS/Mesh button fix
- WAN LED trigger
- per-band Wi-Fi NVMEM MAC cells
- removal of the WR630AX runtime Wi-Fi MAC hotplug workaround

## Current gate before permanent flashing

Permanent installation remains blocked until all of the following are true:

- [x] UART recovery path verified
- [x] U-Boot TFTP boot verified
- [x] Historical support builds reproducibly
- [x] Ethernet verified
- [x] Both Wi-Fi radios verified
- [x] LED mapping verified
- [x] WPS/Mesh button verified
- [x] Factory Wi-Fi MAC offsets verified
- [x] NVMEM MAC fix verified in a fresh initramfs boot
- [ ] New full factory/sysupgrade images built with all fixes
- [ ] BL2 backup copied off-device and checksummed
- [ ] u-boot-env backup copied off-device and checksummed
- [ ] Factory backup copied off-device and checksummed
- [ ] FIP backup copied off-device and checksummed
- [ ] OEM UBI backup copied off-device and checksummed
- [ ] Exact platform install/recovery behavior reviewed

## Recovery assets already verified

The stock bootloader provides multiple recovery paths, including:

- interactive UART console
- TFTP image loading
- direct FIT `bootm`
- U-Boot menu
- Web failsafe entry in the boot menu

That makes RAM-based testing low-risk compared with writing bootloader or Factory partitions.

## Never do this during current testing

Do not run NAND erase/write commands merely to "try" an image.

In particular, never erase or overwrite:

```text
Factory
```

That partition contains device-specific radio calibration and MAC information.

## Factory partition vs OpenWrt factory image

These names are unfortunately easy to confuse:

- **NAND `Factory` partition** → calibration/MAC data; preserve it.
- **OpenWrt `factory.bin`** → an installation image format.

They are completely different things.
