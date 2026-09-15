import socket
import ssl
import urllib.request
import urllib.error
import hashlib
import secrets
import string
import getpass
import time
import os

RESET = "\033[0m"
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"
DIM = "\033[2m"

def clear():
    os.system("clear")

def line():
    print(CYAN + "═" * 50 + RESET)

def pause():
    input("\nPress Enter to return to menu...")

def startup():
    clear()
    print(BLUE + r"""
 ██████  ███    ███  ██████  ██████
██    ██ ████  ████ ██    ██ ██   ██
██    ██ ██ ████ ██ ██    ██ ██████
██    ██ ██  ██  ██ ██    ██ ██   ██
 ██████  ██      ██  ██████  ██   ██
""" + RESET)
    print(CYAN + "          O M O R" + RESET)
    print(WHITE + "       SECURITY TOOL v2.0" + RESET)
    line()
    print(GREEN + "[+] Initializing system..." + RESET)
    time.sleep(0.4)
    print(GREEN + "[+] Loading security modules..." + RESET)
    time.sleep(0.4)
    print(GREEN + "[+] Ethical audit mode enabled..." + RESET)
    time.sleep(0.4)
    print(CYAN + "[+] SYSTEM READY ✓" + RESET)
    time.sleep(0.6)

def check_headers():
    url = input("\nEnter your website URL: ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "OMOR-Security-Tool/2.0"})
        response = urllib.request.urlopen(request, timeout=8)
        security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Referrer-Policy"
        ]
        print("\n" + CYAN + "SECURITY HEADERS" + RESET)
        line()
        found = 0
        for header in security_headers:
            value = response.headers.get(header)
            if value:
                print(GREEN + "[+] " + header + ": FOUND" + RESET)
                found += 1
            else:
                print(RED + "[-] " + header + ": MISSING" + RESET)
        print("\nSecurity Header Score:", str(found) + "/5")
    except Exception as error:
        print(RED + "[!] Error: " + str(error) + RESET)

def check_ports():
    host = input("\nEnter your own/authorized IP or hostname: ").strip()
    ports = {21: "FTP", 22: "SSH", 25: "SMTP", 53: "DNS", 80: "HTTP", 443: "HTTPS", 8080: "Web Proxy"}
    print("\n" + CYAN + "COMMON PORT CHECK" + RESET)
    line()
    for port, service in ports.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.7)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(GREEN + "[+] " + str(port) + " OPEN  → " + service + RESET)
            else:
                print(DIM + "[-] " + str(port) + " CLOSED → " + service + RESET)
            sock.close()
        except Exception:
            print(RED + "[!] Could not check port " + str(port) + RESET)

def clean_domain(value):
    return value.replace("https://", "").replace("http://", "").split("/")[0].strip()

def dns_info():
    domain = clean_domain(input("\nEnter domain: "))
    try:
        ip = socket.gethostbyname(domain)
        print("\n" + CYAN + "DNS INFORMATION" + RESET)
        line()
        print(GREEN + "[+] Domain : " + domain + RESET)
        print(GREEN + "[+] IPv4   : " + ip + RESET)
    except Exception as error:
        print(RED + "[!] Error: " + str(error) + RESET)

def password_strength():
    password = getpass.getpass("\nEnter a password to test locally: ")
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    print("\nPassword Score:", str(score) + "/6")
    if score <= 2:
        print(RED + "Risk: WEAK" + RESET)
    elif score <= 4:
        print(YELLOW + "Risk: MEDIUM" + RESET)
    else:
        print(GREEN + "Risk: STRONG" + RESET)

def ssl_checker():
    domain = clean_domain(input("\nEnter your domain: "))
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=8) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_socket:
                certificate = secure_socket.getpeercert()
                print("\n" + CYAN + "HTTPS / SSL CHECK" + RESET)
                line()
                print(GREEN + "[+] HTTPS connection: OK" + RESET)
                if certificate:
                    print(GREEN + "[+] Certificate: FOUND" + RESET)
                print(GREEN + "[+] TLS connection: SECURE" + RESET)
    except Exception as error:
        print(RED + "[!] HTTPS/SSL error: " + str(error) + RESET)

