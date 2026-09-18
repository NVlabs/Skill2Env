# Liquid Handling with PyLabRobot

## Overview

The liquid handling module (`pylabrobot.liquid_handling`) provides a unified interface for controlling liquid handling robots. The `LiquidHandler` class serves as the main interface for all pipetting operations, working across different hardware platforms through backend abstraction.

## API Cheat Sheet (verified against current PyLabRobot)

These signatures are the common source of errors; the examples below follow them.

- **Backends** live in `pylabrobot.liquid_handling.backends`: `STARBackend`, `VantageBackend`, `OpentronsOT2Backend`, `EVOBackend` (Tecan), and `LiquidHandlerChatterboxBackend` (no-hardware simulation). The bare `STAR` / `Vantage` / `EVO` names are kept as legacy aliases; prefer the `*Backend` form.
- **`aspirate(resources, vols, ...)`** and **`dispense(resources, vols, ...)`**: `vols` is a **list** (one entry per channel/well), e.g. `vols=[100]` for one well, `vols=[100]*8` for a row. Per-call rate/height kwargs are also lists: `flow_rates=[...]`, `liquid_height=[...]`, `blow_out_air_volume=[...]`. There is no scalar `flow_rate`/`liquid_height`.
- **`transfer(source, targets, source_vol=None, target_vols=None, ratios=None, ...)`**: distributes from **one** source well to **many** target wells. There is **no `dest=` and no `vols=`** keyword. Use `source_vol=` (same volume to each target) or `target_vols=[...]` (per-target). For a parallel column-to-column move, call `aspirate` + `dispense` directly.
- **Labware is two-level**: a tip rack or plate is placed into a **carrier site** (`carrier[0] = rack`), and the *carrier* is assigned to a deck rail. `TIP_CAR_480_A00` and `PLT_CAR_L5AC_A00` are **carriers**, not racks — do not index them for wells/tips. Common labware classes: `hamilton_96_tiprack_1000uL_filter` (tips), `Cor_96_wellplate_360ul_Fb` (Corning 96-well plate).

## Basic Setup

### Initializing a Liquid Handler

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STARBackend
from pylabrobot.resources import STARLetDeck

# Create liquid handler with STAR backend
lh = LiquidHandler(backend=STARBackend(), deck=STARLetDeck())
await lh.setup()

# When done
await lh.stop()
```

### Switching Between Backends

Change robots by swapping the backend without rewriting protocols:

```python
# Hamilton STAR
from pylabrobot.liquid_handling.backends import STARBackend
lh = LiquidHandler(backend=STARBackend(), deck=STARLetDeck())

# Opentrons OT-2
from pylabrobot.liquid_handling.backends import OpentronsOT2Backend
lh = LiquidHandler(backend=OpentronsOT2Backend(host="192.168.1.100"), deck=OTDeck())

# Simulation (no hardware required)
from pylabrobot.liquid_handling.backends import LiquidHandlerChatterboxBackend
lh = LiquidHandler(backend=LiquidHandlerChatterboxBackend(), deck=STARLetDeck())
```

## Core Operations

### Tip Management

Picking up and dropping tips is fundamental to liquid handling operations:

```python
# Pick up tips from specific positions
await lh.pick_up_tips(tip_rack["A1"])           # Single tip
await lh.pick_up_tips(tip_rack["A1:H1"])        # Row of 8 tips
await lh.pick_up_tips(tip_rack["A1:A12"])       # Column of 12 tips

# Drop tips
await lh.drop_tips()                             # Drop at current location
await lh.drop_tips(waste)                        # Drop at specific location

# Return tips to original rack
await lh.return_tips()
```

**Tip Tracking**: Enable automatic tip tracking to monitor tip usage:

```python
from pylabrobot.resources import set_tip_tracking
set_tip_tracking(True)  # Enable globally
```

### Aspirating Liquids

Draw liquid from wells or containers:

```python
# Basic aspiration (vols is always a list, one entry per well/channel)
await lh.aspirate(plate["A1"], vols=[100])        # 100 uL from A1

# Multiple wells with same volume
await lh.aspirate(plate["A1:H1"], vols=[100] * 8) # 100 uL from each of 8 wells

# Multiple wells with different volumes
await lh.aspirate(
    plate["A1:A3"],
    vols=[100, 150, 200]                          # Different volumes
)

