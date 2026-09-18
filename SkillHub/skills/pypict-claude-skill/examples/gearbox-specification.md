# Automotive Gearbox Control System - Specification

## 1. System Overview

The Automotive Gearbox Control System is an electronic control unit (ECU) that manages gear shifting in a semi-automatic transmission. The system monitors vehicle conditions and driver inputs to determine optimal gear selection and execute smooth gear changes.

## 2. System Components

### 2.1 Input Sensors
- **Vehicle Speed Sensor**: Measures current speed (0-200 km/h)
- **Engine RPM Sensor**: Measures engine revolutions (0-7000 RPM)
- **Throttle Position Sensor**: Measures accelerator pedal position (0-100%)
- **Brake Pressure Sensor**: Detects brake application
- **Clutch Position Sensor**: Monitors clutch engagement state
- **Gear Position Sensor**: Detects current gear (N, 1-6, R)

### 2.2 Driver Controls
- **Gear Selector**: Manual, Sport, Eco modes
- **Shift Paddles**: Manual up/down shift requests
- **Clutch Pedal**: Manual clutch control (if applicable)

### 2.3 Outputs
- **Gear Actuator**: Mechanical gear selection
- **Clutch Actuator**: Clutch engagement/disengagement
- **Dashboard Display**: Current gear indicator
- **Warning Lights**: System errors and alerts

## 3. Operating Modes

### 3.1 Manual Mode
- Driver has full control over gear selection
- System prevents invalid shifts (e.g., direct 5th to 1st)
- Rev-matching on downshifts
- Neutral safety: requires brake to shift out of Park/Neutral

### 3.2 Sport Mode
- Holds gears longer for higher RPM
- Faster gear changes
- Downshifts on hard braking
- Target shift points: 5000-6500 RPM

### 3.3 Eco Mode
- Early upshifts for fuel efficiency
- Target shift points: 2000-3000 RPM
- Smooth, gradual gear changes
- Skip-shift capability (e.g., 2nd to 4th)

## 4. Functional Requirements

### 4.1 Gear Shifting Logic

#### 4.1.1 Upshift Conditions
- **Eco Mode**: Engine RPM > 2500 AND throttle < 40%
- **Manual Mode**: Driver paddle input OR RPM > 6000
- **Sport Mode**: Engine RPM > 5500

#### 4.1.2 Downshift Conditions
- **Eco Mode**: Engine RPM < 1500 OR heavy throttle (>80%)
- **Manual Mode**: Driver paddle input OR RPM < 1200
- **Sport Mode**: Engine RPM < 2000 OR brake pressure > 50%

#### 4.1.3 Prohibited Shifts
- Cannot shift from Reverse to any forward gear without stopping (speed = 0)
- Cannot shift to Reverse from any forward gear while moving (speed > 0)
- Cannot skip more than 2 gears in a single shift (except computer-controlled skip-shift)
- Cannot downshift if resulting RPM would exceed 7000 (red line protection)

### 4.2 Safety Features

#### 4.2.1 Hill Start Assist
- Activates when: stopped on incline > 5% AND brake released
- Holds brake pressure for 2 seconds
- Prevents rollback

#### 4.2.2 Overrun Protection
- Prevents downshift if resulting engine RPM > 6500
- Displays warning message to driver
- Ignores paddle input if unsafe

#### 4.2.3 Stall Prevention
- Auto-downshift if engine RPM < 800 while moving
- Automatic neutral engagement if stopped for > 3 seconds in gear
- Clutch slip if speed drops below minimum for current gear

#### 4.2.4 Neutral Safety
- Engine start only allowed in Park or Neutral
- Brake pedal required to shift from Park
- Reverse requires full stop (speed = 0 km/h)

### 4.3 Error Handling

#### 4.3.1 Sensor Failures
- **Speed Sensor Failure**: Limit to current gear, disable automatic shifting
- **RPM Sensor Failure**: Use speed-based shift logic as fallback
- **Throttle Sensor Failure**: Default to conservative shift points
- **Multiple Sensor Failures**: Enter limp-home mode (3rd gear only)

#### 4.3.2 Actuator Failures
- **Gear Actuator Jam**: Attempt 3 retries with 200ms delay
- **Clutch Actuator Failure**: Lock in current gear, display warning
- **Hydraulic Pressure Low**: Reduce shift speed, display warning

#### 4.3.3 Temperature Management
- **Normal Operation**: 70-110°C
- **High Temperature Warning**: 110-130°C (reduce shift frequency)
- **Critical Temperature**: >130°C (limp-home mode, 3rd gear only)

## 5. Performance Requirements

### 5.1 Shift Times
- **Eco Mode**: 800-1200 ms per shift
- **Manual Mode**: 400-600 ms per shift
- **Sport Mode**: 150-300 ms per shift

### 5.2 Response Times
- **Paddle Input**: < 50 ms recognition
- **Brake Detection**: < 20 ms
- **Emergency Neutral**: < 100 ms

### 5.3 Reliability
- **MTBF**: > 150,000 km
- **Shift Success Rate**: > 99.5%
- **False Error Rate**: < 0.1%

## 6. Environmental Conditions

### 6.1 Operating Temperature
- **Normal**: -20°C to +50°C ambient
- **Gearbox Oil**: -10°C to +130°C

### 6.2 Altitude
- **Sea Level to 3000m**: Normal operation
- **3000m to 5000m**: Adjusted shift points for reduced air density

### 6.3 Weather Conditions
- Rain, snow, ice: Reduced shift aggressiveness
- Detection via wheel slip sensors and ABS integration

## 7. User Interface Requirements

### 7.1 Dashboard Display
- Current gear number (1-6, R, N, P)
- Selected mode (Manual, Sport, Eco)
- Shift indicator (up/down arrows)
- Warning messages (text + icon)

### 7.2 Warning Messages
- "Gearbox Overheating" (yellow)
- "Shift Not Possible" (red)
- "Service Required" (yellow)
- "Limp-Home Mode Active" (red)

### 7.3 User Feedback
- Shift confirmation (subtle indicator flash)
- Paddle input acknowledgment (haptic feedback if available)
- Audio warning for critical errors

## 8. Integration Requirements

### 8.1 Engine Control Unit (ECU)
- Torque reduction request during shifts
- RPM synchronization for smooth engagement
- Engine braking coordination

### 8.2 Anti-lock Braking System (ABS)
- Wheel slip detection for traction control
- Emergency braking gear hold
- Stability control integration

### 8.3 Electronic Stability Control (ESC)
- Torque vectoring support
- Drift mode compatibility (sport mode)
- Traction control coordination

## 9. Validation Requirements

### 9.1 Unit Testing
- Individual sensor input validation
- Shift logic decision trees
- Safety feature triggering

### 9.2 Integration Testing
- Multi-mode operation
- Sensor failure scenarios
- ECU communication

### 9.3 System Testing
- Real-world driving scenarios
- Extreme condition testing
- Long-term reliability testing

## 10. Constraints and Assumptions

### 10.1 Physical Constraints
- Maximum gear ratio: 1:6.5 (1st gear) to 1:0.85 (6th gear)
- Clutch engagement time: 200-400 ms
- Hydraulic system pressure: 8-12 bar

### 10.2 System Assumptions
- Sensors provide accurate readings within ±5% tolerance
- ECU communication latency < 10 ms
- Battery voltage maintained at 12-14V

### 10.3 Regulatory Compliance
- ISO 26262 (Automotive Safety Integrity Level - ASIL C)
- UNECE R13 (Braking regulations)
- Local emissions standards compliance
