import random

# -----------------------------
# 🔹 SIMULATED SCAN
# -----------------------------
def simulate_scan():
    return {
        "open_ports": random.choice([2, 4, 6, 10, 15]),
        "risky_ports": random.choice([0, 1, 2, 3]),
        "unknown_services": random.choice([0, 1, 2])
    }


# -----------------------------
# 🔹 REAL NMAP SCAN
# -----------------------------
def real_scan(target="127.0.0.1"):
    try:
        import nmap
    except ImportError:
        return {"error": "python-nmap not installed"}

    scanner = nmap.PortScanner()

    try:
        scanner.scan(target, "22-443")

        open_ports = 0
        risky_ports = 0
        unknown_services = 0

        risky_list = [21, 23, 445, 3389]

        for host in scanner.all_hosts():
            if 'tcp' in scanner[host]:
                for port in scanner[host]['tcp']:
                    open_ports += 1

                    service = scanner[host]['tcp'][port]['name']

                    if port in risky_list:
                        risky_ports += 1

                    if service == "" or service == "unknown":
                        unknown_services += 1

        return {
            "open_ports": open_ports,
            "risky_ports": risky_ports,
            "unknown_services": unknown_services
        }

    except Exception as e:
        return {"error": str(e)}