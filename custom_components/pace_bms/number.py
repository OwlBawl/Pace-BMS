"""Number platform for Pace BMS."""
import logging

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    REG_PACK_OV_ALARM,
    REG_PACK_OV_PROTECTION,
    REG_PACK_OV_RELEASE,
    REG_PACK_OV_DELAY,
    REG_CELL_OV_ALARM,
    REG_CELL_OV_PROTECTION,
    REG_CELL_OV_RELEASE,
    REG_CELL_OV_DELAY,
    REG_PACK_UV_ALARM,
    REG_PACK_UV_PROTECTION,
    REG_PACK_UV_RELEASE,
    REG_PACK_UV_DELAY,
    REG_CELL_UV_ALARM,
    REG_CELL_UV_PROTECTION,
    REG_CELL_UV_RELEASE,
    REG_CELL_UV_DELAY,
    REG_CHARGING_OC_ALARM,
    REG_CHARGING_OC_PROTECTION,
    REG_CHARGING_OC_DELAY,
    REG_CHARGING_OC2_PROTECTION,
    REG_CHARGING_OC2_DELAY,
    REG_DISCHARGING_OC_ALARM,
    REG_DISCHARGING_OC_PROTECTION,
    REG_DISCHARGING_OC_DELAY,
    REG_DISCHARGING_OC2_PROTECTION,
    REG_DISCHARGING_OC2_DELAY,
    REG_CHARGING_OT_ALARM,
    REG_CHARGING_OT_PROTECTION,
    REG_CHARGING_OT_RELEASE,
    REG_CHARGING_UT_ALARM,
    REG_CHARGING_UT_PROTECTION,
    REG_CHARGING_UT_RELEASE,
    REG_DISCHARGING_OT_ALARM,
    REG_DISCHARGING_OT_PROTECTION,
    REG_DISCHARGING_OT_RELEASE,
    REG_DISCHARGING_UT_ALARM,
    REG_DISCHARGING_UT_PROTECTION,
    REG_DISCHARGING_UT_RELEASE,
    REG_MOSFET_OT_ALARM,
    REG_MOSFET_OT_PROTECTION,
    REG_MOSFET_OT_RELEASE,
    REG_ENV_OT_ALARM,
    REG_ENV_OT_PROTECTION,
    REG_ENV_OT_RELEASE,
    REG_ENV_UT_ALARM,
    REG_ENV_UT_PROTECTION,
    REG_ENV_UT_RELEASE,
    REG_BALANCE_START_VOLTAGE,
    REG_BALANCE_DELTA_VOLTAGE,
    REG_FULL_CHARGE_VOLTAGE,
    REG_FULL_CHARGE_CURRENT,
    REG_CELL_SLEEP_VOLTAGE,
    REG_CELL_SLEEP_DELAY,
    REG_SHORT_CIRCUIT_DELAY,
    REG_SOC_ALARM_THRESHOLD,
)

_LOGGER = logging.getLogger(__name__)
from .coordinator import PaceBMSCoordinator


