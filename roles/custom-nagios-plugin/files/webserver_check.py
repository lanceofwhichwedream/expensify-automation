#!/usr/bin/env python3
# By Lance Zeligman
import logging
import requests
import sys

def get_hosts():
    """
    Reads the hosts from webhosts.txt
    """

    # Open the Webhosts.txt File
    file = open("/etc/nagios-plugin/webhosts.txt", "r")
    hosts = file.read()

    # Create an array, remove empty elements
    hosts = hosts.split("\n")
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
    logging.info(f"Getting Status of {host}")
    return r.status_code


def combine_results(responses):
    """
    Performs the Logic to determine how many hosts are up
    """
    total_count = 2
    

    for i in responses:
        if i == 200:
            total_count += -1

    return total_count

if __name__ == "__main__":
    # Set up our variables
    logging.basicConfig(
        filename="/var/log/nagios-plugin/webserver_check.log",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )

    hosts = get_hosts()
    hosts = sanitize_hosts(hosts) 
    responses = []
    
    for i in hosts:
        status = check_hosts(i)
        responses.append(status)
    
    total_count = combine_results(responses)

    if total_count == 2:
        logging.info(f"total count is: {total_count}")
        logging.info(f"responses are: {responses}")
        logging.critical(
            "Variables state both Webservers are offline and require investigation"
        )
        print("Both Webservers are offline and require investigation")
        sys.exit(2)
    elif total_count == 1:
        logging.info(f"total count is: {total_count}")
        logging.info(f"responses are: {responses}")
        logging.warning(
            "Variables state one Webserver is offline and requires investigation"
        )
        print("One Webserver is offline and requires investigation")
        sys.exit(1)
    elif total_count == 0:
        logging.info(f"total count is: {total_count}")
        logging.info(f"responses are: {responses}")
        logging.info(
            "Variables state no Webserver are offline and we're doing just fine"
        )
        print("No Webservers are offline and we're doing just fine")
        sys.exit(0)
    else:
        logging.critical("Something else has gone wrong. Troubleshoot accordingly")
        sys.exit(3)
