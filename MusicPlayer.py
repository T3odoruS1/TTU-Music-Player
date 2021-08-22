from tkinter import *
import pygame
import os
##from mutagen.mp3 import MP3
import random


root = Tk()


class MusicPlayer:

    def __init__(self, root):
        self.root = root
        self.root.title("TTU PYTHON MUUSIKA")
        self.root.geometry("900x600")
        pygame.init()
        pygame.mixer.init()
        self.track = StringVar()
        self.paused = True
        self.volume = DoubleVar()
        self.volume.set(1.0)
        self.current_time = IntVar()
        self.current_time.set(0)
        self.trackindex = 0
        self.shuffle = False
        self.prev_track = 0

        self.next_button_img = PhotoImage(file="img/nextbuttonimg.png")
        self.play_button_image = PhotoImage(file="img/playbutton.png")
        self.prev_button_img = PhotoImage(file="img/prevbuttonimg.png")
        self.fireplace_img = PhotoImage(file="img/fireplace.gif")
        self.shuffle_img = PhotoImage(file="img/shuffle.png")
        # ОКНО НАЗВАНИЯ
        song_info_frame = LabelFrame(self.root, text="TTU PYTHON MUUSIKA", font=("Free Mono", 17, "bold"), bg='Gray20',
                                     fg='gray70', bd=1)
        song_info_frame.place(x=0, y=0, relwidth=0.6, relheight=0.8)
        self.song_name = Label(song_info_frame, text=self.track.get(), bg="Gray20", fg="gray70",
                          font=("comicsans", 14, "italic"), bd=2)
        fireplace = Label(song_info_frame, image = self.fireplace_img,bg="gray70")
        fireplace.place(relx = 0.17 , rely = 0.03)
        self.song_name.place(relx=0.05, rely=0.85, height=50, width=400)
        button_frame = LabelFrame(self.root, bd=1, bg="Gray20")
        button_frame.place(relx=0, rely=0.8, relwidth=0.6, relheight=0.2)

        self.end_label = Label(song_info_frame, text="0:0", bg="Gray20", fg="gray70",
                            font=("comicsans", 14, "italic"))
        self.end_label.place(relx=0.80, rely=0.9)

        # КНОПКИ ПРОИГРЫВАНИЕ
        # play_button = Button(button_frame, text = "Alusta", command=self.playsong, borderwidth=0)
        # play_button.place(relx=0.7, rely=0.6)
        pause_button = Button(button_frame, image = self.play_button_image, font=("comicsans", 14, "bold"), command=self.pausesong,borderwidth=0,bg = "gray20")
        pause_button.place(relx=0.42, rely=0.10)
        next_button = Button(button_frame, image = self.next_button_img ,command = self.next_song,borderwidth=0,bg = "gray20")
        next_button.place(relx=0.6, rely=0.1)
        prev_button = Button(button_frame, image = self.prev_button_img ,command=self.prev_song,borderwidth=0,bg = "gray20")
        prev_button.place(relx=0.21, rely=0.1)
        self.shuffle_button = Button(button_frame,image = self.shuffle_img,command=self.toggle_shuffle,borderwidth=0,bg = "gray20")
        self.shuffle_button.place(relx=0.1,rely=0.6)

        # СЛАЙДЕРЫ
        self.volume_slider = Scale(button_frame, orient="horizontal", showvalue=0, variable=self.volume, from_=0.0, to=1.0, resolution=0.01, command=self.set_volume)
        self.volume_slider.place(relx=0.27, rely=0.75, relwidth=0.4, height=20)

        # ОКНО ПЛЕЙЛИСТА
        playlist_frame = LabelFrame(self.root, text="LAULUD", bg="Gray20", fg="gray70",
                                    font=("comicsans", 14, "italic"), bd=2)
        playlist_frame.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)
        scrol_y = Scrollbar(playlist_frame, orient=VERTICAL,)
        scrol_y.pack(side=RIGHT, fill=Y)
        self.playlist_list = Listbox(playlist_frame, font=("comicsans", 11),bg='gray40')
        self.playlist_list.bind('<Double-1>', self.play_on_double_click)
        self.playlist_list.place(relx=0.05, rely=0, relwidth=0.9, relheight=0.95)
        scrol_y.config(command=self.playlist_list.yview)

        # ДОБЫЧА ПЕСЕН ИЗ ПАПКИ
        os.chdir("MusicFolder")
        song_list = os.listdir()
        self.playlist_lengh = 0
        for song in song_list:
            self.playlist_list.insert(END, song)
            self.playlist_lengh += 1


    def toggle_shuffle(self):
        if not self.shuffle:
            self.shuffle = True
            self.shuffle_button.configure(bg="orangered2")
        elif self.shuffle:
            self.shuffle = False
            self.shuffle_button.configure(bg="gray20")


    def initiate_sound(self):
        self.track.set(self.playlist_list.get(self.trackindex))
        pygame.mixer.music.load(self.playlist_list.get(self.trackindex))
        pygame.mixer.music.play()
        self.paused = False
        ##audio = MP3(self.playlist_list.get(self.trackindex))
        ##self.total_lengh = audio.info.length
        ##mins, secs = divmod(self.total_lengh, 60)
        ##mins = round(mins)
        ##secs = round(secs)
        ##timeformat = "{:02d}:{:02d}".format(mins, secs)
        ##self.end_label.configure(text=timeformat)
        ##self.song_name.configure(text=self.playlist_list.get(self.trackindex))



    def play_on_double_click(self, event):
        self.trackindex = self.playlist_list.index(ACTIVE)
        self.initiate_sound()


    def set_volume(self, event):
        pygame.mixer.music.set_volume(self.volume.get())

    def next_song(self):
        if not self.shuffle:
            if self.playlist_lengh  > self.trackindex:
                self.prev_track = self.trackindex
                self.trackindex += 1
                self.playlist_list.activate(self.trackindex)
                self.initiate_sound()
        else:
            self.prev_track = self.trackindex
            self.trackindex = random.randint(0, self.playlist_lengh - 1)
            for i in range(3):
                if self.prev_track == self.trackindex:
                    self.trackindex = random.randint(0, self.playlist_lengh - 1)
            print(self.trackindex)
            self.playlist_list.activate(self.trackindex)
            self.initiate_sound()

    def prev_song(self):
        if not self.shuffle:
            if self.trackindex > 0:
                self.prev_track = self.trackindex
                self.trackindex -= 1
                self.playlist_list.activate(self.trackindex)
                self.initiate_sound()
        else:
            self.prev_track = self.trackindex
            self.trackindex = random.randint(0, self.playlist_lengh-1)
            for i in range(3):
                if self.prev_track == self.trackindex:
                    self.trackindex = random.randint(0, self.playlist_lengh - 1)
            self.playlist_list.activate(self.trackindex)
            self.initiate_sound()

    def pausesong(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
        elif self.paused:
            pygame.mixer.music.unpause()
            self.paused = False


MusicPlayer(root)
root.mainloop()
