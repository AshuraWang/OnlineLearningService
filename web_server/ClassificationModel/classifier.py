import os.path
import cv2
import torch
from torchvision.models.mobilenetv3 import mobilenet_v3_small
from torchvision.models.resnet import resnet18
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from time import time
import uuid


class IPhoneValueClassifier:
    def __init__(self, arc='mobilenet_v3'):
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
        self.sigmoid = torch.nn.Sigmoid()
        self.criterion = torch.nn.BCELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters())

    def predict(self, image, ckpt, threshold=0.5):
        self.model.load_state_dict(torch.load(ckpt))
        self.model.eval()
        # image = cv2.resize(image, [224,224]) # pad first might be better
        input_tensor = self.data_transforms(image).unsqueeze(0)
        start_time = time()
        output_tensor = self.sigmoid(self.model(input_tensor))
        end_time = time()
        output = output_tensor.data.cpu().numpy().squeeze()
        confidence = output
        good = int(confidence > threshold)
        print(confidence)
        return confidence, good, int((end_time-start_time)*1000)

    def train(self,
              dataroot='../data_cache/dataset',
              save_path='../checkpoint',
              epoch=100,
              batch_size=4):
        self.model.train()
        dataset = ImageFolder(dataroot, transform=self.data_transforms) # Image Aug might need
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        for e in range(epoch):
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
        torch.save(self.model.state_dict(), os.path.join(save_path, model_name))
        return os.path.join(save_path, model_name)


if __name__ == '__main__':
    classfier = IPhoneValueClassifier("resnet18")
    image = '/media/wxu/My Passport/DownloadForHsm/Machine Learning HW - SW v3/Machine Learning HW - SW v3/dataset/NG/03.jpg'
    image = cv2.imread(image)
    # classfier.predict(image)
    classfier.train()
    # classfier.predict(image, './checkpoint/mobilenet_v3_9ab2bc28-b0e1-49be-a57e-cb44079eaffe.pth')