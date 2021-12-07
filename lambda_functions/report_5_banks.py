#Download base image ubuntu 16.04
FROM amazon/aws-lambda-python:3.9
WORKDIR /home/ubuntu
RUN yum clean all
RUN yum update -y && yum install -y make curl wget sudo git gcc-c++ libgl1 libgl1-mesa-glx mesa-libGL ffmpeg libsm6 libxext6
RUN pip3 install tqdm pandas gensim glob2 requests joblib zipfile38 boto3 requests zipfile38 openpyxl --target "${LAMBDA_TASK_ROOT}"


WORKDIR "${LAMBDA_TASK_ROOT}"
RUN git clone https://github.com/assansanogo/b_s_processor.git
RUN ls "${LAMBDA_TASK_ROOT}"/b_s_processor/lambda_functions
RUN cp "${LAMBDA_TASK_ROOT}"/b_s_processor/lambda_functions/report_5_banks.py  "${LAMBDA_TASK_ROOT}"
RUN ls "${LAMBDA_TASK_ROOT}"

CMD ["report_5_banks.liberta_leasing_convert_handler"]
