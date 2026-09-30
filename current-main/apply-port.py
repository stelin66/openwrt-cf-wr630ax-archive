#!/usr/bin/env python3
from pathlib import Path

def insert_once(path, anchor, text):
    p = Path(path)
    data = p.read_text()
    if text.strip() in data:
        return
    if anchor not in data:
        raise SystemExit(f"anchor not found in {path}: {anchor!r}")
    p.write_text(data.replace(anchor, text + anchor, 1))

# Image definition. Keep the stock WR630AX NAND/UBI layout and proven FIT load addresses.
filogic = Path("target/linux/mediatek/image/filogic.mk")
data = filogic.read_text()
if "define Device/comfast_cf-wr630ax\n" not in data:
    anchor = "define Device/confiabits_mt7981\n"
    block = """define Device/comfast_cf-wr630ax
  DEVICE_VENDOR := COMFAST
  DEVICE_MODEL := CF-WR630AX
  DEVICE_DTS := mt7981b-comfast-cf-wr630ax
  DEVICE_DTS_DIR := ../dts
  DEVICE_DTC_FLAGS := --pad 4096
  DEVICE_DTS_LOADADDR := 0x43f00000
  DEVICE_PACKAGES := kmod-mt7915e kmod-mt7981-firmware mt7981-wo-firmware
  KERNEL_LOADADDR := 0x44000000
  KERNEL := kernel-bin | lzma | \\
       fit lzma $$(KDIR)/image-$$(firstword $$(DEVICE_DTS)).dtb
  KERNEL_INITRAMFS := kernel-bin | lzma | \\
       fit lzma $$(KDIR)/image-$$(firstword $$(DEVICE_DTS)).dtb with-initrd
  UBINIZE_OPTS := -E 5
  BLOCKSIZE := 128k
  PAGESIZE := 2048
  IMAGE_SIZE := 65536k
  KERNEL_IN_UBI := 1
  IMAGES := sysupgrade.bin factory.bin
  IMAGE/factory.bin := append-ubi | check-size $$$$(IMAGE_SIZE)
  IMAGE/sysupgrade.bin := sysupgrade-tar | append-metadata
endef
TARGET_DEVICES += comfast_cf-wr630ax

"""
    if anchor not in data:
        raise SystemExit("filogic.mk insertion anchor not found")
    filogic.write_text(data.replace(anchor, block + anchor, 1))

# WR630AX has lan1/lan2/lan3 via MT7531 and WAN on gmac1/eth1.
network = Path("target/linux/mediatek/filogic/base-files/etc/board.d/02_network")
data = network.read_text()
if "comfast,cf-wr630ax|\\\n" not in data:
    anchor = "\tabt,asr3000|\\\n"
    if anchor not in data:
        raise SystemExit("02_network insertion anchor not found")
    network.write_text(data.replace(anchor, anchor + "\tcomfast,cf-wr630ax|\\\n", 1))

# Physical WAN LED was verified on GPIO13 and follows gmac1/eth1.
leds = Path("target/linux/mediatek/filogic/base-files/etc/board.d/01_leds")
data = leds.read_text()
case = """comfast,cf-wr630ax)
\tucidef_set_led_netdev "wan" "WAN" "blue:wan" "eth1" "link tx rx"
\t;;
"""
if "comfast,cf-wr630ax)" not in data:
    anchor = "comfast,cf-wa933|\\\n"
    if anchor not in data:
        raise SystemExit("01_leds insertion anchor not found")
    leds.write_text(data.replace(anchor, case + anchor, 1))

# Stock environment is a 512 KiB MTD partition with 128 KiB environment size.
env = Path("package/boot/uboot-tools/uboot-envtools/files/mediatek_filogic")
data = env.read_text()
if "comfast,cf-wr630ax|\\\n" not in data:
    anchor = "comfast,cf-e393ax|\\\n"
    if anchor not in data:
        raise SystemExit("uboot-envtools insertion anchor not found")
    env.write_text(data.replace(anchor, "comfast,cf-wr630ax|\\\n" + anchor, 1))

# Guardrails: no legacy WR630AX Wi-Fi MAC hotplug workaround.
hotplug = Path("target/linux/mediatek/filogic/base-files/etc/hotplug.d/ieee80211/11_fix_wifi_mac")
if "comfast,cf-wr630ax)" in hotplug.read_text():
    raise SystemExit("unexpected legacy WR630AX Wi-Fi MAC hotplug rule present")