# Advanced parameters (per-channel lists)
await lh.aspirate(
    plate["A1"],
    vols=[100],
    flow_rates=[50],                              # uL/s
    liquid_height=[5],                            # mm from bottom
    blow_out_air_volume=[10],                     # uL air
)
```

### Dispensing Liquids

Dispense liquid into wells or containers:

```python
# Basic dispensing
await lh.dispense(plate["A2"], vols=[100])        # 100 uL to A2

# Multiple wells
await lh.dispense(plate["A1:H1"], vols=[100] * 8) # 100 uL to each of 8 wells

# Different volumes
await lh.dispense(
    plate["A1:A3"],
    vols=[100, 150, 200]
)

# Advanced parameters (per-channel lists)
await lh.dispense(
    plate["A2"],
    vols=[100],
    flow_rates=[50],                              # uL/s
    liquid_height=[2],                            # mm from bottom
    blow_out_air_volume=[10],                     # uL air
)
```

### Transferring Liquids

`transfer` distributes from **one** source well to **many** target wells (positional `source, targets`; volume via `source_vol=` or `target_vols=`). It is not a parallel many-to-many move — for that, drive `aspirate`/`dispense` directly.

```python
# One source -> a row of targets, same volume to each
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(
    source_plate["A1"],          # single source well
    dest_plate["A1:H1"],         # eight target wells
    source_vol=100               # 100 uL split-equivalent dispense to each
)
await lh.drop_tips()

# Per-target volumes
await lh.transfer(
    source_plate["A1"],
    dest_plate["B1:D1"],
    target_vols=[50, 100, 150]
)

# Parallel many-to-many (column copy) is aspirate + dispense, not transfer:
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.aspirate(source_plate["A1:H1"], vols=[100] * 8)
await lh.dispense(dest_plate["A1:H1"], vols=[100] * 8)
await lh.drop_tips()
```

## Advanced Techniques

### Serial Dilutions

Create serial dilutions across plate rows or columns:

```python
# 2-fold serial dilution down column A (A1 -> A8)

# Add 50 uL diluent to A2..A8 (one buffer source -> many targets)
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(buffer["A1"], plate["A2:A8"], source_vol=50)
await lh.drop_tips()

# Perform serial dilution (single-channel aspirate/dispense, list vols)
await lh.pick_up_tips(tip_rack["A2"])
for i in range(7):
    await lh.aspirate(plate[f"A{i+1}"], vols=[50])
    await lh.dispense(plate[f"A{i+2}"], vols=[50])
    # Mix
    await lh.aspirate(plate[f"A{i+2}"], vols=[50])
    await lh.dispense(plate[f"A{i+2}"], vols=[50])
await lh.drop_tips()
```

### Plate Replication

Copy an entire plate layout to another plate:

```python
# Setup tips
await lh.pick_up_tips(tip_rack["A1:H1"])

# Replicate 96-well plate column by column (parallel 8-channel)
for col in range(1, 13):
    await lh.aspirate(source_plate[f"A{col}:H{col}"], vols=[100] * 8)
    await lh.dispense(dest_plate[f"A{col}:H{col}"], vols=[100] * 8)

await lh.drop_tips()
```

### Multi-Channel Pipetting

Use multiple channels simultaneously for parallel operations:

```python
# 8-channel move (entire row): aspirate then dispense with list vols
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.aspirate(source_plate["A1:H1"], vols=[100] * 8)
await lh.dispense(dest_plate["A1:H1"], vols=[100] * 8)
await lh.drop_tips()

# Process entire plate with 8-channel, fresh tips per column
for col in range(1, 13):
    await lh.pick_up_tips(tip_rack[f"A{col}:H{col}"])
    await lh.aspirate(source_plate[f"A{col}:H{col}"], vols=[100] * 8)
    await lh.dispense(dest_plate[f"A{col}:H{col}"], vols=[100] * 8)
    await lh.drop_tips()
```

### Mixing Liquids

Mix liquids by repeatedly aspirating and dispensing:

```python
# Mix by aspiration/dispensing
await lh.pick_up_tips(tip_rack["A1"])

# Mix 5 times
for _ in range(5):
    await lh.aspirate(plate["A1"], vols=[80])
    await lh.dispense(plate["A1"], vols=[80])

await lh.drop_tips()
```

## Volume Tracking

Track liquid volumes in wells automatically:

```python
from pylabrobot.resources import set_volume_tracking

# Enable volume tracking globally
set_volume_tracking(True)

# Set initial volumes
plate["A1"].tracker.set_liquids([(None, 200)])  # 200 µL

# After aspirating 100 uL
await lh.aspirate(plate["A1"], vols=[100])
print(plate["A1"].tracker.get_volume())  # 100 uL

