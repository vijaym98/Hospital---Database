from data import Database
import uuid
import datetime

class Patient(object):

    def __init__(self, hospital_id, name, details, controller, created_date=datetime.datetime.utcnow(), _id=None):
        self.hospital_id = hospital_id
        self.name = name
        self.details = details
        self.controller = controller
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'hospital_id': self.hospital_id,
            'controller': self.controller,
            'details': self.details,
            'name': self.name,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, id):
        patient_data = Database.find_one(collection='posts', query={'_id': id})
        return cls(**patient_data)

    @staticmethod
    def from_hospital(id):
        return [patient for patient in Database.find(collection='posts', query={'hospital_id': id})]