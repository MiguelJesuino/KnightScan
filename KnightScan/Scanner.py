# scanner.py
import socket
from queue import Queue
from threading import Thread
from colorama import init, Fore, Style
init(autoreset=True)

known_services = {
    20: "FTP (data)", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",67: "DHCP", 68: "DHCP", 69: "TFTP", 80: "HTTP", 110: "POP3",
    119: "NNTP", 123: "NTP", 137: "NetBIOS", 143: "IMAP", 161: "SNMP", 162: "SNMP Trap", 179: "BGP",  443: "HTTPS", 445: "SMB", 465: "SMTPS",
    514: "Syslog", 587: "SMTP (TLS)", 631: "IPP", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL", 1521: "Oracle DB", 1723: "PPTP",  3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP Alt", 8443: "HTTPS Alt",
}


def scan_port(host, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            return True
    except:
        return False


def grab_banner(host, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))

            if port in [80, 8080, 8000, 443]:
                s.sendall(b"GET / HTTP/1.1\r\nHost: %b\r\n\r\n" % host.encode())
                response = s.recv(1024)
                lines = response.decode(errors="ignore").splitlines()
                if lines:
                    return lines[0]  # pega só a primeira linha (ex: HTTP/1.1 200 OK)
                else:
                    return "Servidor HTTP detectado"
            else:
                banner = s.recv(1024)
                return banner.decode(errors="ignore").strip()
    except:
        return None


# Função simples para detectar o sistema operacional a partir do banner
def detect_os(banner):
    if not banner:
        return "Desconhecido"
    banner_lower = banner.lower()
    if "windows" in banner_lower:
        return "Windows"
    elif "ubuntu" in banner_lower or "debian" in banner_lower or "linux" in banner_lower:
        return "Linux"
    elif "freebsd" in banner_lower:
        return "FreeBSD"
    elif "openbsd" in banner_lower:
        return "OpenBSD"
    else:
        return "Desconhecido"


def worker(host, queue, results, timeout, show_logs):
    while not queue.empty():
        port = queue.get()
        try:
            if scan_port(host, port, timeout):
                banner = grab_banner(host, port, timeout)
                os_info = detect_os(banner)
                results.append({"port": port, "banner": banner, "os": os_info})
                if banner:
                    print(f"✅ Porta {port} ABERTA | Banner: {banner} | OS: {os_info}")
                else:
                    service = known_services.get(port, "Desconhecido")
                    print(f"✅ Porta {port} ABERTA | Serviço provável: {service} (sem banner) | OS: {os_info}")
            else:
                if show_logs:
                    print(f"❌ Porta {port} FECHADA")
        except Exception as e:
            if show_logs:
                print(f"Erro na porta {port}: {e}")
        finally:
            queue.task_done()


# Gerencia as threads para o escaneamento em um host
def threaded_scan(host, ports, num_threads, timeout, show_logs):
    queue = Queue()
    results = []
    for port in ports:
        queue.put(port)

    threads = []

    for _ in range(num_threads):
        t = Thread(target=worker, args=(host, queue, results, timeout, show_logs))
        t.daemon = True
        t.start()
        threads.append(t)

    queue.join()

    return sorted(results, key=lambda x: x["port"])