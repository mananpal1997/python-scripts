import requests, os, bs4, threading, time
z = input("Enter valid directory ( C, D, E or whatever ) where you want to download the XKCD comics : ")
try:
    os.chdir(z+':/')
except:
    print("Invalid Directory.\nProgram closing down.")
    exit()
os.makedirs('xkcd', exist_ok=True)

def download_xkcd(comic_start, comic_end):
    error = 0
    for urlNumber in range(comic_start, comic_end, -1):
        try:
            res = requests.get('http://xkcd.com/%s' % (urlNumber))
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text,'lxml')

            comicElem = soup.select('#comic img')
            if(comicElem == []):
                #print('Could not find comic image.')
                pass
            else:
                comicUrl = comicElem[0].get('src')
                comicUrl = 'http:'+comicUrl
                #print('Downloading image '+str(comicUrl)+'...')
                res = requests.get(comicUrl)
                res.raise_for_status()

                imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
        except:
            error += 1

download_threads = []

#finding latest comic number
###############################################################
res_t = requests.get('http://xkcd.com')
soup_t = bs4.BeautifulSoup(res_t.text,'lxml')
k_t = soup_t.findAll('a')
for g in k_t:
    if('Prev' in str(g)):
        x_t = str(g)
        break
l_t = x_t.find('href="/')
m_t = x_t.find('/',l_t+7)
n_t = int(x_t[l_t+7:m_t])
###############################################################

n = int(input("Enter number of latest XKCD comics you want to download : "))
nn = n
if(nn > n_t):
    print("There are only "+str(n_t)+" comics available.\nDownloading all the comics...")
    nn = n_t

for i in range(n_t + 1, n_t - nn + 1, -1):
    downloadThread = threading.Thread(target=download_xkcd, args=(i, i - 1))
    download_threads.append(downloadThread)
    downloadThread.start()

for download_thread in download_threads:
    download_thread.join()

downloaded = 0

for f1,f2,f3 in os.walk(z+':/xkcd/'):
    for f4 in f3:
        downloaded += 1
not_downloaded = n - downloaded

if(not_downloaded == 0):
    print('\nDownloads Successfully Completed !')
else:
    print(str(not_downloaded)+' out of '+str(n)+' comics were not downloaded due to some error.')
print('You can check the comics in xkcd folder in '+z+' drive of your system.')
