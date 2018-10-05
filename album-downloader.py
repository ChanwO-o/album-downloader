import bs4 as bs
import urllib.request
import os


def getImageName(imageurl : str) -> str:
    sections = imageurl.strip().split('/')
    return sections[-1][0:-5]   # format is 008_11_6.jpg.jpg' , remove last 5 chars

def findServer(albumid : str, samplename : str) -> str:
    servers = ['aa', 'ba', '0a']
    for sv in servers:
        url = 'https://' + sv + '.sitename.la/galleries/' + albumid + '/' + samplename
        print('trying server', sv, 'with ' + url)
        
        try:
            urllib.request.urlopen(url)
        except:
            print(sv, 'failed')
            continue
        print(sv, 'works!')
        return sv
            

##def hasValidImageAt(url : str, index : int) -> bool:
##    pass


if __name__ == '__main__':
    baseurl = input('download url:\n')
    albumid = baseurl.split('/')[-1][0:-5]
    sauce = urllib.request.urlopen(baseurl).read()
    soup = str(bs.BeautifulSoup(sauce, 'lxml'))

    # find image names from reading thumbnails list
    openbr = soup.index('[')
    closebr = soup.index(']')
    imageurls = soup[openbr + 1 : closebr].strip().split(',')
    print('found', str(len(imageurls) - 1), 'images')

    # find server
    server = findServer(albumid, getImageName(imageurls[0]))

    start = int(input('start index (0 for cover image):\n'))
    end = int(input('end index (~' + str(len(imageurls) - 2) + '):\n'))


    for i in range(start, end + 1):
        print('downloading image #', i)
        imagename = getImageName(imageurls[i])
        if imagename == '':
            print('ha! continued')
            continue
        url = 'https://' + server + '.sitename.la/galleries/' + albumid + '/' + imagename
        print(url, '\n')
        urllib.request.urlretrieve(url, imagename)


##    dirname = input('dir name:\n')
##
##    currentdir = os.path.dirname(os.path.abspath(__file__))
##    newdir = currentdir + '\\' + dirname
##    print('current directory:', currentdir)
##    print('creating:', newdir)
##    os.makedirs(newdir)
