# Ansible AF

Ansible Armbian Firstboot Server 

Ansible AF is a server to automate the first boot configuration of Armbian servers using Armbian's [Automatic First Boot Configuration](https://docs.armbian.com/User-Guide_Autoconfig/) and [Ansible](https://docs.ansible.com/).

## How It Works

1. You prepare a custom Armbian image with a `/root/.not_logged_in_yet` file that contains only this line:
    * `PRESET_CONFIGURATION="http://<server_ip>:<port>/register/<config_template>"`
2. Flash and boot your device with your custom image
3. Your device will request a DHCP address
    * (optional) Your DHCP server will register the host's mac address, allowing you to use dynamic DHCP IPs for first boot and static IPs after that
4. When the first boot is complete, Armbian will register with Ansible AF to get a first boot configuration
5. Armbian will apply the first boot configuration, including a static network configuration
6. Armbian AF will run the configured Ansible Playbook(s) against the host

## Installation

### Prerequisites

To use the Ansible Armbian Firstboot Server, you must have:

1. Installed Ansible on your system.
2. [Built an inventory](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html) in `/etc/ansible/hosts`
3. Built one or more [Armbian First Boot Configuariton Templates](https://docs.armbian.com/User-Guide_Autoconfig/)
   * These should be located in `/etc/ansible/playbooks/tempates/`
4. Built one or more [Ansible Playbooks](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html) for configuring your system

**IMPORTANT NOTE**: The name of the First Boot Configuration Template (minus the .j2 extension) must match the name of the Ansible Playbook (minus the .yaml extension) and these both must match the `<config_template>` you supply in the `PRESET_CONFIGURATION` URL. By default this is `armbian_first_boot`, so you would have `/etc/ansible/playbooks/armbian_first_boot.yaml` and `/etc/ansible/playbooks/template/armbian_first_boot.j2`.

### Install The Servers

First, customize the playbook in `examples/etc-ansible-playbooks-ansible_af.yaml` if you want to change the defaults.

Install the service using ansible:

```bash
ansible-playbook -i /etc/ansible/hosts examples/etc-ansible-playbooks-ansible_af.yaml
```

You can use another location if you prefer.

### Customize the service configuration

Systemd unit files will be installed in `/etc/systemd/system`. If you'd like to customize the location of Ansible or change other settings, you can edit the files and change the `Environment=` lines. Make sure to reload and restart when you're done:

```
sudo systemctl daemon-reload
sudo systemctl restart ansible-af-http ansible-af-runner
```

## Configuration

Ansible AF is configured through environment variables. You can also set variables supported by `ansible-playbook` and they will be passed through.

| Variable Name | Default Value | Description |
|---------------|---------------|-------------|
| `ANSIBLE_PATH` | `/etc/ansible` | The base path where ansible files are located |
| `ANSIBLE_INVENTORY_PATH` | `$ANSIBLE_PATH/hosts` | The path to the ansible inventory |
| `ANSIBLE_PLAYBOOK_PATH` | `$ANSIBLE_PATH/playbooks` | The path to the ansible playbooks |
| `ANSIBLE_AF_TEMPLATE_DIR` | `$ANSIBLE_PLAYBOOK_PATH/templates` | The path to ansible tempate files |
| `ANSIBLE_AF_ALLOWLIST` | `armbian_first_boot*` | Templates allowed to be rendered. Can supply a comma separated list. Shell style wildcards (`*`, `?`, `[a-z]`) supported. |
| `ANSIBLE_AF_DENYLIST` | | Templates disallowed from rendering. Same format as `ANSIBLE_AF_ALLOWLIST`, takes precedence. |
| `ANSIBLE_AF_HOST_WAIT` | `30` | Minimum time to wait between host registration and running the playbook. |
| `ANSIBLE_AF_HOST_IP_KEY` | `cluster_ip` | This key will be used to match a registration to the ansible inventory. It must exist in your inventory and match the IP the registration request comes from. |
| `ANSIBLE_AF_SSH_USERNAME` | | The ssh username to connect as when running the playbook. Defaults to the user running `armbian-af-runner`. |

## Armbian Image Preparation

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

Contributions are welcome! Fork the repository and create a pull request with your changes.

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, feel free to open an issue or pull request.
