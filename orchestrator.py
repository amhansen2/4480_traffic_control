import argparse
import subprocess
import sys

def run_command(cmd_list, check=True):
    try:
        subprocess.run(cmd_list, check=check)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd_list)}")
        sys.exit(1)

def create_topology():
    print("Building Network Topology...")
    run_command(["sudo", "docker", "compose", "build", "--no-cache"])
    run_command(["sudo", "docker", "compose", "up", "-d"])

def start_frr():
    routers = ["r1", "r2", "r3", "r4"]
   
    try:
        run_command(["sudo", "docker", "exec", f"4480_traffic_control-r1-1", "./frr.sh"])
        run_command(["sudo", "docker", "exec", f"4480_traffic_control-r2-1", "./frr.sh"])
        run_command(["sudo", "docker", "exec", f"4480_traffic_control-r3-1", "./frr.sh"])
        run_command(["sudo", "docker", "exec", f"4480_traffic_control-r4-1", "./frr.sh"])
    except Exception as e:
        print(f"Failed to start FRR")



def get_interface_by_ip(container_name, target_ip_subnet):
    result = subprocess.run(["sudo", "docker", "exec", container_name, "bash", "-c", "ip -o -f inet addr show | awk '{print $2, $4}'"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    for line in lines:
        interface, cidr = line.split()
        if cidr.startswith(target_ip_subnet):
            return interface
    raise Exception(f"Interface with subnet {target_ip_subnet} not found in {container_name}")





def switch_path(direction):
    print(f"Switching path to {direction}...")

    # find interfaces dynaimcally via prof's suggested "hacky workaround"
    r1_north_iface = get_interface_by_ip("4480_traffic_control-r1-1", "10.0.16.")
    r1_south_iface = get_interface_by_ip("4480_traffic_control-r1-1", "10.0.19.")
    r3_north_iface = get_interface_by_ip("4480_traffic_control-r3-1", "10.0.17.")
    r3_south_iface = get_interface_by_ip("4480_traffic_control-r3-1", "10.0.18.")

    if direction == "north":
        print("Setting lower cost for north path (R1 -> R2 -> R3)...")
        # left
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", f"interface {r1_north_iface}", "-c", "ip ospf cost 10"])
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", f"interface {r1_south_iface}", "-c", "ip ospf cost 100"])
        # right
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r3-1", "vtysh", "-c", "configure terminal", "-c", f"interface {r3_north_iface}", "-c", "ip ospf cost 10"])
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r3-1", "vtysh", "-c", "configure terminal", "-c", f"interface {r3_south_iface}", "-c", "ip ospf cost 100"])

    elif direction == "south":
        print("Setting lower cost for south path (R1 -> R4 -> R3)...")
        # left
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", f"interface {r1_north_iface}", "-c", "ip ospf cost 100"])
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", f"interface {r1_south_iface}", "-c", "ip ospf cost 10"])
        # right
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r3-1", "vtysh", "-c", "configure terminal", "-c", f"interface {r3_north_iface}", "-c", "ip ospf cost 100"])
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r3-1", "vtysh", "-c", "configure terminal", "-c", f"interface {r3_south_iface}", "-c", "ip ospf cost 10"])
    
    else:
        print("Invalid direction. Use 'north' or 'south'.")
        sys.exit(1)
        
        
        

def main():
    parser = argparse.ArgumentParser(description="Network Topology Orchestrator")
    parser.add_argument("action", choices=["create", "frr", "switch"], help="Action to perform")
    parser.add_argument("--north", action="store_true", help="Switch path direction to north (only with 'switch' action)")
    parser.add_argument("--south", action="store_true", help="Switch path direction to south (only with 'switch' action)")

    args = parser.parse_args()

    if args.action == "create":
        create_topology()
        print("Network topology created and started.")
        
    
    if args.action == "frr":
        start_frr()
        print("FRR services started on routers.")


    elif args.action == "switch":
        if args.north and args.south:
            print("Error: You cannot specify both --north and --south at the same time.")
            sys.exit(1)
        elif args.north:
            switch_path("north")
        elif args.south:
            switch_path("south")
        else:
            print("Error: You must specify either --north or --south when switching path.")
            sys.exit(1)

    else:
        print("Command not recognized. Use 'create' to build the topology or 'switch' to change paths.")
        sys.exit(1)

if __name__ == "__main__":
    main()
