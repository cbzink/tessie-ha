"""Tessie binary sensors."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import callback
from homeassistant.const import PERCENTAGE

from .const import DOMAIN
from . import TessieEntity
from homeassistant.const import TEMP_CELSIUS


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup Tessie sensor entities."""

    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    tessie = data["tessie"]

    entities = []

    for vin, vehicle in coordinator.data.items():
        entities.append(InsideTemperatureSensor(coordinator, vin, tessie))
        entities.append(OutsideTemperatureSensor(coordinator, vin, tessie))
        entities.append(BatteryLevel(coordinator, vin, tessie))

    async_add_entities(entities)


class InsideTemperatureSensor(TessieEntity, SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Vehicle inside temperature"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    @callback
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""

        await self.coordinator.async_request_refresh()

    @property
    def unique_id(self):
        return f"{self.vin}_inside_temperature"

    @property
    def native_value(self) -> float | None:
        """Return charge limit."""

        return self.coordinator.data[self.vin].climate_state.inside_temp

class OutsideTemperatureSensor(TessieEntity, SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Vehicle outside temperature"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    @callback
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""

        await self.coordinator.async_request_refresh()

    @property
    def unique_id(self):
        return f"{self.vin}_outside_temperature"

    @property
    def native_value(self) -> float | None:
        """Return charge limit."""

        return self.coordinator.data[self.vin].climate_state.outside_temp


class BatteryLevel(TessieEntity, SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Battery"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_has_entity_name = True

    @callback
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""

        await self.coordinator.async_request_refresh()

    @property
    def unique_id(self):
        return f"{self.vin}battery_level"

    @property
    def native_value(self) -> float | None:
        """Return charge limit."""

        return self.coordinator.data[self.vin].charge_state.battery_level
