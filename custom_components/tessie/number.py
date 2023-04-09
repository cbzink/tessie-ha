"""Tessie binary sensors."""

from homeassistant.components.number import (
    NumberEntity,
    NumberDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import callback
from homeassistant.const import PERCENTAGE

from .const import DOMAIN
from . import TessieEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup Tessie number entities."""

    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    tessie = data["tessie"]

    entities = []

    for vin, vehicle in coordinator.data.items():
        entities.append(ChargeLimitNumberEntity(coordinator, vin, tessie))

    async_add_entities(entities)


class ChargeLimitNumberEntity(TessieEntity, NumberEntity):
    """Representation of a ChargeLimit number entity."""

    _attr_device_class = NumberDeviceClass.BATTERY
    _attr_has_entity_name = True
    _attr_name = "Charge limit"

    @callback
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""

        await self.tessie.charging.set_charge_limit(self.vin, value)
        await self.coordinator.async_request_refresh()

    @property
    def unique_id(self):
        return f"{self.vin}_charge_limit"

    @property
    def native_value(self) -> int:
        """Return charge limit."""

        return self.coordinator.data[self.vin].charge_state.charge_limit_soc

    @property
    def native_min_value(self) -> int:
        """Return minimum charge limit."""

        return self.coordinator.data[self.vin].charge_state.charge_limit_soc_min

    @property
    def native_max_value(self) -> int:
        """Return maximum charge limit."""

        return self.coordinator.data[self.vin].charge_state.charge_limit_soc_max

    @property
    def native_unit_of_measurement(self) -> str:
        """Return percentage."""
        return PERCENTAGE
