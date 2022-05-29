# OnlineLearningService

## Installation
1. clone repo:`git clone https://github.com/AshuraWang/OnlineLearningService.git`
2. install mysql server:`sudo apt-get install mysql-server`
3. if run code locally, install requirement: `pip3 install -r /requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`




## Start Service
### Run code locally
1. start mysql server: `service mysql start`
2. `cd web_server`
3. start web service: `python manage.py runserver 127.0.0.1:8000`
### Use docker
1. build docker: `sh build_docker.sh`
2. run docker: 'sh run.sh'
## Route

|  route   | method  | purpose | example |
|  ----  | ----  | ---- |---- |
| /metadata |GET  | return available models |  `curl http://127.0.0.1:8000/metadata`  |
| /train | POST  | retrain model |  `curl http://127.0.0.1:8000/train -H "Content-Type:application/json"  -d '@./data_utils/new_labeled_data_small.json'`  |
| /predict |POST  | make predictions with 2 latest models in parallel |  `curl -d image_url=$cdn_url http://127.0.0.1:8000/predict` or visit http://127.0.0.1:8000/predict and upload local image |
| /history | POST&GET | return all prediction results |  `curl http://127.0.0.1:8000/history -d nohtml=1` or visit http://127.0.0.1:8000/history |

## Test Data
Test data are uploaded to TencentCloud COS.

List of cdn url is saved in `data_utils`, NG data in `ok.csv` and NG data in `ng.csv`.

Use `python data_utils/generate_labeled_data.py` to generate and simulate new labeled data. Generated data will be saved in `data_utils/new_labeled_data_small.json`.

Here is a cdn url for predict test: `https://online-learning-1312206701.cos.ap-nanjing.myqcloud.com/NG/03.jpg`

