import os
from uuid import uuid4
from zipfile import ZipFile

#

#
class Fullpipe_user():
    #
    _path = "full_pipeline/client_folder/"
    _id = str(uuid4())
    
    def create_specific_user(self):
        #
        if not os.path.exists(self._path):
            os.mkdir(self._path)

        client_path = os.path.join(self._path, self._id)
        os.mkdir(client_path)
        data_path = os.path.join(client_path, 'data_input')
        res_path = os.path.join(client_path, 'results')
        os.mkdir(data_path)
        os.mkdir(res_path)

        return self._id, data_path, res_path


#
def handle_uploaded_file(file):  
    with open('static/upload/'+file.name, 'wb+') as fh:  
        for chunk in file.chunks():  
            fh.write(chunk)

def unzip_and_move(file, data_path):
    if str(file).endswith('.zip'):
    #do something
        with ZipFile('static/upload/' + str(file), 'r') as fr:
            fr.extractall(data_path)
    else:
        print('handle others')