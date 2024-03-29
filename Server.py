#!/usr/bin/python
from _thread import *
import pickle
import socket
import platform
import time

global active_clients, client_rfc, combined_rfc_list

active_clients = []
client_rfc = []
combined_rfc_list = []


# method to lookup a particular rfc
def rfc_lookup(data1, data2):
    response = []
    for rfc_list in combined_rfc_list:
        if rfc_list['RFC_Number'] == data1 and rfc_list['RFC_Title'] == data2:
            response.append(rfc_list)
    if len(response) == 0:
        msg = "P2P-CI/1.0 404 Not Found " + "\n" \
            "Date: " + time.strftime("%a, %d %b %Y %X %Z", time.localtime()) + "\n" \
            "OS: " + str(platform.platform()) + "\n"
    else:
        msg = "P2P-CI/1.0 200 OK " + "\n"
    return pickle.dumps((response, msg))


# method to add a client rfc info to server list
def rfc_add_to_list(connection_socket, address, client_data, peer_port):
    rfc_number = client_data[1][0]
    rfc_title = client_data[1][1]
    connection_socket.send(bytes(
        "P2P-CI/1.0 200 OK \nRFC " + rfc_number + " " + rfc_title +
        " " + str(address[0]) + " " + str(client_data[3]), 'utf-8'))
    keys = ['RFC_Number', 'RFC_Title', 'Host_Name']
    value = [str(rfc_number), rfc_title, address[0]]
    client_rfc.insert(0, dict(zip(keys, value)))
    combined_keys = ['RFC_Number', 'RFC_Title', 'Host_Name', 'Port_Number']
    combined_value = [str(rfc_number), rfc_title, address[0], str(peer_port)]
    combined_rfc_list.insert(0, dict(zip(combined_keys, combined_value)))


def new_child_thread(connectionSocket, address):
    server_data = pickle.loads(connectionSocket.recv(1024))
    peer_port = server_data[3]
    peer_key = ['Host_Name', 'Port_Number']
    peer_value = [address[0], str(peer_port)]
    active_clients.insert(0, dict(zip(peer_key, peer_value)))
    client_rfc_key = ['RFC_Number', 'RFC_Title', 'Host_Name']
    combined_rfc_key = ['RFC_Number', 'RFC_Title', 'Host_Name', 'Port_Number']
    print(server_data[0])
    msg = "P2P-CI/1.0 200 OK \n"
    for rfc in server_data[1]:
        rfc_num = rfc['RFC_Number']
        rfc_ttl = rfc['RFC_Title']
        client_rfc_value = [str(rfc_num), rfc_ttl, address[0]]
        client_rfc.insert(0, dict(zip(client_rfc_key, client_rfc_value)))
        combined_rfc_value = [str(rfc_num), rfc_ttl, address[0], str(server_data[3])]
        combined_rfc_list.insert(0, dict(zip(combined_rfc_key, combined_rfc_value)))
        msg += "RFC " + rfc_num + " " + rfc_ttl + " " + str(address[0]) + " " + str(server_data[3]) + "\n"
    connectionSocket.send(
        bytes("Connection to server {0} established successfully.".format(serverHost) + "\n" + msg, 'utf-8'))
    while True:
        client_data = pickle.loads(connectionSocket.recv(1024))
        if type(client_data) == str:
            print(client_data)
        else: print(client_data[0])
        if client_data == 'exit':
            break
        else:
            if client_data[0][0] == "A":
                rfc_add_to_list(connectionSocket, address, client_data, peer_port)
            elif client_data[1] == "lookup":
                new_data = rfc_lookup(client_data[2], client_data[3])
                connectionSocket.send(new_data)
            elif client_data[1] == 'list':
                connection_msg = "P2P-CI/1.0 200 OK"
                connectionSocket.send(pickle.dumps(
                    [connection_msg, (combined_rfc_list, ['RFC_Number', 'RFC_Title', 'Host_Name', 'Port_Number'])]))
    # Removing Client's information from server data structures when the client leaves the system
    active_clients[:] = [clients for clients in active_clients if clients.get('Host_Name') != address[0]]
    client_rfc[:] = [rfcs for rfcs in client_rfc if rfcs.get('Host_Name') != address[0]]
    combined_rfc_list[:] = [c_rfc for c_rfc in combined_rfc_list if c_rfc.get('Host_Name') != address[0]]
    print("active clients\n", active_clients)
    connectionSocket.close()


if __name__ == "__main__":
    # Starting Socket server to accept incoming client connections
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverPort = 7734
    serverHost = socket.gethostname()
    print(serverHost)
    serverSocket.bind((serverHost, serverPort))
    print(serverSocket.getsockname())
    print("starting the server to listen for incoming connection...\n")
    # listen client connection request and create a new thread which will handle request of the client
    while True:
        serverSocket.listen()
        connectionSocket, address = serverSocket.accept()
        start_new_thread(new_child_thread, (connectionSocket, address))
    print("closing the server.\n")
    serverSocket.close()
