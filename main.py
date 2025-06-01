import os
import json
import logging
import subprocess
from rapidfuzz import process
from ulauncher.api import Extension, Result, Action

logger = logging.getLogger(__name__)

DEVICE_ICONS = {
    'input-gaming': 'gamepad',
}

class BluetoothQC(Extension):
    def on_input(self, input_text: str, trigger_id: str):
        items = []
        devices = {}

        bluetooth_list = subprocess.getoutput("timeout 5s bluetoothctl devices Paired")
        connected_device_list = subprocess.getoutput("timeout 5s bluetoothctl devices Connected")

        for device in bluetooth_list.strip().splitlines():
            parts = device.strip().split(' ')
            if len(parts) < 3:
                continue
            device_mac = parts[1]
            device_name = ' '.join(parts[2:]).capitalize()

            try:
                device_info = subprocess.getoutput(f"timeout 5s bluetoothctl info {device_mac}")
                device_type_line = next((line for line in device_info.splitlines() if "Icon:" in line), None)
                device_type = device_type_line.split(':', 1)[1].strip() if device_type_line else "unknown"
            except Exception as e:
                logger.error(f"Error getting info for {device_mac}: {e}")
                device_type = "unknown"

            is_connected = device_mac in connected_device_list
            state = 'Select to Disconnect' if is_connected else 'Select to Connect'
            devices[device_name] = (device_mac, device_type, state)

        if not devices:
            return [
                Result(
                    name="No devices found",
                    description="Either bluetoothctl is missing or you haven't connected any devices yet",
                    icon="images/disconnect.png",
                    on_enter=Action("none", keep_app_open=True)
                )
            ]

        sorted_keys = process.extract(input_text, devices.keys(), limit=None)
        sorted_devices = {k: devices[k] for k, _, _ in sorted_keys} if sorted_keys else devices

        for name, (mac, dev_type, action_label) in sorted_devices.items():
            action_cmd = f"{'connect' if 'Connect' in action_label else 'disconnect'} {mac}"
            icon_base = DEVICE_ICONS.get(dev_type, "connect" if 'Connect' in action_label else "disconnect")
            icon = f"{icon_base}.png" if 'Connect' in action_label else f"{icon_base}_disconnect.png"
            items.append(Result(
                name=f"{name} | {action_label}",
                description=mac,
                icon=f"images/{icon}",
                on_enter=Action(action_cmd, keep_app_open=True)
            ))

        return items

    def on_item_enter(self, data):
        if data == 'none':
            return Action.HideWindow()

        ret = os.system(f"timeout 8s bluetoothctl {data}")
        result_msg = f"{data.split()[0].capitalize()}ed Successfully" if ret == 0 else f"{data.split()[0].capitalize()}ion Failed"

        return [
            Result(
                name=result_msg,
                icon="images/icon.png",
                on_enter=Action.HideWindow()
            )
        ]


if __name__ == "__main__":
    BluetoothQC().run()
