from __future__ import print_function
import getpass # package for reading passwords without displaying them on the console.
from csv import reader
import requests, json
from cpapi import APIClient, APIClientArgs # cpapi is a library that handles the communication with the Check Point management server.
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    # getting details from the user
    api_server = input("Enter server IP address or hostname:")
    username = input("Enter username: “)

    if sys.stdin.isatty():
        password = getpass.getpass("Enter password: ")
    else:
        print("Attention! Your password will be shown on the screen!")
        password = input("Enter password: ")

    client_args = APIClientArgs(server = api_server)
    
    with APIClient(client_args) as client:

        # The API client, would look for the server's certificate SHA1 fingerprint in a file.
        # If the fingerprint is not found on the file, it will ask the user if he accepts the server's fingerprint.
        # In case the user does not accept the fingerprint, exit the program.
        if client.check_fingerprint() is False:
            print("Could not get the server's fingerprint - Check connectivity with the server.")
            exit(1)

        # login to server:
        login_res = client.login(username, password)

        if login_res.success is False:
            print("Login failed:\n{}".format(login_res.error_message))
            exit(1)

        csv_filepath = input("Enter the filepath: ")
        # delete network objects listed in a csv file
        # read the file
        with open(csv_filepath, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            for host in csv_reader:
                # host variable is a list that represents a row in csv
                unused_host_data = {'name':'{}'.format(str(host[0]))}

                delete_objects_response = client.api_call("delete-host", unused_host_data)
                
                if delete_object_response.success:
                    print("The network object {} has been deleted successfully".format(unused_host_data))            
                else:
                    print("Failed to delete network object {}, Error:\n{}".format(unused_host_data, delete_objects_response.error_message))
                
        # publish the result
        publish_res = client.api_call("publish", {})
        if publish_res.success:
            print("The changes were published successfully.")
        else:
            print("Failed to publish the changes.")

if __name__ == "__main__":
    main()
