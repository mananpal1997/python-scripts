import pafy
import pyperclip
flag=0
result = pyperclip.paste()
type=input("Hit 1 for video,2 for playlist : ")
type=int(type)
qual=input("Hit 1 for best clarity, 2 for worst, 3 for other : ")
qual=int(qual)
if(qual==3):
	flag=1
c=0
if(type==1):
	url = result
	video = pafy.new(url)
	best = video.streams
	if(flag==1):
                for b in best:
                        print(str(c)+str(b))
                        c+=1
		index=input("Enter index : ")
		index=int(index)
	elif(qual==2):
		index=c-1
	elif(qual==1):
		index=0
		
	filename = video.streams[index]
	print (filename)
	x=filename.download(filepath='E:/YouTube/')#+filename.title + "." + filename.extension)

else:
	url=result
	video=pafy.get_playlist(url)
	for i in range(1,108):
		c=0
		best=video['items'][i]['pafy'].streams
		if(flag==1):
                        for b in best:
                                print (str(c)+str(b))
                                c+=1
			index=input("Enter index : ")
			index=int(index)
		elif(qual==2):
			index=c-1
		elif(qual==1):
			index=0
		filename=video['items'][i]['pafy'].streams[index]
		x=filename.download(filepath="E:/YouTube/")
