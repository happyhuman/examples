FROM tensorflow/tensorflow:1.12.0

RUN pip install idx2numpy h5py

ADD train.py /opt/train.py

ENTRYPOINT ["/usr/bin/python", "/opt/train.py"]