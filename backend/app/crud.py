import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
        verify_password(password, DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if updated_password_hash:
        db_user.hashed_password = updated_password_hash
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_boss_jobs(
    *,
    session: Session,
    skip: int = 0,
    limit: int = 100,
    created_time: str | None = None,
    job_name: str | None = None,
    city_name: str | None = None,
) -> tuple[list, int]:
    from datetime import date as date_type
    from app.models import BossJobDetails
    from sqlmodel import col, func

    statement = select(BossJobDetails)
    count_statement = select(func.count()).select_from(BossJobDetails)

    if created_time:
        # Parse date string to date object
        created_date = date_type.fromisoformat(created_time)
        statement = statement.where(BossJobDetails.created_time == created_date)
        count_statement = count_statement.where(BossJobDetails.created_time == created_date)
    if job_name:
        statement = statement.where(BossJobDetails.job_name.ilike(f"%{job_name}%"))
        count_statement = count_statement.where(BossJobDetails.job_name.ilike(f"%{job_name}%"))
    if city_name:
        statement = statement.where(BossJobDetails.city_name == city_name)
        count_statement = count_statement.where(BossJobDetails.city_name == city_name)

    count = session.exec(count_statement).one()

    statement = statement.order_by(col(BossJobDetails.id).desc()).offset(skip).limit(limit)
    jobs = session.exec(statement).all()

    return list(jobs), count
