# Hardware Backends in PyLabRobot

## Overview

PyLabRobot uses a backend abstraction system that allows the same protocol code to run on different liquid handling robots and platforms. Backends handle device-specific communication while the `LiquidHandler` frontend provides a unified interface.

**Current backend class names** (all from `pylabrobot.liquid_handling.backends`): `STARBackend`, `VantageBackend`, `OpentronsOT2Backend`, `EVOBackend` (Tecan EVO), and `LiquidHandlerChatterboxBackend` (no-hardware simulation). Bare `STAR`/`Vantage`/`EVO` remain as legacy aliases; prefer the `*Backend` names. Some examples below still show the short names — substitute the `*Backend` form.

## Backend Architecture

### How Backends Work

1. **Frontend**: `LiquidHandler` class provides high-level API
2. **Backend**: Device-specific class handles hardware communication
3. **Protocol**: Same code works across different backends

```python
# Same protocol code
await lh.pick_up_tips(tip_rack["A1"])
await lh.aspirate(plate["A1"], vols=[100])
await lh.dispense(plate["A2"], vols=[100])
await lh.drop_tips()

# Works with any backend (STAR, Opentrons, simulation, etc.)
```

### Backend Interface

All backends inherit from `LiquidHandlerBackend` and implement:
- `setup()`: Initialize connection to hardware
- `stop()`: Close connection and cleanup
- Device-specific command methods (aspirate, dispense, etc.)

## Supported Backends

### Hamilton STAR (Full Support)

The Hamilton STAR and STARlet liquid handling robots have full PyLabRobot support.

**Setup:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STARBackend
from pylabrobot.resources import STARLetDeck

# Create STAR backend
backend = STARBackend()

# Initialize liquid handler
lh = LiquidHandler(backend=backend, deck=STARLetDeck())
await lh.setup()
```

**Platform Support:**
- Windows ✅
- macOS ✅
- Linux ✅
- Raspberry Pi ✅

**Communication:**
- USB connection to robot
- Direct firmware commands
- No Hamilton software required

**Features:**
- Full liquid handling operations
- CO-RE tip support
- 96-channel head support (if equipped)
- Temperature control
- Carrier and rail-based positioning

**Deck Types:**
```python
from pylabrobot.resources import STARLetDeck, STARDeck

# For STARlet (smaller deck)
deck = STARLetDeck()

# For STAR (full deck)
deck = STARDeck()
```

**Example:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STARBackend
from pylabrobot.resources import (
    STARLetDeck, TIP_CAR_480_A00, PLT_CAR_L5AC_A00,
    hamilton_96_tiprack_1000uL_filter, Cor_96_wellplate_360ul_Fb,
)

# Initialize
lh = LiquidHandler(backend=STARBackend(), deck=STARLetDeck())
await lh.setup()

# Define carriers + labware (rack/plate -> carrier site -> deck rail)
tip_car = TIP_CAR_480_A00(name="tip_carrier")
tip_car[0] = tip_rack = hamilton_96_tiprack_1000uL_filter(name="tips")
lh.deck.assign_child_resource(tip_car, rails=1)

plt_car = PLT_CAR_L5AC_A00(name="plate_carrier")
plt_car[0] = plate = Cor_96_wellplate_360ul_Fb(name="plate")
lh.deck.assign_child_resource(plt_car, rails=10)

# Execute protocol
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(plate["A1"], plate["A2"], source_vol=100)
await lh.drop_tips()

await lh.stop()
```

### Opentrons OT-2 (Supported)

The Opentrons OT-2 is supported through the Opentrons HTTP API.

**Setup:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import OpentronsOT2Backend
from pylabrobot.resources import OTDeck

# Create Opentrons backend (requires robot IP address)
backend = OpentronsOT2Backend(host="192.168.1.100")  # Replace with your robot's IP

# Initialize liquid handler
lh = LiquidHandler(backend=backend, deck=OTDeck())
await lh.setup()
```

**Platform Support:**
- Any platform with network access to OT-2

**Communication:**
- HTTP API over network
- Requires robot IP address
- No Opentrons app required

**Features:**
- 8-channel pipette support
- Single-channel pipette support
- Standard OT-2 deck layout
- Coordinate-based positioning

**Limitations:**
- Uses older Opentrons HTTP API
- Some features may be limited compared to STAR

**Example:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import OpentronsOT2Backend
from pylabrobot.resources import OTDeck, Deck

# Initialize with robot IP
lh = LiquidHandler(
    backend=OpentronsOT2Backend(host="192.168.1.100"),
    deck=OTDeck()
)
await lh.setup()

# Load deck layout
lh.deck = Deck.load_from_json_file("opentrons_layout.json")

# Execute protocol
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(plate["A1"], plate["A2"], source_vol=100)
await lh.drop_tips()

await lh.stop()
```

