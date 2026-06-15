import os
from datetime import datetime, timedelta
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
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from contextlib import contextmanager

load_dotenv()

Base = declarative_base()


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


class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, default=1)
    description = Column(String, nullable=False)
    current_streak = Column(Integer, nullable=False, default=0)
    highest_streak = Column(Integer, nullable=False, default=0)
    last_completed_date = Column(String, nullable=True)  # Format YYYY-MM-DD
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")


# --- Database Engine Management ---
_engines = {}


def get_db_url(db_path=None):
    """Returns the DATABASE_URL if set, otherwise falls back to sqlite via DATABASE_PATH."""
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    # Fallback to local sqlite
    if db_path is None:
        db_path = os.getenv("DATABASE_PATH", "goals.db")
    return f"sqlite:///{db_path}"


def _get_engine(db_path=None):
    url = get_db_url(db_path)
    if url not in _engines:
        if "sqlite" in url:
            # Use NullPool for SQLite on Windows to avoid file locking issues during tests
            _engines[url] = create_engine(url, echo=False, poolclass=NullPool)
        else:
            _engines[url] = create_engine(url, echo=False, pool_pre_ping=True)
    return _engines[url]


def _get_session(db_path=None):
    engine = _get_engine(db_path)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    return Session()


def init_db(db_path=None):
    """Initialize the database with required tables using SQLAlchemy."""
    engine = _get_engine(db_path)
    Base.metadata.create_all(engine)


@contextmanager
def session_scope(db_path=None):
    """Provide a transactional scope around a series of operations."""
    session = _get_session(db_path)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# --- Users ---
def create_user(username, password, db_path=None):
    with session_scope(db_path) as session:
        # Check if user already exists
        existing = session.query(User).filter_by(username=username).first()
        if existing:
            return None

        new_user = User(username=username)
        new_user.set_password(password)
        session.add(new_user)
        # commit is handled by session_scope
        session.flush()
        return new_user.id


def get_user_by_username(username, db_path=None):
    with session_scope(db_path) as session:
        user = session.query(User).filter_by(username=username).first()
        return user


def get_user_by_id(user_id, db_path=None):
    with session_scope(db_path) as session:
        user = session.get(User, int(user_id))
        return user


def update_user_avatar(user_id, avatar_url, db_path=None):
    with session_scope(db_path) as session:
        user = session.get(User, int(user_id))
        success = False
        if user:
            user.avatar_url = avatar_url
            success = True
        return success


def update_user_settings(user_id, notifications_enabled=None, is_public=None, db_path=None):
    with session_scope(db_path) as session:
        user = session.get(User, int(user_id))
        success = False
        if user:
            if notifications_enabled is not None:
                user.notifications_enabled = notifications_enabled
            if is_public is not None:
                user.is_public = is_public
            success = True
        return success


def list_users_for_notifications(db_path=None):
    """Retrieve all users who have notifications enabled."""
    with session_scope(db_path) as session:
        users = session.query(User).filter(User.notifications_enabled is True).all()
        return [{"id": u.id, "username": u.username} for u in users]


def list_public_users(db_path=None):
    """Retrieve all users who have set their profile to public."""
    with session_scope(db_path) as session:
        users = session.query(User).filter(User.is_public is True).all()
        return [{"id": u.id, "username": u.username, "avatar_url": u.avatar_url} for u in users]


# --- Habits ---
def add_habit(description, user_id=1, db_path=None):
    with session_scope(db_path) as session:
        new_habit = Habit(description=description, user_id=user_id)
        session.add(new_habit)
        session.flush()
        return new_habit.id


def list_habits(user_id=1, db_path=None):
    with session_scope(db_path) as session:
        habits = (
            session.query(Habit)
            .filter(Habit.user_id == user_id)
            .order_by(Habit.id.asc())
            .all()
        )
        results = [
            {
                "id": h.id,
                "description": h.description,
                "current_streak": h.current_streak,
                "highest_streak": h.highest_streak,
                "last_completed_date": h.last_completed_date,
            }
            for h in habits
        ]
        return results


def complete_habit(habit_id, completed_date, user_id=1, db_path=None):
    with session_scope(db_path) as session:
        habit = session.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user_id).first()
        success = False
        if habit:
            if habit.last_completed_date == completed_date:
                # Already completed today, do nothing
                pass
            else:
                if habit.last_completed_date:
                    last_date = datetime.strptime(habit.last_completed_date, "%Y-%m-%d").date()
                    curr_date = datetime.strptime(completed_date, "%Y-%m-%d").date()
                    if curr_date - last_date == timedelta(days=1):
                        # Streak continues
                        habit.current_streak += 1
                    else:
                        # Streak broken
                        habit.current_streak = 1
                else:
                    # First completion
                    habit.current_streak = 1

                if habit.current_streak > habit.highest_streak:
                    habit.highest_streak = habit.current_streak

                habit.last_completed_date = completed_date
                success = True
        return success


def delete_habit(habit_id, user_id=1, db_path=None):
    with session_scope(db_path) as session:
        habit = session.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user_id).first()
        success = False
        if habit:
            session.delete(habit)
            success = True
        return success


# --- Daily Goals ---
def add_goal(description, user_id=1, parent_id=None, db_path=None):
    with session_scope(db_path) as session:
        new_goal = Goal(description=description, user_id=user_id, parent_id=parent_id)
        session.add(new_goal)
        session.flush()

        # Return fully serialized goal
        return {
            "id": new_goal.id,
            "description": new_goal.description,
            "parent_id": new_goal.parent_id,
            "subgoals": []
        }


def list_pending_goals(user_id=1, db_path=None):
    with session_scope(db_path) as session:
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

        return [serialize_goal(g) for g in goals]


def list_completed_goals(user_id=1, db_path=None):
    with session_scope(db_path) as session:
        # Return completed goals (flat list is usually fine for history)
        goals = (
            session.query(Goal)
            .filter(Goal.status == "completed", Goal.user_id == user_id)
            .order_by(Goal.id.desc())
            .all()
        )

        return [
            {"id": g.id, "description": g.description, "parent_id": g.parent_id}
            for g in goals
        ]


def list_calendar_goals(user_id=1, db_path=None):
    """Retrieve all goals for a user mapped chronologically by creation date."""
    with session_scope(db_path) as session:
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

        return calendar_data


def complete_goal(goal_id, user_id=1, db_path=None):
    with session_scope(db_path) as session:
        goal = (
            session.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user_id).first()
        )
        success = False
        if goal:
            goal.status = "completed"
            success = True
        return success


def delete_goal(goal_id, user_id=1, db_path=None):
    with session_scope(db_path) as session:
        goal = (
            session.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user_id).first()
        )
        success = False
        if goal:
            session.delete(goal)
            success = True
        return success


# --- Quarterly Initiatives ---
def add_initiative(quarter, description, user_id=1, db_path=None):
    with session_scope(db_path) as session:
        new_init = QuarterlyInitiative(
            quarter=quarter, description=description, user_id=user_id
        )
        session.add(new_init)
        session.flush()
        return new_init.id


def list_pending_initiatives(user_id=1, db_path=None):
    with session_scope(db_path) as session:
        initiatives = (
            session.query(QuarterlyInitiative)
            .filter(
                QuarterlyInitiative.status == "pending",
                QuarterlyInitiative.user_id == user_id,
            )
            .order_by(QuarterlyInitiative.quarter.asc())
            .all()
        )
        return [(i.id, i.quarter, i.description) for i in initiatives]


def complete_initiative(initiative_id, user_id=1, db_path=None):
    with session_scope(db_path) as session:
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
            success = True
        return success
