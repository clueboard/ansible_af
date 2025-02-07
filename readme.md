# Ansible AF

Ansible Armbian Firstboot Server 

Ansible AF is a server to automate the first boot configuration of Armbian servers using Armbian's [Automatic First Boot Configuration](https://docs.armbian.com/User-Guide_Autoconfig/) and [Ansible](https://docs.ansible.com/).

## How It Works

1. You prepare a custom Armbian image with a `/root/.not_logged_in_yet` file that contains only this line:
    * `PRESET_CONFIGURATION="http://<server_ip>:<port>/register/<config_template>"`
2. Flash and boot your device with your custom image
3. Your device will request a DHCP address
    a. (optional) Your DHCP server will register the host's mac address
4. When the first boot is complete, Armbian will register with Ansible AF to get a first boot configuration
5. Armbian AF will run the configured Ansible Playbook(s) against the host

## Installation

### Prerequisites

To use the Ansible Armbian Firstboot Server, you must have:

1. Installed Ansible on your system.
2. [Built an inventory](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html) in `/etc/ansible/hosts`
3. Built one or more [Armbian First Boot Configuariton Templates](https://docs.armbian.com/User-Guide_Autoconfig/)
   * These should be located in `/etc/ansible/playbooks/tempates/`
4. Built one or more [Ansible Playbooks](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html) for configuring your system

### Install The Servers

To install the server to `/srv/ansible_af`, use the following command:

```bash
sudo python3 -m venv /srv/ansible_af
sudo /srv/ansible_af/bin/pip install ansible_af
```

You can use another location if you prefer.

### Start the services (systemd)

There are systemd unit files in [examples](examples/) you can use to install the HTTP server and the Runner. If you'd like to customize the location of Ansible or change other settings, you can edit the files and change the `Environment=` lines.

```
sudo cp examples/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ansible-af-http ansible-af-runner
```

## Usage

These steps require an SD card, USB drive, or another block device. You must perform them on Linux. You will not be able to mount the filesystem on Windows or macOS.

**Warning**: This will erase the device you use. Ensure you are performing these steps against the correct device.

1. Download an [Armbian image](https://www.armbian.com/download/) for your device
2. Uncompress the image:
    * `unxz Armbian_24.11.1_Rpi4b_bookworm_current_6.6.60_minimal.img.xz`
3. Ensure that your block device is empty. Change `/dev/sda` to whatever your drive actually is.
    * `dd if=/dev/zero of=/dev/sda bs=4k`
3. Write Armbian to your device:
    * `dd if=Armbian_24.11.1_Rpi4b_bookworm_current_6.6.60_minimal.img.xz of=/dev/sda bs=4k`
4. Mount the Armbian root partition
    * `mount /dev/sda2 /mnt`
5. Create the first boot file:
    * `echo PRESET_CONFIGURATION="http://<server_ip>/register/<profile_name>"`
6. Unmount the Armbian root partition
    * `umount /mnt`
7. Make a custom image you can write to other machines
    * `dd conv=sparse if=/dev/sda of=Armbian_24.11.1_Rpi4b_bookworm_current_6.6.60_MY_ARMBIAN_AF_IMAGE.img.xz bs=4k`
8. Boot your machine from the drive you just made and watch it automagically boot and configure itself


## Contributing

Please review our [Code of Conduct](code_of_conduct.md) before contributing.

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, feel free to open an issue or pull request.
