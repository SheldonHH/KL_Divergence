docker build -t sheldonhh/python:v1 .
docker stop  $(docker ps -a | grep -E 'sheldonhh/python:v1' | awk '{print $1}' | awk 'NR==1') && docker rm  $(docker ps -a | grep -E 'python' | awk '{print $1}' | awk 'NR==1')
docker run -itd -v ~/KL_Divergence:/root/KL_Divergence sheldonhh/python:v1 /bin/bash
docker exec -it $(docker ps | grep -E 'sheldonhh/python:v1' | awk '{print $1}') /bin/bash
cd ~/KL_Divergence
# pip3 install matplotlib
# pip3 install scipy