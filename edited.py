import pprint
import exifread
import os
import shutil
from subprocess import call

DESTINATION_ROOT = '/Volumes/Pictures/testing/'
SOURCE_ROOT      = '/Volumes/Pictures/John L - 2020 12 30/'
PHOTOGRAPHER     = 'JohnL'

def moveAndUpdate(path, name, extension, year, month, date, time):
    epath = path + 'edited/'
    if extension == '.jpeg':
        destination = DESTINATION_ROOT + year + '/' + year + ' ' + month + '/' + PHOTOGRAPHER + '/' + name + extension
        
        print 'processing', epath + name + extension
        print epath + name + extension + ' -> ' + destination
        #return
    
        shutil.copyfile(epath + name + extension, destination)
        shutil.move(epath + name + extension, epath + 'done/' + name + extension) 
        
        command = 'SetFile -d "' + date + ' ' + time + '" "' + destination + '"'
        call(command, shell=True)
        command = 'SetFile -m "' + date + ' ' + time + '" "' + destination + '"'
        call(command, shell=True)
    
def updateFile(path, file, name):
    epath = path + 'edited/'
    f = open(epath + file, 'rb')
    
    # Extract the create date and time tag from image
    try:
        tags = exifread.process_file(f)
    except:
        print 'error'
        shutil.move(epath + file, epath + 'error/' + file)
        f.close()
        return
    f.close()

    if 'EXIF DateTimeOriginal' not in tags:
        shutil.move(path + file, path + 'skipped/' + file)        
        return
 
    originalDate = str(tags['EXIF DateTimeOriginal'])
    date = originalDate[0:10].replace(':','/')
    year = date[0:4]
    month = date[5:7]
    day = date[8:]
    date = month+'/'+day+'/'+year
    time = originalDate[11:]

    # Create destination directories
    if not os.path.exists(DESTINATION_ROOT + year):
        os.makedirs(DESTINATION_ROOT + year)
    
    if not os.path.exists(DESTINATION_ROOT + year + '/' + year + ' ' + month):
        os.makedirs(DESTINATION_ROOT + year + '/' + year + ' ' + month)

    if not os.path.exists(DESTINATION_ROOT + year + '/' + year + ' ' + month + '/' + PHOTOGRAPHER):
        os.makedirs(DESTINATION_ROOT + year + '/' + year + ' ' + month + '/' + PHOTOGRAPHER)

    if not os.path.exists(DESTINATION_ROOT + year + '/' + year + ' ' + month + '/' + PHOTOGRAPHER + '/other'):
        os.makedirs(DESTINATION_ROOT + year + '/' + year + ' ' + month + '/' + PHOTOGRAPHER + '/other')

    # Update and move jpeg
    moveAndUpdate(path, name, '.jpeg', year, month, date, time)
    
dirs = os.listdir(SOURCE_ROOT + '/edited/')
for file in dirs:
    name, extension = os.path.splitext(file)
    print '*********************', name + extension
    if (extension == '.jpeg'):
        updateFile(SOURCE_ROOT, file, name)
