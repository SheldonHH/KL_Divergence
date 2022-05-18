docker run -itd -v /Users/mac/FedBFT/KL_Divergence:/root python /bin/bash
docker exec -it $(docker ps | grep -E 'python' | awk '{print $1}') /bin/bash

pip3 install matplotlib
pip3 install scipy