from . import db

class User(db.Model):
    __tablename__ = 'profiles'
    id=db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
    userimage=db.Column(db.String(256))
    username=db.Column(db.String(256),unique=True)
    userfname=db.Column(db.String(256))
    userlname=db.Column(db.String(256))
    biography=db.Column(db.String(400))
    userage=db.Column(db.Integer)
    usersex=db.Column(db.String(10))
    useraddon=db.Column(db.DateTime,nullable=False)
    
    def __init__(self,userimage,username,userfname,userlname,biography,userage,usersex,useraddon):
        self.userimage = userimage
        self.username = username
        self.userfname = userfname
        self.userlname = userlname
        self.biography = biography
        self.userage = userage
        self.usersex = usersex
        self.useraddon=useraddon
        
        
    def __repr__(self):
        return '<id {}>'.format(self.id)
