import argparse
import ipaddress
import socket
import threading

results = {}

def scan_host_port(host,port,timeout):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(timeout)
	status = sock.connect_ex((host,port))
	if status == 0:
		results[host].append(port)
	sock.close()

def manage_scans(hosts,ports,thread_max,timeout):
	threads = []
	for host in hosts:
		results[host] = []
		for port in ports:
			thread = threading.Thread(target=scan_host_port,args=[host,port,timeout])
			thread.start()
			threads.append(thread)
			while threading.active_count() > thread_max:
				pass
	[thread.join() for thread in threads]

	return results

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Simple Light Awesome Port Scanner: Because this thing SLAPS")
	parser.add_argument('hosts', help="A comma-separated list of hosts to be scanned")
	parser.add_argument('-p', "--ports", default="21,22,25,53,80,139,389,443,445,3389,8000,8080,8443", help="A comma-separated list of ports to be scanned. Defaults to 21,22,25,53,80,139,443,445,3389,8000,8080,8443")
	parser.add_argument('-t','--threads', type=int, default=100, help="The number of max threads. Defaults to 100")
	parser.add_argument('-w','--wait', type=float, default=1, help="The number of seconds to wait for a response. Defaults to 1")
	parser.add_argument("-j","--json", help="Print full JSON output", action="store_true")
	args = parser.parse_args()

	hosts = []
	for host in args.hosts.split(","):
		if "-" in host:
			start = host.split("-")[0]
			ip = True
			try:
				ipaddress.ip_address(start)
			except:
				ip = False
			if ip:
				first_three = ".".join(start.split(".")[0:-1])
				start = start.split(".")[-1]
				end = host.split("-")[1]
				if "." in end:
					end = end.split(".")[-1]
				hosts.extend([f"{first_three}.{str(host)}" for host in range(int(start),int(end)+1)])
			else:
				hosts.append(host)
		else:
			hosts.append(host)	
	hosts = list(set(hosts))

	ports = []
	for port in args.ports.split(","):
		if "-" in port:
			start = port.split("-")[0]
			end = port.split("-")[1]
			ports.extend([port for port in range(int(start),int(end)+1)])
		else:
			ports.append(int(port))
	ports = list(set(ports))

	output = manage_scans(hosts,ports,args.threads,args.wait)

	if args.json:
		print(output)
	
	else:
		whitespace = len(max(output.keys(),key=len)) + 8
		try:
			scan_results = [key for key in dict(sorted(output.items(), key = lambda item: ipaddress.ip_address(item[0]))) if output[key]]
		except:
			scan_results = [key for key in dict(sorted(output.items())) if output[key]]
		if not scan_results:
			print("No open ports found.")
		else:
			for scan_result in scan_results:
				print(f"{scan_result: <{whitespace}}{','.join([str(port) for port in sorted(output[scan_result])])}")