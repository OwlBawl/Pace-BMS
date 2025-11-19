"""Binary sensor platform for Pace BMS."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PaceBMSCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Pace BMS binary sensors."""
    coordinator: PaceBMSCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        PaceBMSStatusBinarySensor(coordinator, 8, "Charging"),
        PaceBMSStatusBinarySensor(coordinator, 9, "Discharging"),
        PaceBMSStatusBinarySensor(coordinator, 10, "Charging MOSFET"),
        PaceBMSStatusBinarySensor(coordinator, 11, "Discharging MOSFET"),
    ]

    async_add_entities(entities)


class PaceBMSStatusBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for BMS status bits."""
    
    # Enable has_entity_name to automatically use device name prefix
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self, coordinator: PaceBMSCoordinator, bit: int, name: str
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._bit = bit
        # Set name without device prefix - HA will add it automatically
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.entry_id}_status_{bit}"
        # Link to the device
        self._attr_device_info = coordinator.device_info

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        value = self.coordinator.data.get("status_fault", 0)
        return bool(value & (1 << self._bit))