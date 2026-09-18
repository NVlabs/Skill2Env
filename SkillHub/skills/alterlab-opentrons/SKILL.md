---
name: alterlab-opentrons
description: Writes liquid-handling protocols for Opentrons OT-2 and Flex robots using the official Opentrons Protocol API v2, with full access to v2 features for production-grade, officially compatible protocols. Use when authoring or running protocols specifically for Opentrons hardware. For multi-vendor automation or broader equipment control use pylabrobot instead. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(curl:*) Bash(python:*)
compatibility: Requires the opentrons Python package (pip install opentrons); protocols simulate locally via opentrons_simulate, execution needs an Opentrons OT-2 or Flex robot
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Opentrons Integration

## Overview

Opentrons is a Python-based lab automation platform for Flex and OT-2 robots. Write Protocol API v2 protocols for liquid handling, control hardware modules (heater-shaker, thermocycler), manage labware, for automated pipetting workflows.

## When to Use This Skill

This skill should be used when:
- Writing Opentrons Protocol API v2 protocols in Python
- Automating liquid handling workflows on Flex or OT-2 robots
- Controlling hardware modules (temperature, magnetic, heater-shaker, thermocycler)
- Setting up labware configurations and deck layouts
- Implementing complex pipetting operations (serial dilutions, plate replication, PCR setup)
- Managing tip usage and optimizing protocol efficiency
- Working with multi-channel pipettes for 96-well plate operations
- Simulating and testing protocols before robot execution

## Core Capabilities

### 1. Protocol Structure and Metadata

Every Opentrons protocol follows a standard structure:

```python
from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@example.com>',
    'description': 'Protocol description',
    'apiLevel': '2.19'  # Pin to a level your robot's app/firmware accepts
}

# Requirements (optional). When present, apiLevel here takes precedence over the
# value in metadata, and robotType is required for Flex.
requirements = {
    'robotType': 'Flex',  # or 'OT-2'
    'apiLevel': '2.19'
}

# Run function
def run(protocol: protocol_api.ProtocolContext):
    # Protocol commands go here
    pass
```

**Key elements:**
- Import `protocol_api` from `opentrons`
- Define `metadata` dict with protocolName, author, description, apiLevel
- Optional `requirements` dict for robot type and API version
- Implement `run()` function receiving `ProtocolContext` as parameter
- All protocol logic goes inside the `run()` function

### 2. Loading Hardware

**Loading Instruments (Pipettes):**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Load pipette on specific mount
    left_pipette = protocol.load_instrument(
        'flex_1channel_1000',  # Instrument name (Flex convention)
        'left',                # Mount: 'left' or 'right'
        tip_racks=[tip_rack]   # List of tip rack labware objects
    )
```

Common pipette load names (these are the exact `instrument_name` strings — do NOT invent
`p1000_single_flex`-style names; Flex uses the `flex_<channels>_<volume>` convention):
- Flex: `flex_1channel_50`, `flex_1channel_1000`, `flex_8channel_50`, `flex_8channel_1000`, `flex_96channel_1000`
- OT-2: `p20_single_gen2`, `p300_single_gen2`, `p1000_single_gen2`, `p20_multi_gen2`, `p300_multi_gen2`

**Loading Labware:**

```python
# Load labware directly on deck
plate = protocol.load_labware(
    'corning_96_wellplate_360ul_flat',  # Labware API name
    'D1',                                # Deck slot (Flex: A1-D3, OT-2: 1-11)
    label='Sample Plate'                 # Optional display label
)

# Load tip rack
tip_rack = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'C1')

# Load labware on adapter
adapter = protocol.load_adapter('opentrons_flex_96_tiprack_adapter', 'B1')
tips = adapter.load_labware('opentrons_flex_96_tiprack_200ul')
```

**Loading Modules:**

```python
# Temperature module (Flex + OT-2)
temp_module = protocol.load_module('temperature module gen2', 'D3')
temp_plate = temp_module.load_labware('corning_96_wellplate_360ul_flat')

# Heater-Shaker module (Flex + OT-2)
hs_module = protocol.load_module('heaterShakerModuleV1', 'D1')
hs_plate = hs_module.load_labware('corning_96_wellplate_360ul_flat')

