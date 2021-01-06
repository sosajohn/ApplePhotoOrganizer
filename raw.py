import xmltodict
import os
import shutil
from dateutil.parser import parse
from subprocess import call

SOURCE_ROOT      = '/Volumes/Pictures/John L - 2020 12 30/raw/'
DESTINATION_ROOT = '/Volumes/Pictures/testing/'
PHOTOGRAPHER     = 'JohnL'

def fixFilename(name):
    name = name.replace(' ','\ ')
    name = name.replace('(', '\(')
    name = name.replace(')', '\)')
    return name

def moveAndUpdate(filename, year, month, date, time):
    destination = DESTINATION_ROOT + year + '/' + year + ' ' + month + '/' + PHOTOGRAPHER + '/other/'
    
    shutil.copyfile(SOURCE_ROOT + filename, destination + filename)
    shutil.move(SOURCE_ROOT + filename, SOURCE_ROOT + 'done/' + filename) 

    command = 'SetFile -d "' + date + ' ' + time + '" ' + fixFilename(destination + filename)
    call(command, shell=True)
    command = 'SetFile -m "' + date + ' ' + time + '" ' + fixFilename(destination + filename)
    call(command, shell=True)
    
def processFiles(data):
    for file in data:
        if 'createDate' in data[file]:
            date = data[file]['createDate']['date']
            time = data[file]['createDate']['time']
            year = data[file]['createDate']['year']
            month = data[file]['createDate']['month']
            
            # Create destination directories
            if not os.path.exists(DESTINATION_ROOT + year):
                os.makedirs(DESTINATION_ROOT + year)
            
            if not os.path.exists(DESTINATION_ROOT + year + '/' + year + ' ' + month):
                os.makedirs(DESTINATION_ROOT + year + '/' + year + ' ' + month)
        
            if not os.path.exists(DESTINATION_ROOT + year + '/' + year + ' ' + month + '/' + PHOTOGRAPHER):
                os.makedirs(DESTINATION_ROOT + year + '/' + year + ' ' + month + '/' + PHOTOGRAPHER)
        
            if not os.path.exists(DESTINATION_ROOT + year + '/' + year + ' ' + month + '/' + PHOTOGRAPHER + '/other'):
                os.makedirs(DESTINATION_ROOT + year + '/' + year + ' ' + month + '/' + PHOTOGRAPHER + '/other')
    
            for filename in data[file]['files']:
                print 'updating', filename, date, time
                moveAndUpdate(filename, year, month, date, time)

def getCreateDate(data, filename, baseName):
    if os.path.exists(SOURCE_ROOT + filename):
        f = open(SOURCE_ROOT + filename, 'rb')
    else:
        print 'error'
        return
    
    tags = xmltodict.parse(f.read())
    f.close()

    parsedDate = parse(tags['x:xmpmeta']['rdf:RDF']['rdf:Description']['photoshop:DateCreated'],ignoretz=False)
    date = str(parsedDate.strftime('%m/%d/%Y'))
    year = parsedDate.strftime('%Y')
    month = parsedDate.strftime('%m')
    time = str(parsedDate.time())

    data[baseName]['createDate'] = {'date':date, 'time':time, 'year':year, 'month':month}
    return data

def main():
    dirs = os.listdir(SOURCE_ROOT)
    data = {}
    for filename in dirs:
        baseName, extension = os.path.splitext(filename)
        if baseName in data:
            if 'files' not in data[baseName]:
                data[baseName]['files'] = [filename]
            else:
                data[baseName]['files'].append(filename)
        else:
            data[baseName] = {'files':[filename]}
            
        if (extension == '.xmp'):
            print 'processing', baseName + extension
            data = getCreateDate(data, filename, baseName)
    
    # Create done directory where processed files will be moved to.
    if not os.path.exists(SOURCE_ROOT + 'done/'):
        os.makedirs(SOURCE_ROOT + 'done/')
    
    processFiles(data)

if __name__ == '__main__':
    main()