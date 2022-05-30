FROM python
RUN pip3 install matplotlib
RUN pip3 install scipy
RUN pip3 install pandas
RUN pip3 install sidetable
RUN pip3 install lmfit
RUN pip3 install sklearn
RUN cd /root && wget https://go.dev/dl/go1.18.2.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.18.2.linux-amd64.tar.gz
RUN echo "export PATH=$PATH:/usr/local/go/bin" >> /etc/profile
# RUN source /etc/profile