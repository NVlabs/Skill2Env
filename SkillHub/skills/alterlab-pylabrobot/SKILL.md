---
name: alterlab-pylabrobot
description: Programs lab automation with PyLabRobot, a vendor-agnostic Python framework that unifies control across Hamilton, Tecan, Opentrons, plate readers, and pumps, with simulation support. Use when controlling multiple equipment types or needing unified cross-vendor programming for complex, multi-vendor liquid-handling workflows. For Opentrons-only protocols with the official API, alterlab-opentrons may be simpler. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(curl:*) Bash(python:*)
compatibility: Requires the pylabrobot Python package (pip install pylabrobot); runs against the built-in simulator without hardware, real runs need supported devices (Hamilton, Tecan, Opentrons, plate readers, pumps)
metadata:
    skill-author: AlterLab
    version: "1.1.0"
---

# PyLabRobot

## Overview

PyLabRobot is a hardware-agnostic, pure Python Software Development Kit for automated and autonomous laboratories. Use this skill to control liquid handling robots, plate readers, pumps, heater shakers, incubators, centrifuges, and other laboratory automation equipment through a unified Python interface that works across platforms (Windows, macOS, Linux).

## When to Use This Skill

Use this skill when:
- Programming liquid handling robots (Hamilton STAR/STARlet, Opentrons OT-2, Tecan EVO)
- Automating laboratory workflows involving pipetting, sample preparation, or analytical measurements
- Managing deck layouts and laboratory resources (plates, tips, containers, troughs)
- Integrating multiple lab devices (liquid handlers, plate readers, heater shakers, pumps)
- Creating reproducible laboratory protocols with state management
- Simulating protocols before running on physical hardware
- Reading plates using BMG CLARIOstar or other supported plate readers
- Controlling temperature, shaking, centrifugation, or other material handling operations
- Working with laboratory automation in Python

## Core Capabilities

PyLabRobot provides comprehensive laboratory automation through six main capability areas, each detailed in the references/ directory:

### 1. Liquid Handling (`references/liquid-handling.md`)

Control liquid handling robots for aspirating, dispensing, and transferring liquids. Key operations include:
- **Basic Operations**: Aspirate, dispense, transfer liquids between wells
- **Tip Management**: Pick up, drop, and track pipette tips automatically
- **Advanced Techniques**: Multi-channel pipetting, serial dilutions, plate replication
- **Volume Tracking**: Automatic tracking of liquid volumes in wells
- **Hardware Support**: Hamilton STAR/STARlet, Opentrons OT-2, Tecan EVO, and others

### 2. Resource Management (`references/resources.md`)

Manage laboratory resources in a hierarchical system:
- **Resource Types**: Plates, tip racks, troughs, tubes, carriers, and custom labware
- **Deck Layout**: Assign resources to deck positions with coordinate systems
- **State Management**: Track tip presence, liquid volumes, and resource states
- **Serialization**: Save and load deck layouts and states from JSON files
- **Resource Discovery**: Access wells, tips, and containers through intuitive APIs

### 3. Hardware Backends (`references/hardware-backends.md`)

Connect to diverse laboratory equipment through backend abstraction:
- **Liquid Handlers**: Hamilton STAR (full support), Opentrons OT-2, Tecan EVO
- **Simulation**: ChatterboxBackend for protocol testing without hardware
- **Platform Support**: Works on Windows, macOS, Linux, and Raspberry Pi
- **Backend Switching**: Change robots by swapping backend without rewriting protocols

### 4. Analytical Equipment (`references/analytical-equipment.md`)

Integrate plate readers and analytical instruments:
- **Plate Readers**: BMG CLARIOstar for absorbance, luminescence, fluorescence
- **Scales**: Mettler Toledo integration for mass measurements
- **Integration Patterns**: Combine liquid handlers with analytical equipment
- **Automated Workflows**: Move plates between devices automatically

### 5. Material Handling (`references/material-handling.md`)

Control environmental and material handling equipment:
- **Heater Shakers**: Hamilton HeaterShaker, Inheco ThermoShake
- **Incubators**: Inheco and Thermo Fisher incubators with temperature control
- **Centrifuges**: Agilent VSpin with bucket positioning and spin control
- **Pumps**: Cole Parmer Masterflex for fluid pumping operations
- **Temperature Control**: Set and monitor temperatures during protocols

### 6. Visualization & Simulation (`references/visualization.md`)

Visualize and simulate laboratory protocols:
- **Browser Visualizer**: Real-time 3D visualization of deck state
- **Simulation Mode**: Test protocols without physical hardware
- **State Tracking**: Monitor tip presence and liquid volumes visually
- **Deck Editor**: Graphical tool for designing deck layouts
- **Protocol Validation**: Verify protocols before running on hardware

