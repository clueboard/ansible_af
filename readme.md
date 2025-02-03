# Ansible AF

Ansible Armbian Firstboot Server 

Ansible AF is a server to automate the first boot configuration of Armbian servers using Armbian's [Automatic First Boot Configuration](https://docs.armbian.com/User-Guide_Autoconfig/) and [Ansible](https://docs.ansible.com/).

## How It Works

1. You prepare a custom Armbian image with a `/root/.not_logged_in_yet` file that contains only this line:
    * `PRESET_CONFIGURATION="http://<server_ip>:<port>/register/<config_template>"`
2. Flash and boot your device with your custom image
3. Your device will be configured with a DHCP address
4. It will register with Armbian AF and get a static network configuration
5. Armbian AF will run the configured Ansible Playbook(s) against the host

## Installation

To install the package, use the following command:

```bash
sudo python3 -m pip /srv/ansible_af
sudo /srv/ansible_af/bin/pip install ansible_af
```

## Usage

To use the Ansible Armbian Firstboot Server, follow these steps:

1. Ensure you have Ansible installed on your system.
2. Build an inventory in `/etc/ansible/hosts`
3. Build one or more Armbian First Boot Configuariton Templates

## Contributing

Please review our [Code of Conduct](code_of_conduct.md) before contributing.

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or suggestions, feel free to open an issue or pull request.
