# How to use and setup boot on start up

---

## General use

To run the script user needs to habe root permissions. So all calls **has to be** made with 'sudo' or from root user.

```bash
foo@bar:~$ sudo python3 monitoring.py &
```

The script has a greetings message. One can submitt a desire greetings name, but there is 'Yuriy' by default. So if nothing is submittes Yuriy will be shown.

```bash
foo@bar:~$ sudo python3 monitoring.py --name foo &
```

To call help just use the '--help' parameter

```bash
foo@bar:~$ sudo python3 monitoring.py --help
usage: monitoring.py [-h] [-n NAME]

Monitoring system and controlling cpu fan

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  greetings name shown by program start
```

---

## Setup autostart

To run a program on your Raspberry Pi at startup is to use the **systemd** files. **systemd** provides a standard process for controlling what programs run when a Linux system boots up. Note that **systemd** is available only from the Jessie versions of Raspbian OS.

#### Step 1 - Crate a unit file

Open a sample unit file using the command as shown below:

```bash
foo@bar:~$ sudo nano /lib/systemd/system/monitoring.service
```

Add in the following text:

```ini
[Unit]
Description=My Sample Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/sample.py

[Install]
WantedBy=multi-user.target
```

You should save and exit the nano editor.

This defines a new service called “Sample Service” and we are requesting that it is launched once the multi-user environment is available. The “ExecStart” parameter is used to specify the command we want to run. The “Type” is set to “idle” to ensure that the ExecStart command is run only when everything else has loaded. Note that the paths are absolute and define the complete location of Python as well as the location of our Python script.

In order to store the script’s text output in a log file you can change the ExecStart line to:

```ini
ExecStart=/usr/bin/python /home/pi/sample.py > /home/pi/sample.log 2>&1
```

The permission on the unit file needs to be set to 644 :

```bash
foo@bar:~$ sudo chmod 644 /lib/systemd/system/sample.service
```

#### Step 2 - Configure systemd

Now the unit file has been defined we can tell systemd to start it during the boot sequence:

```bash
foo@bar:~$ sudo systemctl daemon-reload
foo@bar:~$ sudo systemctl enable sample.service
```

Reboot the Pi and your custom service should run:

```bash
foo@bar:~$ sudo reboot
```