import torch
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.utils.data import DataLoader,Dataset
import torchvision.utils
import numpy as np
import random
from PIL import Image
import torch
import PIL.ImageOps    
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from torch.autograd import Variable

#커스텀 데이터셋을 정의합시다.
class SiameseNetworkDataset(Dataset):
    def __init__(self,imageFolderDataset,transform=None,should_invert=True):
        self.imageFolderDataset = imageFolderDataset    
        self.transform = transform
        self.should_invert = should_invert

    def __getitem__(self,index):
        img0_tuple = random.choice(self.imageFolderDataset.imgs)
        #we need to make sure approx 50% of images are in the same class
        should_get_same_class = random.randint(0,1) 

        if should_get_same_class:
            while True:
                #keep looping till the same class image is found
                img1_tuple = random.choice(self.imageFolderDataset.imgs) 
                if img0_tuple[1]==img1_tuple[1]:
                    break
        else:
            while True:
              #keep looping till a different class image is found
                img1_tuple = random.choice(self.imageFolderDataset.imgs) 
                if img0_tuple[1] !=img1_tuple[1]:
                    break


        img0 = Image.open(img0_tuple[0])
        img1 = Image.open(img1_tuple[0])
        img0 = img0.convert("L")
        img1 = img1.convert("L")      

        if self.should_invert:
            img0 = PIL.ImageOps.invert(img0)
            img1 = PIL.ImageOps.invert(img1)

        if self.transform is not None:
            img0 = self.transform(img0)
            img1 = self.transform(img1)

        return img0, img1 , torch.from_numpy(np.array([int(img1_tuple[1]!=img0_tuple[1])],dtype=np.float32))

    def __len__(self):
        return len(self.imageFolderDataset.imgs)



#컨볼루션 계층을 정의합니다.
class SiameseNetwork(nn.Module):
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.cnn1 = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(1, 4, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(4),

            nn.ReflectionPad2d(1),
            nn.Conv2d(4, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),

            nn.ReflectionPad2d(1),
            nn.Conv2d(8, 8, kernel_size=3),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(8),
       )

        self.fc1 = nn.Sequential(
            nn.Linear(8*100*100, 500),
            nn.ReLU(inplace=True),

            nn.Linear(500, 500),
            nn.ReLU(inplace=True),

            nn.Linear(500, 5))

    def forward_once(self, x):
        output = self.cnn1(x)
        output = output.view(output.size()[0], -1)
        output = self.fc1(output)
        return output

    def forward(self, input1, input2):
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)
        return output1, output2

#Loss 함수를 정의합니다.
class ContrastiveLoss(torch.nn.Module):
    def __init__(self, margin=2.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, output1, output2, label):
        euclidean_distance = F.pairwise_distance(output1, output2, keepdim = True)
        loss_contrastive = torch.mean((1-label) * torch.pow(euclidean_distance, 2) +
                                      (label) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))
        return loss_contrastive


# 본격적으로 트레인을 시켜보도록 합시다.
#앞서서 진행했던 실습처럼 옵티마이저와 에포크등을 설정합니다.
def train():
    #앞서서 정의한 사용자 데이터셋을 불러옵시다.
    folder_dataset = dset.ImageFolder(root="train")
    siamese_dataset = SiameseNetworkDataset(imageFolderDataset=folder_dataset,
                                            transform=transforms.Compose([transforms.Resize((100,100)),
                                                                        transforms.ToTensor()
                                                                        ])
                                        ,should_invert=False)
    train_dataloader = DataLoader(siamese_dataset, shuffle=True, num_workers=8, batch_size=64)
    net = SiameseNetwork().cuda()
    criterion = ContrastiveLoss()
    optimizer = optim.Adam(net.parameters(),lr = 0.0005 )
    counter = []
    loss_history = [] 
    iteration_number= 0
    for epoch in range(0,10):
        for i, data in enumerate(train_dataloader,0):
            img0, img1 , label = data
            img0, img1 , label = img0.cuda(), img1.cuda() , label.cuda()
            optimizer.zero_grad()
            output1,output2 = net(img0,img1)
            loss_contrastive = criterion(output1,output2,label)
            loss_contrastive.backward()
            optimizer.step()
            if i %10 == 0 :
                print("Epoch {}\n Current loss {}\n".format(epoch,loss_contrastive.item()))
                iteration_number +=10
                counter.append(iteration_number)
                loss_history.append(loss_contrastive.item())
    torch.save(net.state_dict(), 'siamese.pt')


def test(name):
    # 실제 이미지와 테스트
    test = Image.open('test/' + name + '.png')
    test = test.convert("L")
    transform=transforms.Compose([transforms.Resize((100,100)), transforms.ToTensor()])
    test = transform(test)
    test = test.unsqueeze(0)

    siamese_dataset = SiameseNetworkDataset(imageFolderDataset=dset.ImageFolder(root="train"),
                                            transform=transforms.Compose([transforms.Resize((100,100)),
                                                                        transforms.ToTensor()
                                                                        ])
                                        ,should_invert=False)
    test_dataloader = DataLoader(siamese_dataset,num_workers=6,batch_size=1,shuffle=False)

    net = SiameseNetwork().cuda()
    net.load_state_dict(torch.load('siamese.pt'))
    net.eval()

    dataiter = iter(test_dataloader)
    x0,_,_ = next(dataiter)

    distance_history = [] 
    label = []

    for i in range(len(test_dataloader)-1):

        path = test_dataloader.dataset.imageFolderDataset.imgs[i][0]

        data_label = path.split('/')[-2]

        _,x1,label2 = next(dataiter)

        output1,output2 = net(Variable(test).cuda(),Variable(x1).cuda())

        euclidean_distance = F.pairwise_distance(output1, output2)

        distance_history.append(euclidean_distance.item())
        label.append(data_label)

    # print('Dissimilarity:', distance_history, label)
    print(label[distance_history.index(min(distance_history))])

    return label[distance_history.index(min(distance_history))]