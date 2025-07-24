# app/main.py
import logging

from cryptography.fernet import Fernet
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import PlainTextResponse
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.core.db_init import lifespan
from app.controllers import auth_controller, role_controller, user_controller, publication_controller, \
    specialty_controller, ugsn_controller, edu_level_controller, actual_specialty_controller, \
    journal_controller, city_controller, section_controller, grnti_controller, oecd_controller, actual_grnti_controller, \
    actual_oecd_controller, main_section_controller, contact_controller, pub_information_controller, index_controller, \
    review_controller, ip_whitelist_controller
from app.core.security import get_password_hash, verify_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Запуск миграций до старта приложения
#logger.info("Running migrations...")
#run_migrations()
#logger.info("Migrations completed.")

# Создание приложения FastAPI
app = FastAPI(lifespan=lifespan, root_path="/api/v1")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    tb = traceback.format_exc()
    logger.error(f"Exception occurred: {exc}\n{tb}")
    return PlainTextResponse(str(exc), status_code=500)

app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
app.include_router(role_controller.router, prefix="/role", tags=["role"])
app.include_router(user_controller.router, prefix="/users", tags=["users"])
app.include_router(publication_controller.router, prefix="/publications", tags=["Publications"])
app.include_router(ugsn_controller.router, prefix="/ugsn", tags=["UGSN"])
app.include_router(specialty_controller.router, prefix="/specialty", tags=["Specialty"])
app.include_router(edu_level_controller.router, prefix="/edu-levels", tags=["EduLevel"])
app.include_router(actual_specialty_controller.router, prefix="/actual-specialties", tags=["ActualSpecialty"])
app.include_router(journal_controller.router, prefix="/journal", tags=["Journal"])
app.include_router(city_controller.router, prefix="/cities", tags=["City"])
app.include_router(section_controller.router, prefix="/sections", tags=["Section"])
app.include_router(grnti_controller.router, prefix="/grnti", tags=["Grnti"])
app.include_router(oecd_controller.router, prefix="/oecd", tags=["OECD"])
app.include_router(actual_grnti_controller.router, prefix="/actual-grnti", tags=["ActualGRNTI"])
app.include_router(actual_oecd_controller.router, prefix="/actual-oecd", tags=["ActualOECD"])
app.include_router(main_section_controller.router, prefix="/main-sections", tags=["MainSections"])
app.include_router(contact_controller.router, prefix="/contacts", tags=["Contacts"])
app.include_router(pub_information_controller.router, prefix="/pub-information", tags=["PubInformation"])
app.include_router(index_controller.router, prefix="/index", tags=["Index"])
app.include_router(review_controller.router, prefix="/reviews", tags=["Review"])
app.include_router(ip_whitelist_controller.router, prefix="/whitelist", tags=["whitelist"])
@app.get("/checkip")
async def read_root(request: Request):
    # Получаем IP-адрес из заголовка X-Forwarded-For или request.client.host
    client_ip = request.headers.get("x-forwarded-for", request.client.host)
    print(f"IP-адрес клиента: {client_ip}")
    return {"message": "Hello, World!", "client_ip": client_ip}

@app.middleware("http")
async def block_connect_method(request: Request, call_next):
    if request.method == "CONNECT":
        raise HTTPException(status_code=405, detail="Method Not Allowed")
    return await call_next(request)