
import sys, os 
from os import walk
from os import listdir
from os.path import isfile, join
import shutil
import time
import getopt
import re #RegEx
#import yaml

class ArchiveFiles:
    def __init__(self, date):
        #Initializes a dict called job
        self.date = date

    def _backupLog(self, updateText):
    	""" Function used to log actions (copied files, deleted files, etc)."""
    	aFile = "archiving_log.txt"
    	os.rename( aFile, aFile+"~")
    	destination= open( aFile, "w" )
    	source= open( aFile+"~", "r" )
    	for line in source:
    		destination.write( line )
    	destination.write( str(updateText))
    	source.close()
    	destination.close()
    	os.remove(aFile+"~")

    # 2) Copy Data
	#Should copy data to other folder, and log the name of copied file into backup file
	#Should implement only to files with certain dates
    def _archiveData(self, src, dest):
    	"""Goes through files inside directory structure ."""
    	root = os.getcwd()
    	srcPath = join(root,src)
    	destPath = join(root,dest)
    	f = [] #Array with list of files to copy
    	s = [] #Array with list of files successfully copied
    	for (dirpath, dirnames, filenames) in walk(srcPath):
    		f.extend(filenames)
    		if len(f) > 0:
    			for i in f:
    				if str(i) != 'archiving_log.txt' and str(i) != 'archiving_log.txt~' and str(i) != 'archivingScript.py':
    					try:
    						buffer_size = int(20000)
    						fileSrcPath = join(dirpath, i)
    						fileDestPath = join(destPath, i)
    						with open(fileSrcPath, 'rb') as fsrc:
    							with open(fileDestPath, 'wb') as fdest:
    								copy = shutil.copyfileobj(fsrc,fdest,buffer_size)
    								copy
    								self._backupLog('Copy Operation File: '+str(i)+ '\t' + 'Time: '+ str(time.strftime("%H:%M:%S")) + '\t'+ 'Path: '+ str(srcPath)+'\n')
    								s.append(i)
    					except shutil.Error as e:
    						self._backupLog('Error: %s' % e + '\t' + 'File: '+str(i)+ '\t' + 'Time: '+ str(time.strftime("%H:%M:%S")) + '\n')
    					except IOError as e:
    						self._backupLog('Error: %s' % e.strerror  + '\t' + 'File: '+str(i)+ '\t' + 'Time: '+ str(time.strftime("%H:%M:%S")) + '\n')
    	if len(s) >0:
            for (dirpath,dirnames,filenames) in walk(srcPath):
                for cfile in f:
                    for sfile in s:
                        if cfile == sfile:
                            try:
                                filetoDelete = join(srcPath, cfile)
                                os.remove(filetoDelete)
                                self._backupLog('Delete Operation File: '+str(cfile)+ '\t' + 'Time: '+ str(time.strftime("%H:%M:%S")) + '\n')
                            except OSError, e:
                                self._backupLog('Error deleting file: %s - %s.' % (e.filename, e.strerror) + '\t' + 'Time: '+ str(time.strftime("%H:%M:%S")) + '\n')

    def _archiveDataByDate(self, src, dest):
        """Goes through files inside directory structure ."""
        root = os.getcwd()
        srcPath = join(root,src)
        destPath = join(root,dest)
        f = [] #Array with list of files in directory
        fDate = [] #Array with list of files with certain date;
        s = [] #Array with list of files successfully copied
        for (dirpath, dirnames, filenames) in walk(srcPath):
            f.extend(filenames)
            if len(f) > 0:
                for i in f:
                    match = re.search(r'\d{4}-\d{2}-\d{2}', i)
                    if str(i) != 'archiving_log.txt' and str(i) != 'archiving_log.txt~' and str(i) != 'archivingScript.py' and match.group() == self.date:
                        try:
                            buffer_size = int(20000)
                            fileSrcPath = join(dirpath, i)
                            fileDestPath = join(destPath, i)
                            with open(fileSrcPath, 'rb') as fsrc:
                                with open(fileDestPath, 'wb') as fdest:
                                    copy = shutil.copyfileobj(fsrc,fdest,buffer_size)
                                    copy
                                    self._backupLog('Copy Operation File: '+str(i)+ '\t' + 'Time: '+ str(time.strftime("%H:%M:%S")) +'\n') #+ '\t'+ 'Path: '+ str(srcPath)
                                    s.append(i)
                        except shutil.Error as e:
                            self._backupLog('Error: %s' % e + '\t' + 'File: '+str(i)+ '\t' + 'Time: '+ str(time.strftime("%H:%M:%S")) + '\n')
                        except IOError as e:
                            self._backupLog('Error: %s' % e.strerror  + '\t' + 'File: '+str(i)+ '\t' + 'Time: '+ str(time.strftime("%H:%M:%S")) + '\n')
        if len(s) >0:
            for (dirpath,dirnames,filenames) in walk(srcPath):
                for cfile in f:
                    for sfile in s:
                        if cfile == sfile:
                            try:
                                filetoDelete = join(srcPath, cfile)
                                os.remove(filetoDelete)
                                self._backupLog('Delete Operation File: '+str(cfile)+ '\t' + 'Time: '+ str(time.strftime("%H:%M:%S")) + '\n')
                            except OSError, e:
                                self._backupLog('Error deleting file: %s - %s.' % (e.filename, e.strerror) + '\t' + 'Time: '+ str(time.strftime("%H:%M:%S")) + '\n')
	

    def Run(self):
    	"""Executes the job."""
    	src = 'testFolder'
    	dest = 'testFolder2'
    	self._backupLog('\n' + 'Starting Archiving Job - Archiving Files of date: ' + str(time.strftime("%Y-%m-%d")) + '\n' )
    	self._backupLog('Archiving Job Start Time: ' + str(time.strftime("%H:%M:%S")) + '\n' )
    	self._archiveDataByDate(src,dest)
    	self._backupLog('\n' + 'Archiving Job End Time: ' + str(time.strftime("%H:%M:%S")) + '\n' )
    
    #End of Class ArchiveFiles

def main():
    """Main function of the script that executes all necessary functions."""
    today = str(time.strftime("%Y-%m-%d"))
    #today = '2014-10-25'
    date = today
    try:
    #User can specify himself the keys or let system read from local file.
        opts, args = getopt.getopt(sys.argv[1:], '', ['date='])
    except getopt.error, msg:
        print 'python archivingScript.py --date [dateToArchive]'
        sys.exit(2)

    for option, arg in opts:
        if option == '--date':
            date = arg
        

    job = ArchiveFiles(date)
    job.Run()

if __name__ == '__main__':
	main()
