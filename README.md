# IP Geolocation & ASN Tracker 🌍

A Python-based Open-Source Intelligence (OSINT) utility built for Security Operations Center (SOC) analysts to rapidly identify the physical location and ownership of suspicious IP addresses.

**Features:**
* Integrates with public REST APIs via the Python `requests` library to fetch geolocation JSON data without requiring API keys.
* Extracts critical threat hunting data including City, Country, Internet Service Provider (ISP), and Autonomous System Number (ASN).
* Employs multithreading to ensure the Tkinter graphical interface remains responsive during external HTTP requests.
* Includes error handling for reserved/private IP address ranges that cannot be globally routed.

*Built as Day 17 of a 30-Day Network Engineering & Security portfolio streak.*
