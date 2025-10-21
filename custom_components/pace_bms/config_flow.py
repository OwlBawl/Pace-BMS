"""Config flow for Pace BMS integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_BAUDRATE,
    CONF_PORT,
    CONF_SLAVE_ID,
    DEFAULT_BAUDRATE,
    DEFAULT_PORT,
    DEFAULT_SLAVE_ID,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class PaceBMSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pace BMS."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_PORT]}_{user_input[CONF_SLAVE_ID]}"
            )
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input.get(CONF_NAME, "Pace BMS"),
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default="Pace BMS"): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): str,
                vol.Required(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): vol.In(
                    [4800, 9600, 19200, 38400, 57600, 115200]
                ),
                vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): vol.All(
                    vol.Coerce(int), vol.Range(min=0, max=247)
                ),
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)