### Tecan EVO

Support for Tecan EVO liquid handling robots is partial; check the docs for current feature coverage.

**Setup:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import EVOBackend
from pylabrobot.resources import TecanDeck  # or EVO100Deck()/EVO150Deck()/EVO200Deck()

backend = EVOBackend()
lh = LiquidHandler(backend=backend, deck=TecanDeck())
```

### Hamilton Vantage

Hamilton Vantage has near-complete support.

**Setup:**

```python
from pylabrobot.liquid_handling.backends import VantageBackend
from pylabrobot.resources import VantageDeck

lh = LiquidHandler(backend=VantageBackend(), deck=VantageDeck())
```

**Features:**
- Similar to STAR support
- Some advanced features may be limited

## Simulation Backend

### LiquidHandlerChatterboxBackend (Simulation)

Test protocols without physical hardware using the simulation backend. It logs every operation and tracks tips/volumes; pair it with the `Visualizer` for live deck state.

**Setup:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import LiquidHandlerChatterboxBackend
from pylabrobot.resources import STARLetDeck

# Create simulation backend
backend = LiquidHandlerChatterboxBackend(num_channels=8)

# Initialize liquid handler
lh = LiquidHandler(backend=backend, deck=STARLetDeck())
await lh.setup()
```

**Features:**
- No hardware required
- Simulates all liquid handling operations
- Works with visualizer for real-time feedback
- Validates protocol logic
- Tracks tips and volumes

**Use Cases:**
- Protocol development and testing
- Training and education
- CI/CD pipeline testing
- Debugging without hardware access

**Example:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import LiquidHandlerChatterboxBackend
from pylabrobot.resources import (
    STARLetDeck, TIP_CAR_480_A00, PLT_CAR_L5AC_A00,
    hamilton_96_tiprack_1000uL_filter, Cor_96_wellplate_360ul_Fb,
    set_tip_tracking, set_volume_tracking,
)

# Enable tracking for simulation
set_tip_tracking(True)
set_volume_tracking(True)

# Initialize with simulation backend
lh = LiquidHandler(
    backend=LiquidHandlerChatterboxBackend(num_channels=8),
    deck=STARLetDeck()
)
await lh.setup()

# Carriers + labware (rack/plate -> carrier site -> deck rail)
tip_car = TIP_CAR_480_A00(name="tip_carrier")
tip_car[0] = tip_rack = hamilton_96_tiprack_1000uL_filter(name="tips_01")
lh.deck.assign_child_resource(tip_car, rails=1)

plt_car = PLT_CAR_L5AC_A00(name="plate_carrier")
plt_car[0] = plate = Cor_96_wellplate_360ul_Fb(name="plate")
lh.deck.assign_child_resource(plt_car, rails=10)

# Set initial volumes
for well in plate.children:
    well.tracker.set_liquids([(None, 200)])

# Run simulated protocol (parallel 8-channel move)
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.aspirate(plate["A1:H1"], vols=[100] * 8)
await lh.dispense(plate["A2:H2"], vols=[100] * 8)
await lh.drop_tips()

# Check results
print(f"A1 volume: {plate['A1'].tracker.get_volume()} uL")  # 100 uL
print(f"A2 volume: {plate['A2'].tracker.get_volume()} uL")  # 100 uL

await lh.stop()
```

## Switching Backends

### Backend-Agnostic Protocols

Write protocols that work with any backend:

```python
def get_backend(robot_type: str):
    """Factory function to create appropriate backend"""
    if robot_type == "star":
        from pylabrobot.liquid_handling.backends import STARBackend
        return STARBackend()
    elif robot_type == "opentrons":
        from pylabrobot.liquid_handling.backends import OpentronsOT2Backend
        return OpentronsOT2Backend(host="192.168.1.100")
    elif robot_type == "simulation":
        from pylabrobot.liquid_handling.backends import LiquidHandlerChatterboxBackend
        return LiquidHandlerChatterboxBackend()
    else:
        raise ValueError(f"Unknown robot type: {robot_type}")

def get_deck(robot_type: str):
    """Factory function to create appropriate deck"""
    if robot_type == "star":
        from pylabrobot.resources import STARLetDeck
        return STARLetDeck()
    elif robot_type == "opentrons":
        from pylabrobot.resources import OTDeck
        return OTDeck()
    elif robot_type == "simulation":
        from pylabrobot.resources import STARLetDeck
        return STARLetDeck()
    else:
        raise ValueError(f"Unknown robot type: {robot_type}")

# Use in protocol
robot_type = "simulation"  # Change to "star" or "opentrons" as needed
backend = get_backend(robot_type)
deck = get_deck(robot_type)

lh = LiquidHandler(backend=backend, deck=deck)
await lh.setup()

# Protocol code works with any backend
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(plate["A1"], plate["A2"], source_vol=100)
await lh.drop_tips()
```

### Development Workflow

1. **Develop**: Write protocol using ChatterboxBackend
2. **Test**: Run with visualizer to validate logic
3. **Verify**: Test on simulation with real deck layout
4. **Deploy**: Switch to hardware backend (STAR, Opentrons)

```python
# Development
lh = LiquidHandler(backend=LiquidHandlerChatterboxBackend(), deck=STARLetDeck())

# ... develop protocol ...

# Production (just change backend)
lh = LiquidHandler(backend=STARBackend(), deck=STARLetDeck())
```

## Backend Configuration

### Custom Backend Parameters

Some backends accept configuration parameters:

```python
# Opentrons with custom parameters
backend = OpentronsOT2Backend(
    host="192.168.1.100",
    port=31950  # Default Opentrons API port
)

# Simulation backend with custom channels
backend = LiquidHandlerChatterboxBackend(
    num_channels=8  # 8-channel simulation
)
```

### Connection Troubleshooting

**Hamilton STAR:**
- Ensure USB cable is connected
- Check that no other software is using the robot
- Verify firmware is up to date
- On macOS/Linux, may need USB permissions

**Opentrons OT-2:**
- Verify robot IP address is correct
- Check network connectivity (ping robot)
- Ensure robot is powered on
- Confirm Opentrons app is not blocking API access

**General:**
- Use `await lh.setup()` to test connection
- Check error messages for specific issues
- Ensure proper permissions for device access

## Backend-Specific Features

### Hamilton STAR Specific

```python
# Access backend directly for hardware-specific features
star_backend = lh.backend

# Hamilton-specific commands (if needed)
# Most operations should go through LiquidHandler interface
```

### Opentrons Specific

```python
# Opentrons-specific configuration
ot_backend = lh.backend

# Access OT-2 API directly if needed (advanced)
# Most operations should go through LiquidHandler interface
```

## Best Practices

1. **Abstract Hardware**: Write backend-agnostic protocols when possible
2. **Test in Simulation**: Always test with ChatterboxBackend first
3. **Factory Pattern**: Use factory functions to create backends
4. **Error Handling**: Handle connection errors gracefully
5. **Documentation**: Document which backends your protocol supports
6. **Configuration**: Use config files for backend parameters
7. **Version Control**: Track backend versions and compatibility
8. **Cleanup**: Always call `await lh.stop()` to release hardware
9. **Single Connection**: Only one program should connect to hardware at a time
10. **Platform Testing**: Test on target platform before deployment

## Common Patterns

### Multi-Backend Support

```python
import asyncio
from typing import Literal

async def run_protocol(
    robot_type: Literal["star", "opentrons", "simulation"],
    visualize: bool = False
):
    """Run protocol on specified backend"""

    # Create backend
    if robot_type == "star":
        from pylabrobot.liquid_handling.backends import STARBackend
        backend = STARBackend()
        deck = STARLetDeck()
    elif robot_type == "opentrons":
        from pylabrobot.liquid_handling.backends import OpentronsOT2Backend
        backend = OpentronsOT2Backend(host="192.168.1.100")
        deck = OTDeck()
    elif robot_type == "simulation":
        from pylabrobot.liquid_handling.backends import LiquidHandlerChatterboxBackend
        backend = LiquidHandlerChatterboxBackend()
        deck = STARLetDeck()

    # Initialize
    lh = LiquidHandler(backend=backend, deck=deck)
    await lh.setup()

    try:
        # Load deck layout (backend-agnostic)
        # lh.deck = Deck.load_from_json_file(f"{robot_type}_layout.json")

        # Execute protocol (backend-agnostic)
        await lh.pick_up_tips(tip_rack["A1"])
        await lh.transfer(plate["A1"], plate["A2"], source_vol=100)
        await lh.drop_tips()

        print("Protocol completed successfully!")

    finally:
        await lh.stop()

# Run on different backends
await run_protocol("simulation")      # Test in simulation
await run_protocol("star")            # Run on Hamilton STAR
await run_protocol("opentrons")       # Run on Opentrons OT-2
```

## Additional Resources

- Backend Documentation: https://docs.pylabrobot.org/user_guide/backends.html
- Supported Machines: https://docs.pylabrobot.org/user_guide/machines.html
- API Reference: https://docs.pylabrobot.org/user_guide/index.html
- GitHub Examples: https://github.com/PyLabRobot/pylabrobot/tree/main/examples
