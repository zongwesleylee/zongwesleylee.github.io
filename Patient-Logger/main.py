import json
import math
from datetime import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import firebase_admin
from firebase_admin import db, credentials
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.garden.matplotlib import FigureCanvasKivy
from kivy.uix.screenmanager import ScreenManager, Screen

cred = credentials.Certificate("patient-logger-firebase-adminsdk-x8w5z-bc1fd625eb.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://patient-logger-default-rtdb.firebaseio.com/'
})

ref = db.reference("/")


def write_json(datafile, filename='patients.json'):
    with open(filename, 'w') as file:
        json.dump(datafile, file, indent=4)


def load_json():
    with open("patients.json", "r") as f:
        file_contents = json.load(f)
    ref.set(file_contents)


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


class StartingScreen(Screen):
    pass


class LogIn(Screen):
    def verify_credentials(self):
        with open('patients.json') as json_file:
            data = json.load(json_file)
            user = data[f'{self.type}']
        for d in user:
            if self.user.text == d['Username'] and self.pwd.text == d['Password']:
                self.user.text = "Enter username"
                self.pwd.text = "Enter password"
                self.pwd.password = False
                self.authenticate.text = ""
                if self.type == "Doctor":
                    self.manager.get_screen('first').test.text = d['Doc_FName'] + " " + d['Doc_LName']
                self.manager.current = "first"
                break
            else:
                self.authenticate.text = "Username and/or Password is incorrect"

    def on_focus(self, value):
        if value:
            if self.ids[self.type2].text == f'Enter {self.type2}':
                if self.type2 == "password":
                    self.ids[self.type2].password = True
                self.ids[self.type2].text = ""
        else:
            if self.ids[self.type2].text == "":
                self.ids[self.type2].password = False
                self.ids[self.type2].text = f"Enter {self.type2}"


class SignUp(Screen):
    def verify_availability(self):
        with open('patients.json') as json_file:
            data = json.load(json_file)
            user = data[f'{self.type}']

        if self.user.text in ["", "Enter username"] or self.pwd.text in ["", "Enter password"]:
            self.authenticate.text = "Enter username"
        else:
            if self.type == 'Doctor':
                if self.user.text not in [d['Username'] for d in user]:
                    user.append({"Doc_FName": self.ids["First Name"].text,
                                 "Doc_LName": self.ids["Last Name"].text,
                                 "Username": self.user.text,
                                 "Password": self.pwd.text
                                 })
                    write_json(data)

                    load_json()

                    self.manager.current = "login"
                else:
                    self.authenticate2.text = "Username Taken"

            if self.type == 'Medical Assistant':
                if self.user.text not in [d['Username'] for d in user]:
                    user.append({"Med_FName": self.ids["First Name"].text,
                                 "Med_LName": self.ids["Last Name"].text,
                                 "Username": self.user.text,
                                 "Password": self.pwd.text
                                 })
                    write_json(data)

                    load_json()

                    self.manager.current = "login"
                else:
                    self.authenticate2.text = "Username Taken"

    def on_focus(self, value):
        if value:
            if self.ids[self.type2].text == f'Enter {self.type2}':
                if self.type2 == "password":
                    self.ids[self.type2].password = True
                self.ids[self.type2].text = ""
        else:
            if self.ids[self.type2].text == "":
                self.ids[self.type2].password = False
                self.ids[self.type2].text = f"Enter {self.type2}"


class PatientList(Screen):
    def patient_list(self):
        grid = self.ids["grid"]
        if self.type == "Doctor":
            with open('patients.json') as json_file:
                data = json.load(json_file)
                patient = [d for d in data['Doctor-to-Patient'] if self.test.text == d['Doctor']]
                for row in patient:
                    patient_button = Button(
                        text=row['Patient'],
                        pos_hint={"center_x": 0.5, "center_y": 0.3},
                        size_hint=(0.2, 0.3))
                    patient_button.bind(on_press=self.nextscreen)
                    grid.add_widget(patient_button)
        else:
            with open('patients.json') as json_file:
                data = json.load(json_file)
                patient = data['Doctor-to-Patient']
                for row in patient:
                    patient_button = Button(
                        text=row['Patient'] + "\n" + f"[size=13]Doctor:{row['Doctor']}[/size]",
                        pos_hint={"center_x": 0.5, "center_y": 0.3},
                        size_hint=(0.2, 0.3),
                        markup=True
                    )
                    patient_button.bind(on_press=self.nextscreen)
                    grid.add_widget(patient_button)

    def checkout(self):
        self.ids.grid.clear_widgets()
        self.manager.current = 'main'

    def nextscreen(self, button):
        if self.type == "Medical Assistant":
            self.manager.get_screen('patientpage').pdata.disabled = True
            self.manager.get_screen('patientpage').pdata.opacity = 0
        self.manager.get_screen('patientpage').test.text = button.text
        self.manager.get_screen('patientpage').patientpage()
        self.manager.current = 'patientpage'


