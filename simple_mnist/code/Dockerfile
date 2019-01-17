FROM tensorflow/tensorflow:1.12.0

RUN pip install idx2numpy h5py

ADD model.py /opt/model.py

ENTRYPOINT ["/usr/bin/python", "/opt/model.py"]