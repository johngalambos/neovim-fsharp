import urllib.request
import zipfile
import os
from shutil import rmtree

# download a file https://stackoverflow.com/a/31857152/373981

fsac_v = '0.34.0'
wd = os.path.dirname(os.path.realpath(__file__))
print('wd {}'.format(wd))
bin_path = os.path.join(wd, 'bin')
print('bin path {}'.format(bin_path))

file_name = 'fsautocomplete.zip'
fsac_url = 'https://github.com/fsharp/FSharp.AutoComplete' \
           '/releases/download/{}/{}'.format(fsac_v, file_name)


# clean the bin directory if it already exists
if os.path.exists(bin_path):
    rmtree(bin_path)

# make the directory
os.mkdir(bin_path)

print("Downloading {}...".format(fsac_url))
download_file = bin_path + file_name

urllib.request.urlretrieve(fsac_url, download_file)

with zipfile.ZipFile(download_file, 'r') as zipped:
    zipped.extractall(bin_path)

os.remove(download_file)
