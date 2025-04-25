import json
import logging
import os
from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)

DEVICE_ICONS = [
    'headphones', 
    'keyboard', 
    'mouse', 
    'gamepad', 
    'phone', 
    'default'
]

class BluetoothQC(Extension):

    def __init__(self):
        super(BluetoothQC, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        devices = {}
        logger.info('preferences %s' % json.dumps(extension.preferences))

        # get devices from preferences
        if extension.preferences.get('device_list') is not None:
            device_list = extension.preferences['device_list'].split(',')
            for d in device_list:
                if len(d) > 18:
                    devices[d[-(len(d)-18):].strip()] = d.strip()[0:18], d[-(len(d)-18):].strip().split(' ')[0]

            # giv user feedback if no devices has been specified
            if len(devices) == 0:
                items.append(ExtensionResultItem(icon='images/disconnect.png',
                                                 name="No devices specified",
                                                 description="Add them in settings->extentions->BT_manager->device list",
                                                 on_enter=ExtensionCustomAction("none", keep_app_open=True)))
                return RenderResultListAction(items)

        # connect options
        for i in range(len(devices)):
            key = list(devices.keys())[i]
            data = 'connect ' + devices[key][0]
            items.append(ExtensionResultItem(icon=f'images/{devices[key][1] if devices[key][1] in DEVICE_ICONS else 'connect'}.png',
                                             name="Connect to %s" % key.split(' ', 1)[1] if devices[key][1] in DEVICE_ICONS else "Connect to %s" % key,
                                             on_enter=ExtensionCustomAction(data, keep_app_open=True)))

        # disconnect options
        for i in range(len(devices)):
            key = list(devices.keys())[i]
            data = 'disconnect ' + devices[key][0]
            items.append(ExtensionResultItem(icon=f'images/{devices[key][1] + '_disconnect' if devices[key][1] in DEVICE_ICONS else 'disconnect'}.png',
                                             name="Disconnect from %s" % key.split(' ', 1)[1] if devices[key][1] in DEVICE_ICONS else "Disconnect from %s" % key,
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
