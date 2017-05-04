import requests,json
from numpy import base_repr as base


def nth_permutation(n,nums,count):
    size = len(nums)**count
    if n >= size: 
        return None
    out = []
    for i in range(count):
        d = n % len(nums)
        out.append(str(nums[d]))
        n -= d
        n /= len(nums)
    return out
     
def gen_permutations(nums,count):
    out = []
    for i in range(len(nums)**count):
        out.append(nth_permutation(i,nums,count))
    return out

def pull_metadata(n,s,e,w):
    url = "http://dev.virtualearth.net/mapcontrol/HumanScaleServices/GetBubbles.ashx"
    zoom = 3
    out = []
    r = requests.get(url,params={'c': 1,'n': n, 's': s, 'e': e, 'w': w})
    for obj in eval(r.text):
        if 'id' in obj.keys():
            out.append(gen_url(obj,gen_permutations([0,1,2,3],3)))
    return out


def gen_url(data,zoom_coords):
    dirmap = {'FRONT': 1, 'RIGHT': 2, 'BACK': 3, 'LEFT': 4, 'UP': 5, 'DOWN': 6}
    url_id = '{:0>16}'.format(base(data['id'],4))
    url_dir = '{:0>2}'.format(base(2,4))
    lat = data['la']
    lon = data['lo']
    out = []
    for zoom_coord in zoom_coords:
        url_tile_coord = ''.join(zoom_coord)
        url_params = url_id + url_dir + url_tile_coord
        out.append({'url': "http://ak.t1.tiles.virtualearth.net/tiles/hs{}.jpg?g=2981&n=z".format(url_params), 'coord': url_tile_coord})
    return out

def download_images(arr):
    for i in range(len(arr)):
        r = requests.get(arr[i]['url'])
        open('imgs/'+arr[i]['coord'],'wb').write(r.content)

sphere = pull_metadata("40.01910","40.01758","-105.27450","-105.27575")[0]
download_images(sphere)
#print test_url()
