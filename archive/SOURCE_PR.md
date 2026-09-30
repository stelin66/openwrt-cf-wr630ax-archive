# Source: OpenWrt PR #20654

Title: mediatek: add support for Comfast CF-WR633AX CF-WR630AX  CF-WR631AX
PR submitter: ddf29
Device-support commit author: dingjie <DW22965391@outlook.com>
Original CF-WR630AX commit: 17c723ea611972b57d648dbe6e44fe46188e7d30
Created: 2025-11-05T02:41:20Z
Updated: 2025-12-09T13:24:20Z
Closed: 2025-11-06T08:22:19Z
Merged: false
Base commit: 7670addb077d7556a5603f0b26e2bad1b052ae84
Head commit: cd4e07f7b7ec8e26857f18606b7261c334a4a4c0

## Attribution note

The public PR history shows that GitHub account `ddf29` submitted and handled PR #20654, while the actual device-support commits for CF-WR633AX, CF-WR630AX and CF-WR631AX are authored and signed off by `dingjie <DW22965391@outlook.com>`.

This archive therefore does not label `ddf29` as the code author. The relationship between the GitHub account `ddf29` and the Git identity `dingjie` is not established by the public history.

## Original PR description

This commit adds support for Comfast CF-WR633AX CF-WR630AX  CF-WR631AX models.

Hardware
--------
Comfast CF-WR633AX
SOC: MediaTek MT7981A
RAM: 256MB
FLASH: 128MB SPI-NAND (Winbond)
WIFI 2.4G: (Embedded in SOC) b/g/n/ax, MIMO 4x4
WIFI 5G: (Embedded in SOC) a/n/ac/ax, MIMO 4x4
ETHERNET: 1GbE MT7981 (eth1: WAN)
ETHERNET: MediaTek MT7531AE 4xGbE (lan1 lan2 lan3 lan4)
UART: 3.3V 115200 8N1

Comfast CF-WR630AX
SOC: MediaTek MT7981B
RAM: 256MB
FLASH: 128MB SPI-NAND (Winbond)
WIFI 2.4G: (Embedded in SOC) b/g/n/ax, MIMO 4x4
WIFI 5G: (Embedded in SOC) a/n/ac/ax, MIMO 4x4
ETHERNET: 1GbE MT7981 (eth1: WAN)
ETHERNET: MediaTek MT7531AE 3xGbE (lan1 lan2 lan3)
UART: 3.3V 115200 8N1

Comfast CF-WR631AX
SOC: MediaTek MT7981B
RAM: 256MB
FLASH: 128MB SPI-NAND (Winbond)
WIFI 2.4G: (Embedded in SOC) b/g/n/ax, MIMO 4x4
WIFI 5G: (Embedded in SOC) a/n/ac/ax, MIMO 4x4
ETHERNET: 1GbE MT7531AE (WAN)
ETHERNET: MediaTek MT7531AE 3xGbE (lan1 lan2 lan3)
UART: 3.3V 115200 8N1
