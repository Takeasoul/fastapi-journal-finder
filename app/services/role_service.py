from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.role import Role
from app.models.user import User
from app.schemas.role import RoleRequest


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_role(self, data: RoleRequest) -> dict:
        # Проверяем, существует ли роль с таким именем
        result = await self.db.execute(select(Role).where(Role.name == data.name))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Роль уже существует")

        # Создаем новую роль
        role = Role(
            name=data.name,
            parent_id=data.parent_id if data.parent_id else None
        )

        # Добавляем роль в базу данных
        self.db.add(role)
        await self.db.commit()

        return {"message": "Роль успешно создана"}

    async def get_roles(self) -> list:
        result = await self.db.execute(select(Role))
        return list(result.scalars().all())

    async def update_role(self, role_id: int, data: RoleRequest) -> dict:
        result = await self.db.execute(select(Role).where(Role.id == role_id))
        role = result.scalars().first()
        if not role:
            raise HTTPException(status_code=404, detail="Роль не найдена")
        if data.name:
            role.name = data.name
        if data.parent_id:
            role.parent_id = data.parent_id

        await self.db.commit()
        return {"message": "Роль обновлена успешно"}

    async def delete_role(self, role_id: int) -> dict:
        result = await self.db.execute(select(Role).where(Role.id == role_id))
        role = result.scalars().first()
        if not role:
            raise HTTPException(status_code=404, detail="Роль не найдена")
        await self.db.delete(role)
        await self.db.commit()
        return {"message": "Роль удалена успешно"}


    async def has_role(user_role: Role, required_role_name: str) -> bool:
        # Проверяем текущую роль и всех родителей
        current = user_role
        while current:
            if current.name == required_role_name:
                return True
            current = current.parent
        return False