
import sys, os 
from os import walk
from os import listdir
from os.path import isfile, join
import shutil
import time
import getopt
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
    	# 3) Delete only files that have been successfully copied:
		# if len(s) > 0:
  #           for (dirpath, dirnames, filenames) in walk(srcPath):
  #               for cfile in f:
		# 		    for sfile in s:
		# 			#fileSrcPath = join(dirpath, j)
		# 			   if cfile == sfile:
		# 				#print(str(k))
  #                       #self._backupLog('File to delete: '+str(k)+'\n')
  #                       #self._backupLog( str(os.chdir(srcPath)) )
  #                       #os.chdir(srcPath).remove(j)
  #                       self._backupLog('Delete Operation File: '+str(cfile)+ '\t' + 'Time: '+ str(time.strftime("%H:%M:%S")))

	

    def Run(self):
    	"""Executes the job."""
    	src = 'testFolder'
    	dest = 'testFolder2'
    	self._backupLog('\n' + 'Archiving date: ' + str(time.strftime("%d/%m/%Y")) + '\n' )
    	self._backupLog('Archiving Start Time: ' + str(time.strftime("%H:%M:%S")) + '\n' )
    	self._archiveData(src,dest)
    	self._backupLog('\n' + 'Archiving End Time: ' + str(time.strftime("%H:%M:%S")) + '\n' )
    
    #End of Class ArchiveFiles

def main():
	"""Main function of the script that executes all necessary functions."""
	today = str(time.strftime("%d/%m/%Y"))
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
