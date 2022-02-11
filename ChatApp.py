from email import message
import sqlite3
import kivy
from kivymd.app import MDApp 
from kivy.lang import Builder, builder 
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import BooleanProperty, DictProperty, ListProperty, NumericProperty, ObjectProperty, OptionProperty, StringProperty
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.list import *
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivymd.uix.menu import *
from kivymd.uix.button import *
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
#from picker import MDThemePicker
#import Local_Database
from sqlite3 import *
from functools import partial
from importlib import reload
from kivymd.uix.menu import MDDropdownMenu
from kv import *
import os
import time
import re #re = regular expressions aka regex used to find patterns in text
from kivy.clock import Clock
import datetime
from collections import OrderedDict
import gc
from kivy.animation import Animation


connection = sqlite3.connect('friend_list.db')
cursor = connection.cursor() 





Window.size=(320,600)
Builder.load_file('kv/Message.kv')
class Chat_List(Screen):
    pass
class Account(Screen):
    pass
class Chat_List(Screen):
    pass
class Request(Screen):
    pass
class Chat_Screen(Screen):
    text = StringProperty()
    image = ObjectProperty()
    active = BooleanProperty(defaultvalue=False)

class Add_Friend(Screen):
    pass

class ChatBubble(MDBoxLayout):
    '''A chat bubble for the chat screen messages.'''

    profile = DictProperty()
    msg = StringProperty()
    time = StringProperty()
    sender = StringProperty()

