"""The Pace BMS integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .coordinator import PaceBMSCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.NUMBER,
    Platform.BINARY_SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pace BMS from a config entry."""
    coordinator = PaceBMSCoordinator(
        hass,
        entry.data,
        timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady from err

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok