from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from fer import FER
from PIL import Image
import matplotlib.pyplot as plt

class SelfieCameraApp(App):

    def build(self):
        self.camera_obj = Camera()
        self.camera_obj.resolution = (640,480)


        button_obj = Button(text="Click here")
        button_obj.size_hint = (.5, .2)
        button_obj.pos_hint = {'x': .25, 'y': .25}
        button_obj.bind(on_press = self.take_pic)

        layout = BoxLayout()
        layout.add_widget(self.camera_obj)
        layout.add_widget(button_obj)
        return layout

    def take_pic(self,*args):
        print("I am taking a selfie")
        self.camera_obj.export_to_png("./selfie.png")
        im1 = Image.open(r'C:\Users\Jackson Meyer\PycharmProjects\pythonProject\selfie.png')
        im2 = im1.convert('RGB')
        im2.save(r'C:\Users\Jackson Meyer\PycharmProjects\pythonProject\selfie1.jpg')
        self.get_mood()

    def get_mood(self, *args):
        img = plt.imread("selfie1.jpg")
        detector = FER(mtcnn=True)
        print(detector.detect_emotions(img))


if __name__ == '__main__':
    SelfieCameraApp().run()