def http_status():
    url = input("\nEnter website URL: ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "OMOR-Security-Tool/2.0"})
        response = urllib.request.urlopen(request, timeout=8)
        print("\n" + CYAN + "HTTP STATUS" + RESET)
        line()
        print(GREEN + "[+] URL: " + url + RESET)
        print(GREEN + "[+] Status: " + str(response.status) + RESET)
    except urllib.error.HTTPError as error:
        print(YELLOW + "[!] HTTP Status: " + str(error.code) + RESET)
    except Exception as error:
        print(RED + "[!] Error: " + str(error) + RESET)

def security_score():
    url = input("\nEnter your website URL: ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    headers = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Referrer-Policy"
    ]
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "OMOR-Security-Tool/2.0"})
        response = urllib.request.urlopen(request, timeout=8)
        score = 2 if url.startswith("https://") else 0
        for header in headers:
            if response.headers.get(header):
                score += 1
        print("\n" + CYAN + "WEBSITE SECURITY SCORE" + RESET)
        line()
        print("Score:", str(score) + "/7")
        if score >= 6:
            print(GREEN + "Risk Level: LOW" + RESET)
        elif score >= 4:
            print(YELLOW + "Risk Level: MEDIUM" + RESET)
        else:
            print(RED + "Risk Level: NEEDS IMPROVEMENT" + RESET)
    except Exception as error:
        print(RED + "[!] Error: " + str(error) + RESET)

def robots_checker():
    domain = input("\nEnter your website: ").strip()
    if not domain.startswith(("http://", "https://")):
        domain = "https://" + domain
    url = domain.rstrip("/") + "/robots.txt"
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "OMOR-Security-Tool/2.0"})
        response = urllib.request.urlopen(request, timeout=8)
        content = response.read().decode("utf-8", errors="ignore")
        print("\n" + CYAN + "ROBOTS.TXT" + RESET)
        line()
        print(GREEN + "[+] robots.txt found" + RESET)
        print("\n" + content[:1000])
    except Exception:
        print(RED + "[-] robots.txt not found or unavailable" + RESET)

def ip_information():
    domain = clean_domain(input("\nEnter domain: "))
    try:
        ip = socket.gethostbyname(domain)
        print("\n" + CYAN + "IP INFORMATION" + RESET)
        line()
        print(GREEN + "[+] Hostname: " + domain + RESET)
        print(GREEN + "[+] IPv4: " + ip + RESET)
    except Exception as error:
        print(RED + "[!] Error: " + str(error) + RESET)

def hostname_resolver():
    host = input("\nEnter hostname/IP: ").strip()
    try:
        result = socket.gethostbyaddr(host)
        print("\n" + CYAN + "HOSTNAME RESOLVER" + RESET)
        line()
        print(GREEN + "[+] Hostname: " + result[0] + RESET)
    except Exception:
        print(RED + "[-] Could not resolve hostname" + RESET)

def local_network():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print("\n" + CYAN + "LOCAL NETWORK INFO" + RESET)
        line()
        print(GREEN + "[+] Device hostname: " + hostname + RESET)
        print(GREEN + "[+] Local IP: " + ip + RESET)
    except Exception as error:
        print(RED + "[!] Error: " + str(error) + RESET)

def password_generator():
    try:
        length = int(input("\nPassword length (8-32): ").strip())
        if length < 8 or length > 32:
            print(YELLOW + "[!] Choose 8-32 characters." + RESET)
            return
        characters = string.ascii_letters + string.digits + string.punctuation
        password = "".join(secrets.choice(characters) for _ in range(length))
        print("\n" + CYAN + "GENERATED PASSWORD" + RESET)
        line()
        print(GREEN + password + RESET)
    except ValueError:
        print(RED + "[!] Enter a valid number." + RESET)

def hash_generator():
    text = input("\nEnter text: ")
    result = hashlib.sha256(text.encode()).hexdigest()
    print("\n" + CYAN + "SHA-256 HASH" + RESET)
    line()
    print(GREEN + result + RESET)

