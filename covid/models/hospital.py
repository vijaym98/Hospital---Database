from data import Database
from models.patient import Patient
import datetime
import uuid

class Hospital(object):
    def __init__(self, controller, name, city, controller_id, _id=None):
        self.controller = controller
        self.controller_id = controller_id
        self.name = name
        self.city = city
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_patient(self, name, details, date=datetime.datetime.utcnow()):
        patient = Patient(hospital_id=self._id,
                    name=name,
                    details=details,
                    controller = self.controller,
                    created_date=date)
        patient.save_to_mongo()

    def get_patients(self):
        return Patient.from_hospital(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'controller': self.controller,
            'controller_id': self.controller_id,
            'name': self.name,
            'city': self.city,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):
        hospital_data = Database.find_one(collection='blogs',
                                      query={'_id': id})
        return cls(**hospital_data)

    @classmethod
    def find_by_controller_id(cls, controller_id):
        hospitals = Database.find(collection='blogs',
                              query={'controller_id': controller_id})
        return [cls(**hospital) for hospital in hospitals]
