import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref
from sqlalchemy.sql import func
from dotenv import load_dotenv
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

load_dotenv()

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    goals = relationship("Goal", back_populates="user")
    initiatives = relationship("QuarterlyInitiative", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, default=1)
    parent_id = Column(Integer, ForeignKey('goals.id'), nullable=True)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="goals")
    subgoals = relationship("Goal", backref=backref("parent", remote_side=[id]), cascade="all, delete-orphan")

class QuarterlyInitiative(Base):
    __tablename__ = 'quarterly_initiatives'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, default=1)
    quarter = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="initiatives")


# Helper function to get the current database URL
def get_db_url(db_path=None):
    """Returns the DATABASE_URL if set, otherwise falls back to sqlite via DATABASE_PATH."""
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    # Fallback to local sqlite
    if db_path is None:
        db_path = os.getenv("DATABASE_PATH", "goals.db")
    return f'sqlite:///{db_path}'

def _get_session(db_path=None):
    url = get_db_url(db_path)
    engine = create_engine(url, echo=False)
    Session = sessionmaker(bind=engine)
    return Session()

def init_db(db_path=None):
    """Initialize the database with required tables using SQLAlchemy."""
    url = get_db_url(db_path)
    engine = create_engine(url, echo=False)
    Base.metadata.create_all(engine)

# --- Users ---
def create_user(username, password, db_path=None):
    session = _get_session(db_path)
    # Check if user already exists
    existing = session.query(User).filter_by(username=username).first()
    if existing:
        session.close()
        return None

    new_user = User(username=username)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    user_id = new_user.id
    session.close()
    return user_id

def get_user_by_username(username, db_path=None):
    session = _get_session(db_path)
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user

def get_user_by_id(user_id, db_path=None):
    session = _get_session(db_path)
    user = session.get(User, int(user_id))
    session.close()
    return user

# --- Daily Goals ---
def add_goal(description, user_id=1, parent_id=None, db_path=None):
    session = _get_session(db_path)
    new_goal = Goal(description=description, user_id=user_id, parent_id=parent_id)
    session.add(new_goal)
    session.commit()
    goal_id = new_goal.id
    session.close()
    return goal_id

def list_pending_goals(user_id=1, db_path=None):
    session = _get_session(db_path)
    # Return as list of dictionaries to support nested subgoals natively
    goals = session.query(Goal).filter(Goal.status == 'pending', Goal.user_id == user_id, Goal.parent_id == None).all()

    def serialize_goal(g):
        return {
            "id": g.id,
            "description": g.description,
            "subgoals": [serialize_goal(sub) for sub in g.subgoals if sub.status == 'pending']
        }

    results = [serialize_goal(g) for g in goals]
    session.close()
    return results

def list_completed_goals(user_id=1, db_path=None):
    session = _get_session(db_path)
    # Return completed goals (flat list is usually fine for history)
    goals = session.query(Goal).filter(Goal.status == 'completed', Goal.user_id == user_id).order_by(Goal.id.desc()).all()

    results = [{
        "id": g.id,
        "description": g.description,
        "parent_id": g.parent_id
    } for g in goals]

    session.close()
    return results

def complete_goal(goal_id, user_id=1, db_path=None):
    session = _get_session(db_path)
    goal = session.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user_id).first()
    success = False
    if goal:
        goal.status = 'completed'
        session.commit()
        success = True
    session.close()
    return success

# --- Quarterly Initiatives ---
def add_initiative(quarter, description, user_id=1, db_path=None):
    session = _get_session(db_path)
    new_init = QuarterlyInitiative(quarter=quarter, description=description, user_id=user_id)
    session.add(new_init)
    session.commit()
    initiative_id = new_init.id
    session.close()
    return initiative_id

def list_pending_initiatives(user_id=1, db_path=None):
    session = _get_session(db_path)
    initiatives = session.query(QuarterlyInitiative)\
                         .filter(QuarterlyInitiative.status == 'pending', QuarterlyInitiative.user_id == user_id)\
                         .order_by(QuarterlyInitiative.quarter.asc())\
                         .all()
    results = [(i.id, i.quarter, i.description) for i in initiatives]
    session.close()
    return results

def complete_initiative(initiative_id, user_id=1, db_path=None):
    session = _get_session(db_path)
    initiative = session.query(QuarterlyInitiative).filter(QuarterlyInitiative.id == initiative_id, QuarterlyInitiative.user_id == user_id).first()
    success = False
    if initiative:
        initiative.status = 'completed'
        session.commit()
        success = True
    session.close()
    return success
