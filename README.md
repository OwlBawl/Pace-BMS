# Pace BMS Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/OwlBawl/pace_bms.svg)](https://github.com/OwlBawl/pace_bms/releases)
[![License](https://img.shields.io/github/license/OwlBawl/pace_bms.svg)](LICENSE)

A Home Assistant integration for Pace Battery Management Systems (BMS) via Modbus RTU over serial connection.

## Features

- 📊 **Real-time Monitoring**
  - Pack voltage, current, and state of charge (SOC)
  - Individual cell voltages (up to 8 cells)
  - Multiple temperature sensors (cell, MOSFET, environment)
  - Remaining and full capacity
  - Cycle count and state of health (SOH)

- ⚡ **Binary Sensors**
  - Charging/Discharging status
  - MOSFET states
  - Dynamic icons based on state

- 🔧 **Configurable Protection Parameters**
  - Overvoltage/Undervoltage protection (pack and cell level)
  - Overcurrent protection (charging and discharging)
  - Temperature protection (charging, discharging, MOSFET, environment)
  - Balance settings
  - All parameters adjustable via Home Assistant UI

- 🛡️ **Status Monitoring**
  - Warning flags
  - Protection flags
  - Fault status
  - Cell balancing status

## Requirements

- Home Assistant 2023.1 or newer
- Pace BMS connected via USB-to-RS485 or direct serial connection
- Modbus RTU communication configured on BMS

## Installation

### HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed
2. Add this repository as a custom repository in HACS:
   - Open HACS
   - Click on "Integrations"
   - Click the three dots in the top right corner
   - Select "Custom repositories"
   - Add `https://github.com/OwlBawl/Pace-BMS` as repository
   - Select "Integration" as category
   - Click "Add"
3. Click "Install" on the Pace BMS integration
4. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/OwlBawl/Pace-BMS/releases)
2. Extract the `Pace-BMS` folder to your `custom_components` directory
3. Restart Home Assistant

## Configuration

### Adding the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Pace BMS"
4. Enter the configuration:
   - **Name**: Friendly name for your BMS (default: "Pace BMS")
   - **Port**: Serial port (e.g., `/dev/ttyUSB0`, `/dev/ttyACM0`)
   - **Baudrate**: Communication speed (default: 9600)
   - **Slave ID**: Modbus slave address (default: 1)

### Finding Your Serial Port

**Home Assistant OS -> Settings -> Hardware - All Hardware**

Lovelace card example inculuded (change you device name prefix in entities)
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
  <img src="https://github.com/user-attachments/assets/1950a5b5-41ae-46f7-8bb6-e8ed8a2a625c" width="48%">
  <img src="https://github.com/user-attachments/assets/43f47cca-2a4c-4165-8130-22e026348947" width="48%">
  <img src="https://github.com/user-attachments/assets/92bde1f1-622c-45b2-95bf-f248cd27f430" width="48%">
  <img src="https://github.com/user-attachments/assets/415d6356-4171-4655-8e19-d6484bc8a574" width="48%">
  <img src="https://github.com/user-attachments/assets/478c3531-ebb3-49ff-b7cf-d3487669e77f" width="48%">
</div>
