#service mysql start
CURPATH=$(pwd)
sudo docker run -it -v /home/wxu/Code/OnlineLearningService/checkpoint:/checkpoint -v $CURPATH/data_cache:/data_cache  --net="host" online_learning_service:v_0.1 python3 manage.py runserver 127.0.0.1:8000
