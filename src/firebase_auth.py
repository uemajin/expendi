import pyrebase

config = {
  'apiKey': "AIzaSyCZo-Bl380_MKMvNvKVbXfoPPEKq2YEN8U",
  'authDomain': "finance-dash-8e11a.firebaseapp.com",
  'projectId': "finance-dash-8e11a",
  'storageBucket': "finance-dash-8e11a.appspot.com",
  'messagingSenderId': "372530184676",
  "databaseURL":'https://finance-dash-8e11a-default-rtdb.firebaseio.com/',
  'appId': "1:372530184676:web:400496c064c1d42e19c7f1"
}

def get_config():

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()

    return auth, db