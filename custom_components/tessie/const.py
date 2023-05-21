"""The Tessie integration."""

from homeassistant.const import (
    Platform,
)

DOMAIN = "tessie"

PLATFORMS = [Platform.BINARY_SENSOR, Platform.NUMBER, Platform.DEVICE_TRACKER, Platform.SENSOR]

UPDATE_INTERVAL = 30
