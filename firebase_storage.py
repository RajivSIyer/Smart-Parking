"""
Created on Fri Apr 17 18:08:19 2020

@author: Navin Subbu

"""
from firebase import firebase
import pyrebase
import datetime

time = datetime.datetime.now()

# Firebase Initialization wiht App secrets
# firebase =  firebase.FirebaseApplication("https://python-test-1235f.firebaseio.com/",None)

config = {
    "apiKey" : "AIzaSyA61ZKDXOMSaWCptXZmU6McwXK5ejGWIiI",
    "authDomain" : "smart-parking-39ca2.firebaseapp.com",
    "databaseURL" : "https://smart-parking-39ca2.firebaseio.com",
    "projectId" : "smart-parking-39ca2",
    "storageBucket" : "smart-parking-39ca2.appspot.com",
    "messagingSenderId" : "516938731632",
    "appId" : "1:516938731632:web:e355b1c121c29788bf24b5",
    "measurementId" : "G-DVES1GJ65E"
    }



# config = {
#     "apiKey" : "AIzaSyAx3rxrUmCOESoCdj3NP1x_ITyeC_YYjno",
#     "authDomain" : "python-test-1235f.firebaseapp.com",
#     "databaseURL" : "https://python-test-1235f.firebaseio.com",
#     "projectId" : "python-test-1235f",
#     "storageBucket" : "python-test-1235f.appspot.com",
#     "messagingSenderId" : "707011126206",
#     "appId" : "1:707011126206:web:93df56c96e28b114b48fef",
#     "measurementId" : "G-8YHDDWVLP7"
#     }


def firebase_store(path,image_name) :
    """
    This Fucntion stores a given file into Google Firebase Storage in 
    a Specifed location categorised in the order of Year and Month
    Parameters
    ----------
    path : String
        It is the Path of the saved image
    image_name : String
        It is the name of the Image

    Returns
    -------
    None.
    
    """
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    path_on_cloud = "Car Recorded/{0}/{1}".format(path,image_name)
    path_local = "detected/{0}/{1}.".format(path,image_name) 
    storage.child(path_on_cloud).put(path_local)
    
    
    
def firebase_realtime_db(text,month,resident,name) :
    
    """
    This function pushes a given string into Realtime Database in Google Firebase

    Parameters
    ----------
    text : String
        Its a string, the license plate number
    Returns
    -------
    
    None.
    
    """
    # print(text)
    # print(time)
    # print(resident)

    date = time.strftime("%d")
    # time_hours = time.strftime("%I:%M:%S%p")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.child("Detected")
    db.child(month)
    db.child(date).child(resident)
    db.child(name).set(text)
   
    

    # result = firebase.put('/Detected', text)
    # print(result)
    

    
    
    
      
    