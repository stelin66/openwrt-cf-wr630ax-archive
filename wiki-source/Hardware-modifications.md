# Hardware modifications

This page is a build log for planned physical modifications to the COMFAST CF-WR630AX test unit.

> [!IMPORTANT]
> These are **hardware modification notes**, separate from the OpenWrt firmware verification.
> Nothing on this page changes the current rule: firmware is tested from RAM first, and NAND is not written until the recovery/install path has been fully verified.

## Planned enclosure rebuild

The stock plastic enclosure is much larger than the PCB requires. The planned rebuild is a compact aluminium enclosure with external SMA antenna connectors.

Goals:

- smaller enclosure
- rigid mechanical construction
- aluminium chassis as RF shielding
- proper external antenna connectors
- short, controlled 50 Ω RF paths
- passive cooling with the option to thermally couple the existing heatsink to the chassis

## RF layout

The board has four antenna feeds.

Planned external arrangement:

| Group | Antennas |
|---|---|
| 2.4 GHz | 2 × dedicated 2.4 GHz antennas |
| 5 GHz | 2 × dedicated 5 GHz antennas |

The intended layout is two antennas on one side of the enclosure and two on the other, with as much practical spacing as the enclosure allows.

Dedicated single-band antennas are preferred here rather than four dual-band antennas, provided the RF chains are positively identified before the original coax is removed.

## Original coax

At least one of the factory coax leads shows a very sharp bend close to the PCB solder point.

That does **not** prove the centre conductor is broken, but at microwave frequencies a damaged or badly deformed coax section can still cause:

- centre-conductor damage
- displaced or damaged shield
- crushed dielectric
- impedance discontinuity
- increased return loss / insertion loss
- mechanical stress on the PCB RF launch

Because the enclosure is being rebuilt anyway, the current plan is to remove the factory coax assembly rather than reuse it.

## Before desoldering anything

The four original RF connections must be documented first.

Record:

1. PCB connection position
2. original cable route
3. which physical antenna it reaches
4. band / radio assignment once verified
5. chain order within the band if it can be identified

Temporary labels:

```text
RF1
RF2
RF3
RF4
```

Take clear photographs before and after marking them.

The purpose is to preserve enough information to restore the original mapping if later RF measurements show an unexpected result.

## SMA conversion

Planned construction:

- 4 × chassis-mounted 50 Ω SMA connectors
- short internal 50 Ω coax runs
- gentle bend radius
- strain relief so no cable load reaches the PCB RF pads
- solid mechanical bonding of SMA connector bodies to the aluminium chassis

The PCB RF launch areas should not carry the mechanical load of the external connectors.

## Chassis / RF ground

The aluminium enclosure will provide a conductive RF shield around the board.

The SMA connector bodies will naturally bond their coax shields to the chassis when properly mounted.

The final PCB-to-chassis bonding arrangement should be decided after inspecting the board mounting, Ethernet connector shields and DC input grounding. At GHz frequencies, low-inductance chassis bonding matters more than treating the enclosure like a low-frequency single-point-ground exercise.

## Cooling

The current board already uses a substantial passive heatsink.

Before modifying the thermal path:

1. finish firmware validation
2. measure SoC / Wi-Fi temperatures at idle
3. measure temperatures under sustained Ethernet and Wi-Fi load
4. only then decide whether the heatsink should be thermally coupled to the aluminium enclosure

The aluminium enclosure may provide a useful additional heat-spreading surface, but the need should be established by measurement first.

## Status

| Item | Status |
|---|:---:|
| Compact aluminium enclosure selected | 🧪 planned |
| Four SMA positions planned | 🧪 planned |
| 2.4/5 GHz RF-chain identification | ⏳ not yet documented |
| Original coax removal | ⏳ not started |
| SMA conversion | ⏳ not started |
| Thermal measurements | ⏳ not started |
| Chassis thermal coupling | ⏳ undecided |

---

This page should be updated with photographs, measurements and exact RF-chain mapping before the original antenna wiring is removed.
