from distutils.command.config import config

import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCJLNZrOo2HuQlovTUgSLph8zSfvAZn-4s",
    "authDomain": "patient-logger.firebaseapp.com",
    "databaseURL": "https://patient-logger-default-rtdb.firebaseio.com",
    "projectId": "patient-logger",
    "storageBucket": "patient-logger.appspot.com",
    "messagingSenderId": "271849189292",
    "appId": "1:271849189292:web:2f7f74b5d69c15061b5409",
    "measurementId": "G-2PREE9M1KD"
};

# Initializing connection with Firebase
Firebase = pyrebase.initialize_app(config)

# Getting reference to storage feature of Firebase
storage = Firebase.storage()

# Getting reference to Realtime Database of Firebase
database = Firebase.database()

# //////////////////// Functions for Cloud Storage of Firebase \\\\\\\\\\\\\\\\\\\\ #

# ========== Function to send images to firebase ========== #
def dataToFirebase(data):
    path_on_cloud = "Data on Cloud/" + data
    path_local = "Local Data/" + data
    storage.child(path_on_cloud).put(path_local)
    print("Data : " + data + " successfully uploaded to firebase!")
    url = storage.child(path_on_cloud).get_url('GET')
    print("URL of "+ data + " is :"+url)
# ========== ./Function to send images to firebase ========== #


# ========== Function to download images from firebase ========== #
def dataFromFirebase(data):
    path_on_cloud = "Data on Cloud/" + data
    path_local = "Local Data/" + data
    storage.child(path_on_cloud).download(path_local)
    print("Data : " + data + " successfully downloaded from firebase!")
    url = storage.child(path_on_cloud).get_url('GET')
    print("URL of " + data + " is :" + url)
# ========== ./Function to download images from firebase ========== #


# //////////////////// Functions for Realtime Firebase Database \\\\\\\\\\\\\\\\\\\\ #

# ========== Add data to Realtime Database ========== #
def addToDB(data):
    database.child("Parent").child(data)
    data = {"Key1": "Value1", "Key2": "Value2", "Key3": "Value3"}
    database.set(data)
    print("Data added :" + data)
# ========= ./Add data to Realtime Database ========= #



# ========== Update data in Realtime Database ========== #
def updateDB(data):
    database.child("Parent").child(data).update({"key": "Value"})
    print("Data Updated :" + data)
# ========= ./Update data in Realtime Database ========= #



# ========= Search data from Realtime Database ========= #
def searchFromDB(key, parent=None):
    database.child("Parent").child(key).get()
    data = parent.val()
    print(data)

    return data['Key1'], data['Key2'], data['Key3']
# ========= ./Search data from Realtime Database ========= #


# ========= Retrive data from Realtime Database ========= #
def retriveFromDB(accident=None):
    keys = []
    all_nodes = database.child("Parent").get()
    for node in all_nodes.each():
        data = accident.val()
        key = accident.key()
        print(key)
        keys.append(key)
        print(data)
    return keys
# ========= ./Retrive data from Realtime Database ========= #
