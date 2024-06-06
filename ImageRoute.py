import os
import cv2
import webbrowser
from multiprocessing import Process
from datetime import datetime
from PIL import Image, ExifTags


def make_location_object(n, e, date, file_path):
    n = f'{int(n[0])}.{str(int(n[1])/60 + float(n[2])/3600)[2:]}'
    e = f'{int(e[0])}.{str(int(e[1])/60 + float(e[2])/3600)[2:]}'
    return({'Coordinates':f'{n},{e}', 'Date':date, 'Name':file_path, 'Path':os.path.join(root, name)})

def open_image(image):
    url = 'https://www.google.com/maps/place/'
    webbrowser.open(url+image['Coordinates'])
    img = cv2.imread(image['Path'])
    imgr = cv2.resize(img, (500,500))
    cv2.imshow('Img_Window', imgr) 
    cv2.waitKey(0) 

if __name__ == '__main__':
    while True:
        try:
            date_start = input('Enter a starting date. DD MM YYYY\n')
            date_end = input('Enter an end date. DD MM YYYY\n')

            if date_start == '':
                date_start = datetime.strptime('01 01 1800', '%d %m %Y')
            else:
                date_start = datetime.strptime(date_start, '%d %m %Y')
            if date_end == '':
                date_end = datetime.today()

            else:
                date_end = datetime.strptime(date_end, '%d %m %Y')   
            break
        except ValueError as ex:
            print('Please enter a valid date')
    
    route = []

    extensions = ['jpg', 'jpeg', 'png', 'tiff', 'raw']
    while True:
        path = input('Enter a folder')
        if os.path.exists(path):
            break
        print('Enter a valid folder path')

    for root, dirs, files in os.walk(path): #Bron 1
        for name in files:
            if any('.'+ext in name for ext in extensions): 
                try:
                    img = Image.open(os.path.join(root,name))
                    exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS } #Bron 2
                    GPSInfo = exif['GPSInfo']
                    date = exif['DateTime']
                    gps_N = GPSInfo[2]
                    gps_E = GPSInfo[4]
                    #print(gps_N, gps_E, end='\n')
                    #print(os.path.join(root, name))
                    route.append(make_location_object(gps_N, gps_E, date, name))
                except Exception as ex:
                    print(f'ERROR WITH: {name} | {ex}', end='\r')

    route = sorted(route, key=lambda d: d['Date'])
    root_url = 'https://www.google.com/maps/dir/'
    route_url = root_url
   
    for r in route:
        date_obj = datetime.strptime(r['Date'], '%Y:%m:%d %H:%M:%S')
        if date_obj >= date_start and date_obj <= date_end:
            Coords = r['Coordinates']
            place_url = f'https://www.google.com/maps/place/{Coords}'
            route_url = route_url + Coords + '/'
            print(f'Locatie {route.index(r)+1}| {r["Date"]}| {place_url} | File Name: {r["Name"]}\n')


    if route_url != root_url:
        print(f'\n Complete route: {route_url}')
    else:
        print('No Valid Images Found')
    
    while True:
        while True:
            selected = input('Enter image number to open.\n')
            if selected.lower() == 'exit':
                exit()
            try:
                selected = int(selected)
                image = route[selected]
                break
            except Exception as ex:
                print('Enter a valid number\n')
        
        image_process = Process(target=open_image, args=(image,))
        image_process.start()


  #Bronnen 
#Bron 1 https://stackoverflow.com/questions/21697645/how-to-extract-metadata-from-an-image-using-python
#Bron 2 https://stackoverflow.com/questions/6531482/how-to-check-if-a-string-contains-an-element-from-a-list-in-python
#img = Image.open("/path/to/file.jpg")
