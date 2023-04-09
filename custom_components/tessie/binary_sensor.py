"""Tessie binary sensors."""

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import TessieEntity
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup Tessie binary sensors."""

    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    tessie = data["tessie"]

    entities = []

    for vin, vehicle in coordinator.data.items():
        entities.append(PluggedInBinarySensor(coordinator, vin, tessie))
        entities.append(ChargingBinarySensor(coordinator, vin, tessie))

    async_add_entities(entities)


class PluggedInBinarySensor(TessieEntity, BinarySensorEntity):
    """Representation of a PluggedIn binary sensor."""

    _attr_device_class = BinarySensorDeviceClass.PLUG
    _attr_has_entity_name = True
    _attr_name = "Plugged in"

    @property
    def unique_id(self):
        return f"{self.vin}_plugged_in"

    @property
    def is_on(self):
        return (
            self.coordinator.data[self.vin].charge_state.charge_port_latch == "Engaged"
        )


class ChargingBinarySensor(TessieEntity, BinarySensorEntity):
    """Representation of a Charging binary sensor."""

    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING
    _attr_has_entity_name = True
    _attr_name = "Charging"

    @property
    def unique_id(self):
        return f"{self.vin}_charging"

    @property
    def is_on(self):
        return self.coordinator.data[self.vin].charge_state.charging_state == "Charging"
