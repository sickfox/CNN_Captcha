from PIL import Image
import numpy as np

if __name__ == '__main__':
    #轉換csv to npy
    label=np.genfromtxt('label.csv',delimiter=',')
    print (label)
    np.save(r'y_train.npy', label)
    #轉換jpg to npy
    image = []
    for i  in range(6400):
        img = Image.open(str(i)+'.jpg').convert("L")
        image.append(np.asarray(img))
    #print (data)
    np.save(r'x_train.npy', image)
