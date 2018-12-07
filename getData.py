from flask import Flask
import urllib.request
from bs4 import BeautifulSoup
import requests
import os



url = open('url.txt').read().split('\n')[0]
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page.read(), "html.parser")


app = Flask(__name__)

# create new folder for text
text_path = 'txt'
if not os.path.exists(text_path):
         os.mkdir(text_path)

# create new folder for images
images_path = 'img_'+url[8:12]
if not os.path.exists(images_path):
    os.mkdir(images_path)


@app.route('/', methods=['GET'])
def test():

    return 'Hello!'

# get text from web-page
@app.route('/text', methods=['GET'])
def getText():

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    #save text in folder as new file
    f = open(text_path + '/' + url[8:12], 'w')
    f.write(text)
    f.close()

    return text

# get images from web-page
@app.route('/images', methods=['GET'])
def getImages():

    images = []
    for img in soup.findAll('img'):

        if (img.get('src').startswith('http')):
            images.append(img)


    for image in images:
        im = image.get('src')

        # save images in folder img as new files
        if (im.startswith('http')):

            file_name = im.split('/')[-1]
            f = open(images_path + '/' + file_name[0:15], 'wb')

            r = requests.get(im)
            f.write(r.content)
            f.close()



    return str(images)



if __name__=='__main__':
    app.run(debug=True, port=8080)

