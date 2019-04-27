
**Team**
1. Abhishek Arya(aarya) - 200206728
2. Sai Kiran Mayee Maddi(smaddi) - 200257327

**Instructions on how to compile and run**  
This application is created and tested using Python3. So it is recommended to use Python3 to run the application.
First run Server for clients to connect with server.

Following are the steps to run the application -   

***1. Enable connection ports: -***
1. Port 7734 is selected for Server. 
2. Port 8001 is selected for Client.
3. Enable both the port on respective machines which are running Server and Client.
4. For Linux - 
    1. Server machine:- 
        1. sudo apt-get install ufw  
        2. sudo ufw allow 7734
        3. sudo ufw disable
    2. Client machine:-  
        1. sudo apt-get install ufw
        2. sudo ufw allow 8001  
        3. sudo ufw disable 

***2. For Server:-***  
1. Run Server file Server.py using the following command:
        python Server.py(if only python 3 is installed in your system)
        python3 Server.py (if multiple version of python is installed)  

***3. For Client:-***  
1. It is required to provide the Server IP to "serverHost" variable in main method to connect with server.  
2. Run Client file Client.py using the following command:
        python Client.py(if only python 3 is installed in your system)
        python3 Client.py (if multiple version of python is installed)
3. When Client is up and running, provide name of command as per the Description provided on screen that you wish to executed.  

***4. Initial Setup for RFC files: -***  
1. RFC files should be created in rfc folder at the location of the running script.  
2. Name for RFC file should be in rfc +" rfc file number" + .txt format. For example - rfc35.txt
3. Here RFC file name will be the title of the RFC file and the number will be RFC number.  
        for Example: - rfc35.txt -> here rfc35 is RFC file title and 35 is RFC number.  
