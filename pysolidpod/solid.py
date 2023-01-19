import requests
import mimetypes
from urllib.parse import quote_plus
import os
import io
import re

class api:
    def __init__(self):
        self.client = requests
        self.cookies = ''  

    def login(self,idp,username,password):
        if idp[-1] == '/':
            idp = idp[:-1]
        url = '/'.join((idp, 'login/password'))

        data = {
            'username': username,
            'password': password
        }
        r = self.client.post(url, data=data)
        self.cookies = r.cookies
        r.raise_for_status()

        if not r.cookies.get('nssidp.sid'):
            raise Exception('Cannot login.')
        
    def exists(self,url):
        status = False
        try:
            r = self.client.head(url,cookies=self.cookies)
            if r.status_code == 200:
                status = True            
        except:
            pass
        return status
    
    def encode_content(self,content):
        f = io.BytesIO(content.encode('UTF-8'))
        return f          
        
    def put(self,url,content,replace=False):
        mime_type = mimetypes.guess_type(url)[0]
        headers = {'Link': '<http://www.w3.org/ns/ldp#Resource>; rel="type"', 'Content-Type': mime_type}
        data = self.encode_content(content)
        r = ''
        if replace==True:
            try:
                r = self.client.put(url,headers=headers,data=data,cookies=self.cookies)
                print('file created successfully!')
            except:
                r = 'put file fail!'
                print('failed to create file')
        elif not self.exists(url) and replace==False:
            try:
                r = self.client.put(url,headers=headers,data=data,cookies=self.cookies)
                print('file created successfully!')
            except:
                print('put file fail!')
        else:
            print('file exists!')
        return r

    def upload(self,path,filename,replace=False):
        if not self.exists(path):
            self.create_folder(path)
        if not '/' in path[-1]:
            url = path + '/' + quote_plus(os.path.basename(filename))
        else:      
            url = path + quote_plus(os.path.basename(filename))
        r = ''
        mime_type = mimetypes.guess_type(filename)[0]
        if not os.path.exists(filename):
            dir_path = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(dir_path, os.path.basename(filename))
        headers = {'Link': '<http://www.w3.org/ns/ldp#Resource>; rel="type"', 'Content-Type': mime_type}           
        if replace==True:
            with open(filename, 'rb') as file:
                try:
                    r = self.client.put(url,headers=headers,data=file,cookies=self.cookies)
                    print('upload successful!')
                except:
                    print('upload fail!')
        elif not self.exists(url) and replace==False:
            with open(filename, 'rb') as file:
                try:
                    r = self.client.put(url,headers=headers,data=file,cookies=self.cookies)
                    print('upload successful!')
                except:
                    print('upload fail!')
        else:
            print('file exists!')
        return r
    
    def create_folder(self,url):
        if not '/' in url[-1]:
            url = url + '/'
        path = url.split("/")
        del path[-1]
        folder = path[-1]
        url_path = '/'.join(path).replace('/'+folder, '') + '/'
        if not self.exists(url_path):
            self.create_folder(url_path)
        headers = {'Link': '<http://www.w3.org/ns/ldp#BasicContainer>; rel="type"', 'Slug': folder, 'Content-Type': 'text/turtle'}
        r = ''
        if not self.exists(url):
            try:
                r = self.client.post(url_path,headers=headers,cookies=self.cookies)
                print('folder successfully created!')
            except:
                print('failed to create folder!')
        else:
            print('folder exists!')
        return r
    
    def parse_folder(self,url,res,show_links):
        content = res.text
        filters = ['$', '#', '?', '']
        if show_links:
            items = [url + name for name in re.findall("<(.*?)>",content) if not name in filters and not 'http' in name]
        else:
            items = [name for name in re.findall("<(.*?)>",content) if not name in filters and not 'http' in name]
        return items       

    
    def read_folder(self,url,show_links=False):
        if url[-1] != '/':
            url += '/'
        headers = {'Accept': 'text/turtle'}
        try:
            res = self.client.get(url,headers=headers,cookies=self.cookies)
            items = self.parse_folder(url,res,show_links)
        except:
            print('failed to get folder items')
            items = []
        return items

    def delete(self,url):
        headers = {}
        r = ''
        try:
            filename = os.path.basename(url)
            url = url.replace(filename,quote_plus(filename))
        except:
            pass
        try:
            r = self.client.delete(url,cookies=self.cookies)
            print('successfully deleted!')
        except:
            print('delete fail!')
        return r  
