import os, urllib, json, shutil
w=1
q=1
e=1
values=['.','[',']','(',')','m720p','480p','480','DVDSCR','BrRip','New Source','MP3','Mafiaking','1CD',
'mkv','mSD','2CD','BRRip','BRrip','720p','BluRay','YIFY','mp4','XviD','-','x264','ETRG','avi','StyLishSaLH'
,'DVD','dvd','DVDRip','RIP','rip','Rip','Back In Action']
# values contain some common names found in movies, to identify movie files
def find(folder):
	for x in os.listdir(folder):
                #checking for valid movie name
		if(x[0].isdigit() and x[0]>4):
			continue
		movie_name=folder+'//'+x
		for y in range(1500,2100):
			if(str(y) in x):
				x=x.replace(str(y)," ")
		for z in values:
			if(str(z) in x):
				x=x.replace(str(z)," ")
			if("  " in x):
				x=x.replace("  "," ")
		url='http://www.omdbapi.com/?t='+str(x) #The OMDb API is a free web service to obtain movie information,
		response = urllib.urlopen(url).read()
		json_values = json.loads(response)
		if json_values["Response"]=="True": #If movie with the name exists
			imdb_rating = json_values['imdbRating']
			print imdb_rating+" "+x
			destination_directory = 'E:\movies\\'+ imdb_rating #makes folder with rating as name
			if not os.path.exists(destination_directory): 
				os.makedirs(destination_directory) #creates folder if it doesnt exist
			shutil.move(movie_name, destination_directory) #used for moving files
		
		else:
			a=0
			f=1
			e=0
			g=0
			for y in range(1,5):
					x=x.replace(" ",": ",w)
					if(a==1):
						x=x.replace(":"," ",e)
					url='http://www.omdbapi.com/?t='+str(x)
					response = urllib.urlopen(url).read()
					json_values = json.loads(response)
					if json_values["Response"]=="True":
						imdb_rating = json_values['imdbRating']
						print imdb_rating+" "+x
						destination_directory = 'E:\Movies\\'+ imdb_rating
						if not os.path.exists(destination_directory): 
							os.makedirs(destination_directory)
						shutil.move(movie_name, destination_directory)
						break
					else:
						x=x.replace(": ",":",f)
						if(g>0):
							x=x.replace(" ",":",g)
						a=1
						g=g+1
						e=e+1
#directory where the movies exist
find('E:\Movies')
