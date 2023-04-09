"""The Tessie integration."""

from homeassistant.const import (
    Platform,
)

DOMAIN = "tessie"

PLATFORMS = [Platform.BINARY_SENSOR, Platform.NUMBER, Platform.DEVICE_TRACKER]

UPDATE_INTERVAL = 30
