import requests, time
from bs4 import *

def get_info(names, recent_activity):

    for name in names.keys():
        res = requests.get('https://github.com/' + name + '?tab=repositories')
        soup = BeautifulSoup(res.text,'html.parser')
        names.setdefault(name, [])
        for repository in soup.findAll('a'):
            if(('/'+name+'/') in str(repository)):
                if(repository.string != None):
                    repository_name = repository.string.strip()
                    names[name].append("Repo name : "+repository_name)

    for name in names.keys():
        res = requests.get('https://github.com/' + name + '?tab=repositories')
        soup = BeautifulSoup(res.text,'html.parser')
        names.setdefault(name, [])
        index = 0
        for x in soup.findAll('div',{'class':'repo-list-stats'}):
            l = False
            z = ""
            for y in x.children:
                    if('programmingLanguage' in str(y)):
                            l = True
                            z = y.string.strip()
                            break
            if(l==True):
                    names[name][index] += ("\n\t\tTechnology/Langauge(s) used : "+z+"\n")
            else:
                    names[name][index] += ("\n\t\tNo Technology/Language used.\n")
            index += 1
       
    for name in recent_activity.keys():
        res = requests.get('https://github.com/' + name)
        soup = BeautifulSoup(res.text,'html.parser')
        full_name = soup.find('div',{'class':'vcard-fullname'}).string
        print("HANDLE : %s, NAME : %s" % (name, full_name))
        recent_activity.setdefault(name, [])
        try:
            activity = soup.find('ul',{'class':'simple-conversation-list'})
            act_list = activity.findAll('li')
            for acts in act_list:
                cont = acts.contents
                commit = cont[1].string.strip() + ' on ' + cont[2].strip()
                recent_activity[name].append(commit)
        except:
            recent_activity[name].append("No recent commits !")

    print("\nRetreiving data : \n")
    time.sleep(5)
    
    for name in names.keys():
        print(name)
        print('\tRepos : ')
        rep_list = names[name]
        for rep in rep_list:
            print('\t\t',end = '')
            print(rep)
            time.sleep(1)
        print('\tRecent commits : ')
        commit_list = recent_activity[name]
        for commit in commit_list:
            print('\t\t',end = '')
            print(commit)
            time.sleep(1)
        print()
    

if(__name__ == '__main__'):
    x = input("Type your github handle : ")
    response = requests.get('https://github.com/' + x + '/following')
    soup = BeautifulSoup(response.text,'html.parser')
    list_tag = soup.find('ol',{'class':'follow-list clearfix'})
    devs = list_tag.findAll('li')
    names = {}
    recent_activity = {}
    print("People you follow : \n")
    for dev in devs:
        y = str(dev.find('a'))
        end = y.find('>')
        start = y.find('"',8,end)
        names.update({y[start+2:end-1]:[]})
        recent_activity.update({y[start+2:end-1]:[]})
    get_info(names,recent_activity)
