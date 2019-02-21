import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('techLinkCredentials.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'gs://teclink-8e19c.appspot.com/'
})

bucket = storage.bucket()

print('done')
