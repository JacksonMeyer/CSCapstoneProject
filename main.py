from kivy.app import App            #base class for whole project(app)
from kivy.lang import Builder       #reference main.kv file
from kivy.uix.screenmanager import Screen #homescreen inherits from this package
from kivy.uix.button import ButtonBehavior #references features for a button
from kivy.uix.image  import Image       #references features for a button to an image
from kivy.uix.camera import Camera
from fer import FER
from PIL import Image as ImageConv
import matplotlib.pyplot as plt
import Playlist
import webbrowser

class StartScreen(Screen):          # main screen class
    pass                            #everything will be defined in startscreen kv file

class PhotoScreen(Screen):           # homescreen class
    pass

class SettingsScreen(Screen):       #settings class
    pass                            #everything will be defined in settingsscreen kv file

class PlaylistScreen(Screen):       #playlistscreen class
    pass                            #everything will be defined in playlistscreen kv file

class ButtonImage(ButtonBehavior, Image):
    pass


GUI = Builder.load_file("main.kv")      #refernces the file that was called

class MainApp(App):                     #main class
    def build(self):                    #overriding build method
        self.camera_obj = Camera()
        self.plGen = Playlist.playlistGen()
        return GUI                      #returns user interface


    def change_screen(self, screen_name):                   #changes screen in app
        screen_manager = self.root.ids['screen_manager']    #gets widget you want
        screen_manager.current = screen_name                #current screen on app

    def take_pic(self,*args):
        self.camera_obj.export_to_png("./selfie.png")
        im1 = ImageConv.open(r'C:\Users\Jackson Meyer\PycharmProjects\pythonProject\selfie.png')
        im2 = im1.convert('RGB')
        im2.save(r'C:\Users\Jackson Meyer\PycharmProjects\pythonProject\selfie1.jpg')
        self.get_mood()
    def get_mood(self, *args):
        img = plt.imread("selfie1.jpg")
        detector = FER(mtcnn=True)
        valence = self.get_valence(detector,img)
        energy = self.get_energy(detector,img)
        print(detector.detect_emotions(img))
        print(valence,energy)
        self.create_playlist(valence,energy)

    def get_valence(self, detector, img):
        x = detector.detect_emotions(img)
        dict = x[0]
        happy = dict["emotions"]["happy"] * 100
        angry = dict["emotions"]["angry"] * 100
        disgust = dict["emotions"]["disgust"] * 100
        fear = dict["emotions"]["fear"] * 100
        sad = dict["emotions"]["sad"] * 100
        surprise = dict["emotions"]["surprise"] * 100
        neutral = dict["emotions"]["neutral"] * 100

        valence = ((happy*1) + (angry*.1) + (disgust*.2) + (fear*.3) + (sad * 0) + (surprise * .7) + (neutral *.5))
        valence = valence / 100
        return valence

    def get_energy(self,detector,img):
        x = detector.detect_emotions(img)
        dict = x[0]
        happy = dict["emotions"]["happy"] * 100
        angry = dict["emotions"]["angry"] * 100
        disgust = dict["emotions"]["disgust"] * 100
        fear = dict["emotions"]["fear"] * 100
        sad = dict["emotions"]["sad"] * 100
        surprise = dict["emotions"]["surprise"] * 100
        neutral = dict["emotions"]["neutral"] * 100

        energy = ((happy*.9) + (angry*1) + (disgust*.2) + (fear*.25) + (sad*.1) + (surprise*.75) + (neutral * .5))
        energy = energy / 100
        return energy

    def create_playlist(self,valence,energy):


        tracks = self.plGen.gen_recs([valence, energy])
        pl = self.plGen.gen_playlist(tracks)
        print(self.plGen.str_playlist(pl))
        self.plGen.genre_list()

        # to save a playlist to user's spotify account
        self.plGen.save_playlist(tracks)

    def login(self):
        self.plGen.force_login()

    def github_about(self):
        webbrowser.open("https://github.com/manleydrake/capstone-project-team-15-gme")





MainApp().run()                    #starts the app