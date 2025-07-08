from typing import List, Optional
from app.domain.user import User
from app.model.user_record import UserRecord
from app.repo.datasource import DataSource, Repo
from app.utils import uuidutil
from app.utils.hashing import Hash
import uuid


def _map_user_record_to_user(user_record: UserRecord) -> User:
    return User(
        id=getattr(user_record, 'id', None),
        email=str(getattr(user_record, 'email', '')) if getattr(user_record, 'email', None) is not None else '',
        username=getattr(user_record, 'username', None),
        full_name=getattr(user_record, 'full_name', None),
        phone=getattr(user_record, 'phone', None),
        profile_pic_url=getattr(user_record, 'profile_pic_url', None),
        role=getattr(user_record, 'role', None)
    )


class UserRepo(Repo):
    def __init__(self, db: DataSource):
        super().__init__(db)

    def list_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        """List users with pagination support."""
        with self.db.get_session() as session:
            user_records = (
                session.query(UserRecord)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [_map_user_record_to_user(user_record) for user_record in user_records]

    def get_user_by_id(self, id: str) -> Optional[User]:
        with self.db.get_session() as session:
            user_record = (
                session.query(UserRecord)
                .filter(UserRecord.id == id)
                .first()
            )
            if user_record:
                return _map_user_record_to_user(user_record)
        return None

    def get_user_by_email(self, email: str) -> Optional[UserRecord]:
        with self.db.get_session() as session:
            return (
                session.query(UserRecord)
                .filter(UserRecord.email == email)
                .first()
            )

    def get_existing_usernames(self) -> List[str]:
        """Get all existing usernames for uniqueness checking."""
        with self.db.get_session() as session:
            usernames = session.query(UserRecord.username).all()
            return [str(username[0]) for username in usernames if username[0]]

    def update_user(self, id: str, user_data: User) -> Optional[User]:
        with self.db.get_session() as session:
            user_record = (
                session.query(UserRecord)
                .filter(UserRecord.id == id)
                .first()
            )
            if not user_record:
                return None

            # Only update fields that are provided and not None
            if user_data.username is not None:
                setattr(user_record, 'username', user_data.username)
            if user_data.email is not None:
                setattr(user_record, 'email', str(user_data.email))
            if user_data.full_name is not None:
                setattr(user_record, 'full_name', user_data.full_name)
            if user_data.phone is not None:
                setattr(user_record, 'phone', user_data.phone)
            if user_data.profile_pic_url is not None:
                setattr(user_record, 'profile_pic_url', user_data.profile_pic_url)

            session.commit()
            session.refresh(user_record)
            return _map_user_record_to_user(user_record)

    def delete_user(self, id: str) -> bool:
        with self.db.get_session() as session:
            user_record = (
                session.query(UserRecord)
                .filter(UserRecord.id == id)
                .first()
            )
            if user_record:
                session.delete(user_record)
                session.commit()
                return True
        return False

    def get_user_record_by_id(self, id: str) -> Optional[UserRecord]:
        with self.db.get_session() as session:
            return (
                session.query(UserRecord)
                .filter(UserRecord.id == id)
                .first()
            )

    def update_user_password(self, id: str, password: str) -> bool:
        with self.db.get_session() as session:
            user_record = (
                session.query(UserRecord)
                .filter(UserRecord.id == id)
                .first()
            )
            if not user_record:
                return False
            setattr(user_record, 'password', password)
            session.commit()
            return True

    def add_user_record(self, user_record: UserRecord) -> User:
        # Ensure id is set before adding to session
        with self.db.get_session() as session:
            session.add(user_record)
            session.commit()
            session.refresh(user_record)
            return _map_user_record_to_user(user_record)

    def create_user(self, user_data: User, password: str, role: str = "user") -> User:
        with self.db.get_session() as session:
            hashed_password = Hash.hash(password)
            user_record = UserRecord(
                id=str(uuid.uuid4()),
                username=user_data.username,
                email=str(user_data.email),
                password=hashed_password,
                role=role,
                full_name=user_data.full_name,
                phone=user_data.phone,
                profile_pic_url=user_data.profile_pic_url
            )
            session.add(user_record)
            session.commit()
            session.refresh(user_record)
            return _map_user_record_to_user(user_record)