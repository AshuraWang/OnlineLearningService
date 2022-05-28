import csv
import json

def generate_data(save_path='./new_labeled_data_small.json', limit=10):
    ok_list, ng_list = [], []
    with open('./ok.csv', 'r') as f:
        reader = csv.reader(f)
        reader.__next__()
        count = 0
        for row in reader:
            imgname, imgurl = row
            imgurl = imgurl.split('?')[0]
            ok_list.append(imgurl)
            count += 1
            if count > limit:
                break

    with open('./ng.csv', 'r') as f:
        reader = csv.reader(f)
        reader.__next__()
        count = 0
        for row in reader:
            imgname, imgurl = row
            imgurl = imgurl.split('?')[0]
            ng_list.append(imgurl)
            count += 1
            if count > limit:
                break
    data = {
        'data':{
            'ok':ok_list,
            'ng':ng_list
        }
    }
    with open(save_path, 'w') as f:
        json.dump(data, f)



if __name__ == '__main__':
    generate_data()