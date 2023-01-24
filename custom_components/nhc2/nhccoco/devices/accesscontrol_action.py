from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PARAMETER_ACTION, PARAMETER_RINGTONE, \
    PARAMETER_DECLINE_CALL_APPLIED_ON_ALL_DEVICES, PROPERTY_DECLINE_CALL_APPLIED_ON_ALL_DEVICES_VALUE_TRUE, \
    PARAMETER_BUTTON_ID, PROPERTY_BASIC_STATE, PROPERTY_BASIC_STATE_VALUE_ON, PROPERTY_BASIC_STATE_VALUE_TRIGGERED, \
    PROPERTY_DOORLOCK, PROPERTY_DOORLOCK_VALUE_OPEN, PROPERTY_DOORLOCK_VALUE_CLOSED

from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoAccesscontrolAction(CoCoDevice):
    @property
    def status_basic_state(self) -> str:
        return self.extract_property_value(PROPERTY_BASIC_STATE)

    @property
    def is_basic_state_on(self) -> bool:
        return self.status_basic_state == PROPERTY_BASIC_STATE_VALUE_ON

    @property
    def status_doorlock(self) -> str:
        return self.extract_property_value(PROPERTY_DOORLOCK)

    @property
    def is_doorlock_open(self) -> bool:
        return self.status_doorlock == PROPERTY_DOORLOCK_VALUE_OPEN

    @property
    def is_doorlock_closed(self) -> bool:
        return self.status_doorlock == PROPERTY_DOORLOCK_VALUE_CLOSED

    @property
    def status_decline_call_applied_on_all_devices(self) -> str:
        return self.extract_parameter_value(PARAMETER_DECLINE_CALL_APPLIED_ON_ALL_DEVICES)

    @property
    def is_decline_call_applied_on_all_devices(self) -> bool:
        return self.status_decline_call_applied_on_all_devices == PROPERTY_DECLINE_CALL_APPLIED_ON_ALL_DEVICES_VALUE_TRUE

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def press(self, gateway):
        gateway._add_device_control(
            self._device.uuid,
            PROPERTY_BASIC_STATE,
            PROPERTY_BASIC_STATE_VALUE_TRIGGERED
        )

    def open_doorlock(self, gateway):
        gateway._add_device_control(
            self._device.uuid,
            PROPERTY_DOORLOCK,
            PROPERTY_DOORLOCK_VALUE_OPEN
        )
