import requests
from bs4 import BeautifulSoup, Comment
import re
import time
import threading
import os
import random
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
from stem.control import Controller
from stem import Signal

# Initialize Colorama
init(autoreset=True)

# Configuration
MAX_THREADS = 15
TOR_REFRESH_INTERVAL = 10  # Change Tor IP every 10 requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
]
HIDDEN_PATTERNS = [
    r'admin', r'login', r'secret', r'config', r'wp\-?admin', r'phpmyadmin',
    r'test', r'backup', r'old', r'new', r'api', r'v\d', r'internal', r'hidden',
    r'cgi\-bin', r'\.env', r'\.git', r'\.svn', r'\.htaccess', r'\.bak'
]
HIDDEN_TAGS = ['script', 'meta', 'link', 'comment', 'noscript']

# ASCII ART Header
ascii_art = f"""
{Fore.RED}
███████╗██╗      ██████╗ ███████╗███████╗████████╗██████╗ ███████╗██████╗ 
██╔════╝██║     ██╔═══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗
███████╗██║     ██║   ██║███████╗█████╗     ██║   ██████╔╝█████╗  ██████╔╝
╚════██║██║     ██║   ██║╚════██║██╔══╝     ██║   ██╔══██╗██╔══╝  ██╔══██╗
███████║███████╗╚██████╔╝███████║███████╗   ██║   ██║  ██║███████╗██║  ██║
╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{Style.RESET_ALL}
{Fore.YELLOW}Military-Grade Link Extraction System v7.5 (PHANTOM STRIKE){Style.RESET_ALL}
"""

def banner():
    print(ascii_art)
    print(f"{Fore.CYAN}[+] Target Acquisition Module: Activated")
    print(f"[+] Stealth Protocol: Enabled")
    print(f"[+] Multi-Threaded Analyzer: {MAX_THREADS} Parallel Channels")
    print(f"[+] Advanced Heuristics: Signature-Based Detection Engaged{Style.RESET_ALL}\n")

class TorController:
    def __init__(self):
        self.request_count = 0
        self.lock = threading.Lock()
        
    def renew_connection(self):
        with self.lock:
            try:
                with Controller.from_port(port=9051) as controller:
                    controller.authenticate(password="your_tor_password")
                    controller.signal(Signal.NEWNYM)
                print(f"\n{Fore.MAGENTA}[TOR] Identity Rotated Successfully{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[TOR ERROR] Connection Failed: {e}{Style.RESET_ALL}")

def process_link(url, source, use_tor, tor_controller):
    try:
        session = requests.Session()
        if use_tor:
            with tor_controller.lock:
                tor_controller.request_count += 1
                if tor_controller.request_count % TOR_REFRESH_INTERVAL == 0:
                    tor_controller.renew_connection()
            session.proxies = {
                "http": "socks5h://127.0.0.1:9050",
                "https": "socks5h://127.0.0.1:9050"
            }
        
        # Rotate User-Agent and add random delay
        session.headers = {"User-Agent": random.choice(USER_AGENTS)}
        time.sleep(random.uniform(0.1, 0.5))
        
        # Check if hidden
        is_hidden = any(re.search(pattern, url, re.I) for pattern in HIDDEN_PATTERNS) or source in HIDDEN_TAGS
        
        # Send intelligent request
        try:
            resp = session.head(url, timeout=7, allow_redirects=False)
            if resp.status_code == 405:
                resp = session.get(url, timeout=10, allow_redirects=False)
        except (requests.exceptions.SSLError, requests.exceptions.ReadTimeout):
            resp = session.get(url, verify=False, timeout=15, allow_redirects=False)
        except Exception as e:
            return url, 'error', is_hidden, str(e)
        
        # Categorize response
        status = resp.status_code
        if 200 <= status < 300:
            category = 'normal'
        elif status in (301, 302, 303, 307, 308):
            category = 'redirect'
        elif status in (401, 403):
            category = 'forbidden'
        elif 400 <= status < 500:
            category = 'client_error'
        elif 500 <= status < 600:
            category = 'server_error'
        else:
            category = 'other'
            
        return url, category, is_hidden, status
    
    except Exception as e:
        return url, 'error', is_hidden, str(e)

