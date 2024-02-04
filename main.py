from concurrent.futures import ThreadPoolExecutor, as_completed
from socket import AF_INET, SOCK_STREAM, socket
import argparse
import colorama
import ipaddress
import time

def scan_port(port, target_ip, result_list):
    """
    Scans a single port on a target IP address.
    """
    try:
        with socket(AF_INET, SOCK_STREAM) as s:
            s.settimeout(0.5)  # Adjust the timeout value as needed
            conn = s.connect_ex((target_ip, port))

            if conn == 0:
                result_list.append((port, "Open"))
                print(f'Port {port}: Open')
            else:
                result_list.append((port, "Closed"))
                print(f'Port {port}: Closed')

    except OSError as e:
        print(f'Error checking port {port}: {str(e)}')

def main(target_ip, port_range):
    """
    Main function to start the port scanning process.
    """
    result_list = []
    start_time = time.time()

    try:
        target_ip_obj = ipaddress.ip_address(target_ip)
    except ValueError as e:
        print(f'Invalid IP address: {str(e)}')
        return

    time.sleep(1)
    print(f"{colorama.Fore.GREEN}[-]{colorama.Fore.RESET} " + f"Starting scan on {target_ip} \n")

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(scan_port, port, target_ip, result_list) for port in range(port_range[0], port_range[1] + 1)]

        for future in as_completed(futures):
            pass 

    print(f'\nTime: {format(time.time() - start_time, ".2f")}')
    
    if result_list:
        open_ports = [port for port, status in result_list if status == "Open"]
        print('Open ports:', ', '.join(map(str, open_ports)))
    else:
        print('No open ports found.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Port scanning on an IP address.')
    
    parser.add_argument('target_ip', help='Target IP address')
    parser.add_argument('port_range', nargs=2, type=int, help='Port range to check')
    
    args = parser.parse_args()
    main(args.target_ip, args.port_range)
