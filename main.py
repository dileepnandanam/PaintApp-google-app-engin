from google.appengine.ext.webapp import template
import webapp2

from google.appengine.ext import db

class Imgfile(db.Model):
	filename = db.StringProperty()
	objects = db.IntegerProperty()
class Image(db.Model):
	filename = db.StringProperty()
	objectType = db.StringProperty()
	x0 = db.IntegerProperty()
	x1 = db.IntegerProperty()
	y0 = db.IntegerProperty()
	y1 = db.IntegerProperty()
	stroke = db.StringProperty()
	fill = db.StringProperty()
	line = db.IntegerProperty()
	order = db.IntegerProperty()
	

class MainPage(webapp2.RequestHandler):
	
	
	def get(self):
		self.response.headers['content-Type'] = 'html'
		
		
		self.response.write("<h2>Files</h2><ul>")
		
		res=Imgfile.all()
		for f in res:
			self.response.write('<li><a href="/imagestore?fname='+f.filename+'" >'+f.filename+'</a></li>')
		self.response.write("</ul>new:")
		self.response.write("""
			<form action="/" method="post">
				<input name="fname">
				<input value="create new" type=submit>
			</form>
		
		
		
		
		
		""")
		
		
	def post(self):
		fn=self.request.get("fname")
		res=Imgfile.all().filter("filename =",fn)
		
		alreadyExist=0
		for f in res:
			alreadyExist+=1	
		if(alreadyExist==0):
			Imgfile(filename=fn,objects=0).put()
			self.redirect("/imagestore?fname="+fn)
		else:
			self.response.out.write('image Already Exist<br> <a href="/" >back</a>')
		
		
		
		
		
		
		
		
class ImageStore(webapp2.RequestHandler):


	def get(self):
		self.response.headers['content-Type'] = 'html'
		
		fn=self.request.get("fname")
		if fn:
			
			
			
			
			res=Image.all().filter("filename =",fn)
			if res:
				res=sorted(res,key=lambda x:x.order)
			self.response.write('<script> var image=new Array();\n var fname="'+fn+'"\n')
			hist=-1;
			
			for j in res:
				hist+=1;
				
				self.response.write('image['+str(hist)+']={"objectType":"'+j.objectType+'","stroke":"'+j.stroke+'","line":'+str(j.line)+',"fill":"'+j.fill+'","x0":'+str(j.x0)+',"y0":'+str(j.y0)+',"x1":'+str(j.x1)+',"y1":'+str(j.y1)+'};'+"\n")
				
			self.response.write("var hist="+str(hist)+";\n var latestHist="+str(hist)+"; </script>")
			
		self.response.out.write(template.render("p.html",{}));

		self.response.write('<a href="/" >back</a>')








	
	def post(self):
		
		self.response.headers['content-Type'] = 'html'
		imageData=self.request.get('image')
		
		filename=self.request.get('fname')
		self.response.out.write(imageData)
		
		imageData=imageData[1:-1].split('},{')
		imageData[0]=imageData[0][1:]
		imageData[-1]=imageData[-1][0:-1]
		
		
		res=Imgfile.all().filter("filename =",filename)
		for ifile in res:
		
			order=ifile.objects
		
		if(len(imageData)>0):
			for j in imageData:
				
				att=j.split(",")
			
				objectType = att[0].split(':')[1][1:-1]
			
				stroke = att[1].split(':')[1][1:-1]
			
				line = int(att[2].split(':')[1])
				fill = att[3].split(':')[1][1:-1]
				x0 = int(att[4].split(':')[1])
			
				y0 = int(att[5].split(':')[1])
				x1 = int(att[6].split(':')[1])
				y1 = int(att[7].split(':')[1])
				json=Image(filename=filename,objectType=objectType,stroke=stroke,line=line,fill=fill,x0=x0,y0=y0,x1=x1,y1=y1,order=order)
				json.put()
				order+=1
			ifile.objects=order
			ifile.put()
			
			
		#self.redirect("/imagestore?fname="+filename)
		
		
		
app = webapp2.WSGIApplication([('/', MainPage),
								('/imagestore', ImageStore)],
															debug=True)
