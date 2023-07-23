from tabledirectionary import Tabledirectory, fontfile

class Cff(Tabledirectory):
    def __init__(self, fontfile):
        super().__init__(fontfile)
        for table in self.tableRecords:
            if table['tag'] == 'CFF ':
                self.cffoffset = table['offset']
                self.ptr = self.cffoffset
                self.endptr = table['offset'] + table['length']
    
    def get_header(self):
        self.major = int.from_bytes(self.fontfile[self.ptr:self.ptr+1],'big')
        self.ptr += 1
        self.major = int.from_bytes(self.fontfile[self.ptr:self.ptr+1],'big')
        self.ptr += 1
        self.hdrSize = int.from_bytes(self.fontfile[self.ptr:self.ptr+1],'big')
        self.ptr += 1
        self.offsize = int.from_bytes(self.fontfile[self.ptr:self.ptr+self.hdrSize],'big')
        self.ptr += self.hdrSize

cff = Cff(fontfile)
cff.get_header()
print(cff.major)