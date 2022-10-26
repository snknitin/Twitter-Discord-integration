import json
import glob


all_bookmarks=[]
# using glob to read all files in the folder
files = [file for file in glob.glob("JSONBookmarks/*")]
for file_name in files:
    print(file_name)
    with open(file_name) as bk:
        data = json.load(bk)        # reads json data
    all_bookmarks.append(data)