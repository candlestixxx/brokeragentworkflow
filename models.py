import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class QuarterlyInitiative(Base):
    __tablename__ = 'quarterly_initiatives'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quarter = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Helper function to get the current engine / session factory
def get_db_path():
    return os.getenv("DATABASE_PATH", "goals.db")

def _get_session(db_path=None):
    if db_path is None:
        db_path = get_db_path()
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Session = sessionmaker(bind=engine)
    return Session()

def init_db(db_path=None):
    """Initialize the database with required tables using SQLAlchemy."""
    if db_path is None:
        db_path = get_db_path()
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)

# --- Daily Goals ---
def add_goal(description, db_path=None):
    session = _get_session(db_path)
    new_goal = Goal(description=description)
    session.add(new_goal)
    session.commit()
    goal_id = new_goal.id
    session.close()
    return goal_id

def list_pending_goals(db_path=None):
    session = _get_session(db_path)
    # Return as tuples (id, description) to maintain backwards compatibility
    # with the rest of the application that expects a tuple like (1, 'do laundry')
    goals = session.query(Goal).filter(Goal.status == 'pending').all()
    results = [(g.id, g.description) for g in goals]
    session.close()
    return results

def complete_goal(goal_id, db_path=None):
    session = _get_session(db_path)
    goal = session.query(Goal).filter(Goal.id == goal_id).first()
    success = False
    if goal:
        goal.status = 'completed'
        session.commit()
        success = True
    session.close()
    return success

# --- Quarterly Initiatives ---
def add_initiative(quarter, description, db_path=None):
    session = _get_session(db_path)
    new_init = QuarterlyInitiative(quarter=quarter, description=description)
    session.add(new_init)
    session.commit()
    initiative_id = new_init.id
    session.close()
    return initiative_id

def list_pending_initiatives(db_path=None):
    session = _get_session(db_path)
    # Return as tuples (id, quarter, description) to maintain backwards compatibility
    initiatives = session.query(QuarterlyInitiative)\
                         .filter(QuarterlyInitiative.status == 'pending')\
                         .order_by(QuarterlyInitiative.quarter.asc())\
                         .all()
    results = [(i.id, i.quarter, i.description) for i in initiatives]
    session.close()
    return results

def complete_initiative(initiative_id, db_path=None):
    session = _get_session(db_path)
    initiative = session.query(QuarterlyInitiative).filter(QuarterlyInitiative.id == initiative_id).first()
    success = False
    if initiative:
        initiative.status = 'completed'
        session.commit()
        success = True
    session.close()
    return success
