# Hardware Module Control Recipes

Code recipes for controlling each Opentrons hardware module from a Protocol API v2 protocol. Method/property tables for the same modules live in `api_reference.md`.

## Temperature Module

```python
# Set temperature
temp_module.set_temperature(celsius=4)

# Wait for temperature
temp_module.await_temperature(celsius=4)

# Deactivate
temp_module.deactivate()

# Check status
current_temp = temp_module.temperature  # Current temperature
target_temp = temp_module.target  # Target temperature
```

## Magnetic Module (OT-2 only)

The active Magnetic Module exists only on the OT-2. On the Flex, use the unpowered
Magnetic Block (`magneticBlockV1`), which has no `engage`/`disengage` — labware is moved
on and off it with the Gripper.

```python
# Engage (raise magnets)
mag_module.engage(height_from_base=10)  # mm from labware base

# Disengage (lower magnets)
mag_module.disengage()

# Check status
is_engaged = mag_module.status  # 'engaged' or 'disengaged'
```

## Heater-Shaker Module

```python
# Set temperature
hs_module.set_target_temperature(celsius=37)

# Wait for temperature
hs_module.wait_for_temperature()

# Set shake speed
hs_module.set_and_wait_for_shake_speed(rpm=500)

# Close labware latch
hs_module.close_labware_latch()

# Open labware latch
hs_module.open_labware_latch()

# Deactivate heater
hs_module.deactivate_heater()

# Deactivate shaker
hs_module.deactivate_shaker()
```

## Thermocycler Module

```python
# Open lid
tc_module.open_lid()

# Close lid
tc_module.close_lid()

# Set lid temperature
tc_module.set_lid_temperature(celsius=105)

# Set block temperature
tc_module.set_block_temperature(
    temperature=95,
    hold_time_seconds=30,
    hold_time_minutes=0.5,
    block_max_volume=50  # µL per well
)

# Execute profile (PCR cycling)
profile = [
    {'temperature': 95, 'hold_time_seconds': 30},
    {'temperature': 57, 'hold_time_seconds': 30},
    {'temperature': 72, 'hold_time_seconds': 60}
]
tc_module.execute_profile(
    steps=profile,
    repetitions=30,
    block_max_volume=50
)

# Deactivate
tc_module.deactivate_lid()
tc_module.deactivate_block()
```

## Absorbance Plate Reader (Flex)

```python
# Load (lid must be closed to initialize, open to load/read labware)
plate_reader = protocol.load_module('absorbanceReaderV1', 'D3')

# Initialize: wavelengths are set here, NOT on read()
plate_reader.close_lid()
plate_reader.initialize('multi', [450, 650])  # 'single' or 'multi'
plate_reader.open_lid()

# Read the loaded plate (returns a dict keyed by wavelength)
result = plate_reader.read()
```
