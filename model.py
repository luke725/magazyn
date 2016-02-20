from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker, relationship

Base = declarative_base()

class Treatment(Base):
  __tablename__ = 'treatments'

  id = Column(Integer, primary_key=True)
  is_current = Column(Boolean, nullable=False)

  equipment_usages = relationship("EquipmentUsage", back_populates="treatment")

  def __init__(self, is_current=False):
    self.is_current = is_current

  def __repr__(self):
    return "Treatment(%d)" % (self.id)
    
  def find_usage(self, equipment_id):
    for usage in self.equipment_usages:
      if usage.equipment_id == equipment_id:
        return usage
    return None
    
  def add_usage(self, equipment_id, amount=0):
    usage = self.find_usage(equipment_id)
    if usage is not None:
      usage.amount_used += amount
    else:
      usage = EquipmentUsage(equipment_id=equipment_id, amount_used=amount)
      self.equipment_usages.append(usage)

class Equipment(Base):
  __tablename__ = 'equipments'

  id = Column(Integer, primary_key=True)
  amount_available = Column(Integer, nullable=False)
  
  equipment_usages = relationship("EquipmentUsage", back_populates="equipment")

  def __init__(self, id, amount_available=0):
    self.id = id
    self.amount_available = amount_available

  def __repr__(self):
    return "Equipment(%d, %d)" % (self.id, self.amount_available)
    
  def decrease_amount(self, amount):
    self.amount_available -= amount
        
class EquipmentUsage(Base):
    __tablename__ = 'equipment_usages'

    treatment_id = Column(Integer, ForeignKey('treatments.id'), primary_key=True)
    equipment_id = Column(Integer, ForeignKey('equipments.id'), primary_key=True)
    amount_used = Column(Integer, nullable=False)
    
    treatment = relationship("Treatment", back_populates="equipment_usages")
    equipment = relationship("Equipment", back_populates="equipment_usages")

    def __repr__(self):
        return "EquipmentUsage(%d, %d, %d)" % (self.treatment_id, self.equipment_id, self.amount_used)

engine = create_engine('mysql+mysqldb://sql2107606:tU2!bP4%@sql2.freemysqlhosting.net/sql2107606', echo=False)
Base.metadata.create_all(engine)
SessionBase = sessionmaker(bind=engine)

class Session():
  session = SessionBase()
  
  def __get_current_or_none(self):
    return self.session.query(Treatment).filter_by(is_current=True).first()
    
  def __free_current(self):
    current_treatment = self.__get_current_or_none()
    if current_treatment is not None:
      current_treatment.is_current = False

  def __create_new_current_no_free(self):
    current_treatment = Treatment(is_current=True)
    self.session.add(current_treatment)
    return current_treatment

  def create_new_current(self):
    self.__free_current()
    return Treatment.__create_new_current_no_free()
    
  def get_current_or_create(self):
    current_treatment = self.__get_current_or_none()
    if current_treatment is None:
      return self.__create_new_current_no_free()
    else:
      return current_treatment
  
  def set_as_current(self, treatment):
    self.__free_current()
    treatment.is_current = True
    
  def find_equipment(self, equipment_id):
    return self.session.query(Equipment).filter_by(id=equipment_id).first()
    
  def find_equipment_or_create(self, equipment_id):
    equipment = self.find_equipment(equipment_id)
    if equipment is None:
      equipment = Equipment(equipment_id, 100)
      self.session.add(equipment)
    return equipment
    
  def all_equipment(self):
    return self.session.query(Equipment).all()

  def add_usage(self, equipment_id, usage):
    equipment = self.find_equipment_or_create(equipment_id)
    self.get_current_or_create().add_usage(equipment_id, usage)
    equipment.decrease_amount(usage)
    
  def update_equipment(self, equipment_id, amount_available):
    equipment = self.find_equipment(equipment_id)
    equipment.amount_available = amount_available
    
  def begin(self):
    return self.session.begin()
