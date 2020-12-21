# pytorch
import torch
# 최적화 알고리즘 : SGD
import torch.optim as optim


# For reproducibility
torch.manual_seed(1)

# 임의 데이터 생성
# x data 의 경우 1시간 공부하고 2번 수업 참석 -> y data 인덱스에 대응하여 0 ( 불합격 )
#이라는 데이터가 주어지는 것.
x_data = [[1, 2], [2, 3], [3, 1], [4, 3], [5, 3], [6, 2]]
y_data = [[0], [0], [0], [1], [1], [1]]


x_train = torch.FloatTensor(x_data)
y_train = torch.FloatTensor(y_data)

print(x_data)
print(x_train)

print(x_train.shape)
print(y_train.shape)

W = torch.ones((2, 1), requires_grad=True)

print(W)
#변수를 초기화 하는 것.



# 모델 초기화
# 입력데이터 (x) ==> 2 => 차원이 두개이기 때문에  2 by 1
# 출력 (Y) ==> 0 / 1 => 결과 값의 데이터는 0 과 1 가지 1 by 1 이기 때문에
# Matrix Product 를 실시하면 2 by 1 x 1 by 1 으로 2 by 1 이라는 데이터가 나오게 됨.
W = torch.zeros((2, 1), requires_grad=True) # W 의 데이터는 2 by 1 이라고 할 수 있음.
#Torch.zeros 해당 매트릭스를 0( zero ) 로 초기화 한다는 것.
b = torch.zeros(1, requires_grad=True)

# optimizer 설정
optimizer = optim.SGD([W, b], lr=1)

nb_epochs = 10000
for epoch in range(nb_epochs + 1):

    # Cost 계산
    hypothesis = torch.sigmoid(x_train.matmul(W) + b) # or .mm or @
    cost = -(y_train * torch.log(hypothesis) +
             (1 - y_train) * torch.log(1 - hypothesis)).mean()

    # cost로 H(x) 개선
    optimizer.zero_grad()
    cost.backward()
    optimizer.step()

    # 100번마다 로그 출력
    if epoch % 100 == 0:
        print('Epoch {:4d}/{} Cost: {:.6f}'.format(
            epoch, nb_epochs, cost.item()
        ))


hypothesis = torch.sigmoid(x_train.matmul(W) + b)
#print(hypothesis[:5])

prediction = hypothesis >= torch.FloatTensor([0.5])
#print(prediction[:5])

#print(prediction[:5])
#print(y_train[:5])

correct_prediction = prediction.float() == y_train
print(correct_prediction[:5])

accuracy = correct_prediction.sum().item() / len(correct_prediction)
print('The model has an accuracy of {:2.2f}% for the training set.'.format(accuracy * 100))

test = [[4,5]]
test_data=torch.FloatTensor(test)

hypothesis = torch.sigmoid(test_data.matmul(W) + b) # or .mm or @
prediction = hypothesis >= torch.FloatTensor([0.5])


if(prediction == 1 ):
    print("부정행위가 감지되었습니다.")