## Quick Start

To get started with PyLabRobot, install the package and initialize a liquid handler. PyLabRobot is async — all device calls are `await`ed and must run inside an event loop (`asyncio.run(...)` or a Jupyter cell).

```python
# uv pip install pylabrobot

from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STARBackend
from pylabrobot.resources import (
    STARLetDeck,
    TIP_CAR_480_A00,            # tip CARRIER (holds racks at sites [0]..[4])
    PLT_CAR_L5AC_A00,           # plate carrier
    hamilton_96_tiprack_1000uL_filter,
    Cor_96_wellplate_360ul_Fb,
)

lh = LiquidHandler(backend=STARBackend(), deck=STARLetDeck())
await lh.setup()

# Labware is two-level: a rack/plate goes into a carrier site, then the
# carrier is assigned to a deck rail. Carriers are NOT indexed for wells/tips.
tip_car = TIP_CAR_480_A00(name="tip_carrier")
tip_car[0] = tip_rack = hamilton_96_tiprack_1000uL_filter(name="tips_01")
lh.deck.assign_child_resource(tip_car, rails=3)

plt_car = PLT_CAR_L5AC_A00(name="plate_carrier")
plt_car[0] = plate = Cor_96_wellplate_360ul_Fb(name="plate_01")
lh.deck.assign_child_resource(plt_car, rails=15)

# Basic operations
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.aspirate(plate["A1"], vols=[100])
await lh.dispense(plate["A2"], vols=[100])
await lh.drop_tips()
```

## Working with References

Load the matching file in `references/` for task-specific examples and API patterns. The "Core Capabilities" list above maps each capability area to its reference file.

## Best Practices

When creating laboratory automation protocols with PyLabRobot:

1. **Start with Simulation**: Use ChatterboxBackend and the visualizer to test protocols before running on hardware
2. **Enable Tracking**: Turn on tip tracking and volume tracking for accurate state management
3. **Resource Naming**: Use clear, descriptive names for all resources (plates, tip racks, containers)
4. **State Serialization**: Save deck layouts and states to JSON for reproducibility
5. **Error Handling**: Implement proper async error handling for hardware operations
6. **Temperature Control**: Set temperatures early as heating/cooling takes time
7. **Modular Protocols**: Break complex workflows into reusable functions
8. **Documentation**: Reference official docs at https://docs.pylabrobot.org for latest features

## Common Workflows

### Liquid Transfer Protocol

`lh.transfer(source, targets, ...)` distributes from ONE source well to MANY target
wells; it takes `source_vol` or `target_vols` (NOT `vols`, NOT `dest=`). For a
parallel column-to-column move, drive `aspirate`/`dispense` directly with list `vols`.

```python
# Setup
lh = LiquidHandler(backend=STARBackend(), deck=STARLetDeck())
await lh.setup()

# Define carriers + labware (rack/plate -> carrier site -> deck rail)
tip_car = TIP_CAR_480_A00(name="tip_carrier")
tip_car[0] = tip_rack = hamilton_96_tiprack_1000uL_filter(name="tips_01")
lh.deck.assign_child_resource(tip_car, rails=1)

plt_car = PLT_CAR_L5AC_A00(name="plate_carrier")
plt_car[0] = source = Cor_96_wellplate_360ul_Fb(name="source")
plt_car[1] = dest = Cor_96_wellplate_360ul_Fb(name="dest")
lh.deck.assign_child_resource(plt_car, rails=15)

# One-to-many distribute: 100 uL from source A1 into the first column of dest
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(source["A1"], dest["A1:H1"], source_vol=100)
await lh.drop_tips()

# Parallel 8-channel column copy via aspirate + dispense
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.aspirate(source["A1:H1"], vols=[100] * 8)
await lh.dispense(dest["A1:H1"], vols=[100] * 8)
await lh.drop_tips()
```

### Plate Reading Workflow

```python
# Setup plate reader
from pylabrobot.plate_reading import PlateReader
from pylabrobot.plate_reading.clario_star_backend import CLARIOstarBackend

pr = PlateReader(name="CLARIOstar", backend=CLARIOstarBackend(), size_x=0, size_y=0, size_z=0)
await pr.setup()

# Set temperature and read
await pr.set_temperature(37)
await pr.open()
# (manually or robotically load plate)
await pr.close()
data = await pr.read_absorbance(wavelength=450)
```

## Additional Resources

- **Official Documentation**: https://docs.pylabrobot.org
- **GitHub Repository**: https://github.com/PyLabRobot/pylabrobot
- **Community Forum**: https://discuss.pylabrobot.org
- **PyPI Package**: https://pypi.org/project/PyLabRobot/

For detailed usage of specific capabilities, refer to the corresponding reference file in the `references/` directory.

