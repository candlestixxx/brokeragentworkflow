import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref
from sqlalchemy.sql import func
from dotenv import load_dotenv
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

load_dotenv()

Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    notifications_enabled = Column(Boolean, nullable=False, default=True)

    goals = relationship("Goal", back_populates="user")
    initiatives = relationship("QuarterlyInitiative", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, default=1)
    parent_id = Column(Integer, ForeignKey("goals.id"), nullable=True)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="goals")
    subgoals = relationship(
        "Goal",
        backref=backref("parent", remote_side=[id]),
        cascade="all, delete-orphan",
    )


class QuarterlyInitiative(Base):
    __tablename__ = "quarterly_initiatives"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, default=1)
    quarter = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
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
    return f"sqlite:///{db_path}"


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


def update_user_avatar(user_id, avatar_url, db_path=None):
    session = _get_session(db_path)
    user = session.get(User, int(user_id))
    success = False
    if user:
        user.avatar_url = avatar_url
        session.commit()
        success = True
    session.close()
    return success


def update_user_settings(user_id, notifications_enabled, db_path=None):
    session = _get_session(db_path)
    user = session.get(User, int(user_id))
    success = False
    if user:
        user.notifications_enabled = notifications_enabled
        session.commit()
        success = True
    session.close()
    return success


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
    goals = (
        session.query(Goal)
        .filter(
            Goal.status == "pending", Goal.user_id == user_id, Goal.parent_id.is_(None)
        )
        .all()
    )

    def serialize_goal(g):
        return {
            "id": g.id,
            "description": g.description,
            "subgoals": [
                serialize_goal(sub) for sub in g.subgoals if sub.status == "pending"
            ],
        }

    results = [serialize_goal(g) for g in goals]
    session.close()
    return results


def list_completed_goals(user_id=1, db_path=None):
    session = _get_session(db_path)
    # Return completed goals (flat list is usually fine for history)
    goals = (
        session.query(Goal)
        .filter(Goal.status == "completed", Goal.user_id == user_id)
        .order_by(Goal.id.desc())
        .all()
    )

    results = [
        {"id": g.id, "description": g.description, "parent_id": g.parent_id}
        for g in goals
    ]

    session.close()
    return results


def list_calendar_goals(user_id=1, db_path=None):
    """Retrieve all goals for a user mapped chronologically by creation date."""
    session = _get_session(db_path)
    # Fetch all goals ordered by creation date descending
    goals = (
        session.query(Goal)
        .filter(Goal.user_id == user_id)
        .order_by(Goal.created_at.desc())
        .all()
    )

    calendar_data = {}
    for g in goals:
        # Convert datetime to YYYY-MM-DD string
        date_str = g.created_at.strftime("%Y-%m-%d")
        if date_str not in calendar_data:
            calendar_data[date_str] = []

        calendar_data[date_str].append(
            {
                "id": g.id,
                "description": g.description,
                "status": g.status,
                "parent_id": g.parent_id,
            }
        )

    session.close()
    return calendar_data


def complete_goal(goal_id, user_id=1, db_path=None):
    session = _get_session(db_path)
    goal = (
        session.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user_id).first()
    )
    success = False
    if goal:
        goal.status = "completed"
        session.commit()
        success = True
    session.close()
    return success


# --- Quarterly Initiatives ---
def add_initiative(quarter, description, user_id=1, db_path=None):
    session = _get_session(db_path)
    new_init = QuarterlyInitiative(
        quarter=quarter, description=description, user_id=user_id
    )
    session.add(new_init)
    session.commit()
    initiative_id = new_init.id
    session.close()
    return initiative_id


def list_pending_initiatives(user_id=1, db_path=None):
    session = _get_session(db_path)
    initiatives = (
        session.query(QuarterlyInitiative)
        .filter(
            QuarterlyInitiative.status == "pending",
            QuarterlyInitiative.user_id == user_id,
        )
        .order_by(QuarterlyInitiative.quarter.asc())
        .all()
    )
    results = [(i.id, i.quarter, i.description) for i in initiatives]
    session.close()
    return results


def complete_initiative(initiative_id, user_id=1, db_path=None):
    session = _get_session(db_path)
    initiative = (
        session.query(QuarterlyInitiative)
        .filter(
            QuarterlyInitiative.id == initiative_id,
            QuarterlyInitiative.user_id == user_id,
        )
        .first()
    )
    success = False
    if initiative:
        initiative.status = "completed"
        session.commit()
        success = True
    session.close()
    return success

# --- Analytics ---
def get_user_analytics(user_id=1, db_path=None):
    session = _get_session(db_path)

    total_goals = session.query(Goal).filter_by(user_id=user_id).count()
    completed_goals = session.query(Goal).filter_by(user_id=user_id, status="completed").count()
    pending_goals = session.query(Goal).filter_by(user_id=user_id, status="pending").count()

    completion_percentage = 0
    if total_goals > 0:
        completion_percentage = round((completed_goals / total_goals) * 100)

    # Calculate streak (simplified: consecutive days with at least one completed goal)
    completed_dates = session.query(func.date(Goal.created_at)).filter_by(user_id=user_id, status="completed").group_by(func.date(Goal.created_at)).order_by(func.date(Goal.created_at).desc()).all()

    streak = 0
    import datetime
    current_date = datetime.date.today()

    for date_tuple in completed_dates:
        # Check SQLite or Postgres format gracefully
        try:
            d_obj = datetime.datetime.strptime(str(date_tuple[0]), "%Y-%m-%d").date()
        except ValueError:
            break

        if d_obj == current_date:
            streak += 1
            current_date -= datetime.timedelta(days=1)
        elif d_obj == current_date - datetime.timedelta(days=1):
            streak += 1
            current_date -= datetime.timedelta(days=2) # Account for yesterday
        else:
            break

    session.close()

    return {
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "pending_goals": pending_goals,
        "completion_percentage": completion_percentage,
        "streak": streak
    }
