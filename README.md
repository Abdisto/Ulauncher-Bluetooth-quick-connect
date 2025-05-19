# Bluetooth quick connect

Quickly connect and disconnect from the Bluetooth devices you use the most.

![bt_menu](https://user-images.githubusercontent.com/42439472/164915659-777e0c2e-bb73-4a45-9ae7-63ab21f1808e.png)

This extension is listed on the Ulauncher extensions page. 

[![Ulauncher Extension](https://img.shields.io/badge/Ulauncher-Extension-green.svg?style=for-the-badge)](https://ext.ulauncher.io/-/github-eckhoff42-ulauncher-bluetooth-quick-connect)
[![GitHub license](https://img.shields.io/github/license/brpaz/ulauncher-file-search.svg?style=for-the-badge)](LICENSE)

## Settings
![settings](https://user-images.githubusercontent.com/42439472/164915725-84710383-3d91-47ad-80ed-8a3b20b98bf2.png)


Change the keyword under *Bluetooth manager Keyword*

device-types:
- headphones
- keyboard
- mouse
- __gamepad__ (*)
- phone
- default
  
* __BOLD__ are these that have new icons and don't use the default bluetooth icon


**N.B.** This extension uses `bluetoothctl` to connect to your devices. 
Find information about downloading it here: https://command-not-found.com/bluetoothctl

Diff to parent:

- Multiple icons support
- Sort with rapidfuzz
- Different Icons (Preferably done by myself, did not do more than the connect and disconnect till now, may add temporary icons from the web)

What's gonna happen:
- ~~Prob. gonna use bluetoothctl's function in the future. devices Paired | devices Connected -> Paired - Connected -> not_connected. Offer the connection to these devices and disconnect from the connected devices -> info MAC from devices paired / not paired, and get the device type -> set icon. Fuzzy finding with rapidfuzz gonna be simpler since not two unpaired for loops with appending to me unknown class, thus gonna have one list with all options and sorting first by action and then by user input~~(Already done)
- Updating to the API 3.0 for ulauncher v.6 as soon as stable
