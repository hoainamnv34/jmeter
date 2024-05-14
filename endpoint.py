#!/usr/bin/env python

import socket
import subprocess
import sys
import time
import argparse
import requests



def fetchArguments():
    parse = argparse.ArgumentParser()
    parse.add_argument('-t', '--target', help='Specify target to scan',
                       default='http://localhost:80', dest='target')
    parse.add_argument('-z', '--zap-host', help='address and port of ZAP host',
                       default='127.0.0.1:8085', dest='zap_host')
    

    return parse.parse_args()

def wait_for_it(host, port, timeout):
    """
    Wait until a TCP connection can be established to the specified host and port.

    Args:
    host (str): The host to connect to.
    port (int): The port to connect to.
    timeout (int): Timeout in seconds.

    Returns:
    bool: True if connection successful within timeout, False otherwise.
    """
    start_time = time.time()
    end_time = start_time + timeout
    while time.time() < end_time:
        try:
            with socket.create_connection((host, port), timeout=1) as conn:
                print(f"[INFO] Connection to {host}:{port} succeeded!")
                return
        except ConnectionRefusedError:
            print(f"[INFO] Connection to {host}:{port} refused. Retrying...")
            time.sleep(1)
    sys.exit(f"[ERROR] Connection to {host}:{port} failed within {timeout} seconds.")
    


def run_jmeter(jmeter_path, jmx_file, jtl_file, log_file, output_dir):
    """
    Run JMeter command.

    Args:
    jmeter_path (str): Path to the JMeter executable.
    jmx_file (str): Path to the JMX test file.
    jtl_file (str): Path to save the JTL result file.
    log_file (str): Path to save the JMeter log file.
    output_dir (str): Path to save the HTML report.

    Returns:
    int: Return code of the subprocess call.
    """
    # Construct the command
    command = [
        jmeter_path,
        "-Dlog_level.jmeter=DEBUG",
        "-n",
        "-t", jmx_file,
        "-l", jtl_file,
        "-j", log_file,
        "-e",
        "-o", output_dir
    ]

    # Run the command
    try:
        # subprocess.run(["ls", "-l"])
        return subprocess.run(command)
    except Exception as e:
        print(f"Error occurred while running JMeter: {e}")
        return -1  # Return -1 in case of error


def download_file(zap_url, file_name):
    """
    Download a file from a URL constructed by combining zap_url and endpoint, and save it to disk.

    Args:
    zap_url (str): The zap URL of the server.
    file_name (str): The name of the file to save the downloaded data.

    Returns:
    bool: True if download successful, False if unsuccessful.
    """

    endpoint = "OTHER/core/other/xmlreport/"

    try:
        url = zap_url.rstrip('/') + '/' + endpoint.lstrip('/')
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print("File downloaded successfully!")
            return True
        else:
            print("Error: Unable to download file. Status code:", response.status_code)
            return False
    except Exception as e:
        print("Error: Unable to download file:", str(e))
        return False


def delete_site(zap_url, site_url):
    """
    Delete a site from ZAP using GET request.

    Args:
    zap_url (str): The base URL of the ZAP server.
    site_url (str): The URL of the site to be deleted.

    Returns:
    dict: JSON response from the ZAP API if successful, None otherwise.
    """

    endpoint = "JSON/core/action/deleteSiteNode/"

    url = zap_url.rstrip('/') + '/' + endpoint.lstrip('/')

    headers = {'Accept': 'application/json'}
    params = {'url': site_url}
    try:
        print(params)
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()  # Return JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def main():
    args = fetchArguments()
    print("target ", args.target, " zap_host: ", args.zap_host)

    # Parse ZAP host and port
    zap_host_and_port = args.zap_host[len("http://"):]
    zap_host, zap_port = zap_host_and_port.split(':')

    # Convert zap_port to integer
    zap_port = int(zap_port)

    # Wait for ZAP host to be available
    wait_for_it(zap_host, zap_port, 10)
    print("Zap is running")

    # Wait for Target host to be available
    wait_for_it(zap_host, zap_port, 10)
    print("Target is running")


    jmeter_path = "jmeter"  # Replace with actual path to JMeter executable
    jmx_file = "/root/test-file/HTTP_Request.jmx"
    jtl_file = "/root/jmeter-report/HTTP_Request.jtl"
    log_file = "/root/jmeter-report/jmeter.log"
    output_dir = "/root/jmeter-report/output"

    result=run_jmeter(jmeter_path, jmx_file, jtl_file, log_file, output_dir)
    print(result)

    
    zap_url = args.zap_host
    file_name = "report.xml"
    download_file(zap_url, file_name)

    # subprocess.run(["cat", "report.xml"])
    # rp = reports(zap)
    # result = rp.generate(title="ZAP Scanning Report",template= "traditional-xml", reportfilename="testtt.xml", reportdir=None)
    # print(result)

    site_url = args.target
    result = delete_site(zap_url, site_url)
    print("target ", args.target, " zap_host: ", args.zap_host)
    if result:
        print(result)
    else:
        print("Failed to delete site from ZAP.")



if __name__ == '__main__':
    main()
