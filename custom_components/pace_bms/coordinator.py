"""DataUpdateCoordinator for Pace BMS."""
import logging
from datetime import timedelta
from typing import Any

from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_BAUDRATE,
    CONF_PORT,
    CONF_SLAVE_ID,
    DOMAIN,
    MODBUS_BYTESIZE,
    MODBUS_PARITY,
    MODBUS_STOPBITS,
    MODBUS_TIMEOUT,
    REG_BASIC_DATA_COUNT,
    REG_BASIC_DATA_START,
    REG_CELL_VOLTAGE_COUNT,
    REG_CELL_VOLTAGE_START,
    REG_MODEL_SN,
    REG_PACK_SN,
    REG_PROTECTION_PARAMS_COUNT,
    REG_PROTECTION_PARAMS_START,
    REG_STATUS_FLAGS_COUNT,
    REG_STATUS_FLAGS_START,
    REG_TEMP_GROUP_COUNT,
    REG_TEMP_GROUP_START,
    REG_VERSION_INFO,
)

_LOGGER = logging.getLogger(__name__)


class PaceBMSCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Pace BMS data."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: dict[str, Any],
        update_interval: timedelta,
        entry_id: str,
    ) -> None:
        """Initialize."""
        self.config = config
        self.client: ModbusSerialClient | None = None
        self._slave_id = config[CONF_SLAVE_ID]
        self._entry_id = entry_id
        # Store the user-provided name
        self._device_name = config.get(CONF_NAME, "Pace BMS")

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    @property
    def device_name(self) -> str:
        """Return the device name."""
        return self._device_name

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name=self._device_name,  # Use user-provided name
            manufacturer="Pace",
            model="BMS",
            sw_version="1.0.0",
            hw_version=f"Slave ID {self._slave_id}",
            configuration_url=f"homeassistant://config/devices/device/{self._entry_id}",
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via Modbus."""
        return await self.hass.async_add_executor_job(self._fetch_data)

    def _connect(self) -> None:
        """Connect to Modbus device."""
        # Close existing connection if it's in a bad state
        if self.client is not None:
            if not self.client.is_socket_open():
                try:
                    self.client.close()
                except Exception as err:
                    _LOGGER.debug("Error closing old connection: %s", err)
                self.client = None
            else:
                # Connection appears to be open
                return
        
        # Create new connection
        if self.client is None:
            _LOGGER.debug(
                "Connecting to BMS at %s (baudrate=%s, slave_id=%s)",
                self.config[CONF_PORT],
                self.config[CONF_BAUDRATE],
                self._slave_id,
            )
            self.client = ModbusSerialClient(
                port=self.config[CONF_PORT],
                baudrate=self.config[CONF_BAUDRATE],
                bytesize=MODBUS_BYTESIZE,
                parity=MODBUS_PARITY,
                stopbits=MODBUS_STOPBITS,
                timeout=MODBUS_TIMEOUT,
            )
            if not self.client.connect():
                self.client = None
                raise UpdateFailed(
                    f"Failed to connect to BMS at {self.config[CONF_PORT]}. "
                    f"Check that the device is connected and not in use by another application."
                )
            _LOGGER.info("Successfully connected to BMS at %s", self.config[CONF_PORT])

    def disconnect(self) -> None:
        """Disconnect from Modbus device."""
        if self.client is not None:
            try:
                self.client.close()
                _LOGGER.debug("Disconnected from BMS")
            except Exception as err:
                _LOGGER.debug("Error disconnecting: %s", err)
            finally:
                self.client = None

    def _read_holding_registers(self, address: int, count: int = 1) -> list[int]:
        """Read holding registers."""
        try:
            self._connect()
        except Exception as err:
            # Force disconnect on connection error
            self.disconnect()
            raise
        
        try:
            result = self.client.read_holding_registers(
                address=address,
                count=count,
                device_id=self._slave_id,
            )
            if result.isError():
                _LOGGER.error("Modbus error reading address %d: %s", address, result)
                # Don't immediately disconnect on read error, might be transient
                raise UpdateFailed(f"Modbus error reading address {address}: {result}")
            return result.registers
        except ModbusException as err:
            _LOGGER.error("Modbus exception: %s", err)
            # Disconnect on exception to force reconnect next time
            self.disconnect()
            raise UpdateFailed(f"Modbus exception: {err}") from err
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", err)
            self.disconnect()
            raise UpdateFailed(f"Unexpected error: {err}") from err

    def write_register(self, address: int, value: int) -> bool:
        """Write to a holding register using 0x10 (write multiple registers)."""
        self._connect()
        try:
            _LOGGER.debug("Writing to register %d: value=%d, slave_id=%d (using 0x10)", address, value, self._slave_id)
            # Use write_registers (0x10) with single-element array as required by BMS
            result = self.client.write_registers(
                address=address,
                values=[value],
                device_id=self._slave_id,
            )
            if result.isError():
                _LOGGER.error("Modbus write error for address %d: %s", address, result)
                return False
            _LOGGER.debug("Successfully wrote to register %d using 0x10", address)
            return True
        except ModbusException as err:
            _LOGGER.error("Modbus exception writing register %d: %s", address, err)
            return False
        except Exception as err:
            _LOGGER.error("Unexpected error writing register %d: %s", address, err)
            return False

    def _fetch_data(self) -> dict[str, Any]:
        """Fetch all data from BMS."""
        data = {}

        try:
            # Read basic measurements in ONE transaction (registers 0-7)
            basic_data = self._read_holding_registers(
                REG_BASIC_DATA_START, REG_BASIC_DATA_COUNT
            )
            data["current"] = self._to_signed_16(basic_data[0]) * 0.01
            data["pack_voltage"] = basic_data[1] * 0.01
            data["soc"] = basic_data[2]
            data["soh"] = basic_data[3]
            data["remain_capacity"] = basic_data[4] * 0.01
            data["full_capacity"] = basic_data[5] * 0.01
            data["design_capacity"] = basic_data[6] * 0.01
            data["cycle_count"] = basic_data[7]

            # Read status flags in ONE transaction (registers 9-12)
            status_data = self._read_holding_registers(
                REG_STATUS_FLAGS_START, REG_STATUS_FLAGS_COUNT
            )
            data["warning_flags"] = status_data[0]
            data["protection_flags"] = status_data[1]
            data["status_fault"] = status_data[2]
            data["balance_status"] = status_data[3]

            # Read cell voltages in ONE transaction (registers 15-22)
            cell_voltages = self._read_holding_registers(
                REG_CELL_VOLTAGE_START, REG_CELL_VOLTAGE_COUNT
            )
            for i, voltage in enumerate(cell_voltages, start=1):
                data[f"cell_{i}_voltage"] = voltage * 0.001

            # Read temperatures in ONE transaction (registers 31-36)
            temp_data = self._read_holding_registers(
                REG_TEMP_GROUP_START, REG_TEMP_GROUP_COUNT
            )
            data["temp_1"] = self._to_signed_16(temp_data[0]) * 0.1
            data["temp_2"] = self._to_signed_16(temp_data[1]) * 0.1
            # Registers 33-34 are unused/reserved
            data["mosfet_temp"] = self._to_signed_16(temp_data[4]) * 0.1
            data["env_temp"] = self._to_signed_16(temp_data[5]) * 0.1

            # Read parameter values for number entities
            self._fetch_parameter_values(data)

            # Version and identification (string data, 10 registers each = 20 bytes)
            try:
                # Read Version Info (address 150, 10 registers)
                version_regs = self._read_holding_registers(REG_VERSION_INFO, 10)
                data["version_info"] = self._registers_to_string(version_regs)
                
                # Read Model SN (address 160, 10 registers)
                model_regs = self._read_holding_registers(REG_MODEL_SN, 10)
                data["model_sn"] = self._registers_to_string(model_regs)
                
                # Read Pack SN (address 170, 10 registers)
                pack_regs = self._read_holding_registers(REG_PACK_SN, 10)
                data["pack_sn"] = self._registers_to_string(pack_regs)
            except Exception as err:
                _LOGGER.warning("Failed to read identification strings: %s", err)
                data["version_info"] = "Unknown"
                data["model_sn"] = "Unknown"
                data["pack_sn"] = "Unknown"

            return data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with BMS: {err}") from err

    def _fetch_parameter_values(self, data: dict[str, Any]) -> None:
        """Fetch parameter values for number entities."""
        # Import here to avoid circular imports
        from .number import PARAMETER_CONFIG
        
        try:
            # Read ALL protection parameters in ONE transaction (registers 60-114)
            param_data = self._read_holding_registers(
                REG_PROTECTION_PARAMS_START, REG_PROTECTION_PARAMS_COUNT
            )
            
            for key, config in PARAMETER_CONFIG.items():
                try:
                    # Calculate offset from base address (60)
                    offset = config["address"] - REG_PROTECTION_PARAMS_START
                    raw_value = param_data[offset]
                    
                    # Handle signed values for temperature parameters
                    if "temp" in key or "ot_" in key or "ut_" in key:
                        raw_value = self._to_signed_16(raw_value)
                    
                    # Scale the value back to the display value
                    # For scale > 1: divide to get user-facing value
                    # For scale = 1: value is already in correct units (mV, mA, A, %, min)
                    data[key] = raw_value / config["scale"]
                except Exception as err:
                    _LOGGER.warning("Failed to parse parameter %s: %s", key, err)
                    # Set a default value if parsing fails
                    data[key] = config["min"]
                    
        except Exception as err:
            _LOGGER.warning("Failed to read protection parameters block: %s", err)
            # Fallback to default values for all parameters
            for key, config in PARAMETER_CONFIG.items():
                data[key] = config["min"]

    @staticmethod
    def _to_signed_16(value: int) -> int:
        """Convert unsigned 16-bit to signed."""
        return value if value < 32768 else value - 65536

    @staticmethod
    def _registers_to_string(registers: list[int]) -> str:
        """Convert Modbus registers to ASCII string."""
        # Each register is 2 bytes (big-endian)
        bytes_data = []
        for reg in registers:
            bytes_data.append((reg >> 8) & 0xFF)  # High byte
            bytes_data.append(reg & 0xFF)          # Low byte
        
        # Convert to string, removing null bytes and trailing whitespace
        return bytes(bytes_data).decode('ascii', errors='ignore').rstrip('\x00 ')