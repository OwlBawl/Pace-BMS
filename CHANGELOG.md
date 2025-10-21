# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- Initial release
- Real-time monitoring of pack voltage, current, SOC, SOH
- Individual cell voltage monitoring (8 cells)
- Temperature monitoring (cell, MOSFET, environment)
- Binary sensors for charging/discharging status
- Configurable protection parameters via UI
- Overvoltage/undervoltage protection settings
- Overcurrent protection settings
- Temperature protection settings
- Balance settings configuration
- Warning and protection flag monitoring
- Cell balancing status
- Dynamic icons based on state and units
- HACS integration support
- Config flow for easy setup

### Technical
- Modbus RTU communication
- Efficient batch register reading
- Support for pymodbus >= 3.5.4
- Home Assistant 2023.1+ compatibility

[1.0.0]: https://github.com/OwlBawl/pace_bms/releases/tag/v1.0.0