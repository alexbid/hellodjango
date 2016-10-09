import datetime
import glob
import os

class archiveCleaning:
    def __init__(self, root, ext, path):
        self.path = path
        self.ext = ext
        self.root = root
        self.dt_today = datetime.datetime.utcnow()
        listFiles = self.getDateList(glob.glob(path + root + "*" + ext))
        
        years = set()
        for datel in listFiles:
            years.add(datel.year)
        
        months = set()
        for datel in listFiles:
            if self.dt_today.year == datel.year:
                months.add(datel.month)
        
        datesToKeep = []
        for item in years:
            datesToKeep.append(self.maxDate(self.getMaxField(listFiles, 'year', item)))
        for item in months:
            datesToKeep.append(self.maxDate(self.getMaxField(listFiles, 'month', item)))
            datesToKeep = datesToKeep + self.currMonth(listFiles)
        
        self.datesToKeep = list(sorted(set(datesToKeep)))
        self.Alldates = list(sorted(set(listFiles)))
        self.datesToDelete = list(set(listFiles) - set(datesToKeep))
    
    def maxDate(self, listDate):
        buffDate = datetime.datetime(1900, 1, 1, 0, 0, 0)
        for item in listDate:
            if item > buffDate:
                buffDate = item
        return buffDate

    def getDateList(self, listFiles):
        dateList = []
        for item in listFiles:
            buffDate = item.replace(self.path, '').replace(self.root, '').replace(self.ext, '')
            dt_date = datetime.datetime.strptime(buffDate, '%Y%m%d')
            dateList.append(dt_date)
        return dateList

    def currMonth(self, dateList):
        rt_dates = []
        for dt_date in dateList:
            if (dt_date.year == self.dt_today.year) and (dt_date.month == self.dt_today.month):
                rt_dates.append(dt_date)
        return rt_dates

    def getMaxField(self, dateList, field, item):
        dt_dict = {}
        if field == 'year':
            for dt_date in dateList:
                if dt_dict.has_key(dt_date.year):
                    buff2 = []
                    buff2 = dt_dict[dt_date.year]
                    buff2.append(dt_date)
                    dt_dict[dt_date.year] = buff2
                else:
                    buff = []
                    buff.append(dt_date)
                    dt_dict[dt_date.year] = buff
        if field == 'month':
            for dt_date in dateList:
                if self.dt_today.year == dt_date.year:
                    if dt_dict.has_key(dt_date.month):
                        buff2 = []
                        buff2 = dt_dict[dt_date.month]
                        buff2.append(dt_date)
                        dt_dict[dt_date.month] = buff2
                    else:
                        buff = []
                        buff.append(dt_date)
                        dt_dict[dt_date.month] = buff

        if dt_dict.has_key(item) : return dt_dict[item]
        else: return []

    def getFilesToDelete(self):
        for item in self.datesToDelete:
            fyle = self.path + self.root + item.strftime('%Y%m%d') + self.ext
            print fyle
#            os.remove(fyle)

if __name__=='__main__':
    
    toDo = {'DropboxKate_': '.tar.gz', 'volume1Kate_': '.tar.gz', 'GdriveKate_': '.tar.bz2', 'Dropbox_': '.tar.gz', 'Gdrive_': '.tar.bz2'}
    for root,ext in toDo.iteritems():
        ac = archiveCleaning(root, ext, '/Volumes/Archives/')
#        print ac.datesToDelete
        ac.getFilesToDelete()




