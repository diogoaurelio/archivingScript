#Work with directories
import os
#Timing
import time

#read AWS credentials
import yaml

class Archiving(object):
	def __init__(self, email, password):

	def _GetFileDate(self, file_name):
		match = re.search('.*\.([a-zA-Z]{3,}$)', file_name)
    	if match:
      		return match.group(1).upper()
    	return False

    def _backupLog(self, updateText):
    	""" Function used to log every new comment related to a specific File Archiving."""
    	aFile = "archive_log.txt"
    	os.rename( aFile, aFile+"~")
    	destination= open( aFile, "w" )
    	source= open( aFile+"~", "r" )
    	for line in source:
      		destination.write( line )
    	destination.write( str(updateText))
    	source.close()
    	destination.close()
    	os.remove(aFile+"~")
  	
  	def Run(self):
    """Executes the upload function."""
    	self._backupLog('\n' + 'Backup date: ' + str(time.strftime("%d/%m/%Y")) + '\n' )
    	self._backupLog('Backup Starting Time: ' + str(time.strftime("%H:%M:%S")) + '\n' )
    	self._FilesToUpload()
    	self._backupLog('\n' + 'Backup Ending Time: ' + str(time.strftime("%H:%M:%S")) + '\n' )
    	mypath = os.getcwd()


    def move(src,dst):
        src = "/path/to/your/source/directory"
        dst = "/path/to/your/destination/directory/"
        listOfFiles = os.listdir(src)
        for f in listOfFiles:
                fullPath = src + "/" + f
                os.system ("mv"+ " " + src + " " + dst)

def main():
	stream = file('env.yml', 'r')
  	dict_ = yaml.load(stream)
  	myVars = {}
  	for i in dict_:
    	myVars[i] = dict_[i]

  	user = myVars['list1']['account']
  	pw = myVars['list1']['passwd']
  	#key = ''

if __name__ == '__main__':
  main()