from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dep_verify_user import VerifiedUser, depends_verify_user
from core.logging import get_logger
from database.session import get_db_session
from database.user_skills import post_user_skill
from iom.skills import PayloadCreateSkill, ResponseCreateSkill


router = APIRouter()


tags = ["Skills"]


log = get_logger()


@router.post(
    path="/skills",
    tags=tags,
    description="Create a new user skill with the provided content and store it in the Vector Store.",
    response_model=ResponseCreateSkill
)
async def create_user_skill(
    payload: PayloadCreateSkill,
    user: VerifiedUser = Depends(depends_verify_user),
    session: AsyncSession = Depends(get_db_session)
) -> ResponseCreateSkill:
    """Create a new user skill.
    
    This endpoint creates a user skill record in the database and stores the skill description
    in the Vector Store for semantic search capabilities.
    """
    try:
        skill_id = await post_user_skill(
            session=session,
            user_id=user.id,
            name=payload.name,
            description=payload.description,
            skill_text=payload.skill_text,
            parameters_schema=payload.parameters_schema
        )
        
        return ResponseCreateSkill(
            skill_id=skill_id,
            name=payload.name,
            message=f"Skill '{payload.name}' created successfully"
        )
    
    except ValueError as e:
        log.error(f"Value error creating skill: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        log.error(f"Error creating skill: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create skill: {str(e)}"
        )