# Thermocycler module (takes up specific slots automatically)
tc_module = protocol.load_module('thermocyclerModuleV2')
tc_plate = tc_module.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

# Magnetic Module (OT-2 ONLY) — an active, motorized module. Flex does not
# support it; on Flex use the unpowered Magnetic Block instead (see below).
mag_module = protocol.load_module('magnetic module gen2', '1')  # OT-2 numeric slot
mag_plate = mag_module.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

# Magnetic Block (Flex ONLY) — unpowered; labware is moved on/off it with the
# Gripper. There is no engage/disengage; it has no motors.
mag_block = protocol.load_module('magneticBlockV1', 'C2')
block_plate = mag_block.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
```

### 3. Liquid Handling Operations

**Basic Operations:**

```python
# Pick up tip
pipette.pick_up_tip()

# Aspirate (draw liquid in)
pipette.aspirate(
    volume=100,           # Volume in µL
    location=source['A1'] # Well or location object
)

# Dispense (expel liquid)
pipette.dispense(
    volume=100,
    location=dest['B1']
)

# Drop tip
pipette.drop_tip()

# Return tip to rack
pipette.return_tip()
```

**Complex Operations:**

```python
# Transfer (combines pick_up, aspirate, dispense, drop_tip)
pipette.transfer(
    volume=100,
    source=source_plate['A1'],
    dest=dest_plate['B1'],
    new_tip='always'  # 'always', 'once', or 'never'
)

# Distribute (one source to multiple destinations)
pipette.distribute(
    volume=50,
    source=reservoir['A1'],
    dest=[plate['A1'], plate['A2'], plate['A3']],
    new_tip='once'
)

# Consolidate (multiple sources to one destination)
pipette.consolidate(
    volume=50,
    source=[plate['A1'], plate['A2'], plate['A3']],
    dest=reservoir['A1'],
    new_tip='once'
)
```

**Advanced Techniques:**

```python
# Mix (aspirate and dispense in same location)
pipette.mix(
    repetitions=3,
    volume=50,
    location=plate['A1']
)

# Air gap (prevent dripping)
pipette.aspirate(100, source['A1'])
pipette.air_gap(20)  # 20µL air gap
pipette.dispense(120, dest['A1'])

# Blow out (expel remaining liquid)
pipette.blow_out(location=dest['A1'].top())

# Touch tip (remove droplets on tip exterior)
pipette.touch_tip(location=plate['A1'])
```

**Flow Rate Control:**

```python
# Set flow rates (µL/s)
pipette.flow_rate.aspirate = 150
pipette.flow_rate.dispense = 300
pipette.flow_rate.blow_out = 400
```

### 4. Accessing Wells and Locations

**Well Access Methods:**

```python
# By name
well_a1 = plate['A1']

# By index
first_well = plate.wells()[0]

# All wells
all_wells = plate.wells()  # Returns list

# By rows
rows = plate.rows()  # Returns list of lists
row_a = plate.rows()[0]  # All wells in row A

# By columns
columns = plate.columns()  # Returns list of lists
column_1 = plate.columns()[0]  # All wells in column 1

# Wells by name (dictionary)
wells_dict = plate.wells_by_name()  # {'A1': Well, 'A2': Well, ...}
```

**Location Methods:**

```python
# Top of well (default: 1mm below top)
pipette.aspirate(100, well.top())
pipette.aspirate(100, well.top(z=5))  # 5mm above top

# Bottom of well (default: 1mm above bottom)
pipette.aspirate(100, well.bottom())
pipette.aspirate(100, well.bottom(z=2))  # 2mm above bottom

# Center of well
pipette.aspirate(100, well.center())
```

### 5. Hardware Module Control

Control temperature, magnetic, heater-shaker, thermocycler, and absorbance-reader modules. Each module context exposes its own set / wait / deactivate methods plus status properties (e.g. `temp_module.set_temperature`, `hs_module.set_and_wait_for_shake_speed`, `tc_module.execute_profile`). On Flex, the active Magnetic Module is replaced by the unpowered Magnetic Block (`magneticBlockV1`).

Full per-module code recipes (Temperature, Magnetic Module vs Flex Magnetic Block, Heater-Shaker, Thermocycler PCR cycling, Absorbance Plate Reader): see `references/hardware_modules.md`. The corresponding method/property tables are in `references/api_reference.md`.

### 6. Liquid Tracking and Labeling

**Define Liquids:**

```python
# Define liquid types
water = protocol.define_liquid(
    name='Water',
    description='Ultrapure water',
    display_color='#0000FF'  # Hex color code
)

