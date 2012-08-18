import sys, os, re

from PIL import Image

from flask import Flask, render_template
from flask_frozen import Freezer

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

class student:

  def __init__(self, filename):
    f=open(filename,'r')
    info=f.read()
    li=[s.strip() for s in re.split('\w*:',info)]
    self.name,self.major,self.mentor,self.abstract=li[1],li[2],li[3],li[4].decode('latin-1')
    temp=self.name.split()
    self.name=temp[1]+", "+temp[0]
    key=re.search('\w*\.txt',filename).group(0)
    self.key=re.sub('\.txt','',key)
    
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
DEBUG=True,
FREEZER_BASE_URL="/home/spencer/python/rachleff/build"
)
freezer = Freezer(app)

imagedir="images"
abstractdir="abstracts"
studentobjs=[]
abstractobjs={}


def sortImagesByHeight(images):
  heights={}
  for i in images:
    heights[i]=Image.open(i).size[1]
  return sorted(heights, key=heights.get) 


imagelist=os.listdir("./static/"+imagedir)
imagefiles=["./static/images/"+l for l in imagelist]
sortedimages=sortImagesByHeight(imagefiles)
imgs=[re.sub("./static/","",i) for i in sortedimages]

abstractlist=os.listdir('./static/'+abstractdir)
abstractfiles=["./static/abstracts/"+l for l in abstractlist]
studentobjs=[student(l) for l in abstractfiles]
abstractobjs={p.key:p for p in studentobjs}

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/society/")
def society():
  return render_template('society.html')

@app.route("/gallery/")
def gallery():
    return render_template('gallery.html', images=imgs)

@app.route("/scholars/", methods=['GET', 'POST'])
def students():
  return render_template('students.html', students=studentobjs)

@app.route("/scholars/<key>")
def show_abstract(key):
  return render_template('abstracts.html', student=abstractobjs[key])

if __name__=="__main__":
  if len(sys.argv) > 1 and sys.argv[1] == "build":
    freezer.freeze()
  else:
    port=int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)
