docker build -t sheldonhh/python_golang:v1 .
docker stop  $(docker ps -a | grep -E 'sheldonhh/python:v1' | awk '{print $1}' | awk 'NR==1') && docker rm  $(docker ps -a | grep -E 'python' | awk '{print $1}' | awk 'NR==1')
docker stop  $(docker ps -a | grep -E 'sheldonhh/python_golang:v1' | awk '{print $1}' | awk 'NR==1') && docker rm  $(docker ps -a | grep -E 'python_golang' | awk '{print $1}' | awk 'NR==1')
docker run -itd -v /Users/mac/FedBFT/KL_Divergence:/root/KL_Divergence sheldonhh/python_golang:v1 /bin/bash
docker exec -it $(docker ps | grep -E 'sheldonhh/python_golang:v1' | awk '{print $1}') /bin/bash
cd ~/KL_Divergence
export PATH=$PATH:/usr/local/go/bin
echo "export PATH=$PATH:/usr/local/go/bin" >>  /etc/profile
source /etc/profile
# pip3 install matplotlib
# pip3 install scipy