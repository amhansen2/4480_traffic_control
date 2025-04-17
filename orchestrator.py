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
    run_command(["sudo", "docker", "compose", "up", "-d"])


def switch_path(direction):
    print(f"Switching path to {direction}...")

    if direction == "north":
        print("Setting lower cost for north path (R1 -> R2 -> R3)...")
        
        #left side
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", "interface eth1", "-c", "ip ospf cost 10"])
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", "interface eth2", "-c", "ip ospf cost 100"])
        #right side
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r3-1", "vtysh", "-c", "configure terminal", "-c", "interface eth1", "-c", "ip ospf cost 10"])
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r3-1", "vtysh", "-c", "configure terminal", "-c", "interface eth2", "-c", "ip ospf cost 100"])
   
    elif direction == "south":
        print("Setting lower cost for south path (R1 -> R4 -> R3)...")
        
        #left side
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", "interface eth1", "-c", "ip ospf cost 100"])
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", "interface eth2", "-c", "ip ospf cost 10"])
        #right side
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r3-1", "vtysh", "-c", "configure terminal", "-c", "interface eth1", "-c", "ip ospf cost 100"])
        run_command(["sudo", "docker", "exec", "4480_traffic_control-r3-1", "vtysh", "-c", "configure terminal", "-c", "interface eth2", "-c", "ip ospf cost 10"])
    
    else:
        print("Invalid direction. Use 'north' or 'south'.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Network Topology Orchestrator")
    parser.add_argument("action", choices=["create", "switch"], help="Action to perform")
    parser.add_argument("--north", action="store_true", help="Switch path direction to north (only with 'switch' action)")
    parser.add_argument("--south", action="store_true", help="Switch path direction to south (only with 'switch' action)")

    args = parser.parse_args()

    if args.action == "create":
        create_topology()


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
