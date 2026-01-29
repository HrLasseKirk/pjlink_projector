from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .pjlink import PJLinkClient


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    client = PJLinkClient(
        entry.data["host"],
        entry.data.get("port", 4352),
        entry.data.get("password"),
    )
    async_add_entities([PJLinkPowerSensor(client)])


class PJLinkPowerSensor(SensorEntity):
    _attr_name = "Projector Power"
    _attr_icon = "mdi:projector"
    _attr_native_unit_of_measurement = None

    def __init__(self, client: PJLinkClient) -> None:
        self._client = client
        self._attr_native_value = None

    async def async_update(self) -> None:
        self._attr_native_value = await self._client.get_power()

