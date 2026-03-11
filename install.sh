#!/bin/bash

echo -e "\033[31m ready download please wait ...  \033[0m"
pip install urllib3
pip install requests
pip install dnspython
pip install beautifulsoup4
echo -e "\033[31m done ! \033[0m"
clear
python3 .full_alone.py