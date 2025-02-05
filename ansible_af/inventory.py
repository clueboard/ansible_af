from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager

from .config import inventory_path

# Load the inventory
loader = DataLoader()
inventory = InventoryManager(loader=loader, sources=inventory_path)
variable_manager = VariableManager(loader=loader, inventory=inventory)


def find_host_by_ip(ip):
    for host in inventory.hosts.values():
        upstream_ip = host.vars.get('upstream_ip')

        if ip == upstream_ip:
            return variable_manager.get_vars(host=host)

    return None


def find_host_by_name(hostname):
    if hostname in inventory.hosts:
        host = inventory.hosts[hostname]
        return variable_manager.get_vars(host=host)

    return None


if __name__ == '__main__':
    # Access variables for a specific ip
    ip = "172.16.20.11"
    host = find_host_by_ip(ip)

    print('hrm', host)
    if host:
        print(f"Variables for {host['inventory_hostname']}:")

        for key, value in host.items():
            print(f"  {key}: {value}")

    else:
        print(f"\nIP {ip} not found in inventory!")

    # Access variables for a specific hostname
    hostname = 'orange02.cluster01.frop.org'
    host = find_host_by_name(hostname)

    if host:
        print(f"\nVariables for {host['inventory_hostname']}:")

        for key, value in host.items():
            print(f"  {key}: {value}")

    else:
        print(f"\nHost {hostname} not found in inventory!")
