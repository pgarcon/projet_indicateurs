class UserFileJSON:
    def __init__(self, ID, User, IDForum, IDMsg, Filenameo, Filenamer, Filetype, Filesize, Dateupload, Timeupload, Date_la, Time_la, Nbdownload, Filestatus):
        self.ID = ID
        self.User = User
        self.IDForum = IDForum
        self.IDMsg = IDMsg
        self.Filenameo = Filenameo
        self.Filenamer = Filenamer
        self.Filetype = Filetype
        self.Filesize = Filesize
        self.Dateupload = Dateupload
        self.Timeupload = Timeupload
        self.Date_la = Date_la
        self.Time_la = Time_la
        self.Nbdownload = Nbdownload
        self.Filestatus = Filestatus

    def __str__(self):
        return f"ID: {self.ID}, User: {self.User}, IDForum: {self.IDForum}, IDMsg: {self.IDMsg}, Filenameo: {self.Filenameo}, Filenamer: {self.Filenamer}, Filetype: {self.Filetype}, Filesize: {self.Filesize}, Dateupload: {self.Dateupload}, Timeupload: {self.Timeupload}, Date_la: {self.Date_la}, Time_la: {self.Time_la}, Nbdownload: {self.Nbdownload}, Filestatus: {self.Filestatus}"
