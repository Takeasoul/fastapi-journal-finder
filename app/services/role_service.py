from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.role import Role
from app.models.user import User

class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_role(self, name: str) -> dict:
        result = await self.db.execute(select(Role).where(Role.name == name))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Role already exists")
        role = Role(name=name)
        self.db.add(role)
        await self.db.commit()
        return {"message": "Role created successfully"}

    async def get_roles(self) -> list:
        result = await self.db.execute(select(Role))
        return list(result.scalars().all())

    async def update_role(self, role_id: int, name: str) -> dict:
        result = await self.db.execute(select(Role).where(Role.id == role_id))
        role = result.scalars().first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        role.name = name
        await self.db.commit()
        return {"message": "Role updated successfully"}

    async def delete_role(self, role_id: int) -> dict:
        result = await self.db.execute(select(Role).where(Role.id == role_id))
        role = result.scalars().first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        await self.db.delete(role)
        await self.db.commit()
        return {"message": "Role deleted successfully"}


    async def has_role(user_role: Role, required_role_name: str) -> bool:
        # Проверяем текущую роль и всех родителей
        current = user_role
        while current:
            if current.name == required_role_name:
                return True
            current = current.parent
        return False