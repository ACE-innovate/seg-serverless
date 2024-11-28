FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime

RUN apt-get update && apt-get install -y git libgl1 libglib2.0-0

RUN git clone  https://github.com/wildoctopus/huggingface-cloth-segmentation /seg

RUN pip install -r /seg/requirements.txt && pip install flask runpod requests

COPY ./cloth_segm.pth /seg/model/cloth_segm.pth 

COPY ./start.sh /start.sh

COPY ./server.py /seg/server.py

COPY ./handler.py /handler.py 

EXPOSE 8083

CMD ["bash", "-c", "/start.sh"]