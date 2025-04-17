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
        print("[*] Setting lower cost for north path (R1 -> R2 -> R3)...")
        run_command(["docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", "interface eth1", "-c", "ip ospf cost 10"])
        run_command(["docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", "interface eth2", "-c", "ip ospf cost 100"])
    elif direction == "south":
        print("[*] Setting lower cost for south path (R1 -> R4 -> R3)...")
        run_command(["docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", "interface eth1", "-c", "ip ospf cost 100"])
        run_command(["docker", "exec", "4480_traffic_control-r1-1", "vtysh", "-c", "configure terminal", "-c", "interface eth2", "-c", "ip ospf cost 10"])
    else:
        print("Invalid direction. Use 'north' or 'south'.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Network Topology Orchestrator")
    parser.add_argument("action", choices=["create", "switch"], help="Action to perform")
    parser.add_argument("--direction", choices=["north", "south"], help="Direction for path switch (only with 'switch' action)")

    args = parser.parse_args()

    if args.action == "create":
        create_topology()
   
    elif args.action == "switch":
        if not args.direction:
            print("Error: --direction must be specified when switching path.")
            sys.exit(1)
        switch_path(args.direction)
        
    else:
        print("Unknown action.")
        sys.exit(1)

if __name__ == "__main__":
    main()
