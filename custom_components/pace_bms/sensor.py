"""Sensor platform for Pace BMS."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PROTECTION_FLAGS, STATUS_FLAGS, WARNING_FLAGS
from .coordinator import PaceBMSCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Pace BMS sensors."""
    coordinator: PaceBMSCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        # Basic measurements
        PaceBMSSensor(
            coordinator,
            "current",
            "Current",
            UnitOfElectricCurrent.AMPERE,
            SensorDeviceClass.CURRENT,
            SensorStateClass.MEASUREMENT,
        ),
        PaceBMSSensor(
            coordinator,
            "pack_voltage",
            "Pack Voltage",
            UnitOfElectricPotential.VOLT,
            SensorDeviceClass.VOLTAGE,
            SensorStateClass.MEASUREMENT,
        ),
        PaceBMSSensor(
            coordinator,
            "soc",
            "State of Charge",
            PERCENTAGE,
            SensorDeviceClass.BATTERY,
            SensorStateClass.MEASUREMENT,
        ),
        PaceBMSSensor(
            coordinator,
            "soh",
            "State of Health",
            PERCENTAGE,
            None,
            SensorStateClass.MEASUREMENT,
        ),
        PaceBMSSensor(
            coordinator,
            "remain_capacity",
            "Remaining Capacity",
            "Ah",
            None,
            SensorStateClass.MEASUREMENT,
        ),
        PaceBMSSensor(
            coordinator,
            "full_capacity",
            "Full Capacity",
            "Ah",
            None,
            SensorStateClass.MEASUREMENT,
        ),
        PaceBMSSensor(
            coordinator,
            "design_capacity",
            "Design Capacity",
            "Ah",
            None,
            SensorStateClass.MEASUREMENT,
        ),
        PaceBMSSensor(
            coordinator,
            "cycle_count",
            "Cycle Count",
            "cycles",
            None,
            SensorStateClass.TOTAL_INCREASING,
        ),
        # Temperatures
        PaceBMSSensor(
            coordinator,
            "temp_1",
            "Temperature 1",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
        ),
        PaceBMSSensor(
            coordinator,
            "temp_2",
            "Temperature 2",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
        ),
        PaceBMSSensor(
            coordinator,
            "mosfet_temp",
            "MOSFET Temperature",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
        ),
        PaceBMSSensor(
            coordinator,
            "env_temp",
            "Environment Temperature",
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
        ),
    ]

    # Add cell voltage sensors
    for i in range(1, 9):
        entities.append(
            PaceBMSSensor(
                coordinator,
                f"cell_{i}_voltage",
                f"Cell {i} Voltage",
                UnitOfElectricPotential.VOLT,
                SensorDeviceClass.VOLTAGE,
                SensorStateClass.MEASUREMENT,
            )
        )

    # Add flag decode sensors
    entities.extend(
        [
            PaceBMSFlagSensor(coordinator, "warning_flags", "Warnings", WARNING_FLAGS),
            PaceBMSFlagSensor(
                coordinator, "protection_flags", "Protections", PROTECTION_FLAGS
            ),
            PaceBMSFlagSensor(coordinator, "status_fault", "Status", STATUS_FLAGS),
            PaceBMSBalanceSensor(coordinator),
        ]
    )

    # Add version and identification sensors
    entities.extend(
        [
            PaceBMSSensor(coordinator, "version_info", "Version Info", None, None, None),
            PaceBMSSensor(coordinator, "model_sn", "Model SN", None, None, None),
            PaceBMSSensor(coordinator, "pack_sn", "Pack SN", None, None, None),
        ]
    )

    async_add_entities(entities)


class PaceBMSSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Pace BMS sensor."""
    
    # Enable has_entity_name to automatically use device name prefix
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: PaceBMSCoordinator,
        key: str,
        name: str,
        unit: str | None = None,
        device_class: str | None = None,
        state_class: str | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        # Set name without device prefix - HA will add it automatically
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.entry_id}_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        # Link to the device
        self._attr_device_info = coordinator.device_info
        
        # Set precision for voltage and current sensors
        if device_class in [SensorDeviceClass.VOLTAGE, SensorDeviceClass.CURRENT]:
            self._attr_suggested_display_precision = 3

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._key)


class PaceBMSFlagSensor(CoordinatorEntity, SensorEntity):
    """Sensor for decoded flags."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: PaceBMSCoordinator,
        key: str,
        name: str,
        flag_names: list[str],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._flag_names = flag_names
        # Set name without device prefix - HA will add it automatically
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.entry_id}_{key}_decoded"
        self._attr_device_info = coordinator.device_info

    @property
    def native_value(self):
        """Return the decoded flags, filtering out Reserved values."""
        value = self.coordinator.data.get(self._key, 0)
        flags = []
        for i in range(16):
            if value & (1 << i):
                flag_name = self._flag_names[i]
                # Filter out "Reserved" flags
                if flag_name != "Reserved":
                    flags.append(flag_name)
        return ", ".join(flags) if flags else "No"


class PaceBMSBalanceSensor(CoordinatorEntity, SensorEntity):
    """Sensor for balancing cells."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, coordinator: PaceBMSCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        # Set name without device prefix - HA will add it automatically
        self._attr_name = "Balancing Cells"
        self._attr_unique_id = f"{coordinator.entry_id}_balancing_cells"
        self._attr_device_info = coordinator.device_info

    @property
    def native_value(self):
        """Return the balancing cells."""
        value = self.coordinator.data.get("balance_status", 0)
        cells = []
        for i in range(8):
            if value & (1 << i):
                cells.append(str(i + 1))
        return ", ".join(cells) if cells else "Off"