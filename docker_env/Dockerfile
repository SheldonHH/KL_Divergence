FROM python
RUN pip3 install matplotlib
RUN pip3 install scipy
RUN pip3 install pandas
RUN pip3 install sidetable
RUN pip3 install lmfit
RUN pip3 install sklearn
RUN pip3 install pypng
RUN pip3 install torch
RUN pip3 install torchvision
RUN pip3 install imageio
RUN cd /root && wget https://go.dev/dl/go1.18.2.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.18.2.linux-amd64.tar.gz
RUN echo "export PATH=$PATH:/usr/local/go/bin" >> /etc/profile
RUN apt-get update
RUN apt-get install python3-opencv
RUN apt-get install tmux -y
# RUN source /etc/profile