class PatientPage(Screen):

    def patientpage(self):
        grids = self.ids["grids"]

        with open('patients.json') as json_file:
            data = json.load(json_file)
            patient = data['Patient']
            name_check = self.test.text
            name_check = name_check.split('\n')
            name_check2 = name_check[0]
            for row in patient:
                if row["MName"] is None:
                    name = row["FName"] + " " + row["LName"]
                else:
                    name = row["FName"] + " " + row["MName"] + " " + row["LName"]
                if name == name_check2:
                    self.patient.text = name
                    birthyear = Label(text=("Birth Year: " + row["Birth Year"]),
                                      pos_hint={"center_x": 0.5, "top": 0.9},
                                      font_size=25,
                                      size_hint=(0.1, 0.1))
                    gender = Label(text=("Gender: " + row["Gender"]),
                                   pos_hint={"center_x": 0.5, "top": 0.9},
                                   font_size=25,
                                   size_hint=(0.1, 0.1))
                    race = Label(text=("Race: " + row["Race"]),
                                 pos_hint={"center_x": 0.5, "top": 0.9},
                                 font_size=25,
                                 size_hint=(0.1, 0.1))
                    pnumber = Label(text=("Phone Number: " + row["PNumber"]),
                                    pos_hint={"center_x": 0.5, "top": 0.9},
                                    font_size=25,
                                    size_hint=(0.1, 0.1))
                    eaddress = Label(text=("Email Address: " + row["EAddress"]),
                                     pos_hint={"center_x": 0.5, "top": 0.9},
                                     font_size=25,
                                     size_hint=(0.1, 0.1))
                    saddress = Label(text=("Street Address: " + row["SAddress"]),
                                     pos_hint={"center_x": 0.5, "top": 0.9},
                                     font_size=25,
                                     size_hint=(0.1, 0.1))
                    snumber = Label(text=("Social Security Number: " + row["SNumber"]),
                                    pos_hint={"center_x": 0.5, "top": 0.9},
                                    font_size=25,
                                    size_hint=(0.1, 0.1))
                    mcompany = Label(text=("Medical Company: " + row["MCompany"]),
                                     pos_hint={"center_x": 0.5, "top": 0.9},
                                     font_size=25,
                                     size_hint=(0.1, 0.1))

                    grids.add_widget(birthyear)
                    grids.add_widget(gender)
                    grids.add_widget(race)
                    grids.add_widget(pnumber)
                    grids.add_widget(eaddress)
                    grids.add_widget(saddress)
                    grids.add_widget(snumber)
                    grids.add_widget(mcompany)

    def checkout(self):
        self.ids.grids.clear_widgets()
        self.manager.current = 'first'


