# Pace BMS Integration

Monitor and configure your Pace Battery Management System directly from Home Assistant!

## Features

✅ Real-time monitoring of voltage, current, SOC, and temperatures  
✅ Individual cell voltage monitoring (up to 8 cells)  
✅ Configurable protection parameters via UI  
✅ Binary sensors for charging/discharging status  
✅ Warning and protection flag monitoring  
✅ Cell balancing status  
✅ Dynamic icons based on state and units  

## Quick Setup

1. Connect your Pace BMS via USB-to-RS485 or serial cable
2. Add the integration via Settings → Devices & Services
3. Configure serial port, baudrate (usually 9600), and slave ID (usually 1)
4. Start monitoring your battery!

## Configuration

All protection parameters can be adjusted directly in Home Assistant:
- Voltage protection (overvoltage/undervoltage)
- Current protection (overcurrent)
- Temperature protection (over/under temperature)
- Balance settings
- Sleep mode settings

## Need Help?

Check the [full documentation](https://github.com/OwlBawl/PACE-BMS), view [release notes](https://github.com/OwlBawl/PACE-BMS/releases), or [report issues](https://github.com/OwlBawl/PACE-BMS/issues).