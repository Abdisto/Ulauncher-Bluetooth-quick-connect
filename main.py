import json
import logging
import os
from rapidfuzz import process
from time import sleep
import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)

DEVICE_ICONS = {
#    'audio-headset': 'headphones',
#    'headset': 'headphones',
#    'keyboard': 'keyboard',
#    'mouse': 'mouse',
    'input-gaming': 'gamepad',
#    'phone': 'phone',
}

class BluetoothQC(Extension):

    def __init__(self):
        super(BluetoothQC, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        devices = {}
        query = event.get_argument()
        logger.info('preferences %s' % json.dumps(extension.preferences))

        bluetooth_list = subprocess.check_output(
            "bash -c 'timeout 5s bluetoothctl devices Paired'",
             shell=True,
             text=True
        )
        cleaned_bluetooth_list = bluetooth_list[0:bluetooth_list.find("[\x1b[0;92mNEW\x1b[0m]")]
        connected_device_list = subprocess.check_output(
            "bash -c 'timeout 5s bluetoothctl devices Connected'",
            shell=True,
            text=True
        )
        cleaned_device_dict = {}

        for device in cleaned_bluetooth_list.strip().splitlines():
            device_name = ' '.join(device.split(' ')[2:]).capitalize()
            device_mac = device.split(' ')[1]
            device_type = subprocess.check_output(
                f"bash -c 'timeout 5s bluetoothctl info {device_mac}' | grep Icon:",
                shell=True,
                text=True
            ).split(':')[1].strip()
            if device not in connected_device_list:
                devices[device_name] = device_mac, device_type, 'Select to Connect'
            else:
                devices[device_name] = device_mac, device_type, 'Select to Disconnect'

        # give user feedback if no devices has been specified
        if len(devices) == 0:
            items.append(ExtensionResultItem(icon='images/disconnect.png',
                                             name="No devices found",
                                             description="Either bluetoothctl is missing or you haven't connected any devices yet",
                                             on_enter=ExtensionCustomAction("none", keep_app_open=True)))
            return RenderResultListAction(items)

        sorted_keys = process.extract(query, devices.keys(), limit=None)
        sorted_devices = {k: devices[k] for k, score, _ in sorted_keys}

        if sorted_devices != {}:
            devices = sorted_devices


        for i in range(len(devices)):
            key = list(devices.keys())[i]
            data = ('connect ' if devices[key][2] == 'Select to Connect' else 'disconnect ') + devices[key][0]
            if devices[key][2] == 'Select to Connect':
                icon_name = DEVICE_ICONS.get(devices[key][1], "connect")
            else:
                icon_name = DEVICE_ICONS.get(devices[key][1], "disconnect")
                if icon_name != "disconnect":
                    icon_name += "_disconnect"
            items.append(ExtensionResultItem(icon=f'images/{icon_name}.png',
                                             name=f"%s | {devices[key][2]}" % key,
                                             description=devices[key][0],
                                             on_enter=ExtensionCustomAction(data, keep_app_open=True)))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        if (data == 'none'):
            return HideWindowAction()

        # connect to device
        ret = os.system(
            f"bash -c 'timeout 8s bluetoothctl {data}'")

        if ret == 0:
            prompt = data.split()[0] + "ed Successfully"
        else:
            prompt = data.split()[0] + "ion Failed"

        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=prompt,
                                                           on_enter=HideWindowAction())])


if __name__ == '__main__':
    BluetoothQC().run()