class New_Patient(Screen):
    def Add_Patient(self):
        with open('patients.json') as json_file:
            data = json.load(json_file)
            patient = data['Patient']
            docTopat = data['Doctor-to-Patient']
        if self.ids['First name'].text not in [d['FName'] for d in patient] \
                or self.ids['Last name'].text not in [d['LName'] for d in patient]:
            if self.ids["Middle name"].text == "Middle name":
                patient.append({
                    "FName": self.ids['First name'].text,
                    "MName": None,
                    "LName": self.ids['Last name'].text,
                    "Birth Year": self.ids['Month'].text + "/" + self.ids['Day'].text + "/" + self.ids['Year'].text,
                    "Gender": self.ids['Gender'].text,
                    "Race": self.ids['Race/Ethnicity'].text,
                    "PNumber": self.ids['Phone Number'].text,
                    "EAddress": self.ids['Email Address'].text,
                    "SAddress": self.ids['Street Address'].text,
                    "SNumber": self.ids['Social Security'].text,
                    "MCompany": self.ids['Medical Insurance Company'].text
                })
            else:
                patient.append({
                    "FName": self.ids['First name'].text,
                    "MName": self.ids['Middle name'].text,
                    "LName": self.ids['Last name'].text,
                    "Birth Year": self.ids['Month'].text + "/" + self.ids['Day'].text + "/" + self.ids['Year'].text,
                    "Gender": self.ids['Gender'].text,
                    "Race": self.ids['Race/Ethnicity'].text,
                    "PNumber": self.ids['Phone Number'].text,
                    "EAddress": self.ids['Email Address'].text,
                    "SAddress": self.ids['Street Address'].text,
                    "SNumber": self.ids['Social Security'].text,
                    "MCompany": self.ids['Medical Insurance Company'].text
                })
            if self.ids['Middle name'].text == "Middle name":
                docTopat.append(
                    {
                        "Doctor": self.manager.get_screen('first').test.text,
                        "Patient": self.ids['First name'].text + " " + self.ids['Last name'].text
                    }
                )
            else:
                docTopat.append(
                    {
                        "Doctor": self.manager.get_screen('first').test.text,
                        "Patient": self.ids['First name'].text + " "
                                   + self.ids['Middle name'].text + " "
                                   + self.ids['Last name'].text
                    }
                )
            write_json(data)

            load_json()

            self.manager.get_screen('first').checkout()
            self.manager.get_screen('first').patient_list()
            self.manager.current = "first"
        else:
            popup = Popup(content=Label(text='Patient Already Exists', font_size=12),
                          size_hint=(None, None), size=(250, 250))
            popup.open()

    def on_focus(self, value):
        if value:
            if self.ids[self.type2].text == f'{self.type2}':
                if self.type2 == "Social Security":
                    self.ids[self.type2].password = True
                self.ids[self.type2].text = ""
        else:
            if self.ids[self.type2].text == "":
                self.ids[self.type2].password = False
                self.ids[self.type2].text = f"{self.type2}"


