# Provenance and attribution

This project intentionally separates the **archived original support** from later hardware-verification work.

## Original OpenWrt pull request

- Upstream: `openwrt/openwrt`
- Pull request: [#20654](https://github.com/openwrt/openwrt/pull/20654)
- Title: `mediatek: add support for Comfast CF-WR633AX CF-WR630AX CF-WR631AX`
- Base commit: `7670addb077d7556a5603f0b26e2bad1b052ae84`
- PR head: `cd4e07f7b7ec8e26857f18606b7261c334a4a4c0`
- PR state when archived: closed, not merged

## Authorship

The public Git history records:

- **PR submitter / GitHub handler:** `ddf29`
- **Device-support commit author:** `dingjie <DW22965391@outlook.com>`
- **CF-WR630AX support commit:** `17c723ea611972b57d648dbe6e44fe46188e7d30`

The public record does not establish the relationship between the GitHub account `ddf29` and the Git identity `dingjie`. This archive therefore does not claim they are the same person or different people.

Original authorship is preserved exactly as recorded.

## Archived material

The repository preserves:

- the complete original PR patch
- snapshots of all files touched by the PR
- the original PR metadata/description
- the exact historical OpenWrt base
- pinned feed revisions for reproducible builds

See:

- [`archive/openwrt-pr-20654.patch`](../archive/openwrt-pr-20654.patch)
- [`archive/SOURCE_PR.md`](../archive/SOURCE_PR.md)

## Later hardware verification

Hardware corrections are deliberately separate from the archived original:

- LED GPIO/function fixes
- WPS/Mesh button correction
- WAN LED trigger
- Wi-Fi MAC/NVMEM correction

They are maintained in:

[`archive/cf-wr630ax-hwfix-v1.patch`](../archive/cf-wr630ax-hwfix-v1.patch)

This keeps the historical source auditable while making it clear which changes were derived from later measurements on real hardware.
