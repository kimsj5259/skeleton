from uuid import UUID

from fastapi import APIRouter, Depends, status

router = APIRouter()


@router.get("")
async def test():
    """
    Gets my user profile information
    """
    return "first works"