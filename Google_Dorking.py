#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
try:
    from googlesearch import search
except ImportError:
    print("")

import sys
import time
import os
import re
import random
from urllib.parse import urlparse, unquote
from urllib.error import HTTPError

if sys.version[0] in "2":
    print("\n[x] Dorks Eye requires Python 3.x\n")
    exit()

class colors:
    CRED = "\033[1;91m"
    CBLUE = "\033[1;94m"
    CGREEN = "\033[1;92m"
    CYELLOW = "\033[1;93m"
    CPURPLE = "\033[1;95m"
    CEND = "\033[0m"

NEW_BANNER = colors.CRED + r"""
  ▄████  ▒█████   ▒█████    ▄████  ██▓    ▓█████    ▓█████▄  ▒█████   ██▀███   ██ ▄█▀ ██▓ ███▄    █   ▄████
 ██▒ ▀█▒▒██▒  ██▒▒██▒  ██▒ ██▒ ▀█▒▓██▒    ▓█   ▀    ▒██▀ ██▌▒██▒  ██▒▓██ ▒ ██▒ ██▄█▒ ▓██▒ ██ ▀█   █  ██▒ ▀█▒
▒██░▄▄▄░▒██░  ██▒▒██░  ██▒▒██░▄▄▄░▒██░    ▒███      ░██   █▌▒██░  ██▒▓██ ░▄█ ▒▓███▄░ ▒██▒▓██  ▀█ ██▒▒██░▄▄▄░
░▓█  ██▓▒██   ██░▒██   ██░░▓█  ██▓▒██░    ▒▓█  ▄    ░▓█▄   ▌▒██   ██░▒██▀▀█▄  ▓██ █▄ ░██░▓██▒  ▐▌██▒░▓█  ██
░▒▓███▀▒░ ████▓▒░░ ████▓▒░░▒▓███▀▒░██████▒░▒████▒   ░▒████▓ ░ ████▓▒░░██▓ ▒██▒▒██▒ █▄░██░▒██░   ▓██░░▒▓███▀▒
 ░▒   ▒ ░ ▒░▒░▒░ ░ ▒░▒░▒░  ░▒   ▒ ░ ▒░▓  ░░░ ▒░ ░    ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▒ ▓▒░▓  ░ ▒░   ▒ ▒  ░▒   ▒
  ░   ░   ░ ▒ ▒░   ░ ▒ ▒░   ░   ░ ░ ░ ▒  ░ ░ ░  ░    ░ ▒  ▒   ░ ▒ ▒░   ░▒ ░ ▒░░ ░▒ ▒░ ▒ ░░ ░░   ░ ▒░  ░   ░
░ ░   ░ ░ ░ ░ ▒  ░ ░ ░ ▒  ░ ░   ░   ░ ░      ░       ░ ░  ░ ░ ░ ░ ▒    ░░   ░ ░ ░░ ░  ▒ ░   ░   ░ ░ ░ ░   ░
      ░     ░ ░      ░ ░        ░     ░  ░   ░  ░      ░        ░ ░     ░     ░  ░    ░           ░       ░
                                                     ░
""" + colors.CEND
def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(NEW_BANNER)

    info = """
                Author:  AL-MARID
                GitHub:  https://github.com/AL-MARID
                Version: 3.1 (Improved Exact Match)
    """
    print(colors.CBLUE + info + colors.CEND)
    print(colors.CGREEN + "\n\t\t[+] " + colors.CYELLOW + "Dorks Eye: 100% Relevant Dorking" + colors.CEND)
    print(colors.CRED + "\t\t[!] Results match exactly what you type!" + colors.CEND)

def logger(data, filename):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(data + "\n")

def is_exact_match(url, dork):
    cleaned_url = unquote(url).lower()
    dork_lower = dork.lower()

    parsed = urlparse(cleaned_url)

    domain_parts = parsed.netloc.split('.')
    if dork_lower in domain_parts:
        return True

    path_parts = parsed.path.strip('/').split('/')
    if dork_lower in path_parts:
        return True

    if path_parts:
        last_part = path_parts[-1]
        filename = last_part.split('.')[0]
        if filename == dork_lower:
            return True

    pattern = r'\b' + re.escape(dork_lower) + r'\b'
    if re.search(pattern, cleaned_url):
        return True

    return False

