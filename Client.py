#!usr/bin/python
import os
import socket
import time
from _thread import *
import platform
import pickle
import random


def get_rfc_num_ttl():
    rfc_num = input("Enter the rfc number required. \n")
    rfc_ttl = input("Enter the rfc title required. \n")
    return rfc_num, rfc_ttl

def lookup_rfc(rfc_num, rfc_ttl):
    connection_msg = "LOOKUP" + " RFC " + str(rfc_num) + " P2P-CI/1.0 \n" \
        "Host: " + str(socket.gethostname()) + " (" + str(clientSocket.getsockname()[0]) + ") \n" \
        "Port: " + str(clientSocket.getsockname()[1]) + "\n" \
        "Title: " + str(rfc_ttl) + "\n"
    clientSocket.send(pickle.dumps([connection_msg, "lookup", rfc_num]))
    server_data = pickle.loads(clientSocket.recv(1024))
    print(server_data[1], end="")
    for rfc in server_data[0]:
        print('RFC '+' '.join([rfc[r] for r in ['RFC_Number', 'RFC_Title', 'Host_Name', 'Port_Number']]))


def get_rfc(rfc_num, rfc_ttl):
    msg = "LOOKUP" + " RFC " + str(rfc_num) + " P2P-CI/1.0 \n" \
        "Host: " + str(socket.gethostname()) + " (" + str(clientSocket.getsockname()[0]) + ") \n" \
        "Port: " + str(clientSocket.getsockname()[1]) + "\n"
    "Title: " + str(rfc_ttl) + "\n"
    clientSocket.send(pickle.dumps([msg,  "get", rfc_num]))
    server_data = pickle.loads(clientSocket.recv(1024))
    print(server_data)
    if server_data[0]:
        new_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_soc.connect((server_data[0]["Host_Name"], int(server_data[0]["Port_Number"])))
        os_type_version = platform.platform()
        msg = "GET RFC " + str(rfc_num) + " P2P-CI/1.0 \n" \
            "Host: " + str(socket.gethostname()) + " (" + str(clientSocket.getsockname()[0]) + ") \n" \
            "OS: " + str(os_type_version) + "\n"
        new_soc.send(bytes(msg, 'utf-8'))
        response = pickle.loads(new_soc.recv(1024))
        for x in range(len(response)):
            print(response[x])
        path = os.getcwd()
        filename = "rfc" + rfc_num + ".txt"
        type_of_os = platform.system()
        if type_of_os == "Windows":
            filename = path + "\\rfc\\" + filename
        else:
            filename = path + "/rfc/" + filename
        with open(filename, 'w') as f:
            f.write(response[1])
        new_soc.close()
    else:
        print(server_data[1])


def add_rfc(rfc_num, rfc_ttl):
    path_name = os.getcwd()
    file_name = "rfc" + rfc_num + ".txt"
    os_type = platform.system()
    file_path = path_name + "\\rfc\\" + file_name if os_type == "Windows" else path_name + "/rfc/" + file_name;
    print(path_name, os_type, file_name, file_path, '\n')
    connection_msg = ''
    if not os.path.isfile(file_path):
        print(file_name + " does not exist.\n")
    else:
        connection_msg = "ADD RFC " + str(rfc_num) + " P2P-CI/1.0 \n" \
            "Host: " + str(socket.gethostname()) + " (" + str(clientSocket.getsockname()[0]) + ") \n" \
            "Port: " + str(clientSocket.getsockname()[1]) + "\n" \
            "Title: " + str(rfc_ttl) + "\n"
    return connection_msg


def list_rfc():
    connection_msg = "LIST ALL P2P-CI/1.0 \n" \
            "Host: " + str(socket.gethostname()) + " (" + str(clientSocket.getsockname()[0]) + ") \n" \
            "Port: " + str(clientSocket.getsockname()[1]) + "\n"
    clientSocket.send(pickle.dumps([connection_msg, "list"]))
    server_data = pickle.loads(clientSocket.recv(1024))
    for rfc_list in server_data[1][0]:
        print('RFC '+' '.join([rfc_list[rfc_head] for rfc_head in server_data[1][1]]))


