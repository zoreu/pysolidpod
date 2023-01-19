# pysolidpod
this package helps you to manage files in your solid pod


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
solid.upload('https://yourpod.inrupt.net/public', 'filename.pdf')

# upload in replace mode
solid.upload('https://yourpod.inrupt.net/public', 'filename.pdf', replace=True)
```

## delete links
```python
# delete file
solid.delete('https://yourpod.inrupt.net/public/file.txt')

#delete folder
solid.delete('https://yourpod.inrupt.net/public/folder/')
# warning: solid does not allow deleting folders directly containing files
```

## read folder
```python
items = solid.read_folder('https://yourpod.inrupt.net/public/')
# show links
items = solid.read_folder('https://yourpod.inrupt.net/public/', show_links=True)
```
