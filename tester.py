from fer import FER

import matplotlib.pyplot as plt


img = plt.imread("selfie1.jpg")
detector = FER(mtcnn=True)

x = detector.detect_emotions(img)
dict = x[0]
happy = dict["emotions"]["happy"] * 100
angry = dict["emotions"]["angry"] * 100
disgust = dict["emotions"]["disgust"] * 100
fear = dict["emotions"]["fear"] * 100
sad = dict["emotions"]["sad"] * 100
surprise = dict["emotions"]["surprise"] * 100
neutral = dict["emotions"]["neutral"] * 100
print(happy,angry,disgust,fear,sad,surprise,neutral)
valence = ((happy*1) + (angry*.1) + (disgust*.25) + (fear*.25) + (sad * 0) + (surprise * .75) + (neutral *.5))
print(valence/100)

