"""Tessie device tracker entities."""

from homeassistant.components.device_tracker import TrackerEntity, SourceType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from . import TessieEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup Tessie device tracker entities."""

    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    tessie = data["tessie"]

    entities = []

    for vin, vehicle in coordinator.data.items():
        entities.append(VehicleDeviceTrackerEntity(coordinator, vin, tessie))

    async_add_entities(entities)


class VehicleDeviceTrackerEntity(TessieEntity, TrackerEntity):
    """Representation of a Vehicle device tracker entity."""

    _attr_icon = "mdi:car"
    _attr_has_entity_name = True
    _attr_name = None

    @property
    def unique_id(self):
        return f"{self.vin}_device_tracker"

    @property
    def latitude(self) -> float | None:
        return self.coordinator.data[self.vin].drive_state.latitude

    @property
    def longitude(self) -> float | None:
        return self.coordinator.data[self.vin].drive_state.longitude

    @property
    def source_type(self) -> SourceType:
        return SourceType.GPS
