"""Config flow for the Tessie integration."""

import voluptuous as vol

from tessiepy import TessieClient
from tessiepy.exceptions import AuthenticationError

from homeassistant import config_entries
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.helpers import aiohttp_client

from .const import DOMAIN

DATA_SCHEMA = vol.Schema({vol.Required(CONF_ACCESS_TOKEN): str})


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Tessie config flow."""

    VERSION = 1

    async def validate_input(self, access_token: str):
        websession = aiohttp_client.async_get_clientsession(self.hass)
        tessie = TessieClient(access_token, websession)

        try:
            await tessie.current_state.vehicles()
        except AuthenticationError:
            return {CONF_ACCESS_TOKEN: "invalid_access_token"}
        except Exception:
            return {"base": "unknown"}

        return None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors = {}

        if user_input is not None:
            errors = await self.validate_input(user_input[CONF_ACCESS_TOKEN])

            if not errors:
                return self.async_create_entry(title="Tessie", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