def extract_links(target_url, use_tor):
    try:
        session = requests.Session()
        if use_tor:
            session.proxies = {
                "http": "socks5h://127.0.0.1:9050",
                "https": "socks5h://127.0.0.1:9050"
            }
        
        print(f"\n{Fore.BLUE}[*] Establishing Target Connection...{Style.RESET_ALL}")
        response = session.get(target_url, headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=15)
        response.raise_for_status()
        
        print(f"{Fore.GREEN}[+] Target Acquired ({response.status_code}){Style.RESET_ALL}")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all possible links with sources
        links = set()
        for tag in soup.find_all(["a", "link", "script", "img", "iframe", "form", "meta"]):
            attrs = ['href', 'src', 'content', 'data-src', 'action']
            for attr in attrs:
                if tag.has_attr(attr):
                    absolute_url = urljoin(target_url, tag[attr])
                    links.add((absolute_url, tag.name))
        
        # Extract from comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            found_urls = re.findall(r'https?://[^\s\)\'\"]+', comment)
            for url in found_urls:
                absolute_url = urljoin(target_url, url)
                links.add((absolute_url, 'comment'))
        
        print(f"{Fore.YELLOW}[!] Identified {len(links)} Potential Targets{Style.RESET_ALL}")
        
        # Prepare results
        categories = {
            'normal': [], 'hidden': [], 'forbidden': [],
            'redirect': [], 'client_error': [], 'server_error': [],
            'other': [], 'error': []
        }
        
        # Process links with threading
        tor_controller = TorController()
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = {executor.submit(process_link, url, source, use_tor, tor_controller): (url, source) for url, source in links}
            
            for future in as_completed(futures):
                url, category, is_hidden, status = future.result()
                
                # Add to categories
                categories[category].append(url)
                if is_hidden:
                    categories['hidden'].append(url)
                
                # Display real-time results
                color = {
                    'normal': Fore.GREEN, 'hidden': Fore.YELLOW,
                    'forbidden': Fore.RED, 'redirect': Fore.CYAN,
                    'client_error': Fore.MAGENTA, 'server_error': Fore.LIGHTRED_EX,
                    'error': Fore.LIGHTBLACK_EX
                }.get(category, Fore.WHITE)
                
                status_str = f"{status} | " if category != 'error' else ""
                print(f"{color}[{category.upper()}] {status_str}{url}{Style.RESET_ALL}")
        
        # Save results
        domain = urlparse(target_url).netloc
        output_dir = f"extracted_links/{domain}"
        os.makedirs(output_dir, exist_ok=True)
        
        for category, urls in categories.items():
            if urls:
                with open(f"{output_dir}/{category}.txt", 'w') as f:
                    f.write('\n'.join(sorted(set(urls))))
        
        print(f"\n{Fore.CYAN}[+] Mission Summary:{Style.RESET_ALL}")
        for cat, urls in categories.items():
            print(f"{Fore.LIGHTBLUE_EX}{cat.upper().ljust(12)}: {len(urls)}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}[*] All Intelligence Archived to: {output_dir}/{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}[!] Critical Failure: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    banner()
    target_url = input(f"{Fore.YELLOW}[?] Enter Target Coordinates: {Style.RESET_ALL}").strip()
    use_tor = input(f"{Fore.BLUE}[?] Enable Stealth Protocol (Tor)? [y/N]: {Style.RESET_ALL}").lower() == 'y'
    
    start_time = time.time()
    extract_links(target_url, use_tor)
    
    print(f"\n{Fore.MAGENTA}[*] Operation Completed in {time.time()-start_time:.2f} seconds{Style.RESET_ALL}")