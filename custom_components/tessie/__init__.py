"""The Tessie integration."""

import logging

from datetime import timedelta

from tessiepy import TessieClient
from tessiepy.exceptions import AuthenticationError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, UPDATE_INTERVAL, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup Tessie from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    websession = aiohttp_client.async_get_clientsession(hass)

    tessie = TessieClient(entry.data["access_token"], websession)

    async def async_update_data():
        try:
            return await tessie.current_state.vehicles()
        except AuthenticationError:
            raise ConfigEntryAuthFailed
        except Exception:
            raise ConfigEntryNotReady

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Tessie Devices",
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {"tessie": tessie, "coordinator": coordinator}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class TessieEntity(CoordinatorEntity):
    """Base class for Tessie entities."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        vin: str,
        tessie: TessieClient,
    ) -> None:
        """Initialize class."""

        super().__init__(coordinator)

        self.vin = vin
        self.vehicle_name = coordinator.data[vin].display_name
        self.tessie = tessie

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self.vin)},
            name=self.coordinator.data[self.vin].display_name,
            manufacturer="Tesla",
            model=self.coordinator.data[self.vin].vehicle_config.car_type,
            sw_version=self.coordinator.data[self.vin].vehicle_state.car_version,
        )
