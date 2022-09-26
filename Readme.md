# Flask Server for CSE 535 Project


## Firebase Setup

- Create a new project in Firebase Console
- Click on Web App in Project Home
- Copy the Firebase Config which looks like this:
```
{
  apiKey: <Api Key>,
  authDomain: <your_project_name.firebaseapp.com>,
  projectId: <your_project_name.firebaseapp.com>,
  storageBucket: <your_project_name.appspot.com>,
  messagingSenderId: <Message ID>,
  appId: <App ID>
}
```
- Now, create a firebaseConfig.json file in root folder of this project
- Paste the Copied json object here


## Start the server
- First install the dependencies by running following command:
```
pip install -r requirements.txt
```
- Then start the server:
```
python app.py
```
- This should start the server on localhost!