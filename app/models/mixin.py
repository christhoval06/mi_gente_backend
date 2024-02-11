from . import db

class CRUD():
    def update(self, **kwargs):
        if self.id is not None:
            for key in kwargs:
                if key in self.__table__.columns:
                     setattr(self, key, kwargs.get(key))
            
            db.session.add(self)
            db.session.commit()
            return self
        
    def save(self):
        if self.id == None:
            db.session.add(self)
            return db.session.commit()

    def destroy(self):
        db.session.delete(self)
        return db.session.commit()
     

class AppModel(db.Model, CRUD):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now(), onupdate=db.func.now())
