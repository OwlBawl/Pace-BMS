"""Constants for the Pace BMS integration."""
from typing import Final

DOMAIN: Final = "pace_bms"

# Configuration
CONF_SLAVE_ID: Final = "slave_id"
CONF_PORT: Final = "port"
CONF_BAUDRATE: Final = "baudrate"
CONF_SCAN_INTERVAL: Final = "scan_interval"

# Defaults
DEFAULT_SLAVE_ID: Final = 1
DEFAULT_PORT: Final = "/dev/ttyACM0"
DEFAULT_BAUDRATE: Final = 9600
DEFAULT_SCAN_INTERVAL: Final = 10

# Modbus Settings
MODBUS_TIMEOUT: Final = 0.2
MODBUS_BYTESIZE: Final = 8
MODBUS_PARITY: Final = "N"
MODBUS_STOPBITS: Final = 1

# Register Addresses
REG_CURRENT: Final = 0
REG_PACK_VOLTAGE: Final = 1
REG_SOC: Final = 2
REG_SOH: Final = 3
REG_REMAIN_CAPACITY: Final = 4
REG_FULL_CAPACITY: Final = 5
REG_DESIGN_CAPACITY: Final = 6
REG_CYCLE_COUNT: Final = 7
REG_WARNING_FLAGS: Final = 9
REG_PROTECTION_FLAGS: Final = 10
REG_STATUS_FAULT: Final = 11
REG_BALANCE_STATUS: Final = 12

# Register Groups for Efficient Batch Reading (0x03 function)
REG_BASIC_DATA_START: Final = 0  # Reads: Current, Pack Voltage, SOC, SOH, Capacities, Cycle Count
REG_BASIC_DATA_COUNT: Final = 8

REG_STATUS_FLAGS_START: Final = 9  # Reads: Warning, Protection, Status/Fault, Balance
REG_STATUS_FLAGS_COUNT: Final = 4

REG_TEMP_GROUP_START: Final = 31  # Reads: Temp 1, Temp 2, (33-34 unused), MOSFET Temp, Env Temp
REG_TEMP_GROUP_COUNT: Final = 6

REG_PROTECTION_PARAMS_START: Final = 60  # Reads: All protection/balance parameters
REG_PROTECTION_PARAMS_COUNT: Final = 55  # From 60 to 114 inclusive

# Cell Voltage Registers (8 cells)
REG_CELL_VOLTAGE_START: Final = 15
REG_CELL_VOLTAGE_COUNT: Final = 8

# Temperature Registers
REG_TEMP_1: Final = 31
REG_TEMP_2: Final = 32
REG_MOSFET_TEMP: Final = 35
REG_ENV_TEMP: Final = 36

# Protection Settings - Pack Overvoltage
REG_PACK_OV_ALARM: Final = 60
REG_PACK_OV_PROTECTION: Final = 61
REG_PACK_OV_RELEASE: Final = 62
REG_PACK_OV_DELAY: Final = 63

# Protection Settings - Cell Overvoltage
REG_CELL_OV_ALARM: Final = 64
REG_CELL_OV_PROTECTION: Final = 65
REG_CELL_OV_RELEASE: Final = 66
REG_CELL_OV_DELAY: Final = 67

# Protection Settings - Pack Undervoltage
REG_PACK_UV_ALARM: Final = 68
REG_PACK_UV_PROTECTION: Final = 69
REG_PACK_UV_RELEASE: Final = 70
REG_PACK_UV_DELAY: Final = 71

# Protection Settings - Cell Undervoltage
REG_CELL_UV_ALARM: Final = 72
REG_CELL_UV_PROTECTION: Final = 73
REG_CELL_UV_RELEASE: Final = 74
REG_CELL_UV_DELAY: Final = 75

# Protection Settings - Charging Overcurrent
REG_CHARGING_OC_ALARM: Final = 76
REG_CHARGING_OC_PROTECTION: Final = 77
REG_CHARGING_OC_DELAY: Final = 78

