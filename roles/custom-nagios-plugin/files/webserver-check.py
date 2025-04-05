#!/usr/bin/env python
# By Lance Zeligman
import requests


def get_hosts():
    """
    Reads the hosts from webhosts.txt
    """

    # Open the Webhosts.txt File
    file = open("webhosts.txt", "r")
    hosts = file.read()

    # Create an array, remove empty elements
    hosts = hosts.split('\n')
    hosts = [x for x in hosts if x.strip()]

    # Perform Clean up before we return our data
    file.close()

    return hosts

def sanitize_hosts(hosts):
    """
    Requests wants a url scheme rather than a simple ip address
    This Method adds one
    """
    clean_hosts = []

    for i in hosts:
        host = "http://" + i
        clean_hosts.append(host)

    return clean_hosts

def check_hosts(host):
    """
    Pings the ip addresses provided to check for host aliveness
    """

    # Run a get request against the supplied host
    r = requests.get(host)
    return r.status_code

if __name__ == "__main__":
    # Set up our variables
    responses = []
    total_count = 2
    hosts = get_hosts()
    hosts = sanitize_hosts(hosts)

    for i in hosts:
        status = check_hosts(i)
        responses.append(status)

    for i in responses:
        if i == 200:
            total_count += -1
    # Todo: Convert print statements to logging statements 
    if total_count == 2:
        print(f"total count is: {total_count}")
        print(f"responses are: {responses}")
        print("Variables state both Webservers are offline and require investigation")
        exit(2)
    elif total_count == 1:
        print(f"total count is: {total_count}")
        print(f"responses are: {responses}")
        print("Variables state one Webserver is offline and requires investigation")
        exit(1)
    elif total_count == 0:
        print(f"total count is: {total_count}")
        print(f"responses are: {responses}")
        print("Variables state no Webserver are offline and we're doing just fine")
        exit(0)
    else:
        print("Something else has gone wrong. Troubleshoot accordingly")
        exit(3)



