import json
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./hcp_crm.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class HCPInteraction(Base):
    __tablename__ = "hcp_interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcpName = Column(String, default="")
    specialty = Column(String, default="")
    organization = Column(String, default="")
    interactionType = Column(String, default="")
    interactionDate = Column(String, default="")
    interactionTime = Column(String, default="")
    location = Column(String, default="")
    duration = Column(String, default="")
    
    # Store list fields as JSON strings in the database
    _productsDiscussed = Column("productsDiscussed", Text, default="[]")
    _topicsDiscussed = Column("topicsDiscussed", Text, default="[]")
    _materialsShared = Column("materialsShared", Text, default="[]")
    _samplesDistributed = Column("samplesDistributed", Text, default="[]")
    _questionsRaised = Column("questionsRaised", Text, default="[]")
    _objections = Column("objections", Text, default="[]")
    
    followUpDate = Column(String, default="")
    sentiment = Column(String, default="")
    interactionOutcome = Column(String, default="")
    summary = Column(Text, default="")

    @property
    def productsDiscussed(self):
        try:
            return json.loads(self._productsDiscussed or "[]")
        except Exception:
            return []

    @productsDiscussed.setter
    def productsDiscussed(self, value):
        self._productsDiscussed = json.dumps(value or [])

    @property
    def topicsDiscussed(self):
        try:
            return json.loads(self._topicsDiscussed or "[]")
        except Exception:
            return []

    @topicsDiscussed.setter
    def topicsDiscussed(self, value):
        self._topicsDiscussed = json.dumps(value or [])

    @property
    def materialsShared(self):
        try:
            return json.loads(self._materialsShared or "[]")
        except Exception:
            return []

    @materialsShared.setter
    def materialsShared(self, value):
        self._materialsShared = json.dumps(value or [])

    @property
    def samplesDistributed(self):
        try:
            return json.loads(self._samplesDistributed or "[]")
        except Exception:
            return []

    @samplesDistributed.setter
    def samplesDistributed(self, value):
        self._samplesDistributed = json.dumps(value or [])

    @property
    def questionsRaised(self):
        try:
            return json.loads(self._questionsRaised or "[]")
        except Exception:
            return []

    @questionsRaised.setter
    def questionsRaised(self, value):
        self._questionsRaised = json.dumps(value or [])

    @property
    def objections(self):
        try:
            return json.loads(self._objections or "[]")
        except Exception:
            return []

    @objections.setter
    def objections(self, value):
        self._objections = json.dumps(value or [])

    def to_dict(self):
        return {
            "hcpName": self.hcpName or "",
            "specialty": self.specialty or "",
            "organization": self.organization or "",
            "interactionType": self.interactionType or "",
            "interactionDate": self.interactionDate or "",
            "interactionTime": self.interactionTime or "",
            "location": self.location or "",
            "duration": self.duration or "",
            "productsDiscussed": self.productsDiscussed,
            "topicsDiscussed": self.topicsDiscussed,
            "materialsShared": self.materialsShared,
            "samplesDistributed": self.samplesDistributed,
            "questionsRaised": self.questionsRaised,
            "objections": self.objections,
            "followUpDate": self.followUpDate or "",
            "sentiment": self.sentiment or "",
            "interactionOutcome": self.interactionOutcome or "",
            "summary": self.summary or ""
        }

Base.metadata.create_all(bind=engine)

def get_current_interaction():
    db = SessionLocal()
    try:
        interaction = db.query(HCPInteraction).filter_by(id=1).first()
        if not interaction:
            interaction = HCPInteraction(id=1)
            db.add(interaction)
            db.commit()
            db.refresh(interaction)
        return interaction.to_dict()
    finally:
        db.close()

def update_current_interaction(data: dict):
    db = SessionLocal()
    try:
        interaction = db.query(HCPInteraction).filter_by(id=1).first()
        if not interaction:
            interaction = HCPInteraction(id=1)
            db.add(interaction)
        
        # Update fields
        for key, value in data.items():
            if key in ["productsDiscussed", "topicsDiscussed", "materialsShared", "samplesDistributed", "questionsRaised", "objections"]:
                setattr(interaction, key, value)
            elif hasattr(interaction, key):
                setattr(interaction, key, value or "")
                
        db.commit()
        db.refresh(interaction)
        return interaction.to_dict()
    finally:
        db.close()

def reset_current_interaction():
    db = SessionLocal()
    try:
        interaction = db.query(HCPInteraction).filter_by(id=1).first()
        if interaction:
            db.delete(interaction)
            db.commit()
        
        new_interaction = HCPInteraction(id=1)
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        return new_interaction.to_dict()
    finally:
        db.close()