# Protection Settings - Discharging Overcurrent
REG_DISCHARGING_OC_ALARM: Final = 79
REG_DISCHARGING_OC_PROTECTION: Final = 80
REG_DISCHARGING_OC_DELAY: Final = 81
REG_DISCHARGING_OC2_PROTECTION: Final = 82
REG_DISCHARGING_OC2_DELAY: Final = 83

# Protection Settings - Charging Temperature
REG_CHARGING_OT_ALARM: Final = 84
REG_CHARGING_OT_PROTECTION: Final = 85
REG_CHARGING_OT_RELEASE: Final = 86
REG_DISCHARGING_OT_ALARM: Final = 87
REG_DISCHARGING_OT_PROTECTION: Final = 88
REG_DISCHARGING_OT_RELEASE: Final = 89
REG_CHARGING_UT_ALARM: Final = 90
REG_CHARGING_UT_PROTECTION: Final = 91
REG_CHARGING_UT_RELEASE: Final = 92
REG_DISCHARGING_UT_ALARM: Final = 93
REG_DISCHARGING_UT_PROTECTION: Final = 94
REG_DISCHARGING_UT_RELEASE: Final = 95

# Protection Settings - MOSFET Temperature
REG_MOSFET_OT_ALARM: Final = 96
REG_MOSFET_OT_PROTECTION: Final = 97
REG_MOSFET_OT_RELEASE: Final = 98

# Protection Settings - Environment Temperature
REG_ENV_OT_ALARM: Final = 99
REG_ENV_OT_PROTECTION: Final = 100
REG_ENV_OT_RELEASE: Final = 101
REG_ENV_UT_ALARM: Final = 102
REG_ENV_UT_PROTECTION: Final = 103
REG_ENV_UT_RELEASE: Final = 104

# Balance and Charge Settings
REG_BALANCE_START_VOLTAGE: Final = 105
REG_BALANCE_DELTA_VOLTAGE: Final = 106
REG_FULL_CHARGE_VOLTAGE: Final = 107
REG_FULL_CHARGE_CURRENT: Final = 108
REG_CELL_SLEEP_VOLTAGE: Final = 109
REG_CELL_SLEEP_DELAY: Final = 110
REG_SHORT_CIRCUIT_DELAY: Final = 111
REG_SOC_ALARM_THRESHOLD: Final = 112
REG_CHARGING_OC2_PROTECTION: Final = 113
REG_CHARGING_OC2_DELAY: Final = 114

# Version and Identification
REG_VERSION_INFO: Final = 150
REG_MODEL_SN: Final = 160
REG_PACK_SN: Final = 170

# Flag Definitions
WARNING_FLAGS = [
    "Cell OV", "Cell UV", "Pack OV", "Pack UV",
    "Charging OC", "Discharging OC", "Reserved", "Reserved",
    "Charging OT", "Discharging OT", "Charging UT", "Discharging UT",
    "Environment OT", "Environment UT", "MOSFET OT", "SOC Low"
]

PROTECTION_FLAGS = [
    "Cell OV", "Cell UV", "Pack OV", "Pack UV",
    "Charging OC", "Discharging OC", "Short Circuit", "Charger OV",
    "Charging OT", "Discharging OT", "Charging UT", "Discharging UT",
    "MOSFET OT", "Environment OT", "Environment UT", "Reserved"
]

STATUS_FLAGS = [
    "Charging MOSFET Fault", "Discharging MOSFET Fault",
    "Temperature Sensor Fault", "Reserved", "Battery Cell Fault",
    "Front-end Sampling Fault", "Reserved", "Reserved",
    "State of Charge", "State of Discharge", "Charging MOSFET ON",
    "Discharging MOSFET ON", "Charging Limiter ON", "Reserved",
    "Charger Inversed", "Heater ON"
]