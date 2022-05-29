import os
from PIL import Image
import uuid
from time import time

import torch
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

from torchvision.models.mobilenetv3 import mobilenet_v3_small
from torchvision.models.resnet import resnet18


class IPhoneValueClassifier:
    def __init__(self, arc='mobilenet_v3', epoch=1):
        self.arc = arc
        if self.arc == 'mobilenet_v3':
            self.model = mobilenet_v3_small(pretrained=False, num_classes=1)
        elif self.arc == 'resnet18':
            self.model = resnet18(pretrained=False, num_classes=1)
        self.data_transforms = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((224, 224)),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        # train config
        self.sigmoid = torch.nn.Sigmoid()
        self.criterion = torch.nn.BCELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters())
        self.epoch = epoch

    def switch_model(self, arc):
        self.arc = arc
        if self.arc == 'mobilenet_v3':
            self.model = mobilenet_v3_small(pretrained=False, num_classes=1)
        elif self.arc == 'resnet18':
            self.model = resnet18(pretrained=False, num_classes=1)
        else:
            return False
        self.optimizer = torch.optim.Adam(self.model.parameters())
        return True

    def predict(self, image, ckpt, threshold=0.5):
        self.model.load_state_dict(torch.load(ckpt))
        self.model.eval()
        # image = cv2.resize(image, [224,224]) # pad first might be better
        input_tensor = self.data_transforms(image).unsqueeze(0)
        start_time = time()
        output_tensor = self.sigmoid(self.model(input_tensor))
        end_time = time()
        output = output_tensor.data.cpu().numpy().squeeze()
        confidence = float(output)
        good = int(confidence > threshold)
        print(confidence)
        return round(confidence, 3), good, int((end_time-start_time)*1000)

    def train(self,
              dataroot='../data_cache/dataset',
              save_path='../checkpoint',
              batch_size=1):
        self.model.train()
        dataset = ImageFolder(dataroot, transform=self.data_transforms) # Image Aug might need
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        for e in range(self.epoch):
            for i, (x, t) in enumerate(dataloader):
                t = t.unsqueeze(1).float()
                y = self.model(x)
                y = self.sigmoid(y)
                loss = self.criterion(y, t)
                self.optimizer.zero_grad()
                loss.backward()
                print(f'epoch:{e}-{i}th data-loss:{loss.data.cpu().numpy()}')
                self.optimizer.step()
        model_name = f"{self.arc}_{str(uuid.uuid4())}.pth"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        torch.save(self.model.state_dict(), os.path.join(save_path, model_name))
        return os.path.join(save_path, model_name)

    def reset(self):
        self.epoch = 1
        self.arc = 'mobilenet_v3'


if __name__ == '__main__':
    classfier = IPhoneValueClassifier()
    image_path= '/home/wxu/Code/OnlineLearningService/data_cache/dataset/NG/92.jpg'
    # image = Image.open(image_path)
    # classfier.predict(image, '../checkpoint/mobilenet_v3_9ab2bc28-b0e1-49be-a57e-cb44079eaffe.pth')

    a = time()
    s = classfier.train()
    b = time()
    print(b-a, s)