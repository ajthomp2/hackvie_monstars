from sklearn.neural_network import MLPClassifier
import numpy as np

if __name__ == "__main__":
    import os
    # assumes files only located in word directories
    X, Y = [], []
    num_to_word = {"voices":0,"destiny":1,"danger":2}
    for folder, subdirList, fileList in os.walk("./data/raw"):
        word = folder.split('/')[-1]
        print(word, fileList)
        for f in fileList:
            src = folder + '/' + f
            print(num_to_word[word])
            X.append(np.load(src))
            Y.append(num_to_word[word])

N = len(X)
X, Y = np.array(X), np.array(Y)
# X_train, Y_train = X[:int(.8*N)], Y[:int(.8*N)]
# X_test, Y_test = X[int(.8*N):], Y[int(.8*N):]
X_train, Y_train = X, Y
X_test, Y_test = X, Y


print(X_train.shape)
print(Y_train.shape)
print(X_train)
print(Y_train)

nn = MLPClassifier(hidden_layer_sizes=(1500, 500))
nn.fit(X_train, Y_train)

print(nn.score(X_test, Y_test))

for folder, subdirList, fileList in os.walk("./data/raw"):
    word = folder.split('/')[-1]
    print(word, fileList)
    for f in fileList:
        src = folder + '/' + f
        y = nn.predict(np.load(src))
        print(num_to_word[word])
