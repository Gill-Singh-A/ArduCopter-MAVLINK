# Setup
Run the following commands in the terminal to setup the required Tools, Libraries, Modules and Software
```bash
sudo apt update
sudo apt-get update
sudp apt upgrade
sudo apt install python3-pip python3-dev python-dev-is-python3 screen python3-wxgtk4.0 python3-lxml
sudo apt install python3-future
sudo pip3 install pyserial MAVProxy colorama pymavlink --break-system-packages
```
# Configure UART Communication
Type the following command to open up the Raspberry Pi Configuration in Terminal
```bash
sudo raspi-config
```
* Then Select **3. Interface Options**<br />
![Raspberry Pi Configuration : Interface Options](assets/images/interface.png)<br />
* Then Select **P6 Serial Port**<br />
![Raspberry Pi Configuration : Serial Port](assets/images/serial_port.png)<br />
* Select **No** for **Login Shell to be accessible over serial**<br />
![Raspberry Pi Configuration : Login Shell over UART](assets/images/login_shell_over_uart.png)<br />
* Select **Yes** for **Serial Port Hardware to be enabled**<br />
![Raspberry Pi Configuration : Serial Port Hardware](assets/images/serial_port_hardware.png)<br />
* Click OK<br />
![Raspberry Pi Configuration](assets/images/raspi_config.png)<br />
* Then Finish the Setup
## Disable Usage of UART by Bluetooth
In Raspberry Pi, the Bluetooth uses the UART. So to disable it, type the following command in the terminal
```bash
sudo echo 'dtoverlay=disable-bt' >> /boot/firmware/config.txt
```