def strict_search(dork, num_results, pause=2):
    seen = set()
    count = 0
    start = 0
    max_retries = 3
    retries = 0

    num_results = min(num_results, 100)

    while count < num_results and retries < max_retries:
        try:
            for url in search(dork, tld="com", lang="en", num=10, start=start, stop=None, pause=pause):
                if count >= num_results:
                    break

                if url in seen:
                    continue
                seen.add(url)

                if is_exact_match(url, dork):
                    count += 1
                    yield url

            start += 10
            retries = 0

        except HTTPError as e:
            if e.code == 429:
                retries += 1
                wait_time = 10 * retries
                print(colors.CRED + f"[!] Too many requests. Waiting {wait_time} seconds..." + colors.CEND)
                time.sleep(wait_time)
            else:
                print(colors.CRED + f"[!] HTTP error: {e}" + colors.CEND)
                break
        except Exception as e:
            print(colors.CRED + f"[!] Error: {e}" + colors.CEND)
            retries += 1
            time.sleep(5 * retries)

def advanced_dorking():
    try:
        dork = input("\n[+] " + colors.CGREEN + "Enter The Exact Dork Query: " + colors.CEND).strip()
        if not dork:
            print(colors.CRED + "[!] Dork query cannot be empty!" + colors.CEND)
            return

        requested_num = int(input("[+] " + colors.CGREEN + "Enter The Exact Number Of Results: " + colors.CEND))
        if requested_num <= 0:
            print(colors.CRED + "[!] Number must be greater than 0" + colors.CEND)
            return

        save_output = input("\n[+] " + colors.CYELLOW + "Save results to file? (Y/N): " + colors.CEND).strip().lower()
        output_file = None
        if save_output == 'y':
            output_file = input("[+] " + colors.CYELLOW + "Output filename (press Enter for 'results.txt'): " + colors.CEND).strip()
            if not output_file:
                output_file = "results.txt"

        print("\n" + colors.CGREEN + "="*80 + colors.CEND)
        print(colors.CYELLOW + f"[+] Starting EXACT MATCH search for: '{dork}'" + colors.CEND)
        print(colors.CYELLOW + f"[+] Fetching exactly {requested_num} 100% relevant results..." + colors.CEND)
        print(colors.CGREEN + "="*80 + "\n" + colors.CEND)

        counter = 0
        for url in strict_search(dork, requested_num):
            counter += 1
            print(f"[{counter}] {url}")
            if output_file:
                logger(url, output_file)

        print("\n" + colors.CGREEN + "="*80 + colors.CEND)
        print(colors.CGREEN + f"\n[•] Found {counter} EXACT MATCH results." + colors.CEND)

        if requested_num > 100:
            print(colors.CRED + f"[!] Note: The maximum number of results is limited to 100. Found {counter} results." + colors.CEND)
        elif counter < requested_num:
            print(colors.CRED + f"[!] Only found {counter} exact matches (requested: {requested_num})" + colors.CEND)

        if output_file:
            print(colors.CYELLOW + f"[+] Results saved to: {output_file}" + colors.CEND)

        print(colors.CRED + "\t\t[!] Keep learning and stay ethical!" + colors.CEND)
        print(colors.CYELLOW + "\t\t[+] Follow me on GitHub: https://github.com/AL-MARID\n" + colors.CEND)

    except KeyboardInterrupt:
        print("\n" + colors.CRED + "[!] Search interrupted by user." + colors.CEND)
        if output_file:
            print(colors.CYELLOW + f"[+] Partial results saved to: {output_file}" + colors.CEND)
        sys.exit(0)
    except Exception as e:
        print("\n" + colors.CRED + f"[!] Critical error: {e}" + colors.CEND)
        sys.exit(1)

if __name__ == "__main__":
    print_banner()
    advanced_dorking()

