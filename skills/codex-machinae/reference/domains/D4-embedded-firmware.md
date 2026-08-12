## D4 Embedded / Firmware

**Activation trigger.** The project runs on fixed hardware with bounded memory, storage,
or energy; or requires toolchains cross-compiling to a target architecture; or depends on
peripherals (sensors, radios, actuators) whose contracts are captured in the Boundary Contract
Map under the Hardware axis.

**In addition to Core.** Core applies fully — requirements, code quality, testing pyramid,
documentation, CI/CD concepts, boundary contracts, change classification, remediation. This
appendix adds the patterns that only arise when the artefact runs on constrained hardware.

### D4.1 Hardware boundary contracts

Every peripheral (sensor, actuator, radio, display, storage) is an outbound contract in the
Boundary Contract Map (§8, axis `hardware`). The contract entry records:

| Field | Content |
|-------|---------|
| `device` | Part number or family (e.g. `BME280`, `SX1276`) |
| `bus` | Communication bus (I2C, SPI, UART, GPIO, USB, CAN, …) |
| `address` | Bus address or pin assignment |
| `driver` | Source file that owns the abstraction |
| `datasheet` | Path or URL to the canonical datasheet |
| `voltage_level` | Logic-level voltage (e.g. 3.3 V, 5 V) |
| `power_budget_mW` | Typical and peak draw (from datasheet) |

**Hardware Abstraction Layer (HAL).** All peripheral access passes through a thin HAL whose
interface is defined independently of the hardware. Application code never reads a register
or toggles a pin directly. The HAL is the contract boundary: changes to the board layout or
to a peripheral revision affect only the HAL implementation, never the application.

### D4.2 Cross-compilation and toolchain

- The project declares the exact toolchain version (compiler, linker, SDK) in a version-locked
  file (`toolchain.toml`, `platformio.ini`, `west.yml`, or equivalent). The same file is used
  by CI and by every developer.
- The build produces a deterministic binary: same source + same toolchain + same flags = same
  output, byte-for-byte. When full determinism is not achievable, the delta is documented in
  an ADR.
- Binary size is tracked as a ratchet (§5.3 pattern): a CI step compares the artefact size
  against a committed baseline. A regression beyond a declared threshold (e.g. +2%) fails
  the build unless the increase is justified in the commit message.

### D4.3 Hardware-in-the-loop (HIL) testing

Core §5 testing pyramid applies. This section adds the tier that can only run on real hardware
or a cycle-accurate simulator.

**HIL tier placement.** HIL tests sit above integration tests in the pyramid. They are slower
and more expensive; they run on merge to `main` or on a nightly schedule, not on every push.

**What HIL tests cover:**

| Category | Example |
|----------|---------|
| Peripheral I/O | Sensor reads return plausible values; actuator commands reach the device |
| Timing | ISR latency stays within the declared deadline |
| Power state transitions | Sleep → wake → resume produces the correct peripheral state |
| Communication protocols | Full frame exchange on bus (CAN, I2C, SPI) with a real or loopback peer |
| Firmware update | OTA or flash-based update completes and the device boots the new image |

**HIL infrastructure.** The CI runner has access to a physical board (or a farm of boards)
via a debug probe (J-Link, ST-Link, OpenOCD, or equivalent). The runner flashes the artefact,
executes the test suite over the debug channel, and collects results. If no physical board is
available, a cycle-accurate simulator (QEMU with the correct machine model, Renode, or vendor
simulator) is an acceptable substitute — but the substitution is recorded in the contract map
so the team knows which contracts are verified on real hardware and which on simulation.

### D4.4 Flash and OTA update strategy

- **Image signing.** Every firmware image is signed before distribution. The bootloader
  verifies the signature before applying the update. Unsigned images are rejected.
- **A/B partitioning.** The device maintains two firmware slots (A and B). The new image is
  written to the inactive slot. If the boot self-test fails, the bootloader reverts to the
  previous slot automatically.
- **Rollback trigger.** The application reports "healthy" to the bootloader within a
  configurable window after first boot (watchdog or explicit confirmation). If the window
  expires without confirmation, the bootloader treats the update as failed and reverts.
- **OTA transport.** When the device has network connectivity, updates are delivered over an
  encrypted channel (TLS 1.2+). The update payload includes a manifest with version, size,
  SHA-256 hash, and signature. The device verifies the manifest before downloading the image.
- **Offline update.** When no network is available, updates are delivered via removable media
  (SD card, USB). The same signing and verification rules apply.
- **Version contract.** The running firmware version is always queryable (via a debug command,
  a status register, or an API endpoint). The version string follows the project's tagging
  convention (§3.8).

### D4.5 Power and thermal budgets

**Power budget.** The project maintains a power budget document (`docs/power-budget.md` or
equivalent) that lists every component's draw in each operating mode:

| Component | Sleep (mW) | Idle (mW) | Active (mW) | Peak (mW) | Source |
|-----------|-----------|-----------|-------------|-----------|--------|
| MCU | — | — | — | — | Datasheet §X.Y |
| Radio | — | — | — | — | Datasheet §X.Y |
| Sensor A | — | — | — | — | Measured |
| … | | | | | |
| **Total** | — | — | — | — | |

The budget is validated against the power source (battery capacity, solar harvest rate, USB
supply) to derive a minimum operating life. Any change that adds a component or increases
duty cycle updates the budget document and verifies that the operating-life target still holds.

**Thermal budget.** When the system operates in an enclosure or in an environment with
constrained dissipation, the same table includes a thermal column (junction temperature at
steady state). The thermal budget is validated by measurement during HIL testing (D4.3) or
by thermal simulation.

### D4.6 Bring-up checklist

When a new board revision arrives, the following checklist is executed before any application
code runs. Each step is recorded in `docs/bring-up/<board-rev>.md`.

- [ ] Visual inspection: correct components populated, no solder bridges
- [ ] Power rail verification: each rail within ±5% of nominal at no-load
- [ ] Programmer connection: debug probe communicates with the MCU
- [ ] Bootloader flash: bootloader boots, serial/debug console active
- [ ] Peripheral smoke test: each peripheral responds to a basic read/write
- [ ] Clock verification: system clock within ±50 ppm of expected frequency
- [ ] Power measurement: idle and active draw match the power budget (D4.5) within ±15%
- [ ] Firmware flash: full application boots on the new board
- [ ] HIL suite pass: all D4.3 tests pass on the new revision

