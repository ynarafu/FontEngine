fontfile = open('FOT-TsukuGoPr5-D.otf', 'rb')
fontfile = fontfile.read()

class Tabledirectory():
    def __init__(self, fontfile):
        self.fontfile = fontfile
        self.sfnt = self.fontfile[0:4].decode('unicode-escape')
        self.numTables = int.from_bytes(self.fontfile[4:6],'big')
        self.searchRange = int.from_bytes(self.fontfile[6:8],'big')
        self.entrySelector = int.from_bytes(self.fontfile[8:10],'big')
        self.rangeShift = int.from_bytes(self.fontfile[10:12],'big')
        self.ptr = 12
        self.tableRecords = []
        for i in range(self.numTables):
            self.table = {'tag':self.fontfile[self.ptr:self.ptr+4].decode('unicode-escape'),
                          'checksum':int.from_bytes(self.fontfile[self.ptr+4:self.ptr+8],'big'),
                          'offset':int.from_bytes(self.fontfile[self.ptr+8:self.ptr+12],'big'),
                          'length':int.from_bytes(self.fontfile[self.ptr+12:self.ptr+16],'big')}
            self.tableRecords.append(self.table)
            self.ptr += 16


font=Tabledirectory(fontfile)
for table in font.tableRecords:
    print(table)