sample = protocol.define_liquid(
    name='Sample',
    description='Cell lysate sample',
    display_color='#FF0000'
)
```

**Load Liquids into Wells:**

```python
# Load liquid into specific wells
reservoir['A1'].load_liquid(liquid=water, volume=50000)  # µL
plate['A1'].load_liquid(liquid=sample, volume=100)

# Mark wells as empty
plate['B1'].load_empty()
```

### 7. Protocol Control and Utilities

**Execution Control:**

```python
# Pause protocol
protocol.pause(msg='Replace tip box and resume')

# Delay
protocol.delay(seconds=60)
protocol.delay(minutes=5)

# Comment (appears in logs)
protocol.comment('Starting serial dilution')

# Home robot
protocol.home()
```

**Conditional Logic:**

```python
# Check if simulating
if protocol.is_simulating():
    protocol.comment('Running in simulation mode')
else:
    protocol.comment('Running on actual robot')
```

**Rail Lights (Flex only):**

```python
# Turn lights on
protocol.set_rail_lights(on=True)

# Turn lights off
protocol.set_rail_lights(on=False)
```

### 8. Multi-Channel and 8-Channel Pipetting

When using multi-channel pipettes:

```python
# Load 8-channel pipette
multi_pipette = protocol.load_instrument(
    'p300_multi_gen2',
    'left',
    tip_racks=[tips]
)

# Access entire column with single well reference
multi_pipette.transfer(
    volume=100,
    source=source_plate['A1'],  # Accesses entire column 1
    dest=dest_plate['A1']       # Dispenses to entire column 1
)

# Use rows() for row-wise operations
for row in plate.rows():
    multi_pipette.transfer(100, reservoir['A1'], row[0])
```

### 9. Common Protocol Patterns

Reusable end-to-end templates cover the most common workflows: serial dilution (diluent fill plus mix-after cascade across a row), plate replication (whole-plate `wells()`-to-`wells()` copy), and PCR setup (master-mix distribute, per-sample transfer, thermocycler cycling).

Full worked-example protocols for each pattern: see `references/protocol_patterns.md`. Runnable `.py` versions are in the `scripts/` directory (`serial_dilution_template.py`, `basic_protocol_template.py`, `pcr_setup_template.py`).

## Best Practices

1. **Always specify API level**: Pin a stable `apiLevel` your robot's app/firmware supports (run `opentrons_simulate` to confirm); do not blindly use a number higher than the robot accepts
2. **Use meaningful labels**: Label labware for easier identification in logs
3. **Check tip availability**: Ensure sufficient tips for protocol completion
4. **Add comments**: Use `protocol.comment()` for debugging and logging
5. **Simulate first**: Always test protocols in simulation before running on robot
6. **Handle errors gracefully**: Add pauses for manual intervention when needed
7. **Consider timing**: Use delays when protocols require incubation periods
8. **Track liquids**: Use liquid tracking for better setup validation
9. **Optimize tip usage**: Use `new_tip='once'` when appropriate to save tips
10. **Control flow rates**: Adjust flow rates for viscous or volatile liquids

## Troubleshooting

**Common Issues:**

- **Out of tips**: Verify tip rack capacity matches protocol requirements
- **Labware collisions**: Check deck layout for spatial conflicts
- **Volume errors**: Ensure volumes don't exceed well or pipette capacities
- **Module not responding**: Verify module is properly connected and firmware is updated
- **Inaccurate volumes**: Calibrate pipettes and check for air bubbles
- **Protocol fails in simulation**: Check API version compatibility and labware definitions

## Resources

For detailed API documentation, see `references/api_reference.md` in this skill directory.

For example protocol templates, see `scripts/` directory.

