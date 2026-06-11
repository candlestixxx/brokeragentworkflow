import os

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Table
)

from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref
from sqlalchemy.sql import func
from dotenv import load_dotenv
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

load_dotenv()

Base = declarative_base()



user_badges = Table(
    'user_badges', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('badge_id', Integer, ForeignKey('badges.id'), primary_key=True),
    Column('awarded_at', DateTime(timezone=True), server_default=func.now())
)

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(250), nullable=False)
    icon = Column(String(50), nullable=False, default="StarIcon")

    users = relationship("User", secondary=user_badges, back_populates="badges")

class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    notifications_enabled = Column(Boolean, nullable=False, default=True)
    is_public = Column(Boolean, nullable=False, default=False)

    goals = relationship("Goal", back_populates="user")
    initiatives = relationship("QuarterlyInitiative", back_populates="user")
    badges = relationship("Badge", secondary=user_badges, back_populates="users")

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
    seed_badges(db_path)


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

# --- Gamification / Badges ---
def seed_badges(db_path=None):
    session = _get_session(db_path)
    default_badges = [
        {"name": "First Step", "description": "Complete your first goal", "icon": "StarIcon"},
        {"name": "On a Roll", "description": "Complete 5 goals", "icon": "FireIcon"},
        {"name": "Goal Crusher", "description": "Complete 20 goals", "icon": "TrophyIcon"},
        {"name": "Consistent", "description": "Achieve a 3-day streak", "icon": "CheckBadgeIcon"}
    ]

    for b_data in default_badges:
        existing = session.query(Badge).filter_by(name=b_data["name"]).first()
        if not existing:
            new_badge = Badge(**b_data)
            session.add(new_badge)

    session.commit()
    session.close()

def evaluate_badges(user_id, db_path=None):
    session = _get_session(db_path)
    user = session.get(User, int(user_id))
    if not user:
        session.close()
        return []

    stats = get_user_analytics(user_id, db_path)
    newly_awarded = []

    badges_by_name = {b.name: b for b in session.query(Badge).all()}
    user_badge_names = [b.name for b in user.badges]

    rules = [
        ("First Step", lambda s: s["completed_goals"] >= 1),
        ("On a Roll", lambda s: s["completed_goals"] >= 5),
        ("Goal Crusher", lambda s: s["completed_goals"] >= 20),
        ("Consistent", lambda s: s["streak"] >= 3)
    ]

    for b_name, condition in rules:
        if b_name not in user_badge_names and condition(stats):
            badge = badges_by_name.get(b_name)
            if badge:
                user.badges.append(badge)
                newly_awarded.append({"name": badge.name, "description": badge.description, "icon": badge.icon})

    if newly_awarded:
        session.commit()

    session.close()
    return newly_awarded

def get_user_badges(user_id, db_path=None):
    session = _get_session(db_path)
    user = session.get(User, int(user_id))
    if not user:
        session.close()
        return []

    badges = [{"id": b.id, "name": b.name, "description": b.description, "icon": b.icon} for b in user.badges]
    session.close()
    return badges

def list_users_for_notifications(db_path=None):
    session = _get_session(db_path)
    users = session.query(User).filter_by(notifications_enabled=True).all()
    results = [{"id": u.id, "username": u.username} for u in users]
    session.close()
    return results

def list_public_users(db_path=None):
    session = _get_session(db_path)
    users = session.query(User).filter_by(is_public=True).all()
    results = [{"id": u.id, "username": u.username, "avatar_url": u.avatar_url} for u in users]
    session.close()
    return results

class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    current_streak = Column(Integer, default=0)
    highest_streak = Column(Integer, default=0)
    last_completed_date = Column(String(50), nullable=True)

    user = relationship("User", back_populates="habits")

User.habits = relationship("Habit", order_by=Habit.id, back_populates="user")

def list_habits(user_id, db_path=None):
    session = _get_session(db_path)
    habits = session.query(Habit).filter_by(user_id=user_id).all()
    results = [
        {
            "id": h.id,
            "description": h.description,
            "current_streak": h.current_streak,
            "highest_streak": h.highest_streak,
            "last_completed_date": h.last_completed_date
        }
        for h in habits
    ]
    session.close()
    return results

def delete_goal(goal_id, user_id, db_path=None):
    session = _get_session(db_path)
    goal = session.query(Goal).filter_by(id=goal_id, user_id=user_id).first()
    if goal:
        session.delete(goal)
        session.commit()
        session.close()
        return True
    session.close()
    return False

def complete_habit(habit_id, user_id, db_path=None):
    session = _get_session(db_path)
    habit = session.query(Habit).filter_by(id=habit_id, user_id=user_id).first()
    if habit:
        habit.current_streak += 1
        if habit.current_streak > habit.highest_streak:
            habit.highest_streak = habit.current_streak
        session.commit()
        session.close()
        return True
    session.close()
    return False

def add_habit(description, user_id, db_path=None):
    session = _get_session(db_path)
    habit = Habit(description=description, user_id=user_id, current_streak=0, highest_streak=0)
    session.add(habit)
    session.commit()
    habit_id = habit.id
    session.close()
    return habit_id

def delete_habit(habit_id, user_id, db_path=None):
    session = _get_session(db_path)
    habit = session.query(Habit).filter_by(id=habit_id, user_id=user_id).first()
    if habit:
        session.delete(habit)
        session.commit()
        session.close()
        return True
    session.close()
    return False
