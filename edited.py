import exifread
import os
import shutil
from subprocess import call

SOURCE_ROOT      = '/Volumes/Pictures/Elein - 2021 01 07/edited/'
DESTINATION_ROOT = '/Volumes/Pictures/Pictures/'
PHOTOGRAPHER     = 'Elein'

def moveAndUpdate(name, extension, year, month, date, time):
    if extension == '.jpeg':
        destination = DESTINATION_ROOT + year + '/' + year + ' ' + month + '/' + PHOTOGRAPHER + '/' + name + extension
        
        print 'processing', SOURCE_ROOT + name + extension
        print SOURCE_ROOT + name + extension + ' -> ' + destination
    
        shutil.copyfile(SOURCE_ROOT + name + extension, destination)
        shutil.move(SOURCE_ROOT + name + extension, SOURCE_ROOT + 'done/' + name + extension) 
        
        command = 'SetFile -d "' + date + ' ' + time + '" "' + destination + '"'
        call(command, shell=True)
        command = 'SetFile -m "' + date + ' ' + time + '" "' + destination + '"'
        call(command, shell=True)
    
def updateFile(file, name):
    f = open(SOURCE_ROOT + file, 'rb')
    
    # Extract the create date and time tag from image
    try:
        tags = exifread.process_file(f)
    except:
        print 'error'
        shutil.move(SOURCE_ROOT + file, SOURCE_ROOT + 'error/' + file)
        f.close()
        return
    f.close()

    if 'EXIF DateTimeOriginal' not in tags:
        shutil.move(SOURCE_ROOT + file, SOURCE_ROOT + 'skipped/' + file)        
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
    moveAndUpdate(name, '.jpeg', year, month, date, time)

def main():
    # Create done directory where processed files and files with errors will be moved to.
    if not os.path.exists(SOURCE_ROOT + 'done/'):
        os.makedirs(SOURCE_ROOT + 'done/')
    
    if not os.path.exists(SOURCE_ROOT + 'error/'):
        os.makedirs(SOURCE_ROOT + 'error/')
    
    if not os.path.exists(SOURCE_ROOT + 'skipped/'):
        os.makedirs(SOURCE_ROOT + 'skipped/')
    
    dirs = os.listdir(SOURCE_ROOT)
    for file in dirs:
        name, extension = os.path.splitext(file)
        print '*********************', name + extension
        if (extension == '.jpeg'):
            updateFile(file, name)

if __name__ == '__main__':
    main()