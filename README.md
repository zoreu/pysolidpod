# pysolidpod
this package helps you to manage files in your solid pod

# get solid pod
https://solidproject.org/users/get-a-pod


# Installation

compatible with python 3+

```bash
pip install git+https://github.com/zoreu/pysolidpod
```


## login
```python
from pysolidpod import solid

solid = solid.api()
solid.login('https://yourpod.inrupt.net/', 'username', 'password')
```

## put file
```python
text = 'text example'
solid.put('https://yourpod.inrupt.net/public/example.txt', text)

# replace mode
solid.put('https://yourpod.inrupt.net/public/example.txt', text, replace=True)
```

## create folder
```python
solid.create_folder('https://yourpod.inrupt.net/public/new_folder')

# create folder persistently
solid.create_folder('https://yourpod.inrupt.net/public/new_folder/sub_folder/sub_sub_folder')
```

## upload files
```python
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

file_path = os.path.join(dir_path, 'example.pdf')
solid.upload('https://yourpod.inrupt.net/public', file_path)

# upload in replace mode
solid.upload('https://yourpod.inrupt.net/public', file_path, replace=True)
```

## delete links
```python
# delete file
solid.delete('https://yourpod.inrupt.net/public/file.txt')

#delete folder
solid.delete('https://yourpod.inrupt.net/public/folder/')
# notice: solid does not allow deleting folders directly containing files
```

## read folder
```python
items = solid.read_folder('https://yourpod.inrupt.net/public/')
# show links
items = solid.read_folder('https://yourpod.inrupt.net/public/', show_links=True)
```

## get file
```python
r = solid.get('https://yourpod.inrupt.net/private/example.txt')
print(r.text) # example text
```

## folders

private - display files only with login

public - show files to everyone
