# Bluetooth quick connect

Quickly connect and disconnect from the Bluetooth devices you use the most.

![bt_menu](https://user-images.githubusercontent.com/42439472/164915659-777e0c2e-bb73-4a45-9ae7-63ab21f1808e.png)

This extension is listed on the Ulauncher extensions page. 

[![Ulauncher Extension](https://img.shields.io/badge/Ulauncher-Extension-green.svg?style=for-the-badge)](https://ext.ulauncher.io/-/github-eckhoff42-ulauncher-bluetooth-quick-connect)
[![GitHub license](https://img.shields.io/github/license/brpaz/ulauncher-file-search.svg?style=for-the-badge)](LICENSE)

## Settings
![settings](https://user-images.githubusercontent.com/42439472/164915725-84710383-3d91-47ad-80ed-8a3b20b98bf2.png)


Change the keyword under *Bluetooth manager Keyword*

Add your devices to the *Device list*. The format is as follows:
```python
A1:A2:17:6E:87:C1 <device-type> <device-name>, A1:A2:90:19:04:2D <device-type> <device-name>
```
You can find your devices MAC address in the Bluetooth settings or with the command `bluetoothctl scan on`

device-types:
- headphones
- keyboard
- mouse
- gamepad 
- phone
- default

**N.B.** This extension uses `bluetoothctl` to connect to your devices. 
Find information about downloading it here: https://command-not-found.com/bluetoothctl

Diff to parent:

- Multiple icons support
- Sort with rapidfuzz (Can be improved with sorting the keyword even earlier to filter by connect/disconnet)
- Different Icons (Preferably done by myself, did not do more than the connect and disconnect till now, may add temporary icons from the web)
