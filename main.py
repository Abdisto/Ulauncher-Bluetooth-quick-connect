import json
import logging
import os
import subprocess

from rapidfuzz import process
from ulauncher.api import Extension, Result
from ulauncher.api.actions import RunScriptAction, ExtensionCustomAction, HideWindowAction

logger = logging.getLogger(__name__)

DEVICE_ICONS = {
    'input-gaming': 'gamepad',
}

class BluetoothQC(Extension):
    def __init__(self):
        super().__init__()

    def on_input(self, input_text: str, trigger_id: str):
        items = []
        devices = {}

        bluetooth_list = subprocess.check_output(
            "bash -c 'timeout 5s bluetoothctl devices Paired'",
            shell=True,
            text=True
        )
        connected_device_list = subprocess.check_output(
            "bash -c 'timeout 5s bluetoothctl devices Connected'",
            shell=True,
            text=True
        )

        for device in bluetooth_list.strip().splitlines():
            device_name = ' '.join(device.split(' ')[2:]).capitalize()
            device_mac = device.split(' ')[1]
            try:
                device_type = subprocess.check_output(
                    f"bash -c 'timeout 5s bluetoothctl info {device_mac}' | grep Icon:",
                    shell=True,
                    text=True
                ).split(':')[1].strip()
            except Exception:
                device_type = 'unknown'

            is_connected = device in connected_device_list
            action_label = 'Select to Disconnect' if is_connected else 'Select to Connect'
            devices[device_name] = (device_mac, device_type, action_label)

        if not devices:
            return [
                Result(
                    icon='images/disconnect.png',
                    name="No devices found",
                    description="Either bluetoothctl is missing or you haven't connected any devices yet",
                    on_enter=ExtensionCustomAction("none", keep_app_open=True)
                )
            ]

        # Use fuzzy search
        sorted_keys = process.extract(input_text, devices.keys(), limit=None)
        sorted_devices = {k: devices[k] for k, score, _ in sorted_keys}

        results = []
        for key, (mac, dev_type, label) in sorted_devices.items():
            action = 'disconnect' if 'Disconnect' in label else 'connect'
            data = f"{action} {mac}"

            icon_name = DEVICE_ICONS.get(dev_type, "disconnect" if action == 'disconnect' else "connect")
            if action == 'disconnect' and icon_name != "disconnect":
                icon_name += "_disconnect"

            results.append(Result(
                icon=f'images/{icon_name}.png',
                name=f"{key} | {label}",
                description=mac,
                on_enter=ExtensionCustomAction(data, keep_app_open=True)
            ))

        return results

    def on_item_enter(self, data):
        if data == 'none':
            return HideWindowAction()

        ret = os.system(f"bash -c 'timeout 8s bluetoothctl {data}'")

        prompt = f"{data.split()[0].capitalize()}ed Successfully" if ret == 0 else f"{data.split()[0].capitalize()}ion Failed"

        return [
            Result(
                icon='images/icon.png',
                name=prompt,
                on_enter=HideWindowAction()
            )
        ]


if __name__ == '__main__':
    BluetoothQC().run()
