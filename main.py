from concurrent.futures import ThreadPoolExecutor
from socket import AF_INET

import argparse
import colorama
import socket
import time

def scan_port(port, target_IP):
    """
    Scans a single port on a target IP address.
    """
    try:
        s = socket.socket(AF_INET, socket.SOCK_STREAM)
        conn = s.connect_ex((target_IP, port))
        s.settimeout(1)

        if conn == 0:
            open_ports.append(port)
            print(f'Port {port}: Open')
            
        else:
            print(f'Port {port}: Closed')
            
    except Exception as e:
        print(f'Error checking port {port}: {str(e)}')
        
    finally:
        s.close()

def main(target_IP, port_range):
    """
    Main function to start the port scanning process.
    """
    global open_ports
    open_ports = []
    start_time = time.time()
    
    time.sleep(1)   
    print(f"{colorama.Fore.GREEN}[-]{colorama.Fore.RESET} " + f"Starting scan on {target_IP} \n")
    
    with ThreadPoolExecutor(max_workers=100) as executor: 
        for port in range(port_range[0], port_range[1] + 1):
            executor.submit(scan_port, port, target_IP)
            
    print(f'\nTime: {format(time.time() - start_time, ".2f")}')
    
    if open_ports:
        print('Open ports:', ', '.join(map(str, open_ports)))
    else:
        print('No open ports found.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Port scanning on an IP address.')
    
    parser.add_argument('target_IP', help='Target IP address')
    parser.add_argument('port_range', nargs=2, type=int, help='Port range to check')
    
    args = parser.parse_args()
    main(args.target_IP, args.port_range)