# Register address mapping for all configurable parameters
PARAMETER_CONFIG = {
    # ==================== PACK OVERVOLTAGE PROTECTION ====================
    "pack_ov_alarm": {
        "address": REG_PACK_OV_ALARM,
        "scale": 1,
        "min": 20000,
        "max": 29200,
        "step": 100,
        "unit": "mV",
    },
    "pack_ov_protection": {
        "address": REG_PACK_OV_PROTECTION,
        "scale": 1,
        "min": 20000,
        "max": 29200,
        "step": 100,
        "unit": "mV",
    },
    "pack_ov_release": {
        "address": REG_PACK_OV_RELEASE,
        "scale": 1,
        "min": 20000,
        "max": 29200,
        "step": 100,
        "unit": "mV",
    },
    "pack_ov_delay": {
        "address": REG_PACK_OV_DELAY,
        "scale": 10,
        "min": 0.1,
        "max": 25.5,
        "step": 0.1,
        "unit": "s",
    },
    # ==================== CELL OVERVOLTAGE PROTECTION ====================
    "cell_ov_alarm": {
        "address": REG_CELL_OV_ALARM,
        "scale": 1,
        "min": 2500,
        "max": 3650,
        "step": 10,
        "unit": "mV",
    },
    "cell_ov_protection": {
        "address": REG_CELL_OV_PROTECTION,
        "scale": 1,
        "min": 2500,
        "max": 3650,
        "step": 10,
        "unit": "mV",
    },
    "cell_ov_release": {
        "address": REG_CELL_OV_RELEASE,
        "scale": 1,
        "min": 2500,
        "max": 3650,
        "step": 10,
        "unit": "mV",
    },
    "cell_ov_delay": {
        "address": REG_CELL_OV_DELAY,
        "scale": 10,
        "min": 0.1,
        "max": 25.5,
        "step": 0.1,
        "unit": "s",
    },
    # ==================== PACK UNDERVOLTAGE PROTECTION ====================
    "pack_uv_alarm": {
        "address": REG_PACK_UV_ALARM,
        "scale": 1,
        "min": 20000,
        "max": 29200,
        "step": 100,
        "unit": "mV",
    },
    "pack_uv_protection": {
        "address": REG_PACK_UV_PROTECTION,
        "scale": 1,
        "min": 20000,
        "max": 29200,
        "step": 100,
        "unit": "mV",
    },
    "pack_uv_release": {
        "address": REG_PACK_UV_RELEASE,
        "scale": 1,
        "min": 20000,
        "max": 29200,
        "step": 100,
        "unit": "mV",
    },
    "pack_uv_delay": {
        "address": REG_PACK_UV_DELAY,
        "scale": 10,
        "min": 0.1,
        "max": 25.5,
        "step": 0.1,
        "unit": "s",
    },
    # ==================== CELL UNDERVOLTAGE PROTECTION ====================
    "cell_uv_alarm": {
        "address": REG_CELL_UV_ALARM,
        "scale": 1,
        "min": 2500,
        "max": 3650,
        "step": 10,
        "unit": "mV",
    },
    "cell_uv_protection": {
        "address": REG_CELL_UV_PROTECTION,
        "scale": 1,
        "min": 2500,
        "max": 3650,
        "step": 10,
        "unit": "mV",
    },
    "cell_uv_release": {
        "address": REG_CELL_UV_RELEASE,
        "scale": 1,
        "min": 2500,
        "max": 3650,
        "step": 10,
        "unit": "mV",
    },
    "cell_uv_delay": {
        "address": REG_CELL_UV_DELAY,
        "scale": 10,
        "min": 0.1,
        "max": 25.5,
        "step": 0.1,
        "unit": "s",
    },
    # ==================== CHARGING OVERCURRENT PROTECTION ====================
    "charging_oc_alarm": {
        "address": REG_CHARGING_OC_ALARM,
        "scale": 1,
        "min": 50,
        "max": 250,
        "step": 1,
        "unit": "A",
    },
    "charging_oc_protection": {
        "address": REG_CHARGING_OC_PROTECTION,
        "scale": 1,
        "min": 50,
        "max": 250,
        "step": 1,
        "unit": "A",
    },
    "charging_oc_delay": {
        "address": REG_CHARGING_OC_DELAY,
        "scale": 10,
        "min": 0.1,
        "max": 25.5,
        "step": 0.1,
        "unit": "s",
    },
    "charging_oc2_protection": {
        "address": REG_CHARGING_OC2_PROTECTION,
        "scale": 1,
        "min": 50,
        "max": 250,
        "step": 1,
        "unit": "A",
    },
    "charging_oc2_delay": {
        "address": REG_CHARGING_OC2_DELAY,
        "scale": 0.04,
        "min": 25,
        "max": 6375,
        "step": 25,
        "unit": "ms",
    },
    # ==================== DISCHARGING OVERCURRENT PROTECTION ====================
    "discharging_oc_alarm": {
        "address": REG_DISCHARGING_OC_ALARM,
        "scale": 1,
        "min": 50,
        "max": 250,
        "step": 1,
        "unit": "A",
    },
    "discharging_oc_protection": {
        "address": REG_DISCHARGING_OC_PROTECTION,
        "scale": 1,
        "min": 50,
        "max": 250,
        "step": 1,
        "unit": "A",
    },
    "discharging_oc_delay": {
        "address": REG_DISCHARGING_OC_DELAY,
        "scale": 10,
        "min": 0.1,
        "max": 25.5,
        "step": 0.1,
        "unit": "s",
    },
    "discharging_oc2_protection": {
        "address": REG_DISCHARGING_OC2_PROTECTION,
        "scale": 1,
        "min": 50,
        "max": 250,
        "step": 1,
        "unit": "A",
    },
    "discharging_oc2_delay": {
        "address": REG_DISCHARGING_OC2_DELAY,
        "scale": 0.04,
        "min": 25,
        "max": 6375,
        "step": 25,
        "unit": "ms",
    },
    # ==================== CHARGING TEMPERATURE PROTECTION ====================
    "charging_ot_alarm": {
        "address": REG_CHARGING_OT_ALARM,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "charging_ot_protection": {
        "address": REG_CHARGING_OT_PROTECTION,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "charging_ot_release": {
        "address": REG_CHARGING_OT_RELEASE,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "charging_ut_alarm": {
        "address": REG_CHARGING_UT_ALARM,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "charging_ut_protection": {
        "address": REG_CHARGING_UT_PROTECTION,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "charging_ut_release": {
        "address": REG_CHARGING_UT_RELEASE,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    # ==================== DISCHARGING TEMPERATURE PROTECTION ====================
    "discharging_ot_alarm": {
        "address": REG_DISCHARGING_OT_ALARM,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "discharging_ot_protection": {
        "address": REG_DISCHARGING_OT_PROTECTION,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "discharging_ot_release": {
        "address": REG_DISCHARGING_OT_RELEASE,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "discharging_ut_alarm": {
        "address": REG_DISCHARGING_UT_ALARM,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "discharging_ut_protection": {
        "address": REG_DISCHARGING_UT_PROTECTION,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "discharging_ut_release": {
        "address": REG_DISCHARGING_UT_RELEASE,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    # ==================== MOSFET TEMPERATURE PROTECTION ====================
    "mosfet_ot_alarm": {
        "address": REG_MOSFET_OT_ALARM,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "mosfet_ot_protection": {
        "address": REG_MOSFET_OT_PROTECTION,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "mosfet_ot_release": {
        "address": REG_MOSFET_OT_RELEASE,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    # ==================== ENVIRONMENT TEMPERATURE PROTECTION ====================
    "env_ot_alarm": {
        "address": REG_ENV_OT_ALARM,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "env_ot_protection": {
        "address": REG_ENV_OT_PROTECTION,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "env_ot_release": {
        "address": REG_ENV_OT_RELEASE,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "env_ut_alarm": {
        "address": REG_ENV_UT_ALARM,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "env_ut_protection": {
        "address": REG_ENV_UT_PROTECTION,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    "env_ut_release": {
        "address": REG_ENV_UT_RELEASE,
        "scale": 10,
        "min": -50,
        "max": 150,
        "step": 5,
        "unit": "°C",
    },
    # ==================== BALANCE SETTINGS ====================
    "balance_start_voltage": {
        "address": REG_BALANCE_START_VOLTAGE,
        "scale": 1,
        "min": 2500,
        "max": 3650,
        "step": 10,
        "unit": "mV",
    },
    "balance_delta_voltage": {
        "address": REG_BALANCE_DELTA_VOLTAGE,
        "scale": 1,
        "min": 10,
        "max": 100,
        "step": 10,
        "unit": "mV",
    },
    # ==================== CHARGE SETTINGS ====================
    "full_charge_voltage": {
        "address": REG_FULL_CHARGE_VOLTAGE,
        "scale": 1,
        "min": 20000,
        "max": 29200,
        "step": 100,
        "unit": "mV",
    },
    "full_charge_current": {
        "address": REG_FULL_CHARGE_CURRENT,
        "scale": 1,
        "min": 1000,
        "max": 20000,
        "step": 500,
        "unit": "mA",
    },
    "cell_sleep_voltage": {
        "address": REG_CELL_SLEEP_VOLTAGE,
        "scale": 1,
        "min": 2500,
        "max": 3650,
        "step": 10,
        "unit": "mV",
    },
    "cell_sleep_delay": {
        "address": REG_CELL_SLEEP_DELAY,
        "scale": 1,
        "min": 1,
        "max": 60,
        "step": 1,
        "unit": "min",
    },
    "short_circuit_delay": {
        "address": REG_SHORT_CIRCUIT_DELAY,
        "scale": 0.04,
        "min": 50,
        "max": 500,
        "step": 50,
        "unit": "μs",
    },
    "soc_alarm_threshold": {
        "address": REG_SOC_ALARM_THRESHOLD,
        "scale": 1,
        "min": 1,
        "max": 50,
        "step": 1,
        "unit": "%",
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Pace BMS number entities."""
    coordinator: PaceBMSCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for key, config in PARAMETER_CONFIG.items():
        entities.append(PaceBMSNumber(coordinator, key, config))

    async_add_entities(entities)


class PaceBMSNumber(CoordinatorEntity, NumberEntity):
    """Representation of a Pace BMS configurable parameter."""
    
    # Enable has_entity_name to automatically use device name prefix
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: PaceBMSCoordinator,
        key: str,
        config: dict,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._key = key
        self._config = config
        # Set name without device prefix - HA will add it automatically
        self._attr_name = key.replace('_', ' ').title()
        self._attr_unique_id = f"{coordinator.entry_id}_{key}"
        self._attr_native_min_value = config["min"]
        self._attr_native_max_value = config["max"]
        self._attr_native_step = config["step"]
        self._attr_mode = NumberMode.SLIDER
        self._attr_native_unit_of_measurement = config.get("unit")
        # Link to the device
        self._attr_device_info = coordinator.device_info

    @property
    def native_value(self):
        """Return the current value."""
        value = self.coordinator.data.get(self._key)
        if value is None:
            return self._config["min"]
        return value

    async def async_set_native_value(self, value: float) -> None:
        """Update the value."""
        if value < self._config["min"] or value > self._config["max"]:
            _LOGGER.error(
                "Value %.3f for %s is outside valid range [%.3f, %.3f]",
                value, self._key, self._config["min"], self._config["max"]
            )
            return
        
        scaled_value = int(value * self._config["scale"])
        
        _LOGGER.info(
            "Writing %s: value=%.3f, scaled=%d, address=%d, scale=%d",
            self._key, value, scaled_value, self._config["address"], self._config["scale"]
        )
        
        success = await self.hass.async_add_executor_job(
            self.coordinator.write_register,
            self._config["address"],
            scaled_value,
        )
        
        if not success:
            _LOGGER.error("Failed to write %s to address %d", self._key, self._config["address"])
            return
        
        await self.coordinator.async_request_refresh()
        
        readback_value = self.coordinator.data.get(self._key)
        if readback_value is not None:
            expected_scaled = int(value * self._config["scale"])
            actual_scaled = int(readback_value * self._config["scale"])
            if abs(expected_scaled - actual_scaled) > 1:
                _LOGGER.warning(
                    "Write verification failed for %s: expected=%d, actual=%d",
                    self._key, expected_scaled, actual_scaled
                )
            else:
                _LOGGER.info("Write verification successful for %s", self._key)