def connection_reply(rfc_num):
    filename = "rfc" + str(rfc_num) + ".txt"
    filename = "".join(filename.split())
    filename = "rfc\\" + filename if platform.system == "Windows" else "rfc/" + filename
    if not os.path.exists(filename) == 0:
        file = open(filename)
        return ["P2P-CI/1.0 200 OK\n" \
                "Date: " + time.strftime("%a, %d %b %Y %X %Z", time.localtime()) + "\n" \
                "OS: " + str(platform.system()) + "\n" \
                "Last-Modified: " + time.ctime(os.path.getmtime(filename)) + "\n" \
                "Content-Length: " + str(os.path.getsize(filename)) + "\n" \
                "Content-Type: text/text \n",
                str(file.read())]
    else:
        return "P2P-CI/1.0 404 Not Found\n" \
               "Date:" + time.strftime("%a, %d %b %Y %X %Z", time.localtime()) + "\n" \
                "OS: " + str(platform.system()) + "\n"


def connect_peer():
    upload_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    upload_host = socket.gethostname()
    upload_socket.bind((upload_host, upload_client_port))
    upload_socket.listen(10)
    while True:
        conn, ip = upload_socket.accept()
        data = conn.recv(1024).decode('utf-8')
        rfc_no = data[data.index('C') + 1: data.index('P') - 1]
        conn.send(pickle.dumps(connection_reply(rfc_no)))
        conn.close()


if __name__ == "__main__":
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # serverHost address depend on the system which is hosting the server, So may have to change every time
    serverHost = '192.168.56.1' #'192.168.0.20' #'10.155.55.187'
    serverPort = 7734
    clientSocket.connect((serverHost, serverPort))
    upload_client_port = 8000 + random.randint(1, 100)
    client_rfc_list = []
    peer_keys = ['RFC_Number', 'RFC_Title']
    RFC_Number = [number[number.find("c") + 1: number.find(".")] for number in os.listdir(os.getcwd() + "/rfc") if 'rfc' in number]
    RFC_Title = [number[0: number.find(".")] for number in os.listdir(os.getcwd() + "/rfc") if 'rfc' in number]
    connection_message = ""
    for number, title in zip(RFC_Number, RFC_Title):
        client_rfc_list.insert(0, dict(zip(peer_keys,[number, title])))
        connection_message += add_rfc(number, title)
    clientSocket.send(
        pickle.dumps([connection_message, client_rfc_list, clientSocket.getsockname()[0], upload_client_port]))
    print(clientSocket.recv(1024).decode('utf-8'))

    start_new_thread(connect_peer, ())
    while True:
        try:
            method = input("Enter a method from: get, add, lookup, list, exit\n")
            if method == 'exit':
                clientSocket.send(pickle.dumps("exit"))
                clientSocket.close()
                break
            elif method == 'get':
                rfc_num, rfc_ttl = get_rfc_num_ttl()
                get_rfc(rfc_num, rfc_ttl)
            elif method == 'add':
                rfc_num, rfc_ttl = get_rfc_num_ttl()
                temp_rfc_list = [rfc_num, rfc_ttl]
                connection_msg = add_rfc(rfc_num, rfc_ttl)
                if len(connection_msg) > 0:
                    clientSocket.send(
                        pickle.dumps([connection_msg, temp_rfc_list, clientSocket.getsockname()[0], upload_client_port]))
                    print(clientSocket.recv(1024).decode('utf-8'))
                else:
                    print("either {0} or {1} does not exist".format(rfc_num, rfc_ttl))
            elif method == 'lookup':
                rfc_num, rfc_ttl = get_rfc_num_ttl()
                # print(rfc_num, rfc_ttl)
                lookup_rfc(rfc_num, rfc_ttl)
            elif method == 'list':
                list_rfc()
            else:
                print("Please enter correct input.\n")
        except Exception as e:
            print(e)
            print("exited due to some exception.")
            clientSocket.send(pickle.dumps("exit"))
            clientSocket.close()
            break
