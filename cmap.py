from tabledirectionary import Tabledirectory, fontfile

class Cmap(Tabledirectory):
    def __init__(self, fontfile):
        super().__init__(fontfile)
        for table in self.tableRecords:
            if table['tag'] == 'cmap':
                self.cmapoffset = table['offset']
                self.ptr = self.cmapoffset
                self.endptr = table['offset'] + table['length']
        self.cmapversion = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
        self.ptr += 2
        self.cmapnumTables = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
        self.ptr += 2
        self.encodingTables = []
        for i in range(self.cmapnumTables):
            self.table = {'platformID':int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big'),
                          'encodingID':int.from_bytes(self.fontfile[self.ptr+2:self.ptr+4],'big'),
                          'offset':int.from_bytes(self.fontfile[self.ptr+4:self.ptr+8],'big')}
            self.encodingTables.append(self.table)
            self.ptr += 8


# glyphIDAllayを取得,platformID=0(unicode),enodingID=3(BMP)
    def getsubtalbe(self):
        for etable in self.encodingTables:
            if etable['platformID'] == 0 and etable['encodingID'] == 3:
                self.BMPoffset = etable['offset']
                self.ptr = self.BMPoffset + self.cmapoffset
                break
        self.format = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
        self.ptr += 2
        if self.format == 4:
            self.endCode = []
            self.startCode = []
            self.idDelta = []
            self.idRangeOffsets = []
            self.glyphIDArray = []
            self.length = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            self.language = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            self.segCountX2 = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            self.searchRange = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            self.entrySelector = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            self.rangeShift = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            for i in range(self.segCountX2//2):
                self.endCode.append(int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big'))
                self.ptr += 2
            self.reservedPad = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            for i in range(self.segCountX2//2):
                self.startCode.append(int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big'))
                self.ptr += 2
            for i in range(self.segCountX2//2):
                self.idDelta.append(int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big'))
                self.ptr += 2
            for i in range(self.segCountX2//2):
                self.idRangeOffsets.append(int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big'))
                self.ptr += 2
            while(self.ptr < self.BMPoffset + self.cmapoffset + self.length):
                self.glyphIDArray.append(int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big'))
                self.ptr += 2
        else:
            print('対応していないサブテーブルフォーマットです。現在Format4のみ対応')
        return self.glyphIDArray

# ユニコードに応じたGIDを取得,platformID=0(unicode),enodingID=3(BMP)
    def getGID(self, code):
        for table in self.encodingTables:
            if table['platformID'] == 0 and table['encodingID'] == 3:
                self.BMPoffset = table['offset']
                self.ptr = self.BMPoffset + self.cmapoffset
                break
        self.format = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
        self.ptr += 2
        if self.format == 4:
            self.length = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            self.language = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            self.segCountX2 = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            self.searchRange = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            self.entrySelector = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            self.rangeShift = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            self.ptr += 2
            for i in range(self.segCountX2//2):
                self.endCode = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
                if self.endCode >= code:
                    break
                self.ptr += 2
            self.ptr +=  self.segCountX2 + 2
            self.startCode = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
            if code < self.startCode:
                self.gid = 0
            else:
                self.ptr += self.segCountX2
                self.idDelta = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
                self.ptr += self.segCountX2
                self.idRangeOffsets = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
                if self.idRangeOffsets == 0:
                    self.gid = (code + self.idDelta) & 0xFFFF
                else:
                    self.ptr += self.idRangeOffsets + (code - self.startCode) * 2
                    self.gid = int.from_bytes(self.fontfile[self.ptr:self.ptr+2],'big')
        else:
            print('対応していないサブテーブルフォーマットです。現在Format4のみ対応')

        return self.gid

code = 0x6962

cmap = Cmap(fontfile)

print(cmap.getGID(code))

