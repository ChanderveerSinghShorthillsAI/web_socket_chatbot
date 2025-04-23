# Importing the FastAPI class to create a FastAPI application instance
from fastapi import FastAPI

# Importing StaticFiles to serve static files (e.g., HTML, CSS, JavaScript) from a directory
from fastapi.staticfiles import StaticFiles

# Importing the router object from the app.routes module to include API routes in the application
from app.routes import router

# Creating an instance of the FastAPI application
app = FastAPI()

# Including the router object into the FastAPI application to register all the routes defined in the router
app.include_router(router)

# Mounting a static files directory to serve frontend files (e.g., HTML, CSS, JS) from the "static" folder
# The `html=True` option allows serving an client.html file when accessing the root URL
# The name "static" is used to identify this mounted static files directory
app.mount("/", StaticFiles(directory="static", html=True), name="static")