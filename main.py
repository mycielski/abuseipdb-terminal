import argparse
import socket  # to check validity of ip addresses passed as arguments before sending them to AbuseIPDB

from requests import get
from bs4 import BeautifulSoup  # to extract meaningful data from response easily and quickly

parser = argparse.ArgumentParser(description="Check IP addresses in AbuseIPDB.")
parser.add_argument("addresses", metavar="ip", type=str, nargs='+', help="an address to check")
#parser.add_argument("csv", metavar="filepath", type=str)

args = parser.parse_args()

addresses_validated = []
addresses_invalidated = []

for argument in args.addresses:
    try:
        socket.inet_aton(argument)
        addresses_validated.append(argument)
    except socket.error:
        addresses_invalidated.append(argument)

print("Parsed IP addresses:")
for address in addresses_validated:
    print(address)

if len(addresses_invalidated) != 0:
    print("\nInvalid IP addresses:")
    for address in addresses_invalidated:
        print(address)

for address in addresses_validated:
    print()
    request_address = "https://www.abuseipdb.com/check/" + address
    r = get(request_address)
    soup = BeautifulSoup(r.text, "html.parser")  # for increased speed download and use "lxml.parser"
    response = soup.find('div', {'class': 'well'}).text
    if "was found in our database!" in response:
        print(address + " was FOUND in AbuseIPDB:")
        if "is a private IP address" in response:
            print(address + " is a PRIVATE address according to AbuseIPDB.")
        else:
            confidence_of_abuse = soup.find('div', {'class': 'progress-bar'}).text.replace("\n", "")
            print("Confidence of Abuse:\t" + confidence_of_abuse)
            results = soup.find_all('td')
            print("ISP:\t\t\t" + results[0].text.replace("\n", ""))
            print("Usage Type:\t\t" + results[1].text.replace("\n", ""))
            print("Domain Name:\t\t" + results[2].text.replace("\n", ""))
            print("Country:\t\t" + results[3].text.replace("\n", ""))
            print("City:\t\t\t" + results[4].text.replace("\n", ""))
    elif "was not found in our database" in response:
        print(address + " was NOT found in AbuseIPDB.")