# Check remaining volume
remaining = plate["A1"].tracker.get_volume()
```

## Liquid Classes

PyLabRobot ships liquid-class definitions (under `pylabrobot.liquid_handling.liquid_classes`) that encode vendor-tuned aspiration/dispense parameters for a given liquid, tip, and volume. How a liquid class is selected and applied is backend-specific (e.g. the Hamilton STAR backend resolves a class from the well's liquid and the tip). Consult the docs for the exact API of your backend before wiring liquid classes into a protocol, rather than passing flow parameters ad hoc; for explicit per-call control use the `flow_rates=[...]` / `blow_out_air_volume=[...]` lists on `aspirate`/`dispense` shown above.

## Error Handling

Handle errors in liquid handling operations:

```python
try:
    await lh.setup()
    await lh.pick_up_tips(tip_rack["A1"])
    await lh.transfer(source["A1"], dest["A1"], source_vol=100)
    await lh.drop_tips()
except Exception as e:
    print(f"Error during liquid handling: {e}")
    # Attempt to drop tips if holding them
    try:
        await lh.drop_tips()
    except:
        pass
finally:
    await lh.stop()
```

## Best Practices

1. **Always Setup and Stop**: Call `await lh.setup()` before operations and `await lh.stop()` when done
2. **Enable Tracking**: Use tip tracking and volume tracking for accurate state management
3. **Tip Management**: Always pick up tips before aspirating and drop them when done
4. **Flow Rates**: Adjust flow rates based on liquid viscosity and vessel type
5. **Liquid Height**: Set appropriate aspiration/dispense heights to avoid splashing
6. **Error Handling**: Use try/finally blocks to ensure proper cleanup
7. **Test in Simulation**: Use ChatterboxBackend to test protocols before running on hardware
8. **Volume Limits**: Respect tip volume limits and well capacities
9. **Mixing**: Mix after dispensing viscous liquids or when accuracy is critical
10. **Documentation**: Document liquid classes and custom parameters for reproducibility

## Common Patterns

### Complete Liquid Handling Protocol

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STARBackend
from pylabrobot.resources import (
    STARLetDeck, TIP_CAR_480_A00, PLT_CAR_L5AC_A00,
    hamilton_96_tiprack_1000uL_filter, Cor_96_wellplate_360ul_Fb,
    set_tip_tracking, set_volume_tracking,
)

# Enable tracking
set_tip_tracking(True)
set_volume_tracking(True)

# Initialize
lh = LiquidHandler(backend=STARBackend(), deck=STARLetDeck())
await lh.setup()

try:
    # Define carriers + labware (rack/plate -> carrier site -> deck rail)
    tip_car = TIP_CAR_480_A00(name="tip_carrier")
    tip_car[0] = tip_rack = hamilton_96_tiprack_1000uL_filter(name="tips_01")
    lh.deck.assign_child_resource(tip_car, rails=1)

    plt_car = PLT_CAR_L5AC_A00(name="plate_carrier")
    plt_car[0] = source = Cor_96_wellplate_360ul_Fb(name="source")
    plt_car[1] = dest = Cor_96_wellplate_360ul_Fb(name="dest")
    lh.deck.assign_child_resource(plt_car, rails=15)

    # Set initial volumes
    for well in source.children:
        well.tracker.set_liquids([(None, 200)])

    # Execute protocol: parallel 8-channel column copy
    await lh.pick_up_tips(tip_rack["A1:H1"])
    for col in range(1, 13):
        await lh.aspirate(source[f"A{col}:H{col}"], vols=[100] * 8)
        await lh.dispense(dest[f"A{col}:H{col}"], vols=[100] * 8)
    await lh.drop_tips()

finally:
    await lh.stop()
```

## Hardware-Specific Notes

### Hamilton STAR

- Supports full liquid handling capabilities
- Uses USB connection for communication
- Firmware commands executed directly
- Supports CO-RE (Compressed O-Ring Expansion) tips

### Opentrons OT-2

- Requires IP address for network connection
- Uses HTTP API for communication
- Limited to 8-channel and single-channel pipettes
- Simpler deck layout compared to STAR

### Tecan EVO

- Work-in-progress support
- Similar capabilities to Hamilton STAR
- Check current compatibility status in documentation

## Additional Resources

- Official Liquid Handling Guide: https://docs.pylabrobot.org/user_guide/basic.html
- API Reference: https://docs.pylabrobot.org/user_guide/index.html
- Example Protocols: https://github.com/PyLabRobot/pylabrobot/tree/main/examples
