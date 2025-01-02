from fastapi import FastAPI
from routers import user_router
from routers.auth_router import router as auth_router

description = """
## Service Log API

This API allows you to manage service logs efficiently.

### Endpoints
- **Users**: Manage user accounts.
- **Customers**: Handle customer data.
- **Machine Models**: Work with machine models.
- **Ticket**: Handle tickets data.
"""

app = FastAPI(
    title="Service Log API",
    description=description,
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Suriya S.",
        "url": "https://github.com/suriyasonp/service_log_app",
        "email": "suriyasonp.tech@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Service Log API is running!"}