class ChatApp(MDApp):
    dialog = None
    list_item = ObjectProperty     
    list_item = []                                        # every manually added friend is a list which will be contained within these brackets 
    connection = None
    cursor = None
    dropdown = ObjectProperty()

    #def __init__(self, **args):
        #dt = datetime
        #self.datetime = dt
        #super().__init__(**args)
    
    def build(self):
        GUI=Builder.load_file('Screens.kv')
        self.connection = sqlite3.connect('myapp.db')
        self.cursor = self.connection.cursor()
        #self.cursor.execute("""SELECT * FROM theme ;""")
        current_theme = self.cursor.fetchall()
        self.connection.commit()

        # print(current_theme)
        # [('Purple', 'BlueGray', 'Light')]
        
        if len(current_theme) == 0:
            self.theme_cls.primary_palette = 'BlueGray'
            self.theme_cls.accent_palette = "BlueGray"
            self.theme_cls.primary_hue = "500"
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.primary_palette = current_theme[0][0]
            self.theme_cls.accent_palette = current_theme[0][1]
            self.theme_cls.primary_hue = "500"
            self.theme_cls.theme_style = current_theme[0][2]
        
        
        return GUI

    def on_start(self):
        list_item = ObjectProperty
        list_item = [] 
        self.connection = sqlite3.connect('friend_list.db')
        self.cursor = self.connection.cursor() 
        #self.cursor.execute("""SELECT * FROM friend_list ;""")
        self.connection.row_factory = lambda cursor, row: row[0]
        #friends = self.connection.execute('SELECT name FROM friend_list').fetchall()
        friends = ["test","test 2"]
        for name in friends:
            print(name)
            button = OneLineAvatarIconListItem(text = name,on_press=lambda widget:self.change_screen("Chat_Screen"),on_release=self.create_chat)
            button.bind(on_release = self.recieve_message)
            self.root.ids["Chat_List"].ids["list"].add_widget(button)
            button.bind(on_press=self.press)
            list_item.append(name)

        
            if name not in list_item:
                a = list_item[-1]
                button = OneLineAvatarIconListItem(text = (a),on_press=lambda widget:self.change_screen("Chat_Screen"),on_release=self.create_chat)
                button.bind(on_press=self.press)
                button.bind(on_release = self.message_check_in_real_time)
                self.root.ids["Chat_List"].ids["list"].add_widget(button)
                button.bind(on_press=self.press)
                print(list_item)

        '''create notepad txt files'''
        #for name in friends:
            #file = open((name)+'.txt', "w")
            #list_item.append(name)
            #if name not in list_item:
                #last_item = list_item[-1]
                #file = open(last_item+'.txt',"w")
                


    def press(self, button):
        print("Called! ", button.text)
        self.root.ids['Chat_Screen'].ids['name'].text = button.text
        file = open(button.text+'.txt',"r")
        print(file.read())
        file.close()


    def delete(self , button):
        pass

    def change_screen(self,screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

    #def show_theme_picker(self):
        #theme_dialog = MDThemePicker()
        #theme_dialog.open()
    
    def print_theme(self):
        self.connection = sqlite3.connect('myapp.db')
        self.cursor = self.connection.cursor()        
        self.cursor.execute("""SELECT * FROM theme ;""")
        current_theme = self.cursor.fetchall()
        self.connection.commit()
    
        if len(current_theme) == 0:
            self.cursor.execute("""INSERT INTO theme (primary_palette, accent_palette, theme_style) VALUES (?, ?, ?);""", (self.theme_cls.primary_palette, self.theme_cls.accent_palette, self.theme_cls.theme_style))
            self.connection.commit()
        else:
            self.cursor.execute("""UPDATE theme SET primary_palette = ? , accent_palette = ? , theme_style = ? ;""", (self.theme_cls.primary_palette, self.theme_cls.accent_palette, self.theme_cls.theme_style))
            self.connection.commit()

    def comming_soon(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Yet not implimented :)"
            )
        self.dialog.open()
    
    def delete_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Are you sure you want to remove this contact ? , if you do then please restart your app as proceeding without restart may crash your app",
                buttons = [MDFlatButton(text = 'Cancel',on_press=self.close_dialog),MDFlatButton(text = 'Proceed',on_press=self.delete_contact)]
            )
        self.dialog.open()

    def create_chat(self, button):
        #self.clear()
        #self.root.ids['Chat_Screen'].ids['scroll'].remove_widget(self.msg)
        self.root.ids['Chat_Screen'].ids['name'].text = button.text
        rec = open("log_record.txt","a+")
        name = button.text+"\n"
        #self.root.ids['Chat_Screen'].ids['msglist'].scroll_to(message)
        self.msg = ChatBubble()
        self.root.ids['Chat_Screen'].ids['scroll'].remove_widget(self.msg)
        self.root.ids['Chat_Screen'].ids['scroll'].scroll_to(self.msg)
        with open(button.text+".txt") as file:
            chat_file = file.read()
        pattern = re.compile(r'(^you:|^client:)(.*?)(?: - \d\d\d\d-\d\d-\d\d )(.*?)(\d\d:\d\d)(.*?)(?::\d\d.\d\d\d\d\d\d -)(.*?)(?=(^you:|^client:|\Z))', re.S|re.M )
        groups = pattern.findall(chat_file)
        #print(groups)
        # printing time
        if rec.readlines() == [] or rec.readlines()!=[name]:
            overwrite = open("log_record.txt","w")
            overwrite.write(name)
            print("-"*70,"done")
        for chat in groups:
            #print(chat)
            self.msg = ChatBubble()
            k,l,m,n,o,p = chat[0:6]
            #print(k,n,p)
            if k  == 'you:':
                # handle the you: message
                self.msg = ChatBubble()
                #print(len(p),p) 
                if len(p) <= 5:
                    width = 50
                elif 5 < len(p) <=10 :
                    width = 70
                elif 10 < len(p) <=15:
                    width = 120
                elif 15 < len(p) <=20:
                    width = 150
                elif 20<len(p)<=25  :
                    width = 170
                elif len(p) > 20:
                    width = 200

                self.msg.ids["box"].pos_hint= {'right': 1}
                self.msg.ids["box"].width = width
                self.msg.ids["msg_content"].text = p
                self.msg.ids["timed"].text = n
                self.root.ids["Chat_Screen"].ids["msglist"].add_widget(self.msg)
                #self.msg.ids['box'].width = t
                #print(f'This is a "you" message: {m}')
            elif k   == 'client:':
                # handle the client message
                self.msg.ids["box"].pos_hint = {'left': 0}
                #print(len(p),p) 
                if len(p) <= 5:
                    width = 50
                elif 5 < len(p) <=10 :
                    width = 70
                elif 10 < len(p) <=15:
                    width = 120
                elif 15 < len(p) <=20:
                    width = 150
                elif 20<len(p)<=25:
                    width = 170
                elif len(p)>25:
                    width = 200
                self.msg.ids["box"].width = width
                self.msg.ids["msg_content"].text = p
                #self.msg.ids['box'].width = t
                self.msg.ids["timed"].text = n
                self.root.ids["Chat_Screen"].ids["msglist"].add_widget(self.msg)
                #print(f'This is a "client" message: {m}')
            else:
                pass
                #print('Error invalid data') 

    def clear(self):
        self.root.ids["Chat_Screen"].ids["scroll"].clear_widgets()
    

    def stop(self):                                     
        self.root.ids["Chat_Screen"].ids["msglist"].clear_widgets()
        #return ChatApp().run()


    def send_message(self,message):
        #print('working')
        file_text = self.root.ids['Chat_Screen'].ids['name'].text 
        file = open(file_text+'.txt',"a")
        #file.write('you: '+message+"\n")
        self.msg = ChatBubble()
        self.root.ids["Chat_Screen"].ids["msg"].text = ""
        self.msg.ids["box"].pos_hint= {'right': 1}
        self.msg.ids["msg_content"].text = message.strip("you:")
        p = message
        if len(p) <= 5:
            width = 70
        elif 5 < len(p) <=10 :
            width = 80
        elif 10 < len(p) <=15:
            width = 120
        elif 15 < len(p) <=20:
            width = 150
        elif 20<len(p)<=25:
            width = 170
        elif len(p)>25:
            width = 220
        print(message)
        self.msg.ids["box"].width = width + 40
        #self.msg.ids["box"].height = 100
        self.root.ids["Chat_Screen"].ids["msglist"].add_widget(self.msg)
        self.connection = sqlite3.connect('friend_list.db')
        cursor = self.connection.cursor()
        self.connection.row_factory = lambda cursor, row: row[0]
        #a = self.connection.execute("""SELECT id FROM friend_list WHERE name = (?)""",(file_text,)).fetchall()
        #a = a[0]
        #print(a[0])
        
        #uuid = db.child("messages").child("user").child(a).child("friends").child('LwjjwxpLWwVcLRXKbbZpjfLIVHB2').get()
        time = str(datetime.datetime.now())
        data = {'message' : message,"timestamp":time}
        file.write('you: '+'- '+ time +' - ' +message+"\n")
        file.close()
        time_pattern = re.compile(r'\d\d:\d\d',re.S|re.M)
        timepattern = time_pattern.findall(time)
        timepattern = timepattern[0]
        self.msg.ids["timed"].text = timepattern
        # here data is being push to user dynamically , please do automate this process before finalising ---> done
        #print(datetime.datetime.now())

    def recieve_message(self,message):

        name = self.root.ids['Chat_Screen'].ids['name'].text 
        print(name," aaaaa")
        file = open(name+'.txt',"a")
        log_write = open(name+" log"+".txt","a")
        log_read=open(name+" log"+".txt","r")
        log_read = log_read.readlines()
        #logg.write("dsg")
        log_file = name+" log"+".txt"
        log_open = open(log_file,"a+")
        #log_write.write("test")
        #self.connection = sqlite3.connect('friend_list.db')
        #cursor = self.connection.cursor()
        #self.connection.row_factory = lambda cursor, row: row[0]
        #a = self.connection.execute("""SELECT id FROM friend_list WHERE name = (?)""",(name,)).fetchall()
        #print(a," printed")
        #ppl=a[0]
        #print(ppl)
        #print(os.getcwd())
        directory = os.getcwd()+"/"+log_file

    def set_selection_mode(self, instance_selection_list, mode):
        if mode:
            self.root.ids['Chat_Screen'].ids['LIST'].icon = 'trash-can'
            a = self.root.ids['Chat_Screen'].ids['LIST']
            self.root.ids["Chat_Screen"].ids["back_buttons"].icon = "alpha-x-box"
            self.root.ids['Chat_Screen'].ids['dropdown'].icon = 'content-copy'
            #a = self.root.ids['Chat_Screen'].ids['back_buttons']
            #a.bind(on_press = self.unselect)
        else:
            self.root.ids['Chat_Screen'].ids['LIST'].icon = 'camera'
            self.root.ids["Chat_Screen"].ids["back_buttons"].icon = "arrow-left"
            self.root.ids['Chat_Screen'].ids['dropdown'].icon = 'microphone'

        Animation(d=0.2).start(self.root.ids['Chat_Screen'].ids['headbox'])
        #self.root.ids['Chat_Screen'].ids["back_buttons"] = left_action_items
        #self.root.ids['Chat_Screen'].ids['headbox']  = right_action_items
    
    def selected(self,instance_selection_list,instance_selection_item):
        a = self.root.ids['Chat_Screen'].ids['LIST']
        a.bind(on_press = lambda x : self.root.ids['Chat_Screen'].ids['msglist'].remove_widget(instance_selection_item))
        
        
        #a.bind(on_release = lambda x : self.root.ids['Chat_Screen'].ids['msglist'].remove_widget(instance_selection_item))

    def Camera(self):
        print("camera")

    
    def unselected(self,instance_selection_list,instance_selection_item):
        if self.root.ids["Chat_Screen"].ids["back_buttons"].icon == "alpha-x-box":
            cross = self.root.ids["Chat_Screen"].ids["back_buttons"]
            cross.bind(on_press = lambda x : self.root.ids["Chat_Screen"].ids["msglist"].unselected_all())
            cam = self.root.ids['Chat_Screen'].ids['LIST']
            cam.bind(on_press = lambda x : self.Camera())
            if self.root.ids["Chat_Screen"].ids["LIST"].icon=="camera":
                cross.unbind(on_press = self.root.ids['Chat_Screen'].ids['msglist'].remove_widget(instance_selection_item))


            #cross.bind(on_release = lambda x : self.root.ids["Chat_Screen"].ids["back buttons"].icon = "arrow-left")
    
        #self.root.ids['Chat_Screen'].ids['msglist'].remove_widget(instance_selection_item)

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def delete_contact(self,text):
        delete = self.root.ids['Chat_Screen'].ids['name'].text
        print(delete)
        self.connection = sqlite3.connect('friend_list.db')
        self.cursor = self.connection.cursor() 
        self.cursor.execute(""" DELETE FROM friend_list WHERE name = (?) """,(delete,))
        self.connection.commit()
        with open(delete +".txt") as opened:
            opened.close()
            os.remove(delete+'.txt')
        self.stop()
        return ChatApp().run()

    def drop_down(self):
        dropmenu = self.root.ids['Chat_Screen'].ids['dropdown']
        items = [{'text':'Remove Contact',"viewclass": "OneLineListItem",'on_press':self.delete_dialog}]
        self.dropdown = MDDropdownMenu(caller = dropmenu, items=items, width_mult=4)
        self.dropdown.open()
        
    def refresh(self):
        self.stop
        return self.change_screen('Chat_Screen')

    def remove_box(self,text_of_option):
        print(text_of_option)

    def msg_builder(self,friends,screen):
        pass

    def reset(self):
        self.change_screen('Chat_List')
        #self.root.ids["Chat_Screen"].ids["msglist"].clear_widgets()
        time.sleep(0.1)
        self.stop()
        return ChatApp().run()


    #   create a button.text thingu to update datanase acc to msg sent

    def idcheck(self,id,name):
        #print(uuid.key())
        database =  cursor.execute('SELECT id from friend_list where id = ?',(id,)).fetchall()
        print(database)
        if database != []:
            print("entry exists")



if __name__ == "__main__":
    ChatApp().run()