def hash_checker():
    text = input("\nEnter original text: ")
    expected = input("Enter SHA-256 hash: ").strip().lower()
    result = hashlib.sha256(text.encode()).hexdigest()
    if result == expected:
        print(GREEN + "[+] HASH MATCH ✓" + RESET)
    else:
        print(RED + "[-] HASH DOES NOT MATCH" + RESET)

def security_tips():
    clear()
    print(CYAN + "SECURITY TIPS" + RESET)
    line()
    tips = [
        "Use HTTPS on websites.",
        "Use strong and unique passwords.",
        "Enable 2FA on important accounts.",
        "Never expose API keys in frontend code.",
        "Keep software and dependencies updated.",
        "Do not share passwords or recovery codes.",
        "Only test systems you own or have permission to test."
    ]
    for number, tip in enumerate(tips, 1):
        print(GREEN + "[" + str(number) + "] " + WHITE + tip + RESET)
    pause()

def help_menu():
    clear()
    print(BLUE + "OMOR SECURITY TOOL — HELP" + RESET)
    line()
    print("""
1  → Website security headers
2  → Common network ports
3  → DNS information
4  → Local password strength
5  → HTTPS / SSL check
6  → HTTP status
7  → Basic security score
8  → robots.txt check
9  → IP information
10 → Hostname resolver
11 → Local network information
12 → Secure password generator
13 → SHA-256 hash generator
14 → SHA-256 hash checker
15 → Security tips
16 → Help
0  → Exit

Use these tools only on systems you own
or have explicit permission to test.
""")
    pause()

def menu():
    while True:
        clear()
        print(BLUE + r"""
╔══════════════════════════════════════════════════╗
║                                                  ║
║             ⚡  O M O R  ⚡                      ║
║             SECURITY TOOL v2.0                  ║
║                                                  ║
║              [ SYSTEM ONLINE ]                  ║
║                                                  ║
╚══════════════════════════════════════════════════╝
""" + RESET)
        print(CYAN + "[01]" + WHITE + " Security Headers")
        print(CYAN + "[02]" + WHITE + " Common Port Checker")
        print(CYAN + "[03]" + WHITE + " DNS Information")
        print(CYAN + "[04]" + WHITE + " Password Strength")
        print(CYAN + "[05]" + WHITE + " HTTPS / SSL Checker")
        print(CYAN + "[06]" + WHITE + " HTTP Status")
        print(CYAN + "[07]" + WHITE + " Website Security Score")
        print(CYAN + "[08]" + WHITE + " Robots.txt Checker")
        print(CYAN + "[09]" + WHITE + " IP Information")
        print(CYAN + "[10]" + WHITE + " Hostname Resolver")
        print(CYAN + "[11]" + WHITE + " Local Network Info")
        print(CYAN + "[12]" + WHITE + " Password Generator")
        print(CYAN + "[13]" + WHITE + " SHA-256 Generator")
        print(CYAN + "[14]" + WHITE + " SHA-256 Checker")
        print(CYAN + "[15]" + WHITE + " Security Tips")
        print(CYAN + "[16]" + WHITE + " Help")
        print(CYAN + "[00]" + WHITE + " Exit")
        line()
        choice = input(CYAN + "OMOR@TERMUX > " + RESET).strip()

        actions = {
            "1": check_headers, "2": check_ports, "3": dns_info,
            "4": password_strength, "5": ssl_checker, "6": http_status,
            "7": security_score, "8": robots_checker, "9": ip_information,
            "10": hostname_resolver, "11": local_network,
            "12": password_generator, "13": hash_generator,
            "14": hash_checker, "15": security_tips, "16": help_menu
        }

        if choice in actions:
            actions[choice]()
            if choice not in ("15", "16"):
                pause()
        elif choice in ("0", "00"):
            clear()
            print(GREEN + "OMOR SECURITY TOOL closed." + RESET)
            break
        else:
            print(RED + "[!] Invalid option." + RESET)
            time.sleep(1)

if __name__ == "__main__":
    startup()
    menu()