class Data(Screen):
    def on_kv_post(self, base_widget):
        grid = self.ids["grid"]
        data = pd.read_csv("testData1.csv")
        columns = data.columns
        time = [dt.strptime(timestamp, '%H:%M:%S') for timestamp in data[columns[0]]]
        # Plot 1-----------------------------------------------------------------------------------
        fig1, ax1 = plt.subplots(1, 1)
        ax1.plot(time, data[columns[1]], '--r', label='AccX')
        ax1.plot(time, data[columns[2]], '--b', label='AccY')
        ax1.plot(time, data[columns[3]], '--g', label='AccZ')
        ax1.set_xlabel("Time", fontsize=15)
        ax1.set_ylabel("Acceleration [mg]", fontsize=15, labelpad=-15)
        ax1.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=10)
        ax1.set_title("Acceleration", fontsize=25)
        ax1.grid()
        my_mpl_kivy_widget = FigureCanvasKivy(fig1)

        bx1 = BoxLayout(size_hint=(1, 1), size=(Window.width * 0.93, Window.height / 1.2))
        bx1.add_widget(my_mpl_kivy_widget)

        grid.add_widget(bx1)
        # Plot 2-----------------------------------------------------------------------------------
        fig2, ax2 = plt.subplots()
        ax2.plot(time, data[columns[4]], '--r', label='GyroX')
        ax2.plot(time, data[columns[5]], '--b', label='GyroY')
        ax2.plot(time, data[columns[6]], '--g', label='GyroZ')
        ax2.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=10)
        ax2.set_xlabel("Time", fontsize=15)
        ax2.set_ylabel("Gyroscope [mdps]", fontsize=15, labelpad=-15)
        ax2.set_title("Gyroscope", fontsize=25)
        ax2.grid()
        my_mpl_kivy_widget = FigureCanvasKivy(fig2)

        bx2 = BoxLayout(size_hint=(1, 1), size=(Window.width * 0.93, Window.height / 1.2))
        bx2.add_widget(my_mpl_kivy_widget)

        grid.add_widget(bx2)
        # Plot 3-----------------------------------------------------------------------------------
        fig3, ax3 = plt.subplots()
        ax3.plot(time, data[columns[7]], '--r', label='MagX')
        ax3.plot(time, data[columns[8]], '--b', label='MagY')
        ax3.plot(time, data[columns[9]], '--g', label='MagZ')
        ax3.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=10)
        ax3.set_xlabel("Time", fontsize=15)
        ax3.set_ylabel("Magnitude [mgauss]", fontsize=15, labelpad=-15)
        ax3.set_title("Magnitude", fontsize=25)
        ax3.grid()
        my_mpl_kivy_widget = FigureCanvasKivy(fig3)

        bx3 = BoxLayout(size_hint=(1, 1), size=(Window.width * 0.93, Window.height / 1.2))
        bx3.add_widget(my_mpl_kivy_widget)

        grid.add_widget(bx3)
        # Plot 4-----------------------------------------------------------------------------------
        fig4, ax4 = plt.subplots()
        ax4.plot(time, data[columns[10]], '--r', label='P')
        ax4.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=10)
        ax4.set_xlabel("Time", fontsize=15)
        ax4.set_ylabel("Pressure [mB]", fontsize=15, labelpad=-15)
        ax4.set_title("Pressure", fontsize=25)
        ax4.grid()
        my_mpl_kivy_widget = FigureCanvasKivy(fig4)

        bx4 = BoxLayout(size_hint=(1, 1), size=(Window.width * 0.93, Window.height / 1.2))
        bx4.add_widget(my_mpl_kivy_widget)

        grid.add_widget(bx4)
        # Plot 5-----------------------------------------------------------------------------------
        fig5, ax5 = plt.subplots()
        ax5.plot(time, data[columns[11]], '--r', label='T1')
        ax5.plot(time, data[columns[12]], '--b', label='T2')
        ax5.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=10)
        ax5.set_xlabel("Time", fontsize=15)
        ax5.set_ylabel("Temperature [°C]", fontsize=15, labelpad=-15)
        ax5.set_title("Temperature", fontsize=25)
        ax5.grid()
        my_mpl_kivy_widget = FigureCanvasKivy(fig5)

        bx5 = BoxLayout(size_hint=(1, 1), size=(Window.width * 0.93, Window.height / 1.2))
        bx5.add_widget(my_mpl_kivy_widget)

        grid.add_widget(bx5)
        # Plot 6-----------------------------------------------------------------------------------
        fig6, ax6 = plt.subplots()
        ax6.plot(time, data[columns[13]], '--r', label='qi')
        ax6.plot(time, data[columns[14]], '--b', label='qj')
        ax6.plot(time, data[columns[15]], '--g', label='qk')
        ax6.plot(time, data[columns[16]], '--y', label='qs')
        ax6.set_xlabel("Time", fontsize=15)
        ax6.set_ylabel("MEMS Fusion", fontsize=15, labelpad=-15)
        ax6.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=10)
        ax6.set_title("MEMS Fusion", fontsize=25)
        ax6.grid()
        my_mpl_kivy_widget = FigureCanvasKivy(fig6)

        bx6 = BoxLayout(size_hint=(1, 1), size=(Window.width * 0.93, Window.height / 1.2))
        bx6.add_widget(my_mpl_kivy_widget)

        grid.add_widget(bx6)
        # rangeVal = max(data[columns[i + 1]]) - min(data[columns[i + 1]])
        # avg = stat.mean(data[columns[i + 1]])
        # graph = Graph(xlabel="Time",
        #               ylabel=columns[i + 1],
        #               x_ticks_minor=5,
        #               x_ticks_major=(abs(len(data[columns[0]]) / 10)),
        #               y_ticks_minor=abs(round_up(avg + rangeVal, -1) - round_down(avg - rangeVal, -1)) / 10,
        #               y_ticks_major=abs(round_up(avg + rangeVal, -1) - round_down(avg - rangeVal, -1)) / 5,
        #               y_grid_label=True,
        #               x_grid_label=True,
        #               padding=10,
        #               x_grid=True,
        #               y_grid=True,
        #               xmin=0,
        #               xmax=len(data[columns[0]]),
        #               ymin=round_down(avg - rangeVal, -1),
        #               ymax=round_up(avg + rangeVal, -1),
        #               border_color=[0, 0, 0, 0])
        # plot = SmoothLinePlot(color=[1, random.random(), random.random(), random.random()])
        # plot.points = [(x, y) for x, y in zip(range(len(data[columns[0]])), data[columns[i + 1]])]
        # graph.add_plot(plot)
        # grid.add_widget(graph)


class ScreenManagement(ScreenManager):
    TYPE_GLOBAL = StringProperty()
    TYPE_GLOBAL2 = StringProperty()


kv_file = Builder.load_file('main.kv')


class Starting(App):
    def build(self):
        return kv_file


Starting().run()
