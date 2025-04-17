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
    run_command(["docker", "compose up", "-d"])

def start_ospf():
    print("Starting OSPF on routers...")
    routers = ["r1", "r2", "r3", "r4"]
    for router in routers:
        print(f"* * * Starting FRR services on {router}...")
        run_command(["docker", "exec", router, "./frr.sh"])

def install_routes():
    print("[*] Installing static routes on hosts...")
    # Example routes - you must adapt IP addresses according to your real topology
    run_command(["docker", "exec", "ha", "ip", "route", "add", "10.0.3.0/24", "via", "10.0.1.1"])
    run_command(["docker", "exec", "hb", "ip", "route", "add", "10.0.1.0/24", "via", "10.0.3.1"])

def switch_path(direction):
    print(f"[*] Switching path to {direction}...")

    if direction == "north":
        print("[*] Setting lower cost for north path (R1 -> R2 -> R3)...")
        run_command(["docker", "exec", "r1", "vtysh", "-c", "configure terminal", "-c", "interface eth1", "-c", "ip ospf cost 10"])
        run_command(["docker", "exec", "r1", "vtysh", "-c", "configure terminal", "-c", "interface eth2", "-c", "ip ospf cost 100"])
    elif direction == "south":
        print("[*] Setting lower cost for south path (R1 -> R4 -> R3)...")
        run_command(["docker", "exec", "r1", "vtysh", "-c", "configure terminal", "-c", "interface eth1", "-c", "ip ospf cost 100"])
        run_command(["docker", "exec", "r1", "vtysh", "-c", "configure terminal", "-c", "interface eth2", "-c", "ip ospf cost 10"])
    else:
        print("Invalid direction. Use 'north' or 'south'.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Network Topology Orchestrator")
    parser.add_argument("action", choices=["create", "ospf", "routes", "switch"], help="Action to perform")
    parser.add_argument("--direction", choices=["north", "south"], help="Direction for path switch (only with 'switch' action)")

    args = parser.parse_args()

    if args.action == "create":
        create_topology()
    elif args.action == "ospf":
        start_ospf()
    elif args.action == "routes":
        install_routes()
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
