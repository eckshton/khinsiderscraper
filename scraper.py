import requests
import os

url = input("Enter url: ")
type = input("Type: ")

sub = url.split("/")

r = requests.get(url)
text = r.text
hrefs = []
songnames = []

while text.find('<a href="/' + sub[3] + '/album/' + sub[5] + '/') != -1:
    start = text.find('<a href="/' + sub[3] + '/album/' + sub[5] + '/')
    end = text.find('</a>', start)
    hrefs.append(text[start:end])
    text = text[end:]


condensedhrefs = []

for x in hrefs:
    condensedhrefs.append(x.split('"')[1])

uniqueurls = []

for x in condensedhrefs:
    alreadythere = False
    for y in uniqueurls:
        if x == y:
            alreadythere = True
            break
    if alreadythere == False:
        uniqueurls.append(x)
        songnames.append(hrefs[condensedhrefs.index(x)].split('">')[1])

finalurls = []

print('finalizing urls')

if type=='flac':
    for x in uniqueurls:
        s = requests.get('https://downloads.khinsider.com' + x)
        text2 = s.text
        start = text2.find('href="https://vgmsite.com/soundtracks/' + sub[5] + '/')
        end = text2.find('">',start)
        start2 = text2.find('href="https://vgmsite.com/soundtracks/' + sub[5] + '/', end)
        end2 = text2.find('">',start2)
        finalurls.append(text2[start2+6:end2])
if type=='mp3':
    for x in uniqueurls:
        s = requests.get('https://downloads.khinsider.com' + x)
        text2 = s.text
        start = text2.find('href="https://vgmsite.com/soundtracks/' + sub[5] + '/')
        end = text2.find('">',start)
        finalurls.append(text2[start+6:end])
try:
    os.mkdir("./" + sub[5])
except:
    print('filling premade dir')
    



for x in finalurls:
    if(os.path.isfile(sub[5]+"/"+songnames[finalurls.index(x)]+"."+type)):
        print(songnames[finalurls.index(x)] + " already exists")
        continue

    print("getting " + songnames[finalurls.index(x)])
    s = requests.get(x)
    file = open(sub[5]+"/"+songnames[finalurls.index(x)]+"."+type,"wb")
    file.write(s.content)
    file.close()