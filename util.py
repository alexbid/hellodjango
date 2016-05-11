import os.path
import shutil

path1 = '//lapetitemaison/LaPetiteMaison/Nouveau dossier/IT/software/Raspberry Pi/RECOVERY_INIT'
path2 = '/cygdrive/f'
#path2 = '/cygdrive/f/RECOVERY_INIT'
#path1 = '/cygdrive/j'
#path2 = '//lapetitemaison/LaPetiteMaison/Nouveau dossier'


class DirectoryLister:

	rootPath = ''
	
	def __init__(self, DirName):

		self.rootPath = DirName
		self.files = []

		os.path.walk(DirName, self.CallBack, None)

	def CallBack(self, args, dirname, filenames):
		path = ''

		for filename in filenames:
			path = os.path.join(dirname, filename)
			if os.path.isfile(path):
				#print path.replace(dirname, '')
				self.files.append(path.replace(self.rootPath, ''))

print "1"
source = DirectoryLister(path1)
print "2"
target = DirectoryLister(path2)
print "3"
todo = list(set(source.files) - set(target.files))
print "4"
errorList = []

if len(todo) > 0:
	i = 1
	for file in todo:
		folder = (path2 + file).replace(file.split('/')[-1],'')[:-1]
		print folder
		if not os.path.exists(folder): os.makedirs(folder)
		print "copying file => ", i, "/", len(todo), path1 + file
		try: shutil.copy2(path1 + file, path2 + file)
		except: errorList.append(path1 + file)
		i += 1
else: print "no file to copy...."
if len(errorList) > 0: print "error with the files: ", errorList