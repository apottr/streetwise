import requests,json
from numpy import base_repr as base
from PIL import Image

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

def pull_metadata(n,s,e,w,direction):
    url = "http://dev.virtualearth.net/mapcontrol/HumanScaleServices/GetBubbles.ashx"
    zoom = 3
    out = []
    r = requests.get(url,params={'c': 1,'n': n, 's': s, 'e': e, 'w': w})
    for obj in eval(r.text):
        if 'id' in obj.keys():
            out.append(gen_url(obj,gen_permutations([0,1,2,3],3),direction))
    return out


def gen_url(data,zoom_coords,direction):
    dirmap = {'FRONT': 1, 'RIGHT': 2, 'BACK': 3, 'LEFT': 4, 'UP': 5, 'DOWN': 6}
    url_id = '{:0>16}'.format(base(data['id'],4))
    url_dir = '{:0>2}'.format(base(dirmap[direction],4))
    lat = data['la']
    lon = data['lo']
    out = []
    for zoom_coord in zoom_coords:
        url_tile_coord = ''.join(zoom_coord)
        url_params = url_id + url_dir + url_tile_coord
        out.append({'url': "http://ak.t1.tiles.virtualearth.net/tiles/hs{}.jpg?g=2981&n=z".format(url_params), 'coord': url_tile_coord})
    return out

def download_images(arr,direction):
    for i in range(len(arr)):
        r = requests.get(arr[i]['url'])
        open('imgs/{}_{}.jpg'.format(arr[i]['coord'],direction),'wb').write(r.content)

def generate_sides(d):
    tcoords = [
            ['000','001','010','011','100','101','110','111'],
            ['002','003','012','013','102','103','112','113'],
            ['020','021','030','031','120','121','130','131'],
            ['022','023','032','033','122','123','132','133'],
            ['200','201','210','211','300','301','310','311'],
            ['202','203','212','213','302','303','312','313'],
            ['220','221','230','231','320','321','330','331'],
            ['222','223','232','233','322','323','332','333']
            ]
    new_img = Image.new('RGB', (256*8,256*8))
    for y in range(8):
        for x in range(8):
            new_img.paste(Image.open('imgs/{}_{}.jpg'.format(tcoords[y][x],d)),(x*256,y*256))

    new_img.save("{}.jpg".format(d))

def main():
    bbox = [["40.01910","-105.27450"],["40.01758","-105.27575"]]
    for d in ["FRONT","RIGHT","BACK","LEFT","UP","DOWN"]:
        sphere = pull_metadata(bbox[0][0],bbox[1][0],bbox[0][1],bbox[1][1],d)[0]
        download_images(sphere,d)
        generate_sides(d)


main()
