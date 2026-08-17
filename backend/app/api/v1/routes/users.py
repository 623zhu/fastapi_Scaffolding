from fastapi import APIRouter, HTTPException, status

from app.api.deps import DatabaseSession
from app.schemas.user import UserCreate, UserRead
from app.services.user import UserAlreadyExistsError, UserService

router = APIRouter()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(data: UserCreate, session: DatabaseSession) -> UserRead:
    try:
        user = await UserService(session).register(data)
    except UserAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        ) from error

    return UserRead.model_validate(user)
