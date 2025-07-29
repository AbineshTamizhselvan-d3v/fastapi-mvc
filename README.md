
# FastAPI JWT Authentication with MVC Pattern

This project is a robust boilerplate for building FastAPI applications with a clean and scalable Model-View-Controller (MVC) architecture. It features a complete JWT (JSON Web Token) authentication system, MongoDB integration using Beanie ODM, and a well-organized project structure.

## ✨ Features

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **MVC Architecture**: A clean and organized project structure that separates concerns into Models, Views (Controllers in API context), and Services (business logic).
- **JWT Authentication**: Secure user authentication using JSON Web Tokens, including token generation, validation, and refresh mechanisms.
- **MongoDB Integration**: Asynchronous database operations with MongoDB, powered by `motor` and `beanie` (ODM - Object-Document Mapper).
- **Pydantic**: Data validation and settings management using Pydantic models.
- **Dependency Injection**: FastAPI's powerful dependency injection system is used to manage dependencies like database sessions and services.
- **CORS Middleware**: Configured to allow cross-origin requests, essential for modern web applications.
- **Docker Support**: Comes with `Dockerfile` and `docker-compose.yml` for easy containerization and deployment.
- **Environment-based Configuration**: Manage application settings for different environments using `.env` files.
- **Testing Script**: Includes a script to test the authentication endpoints.

## 📂 Folder Structure

The project follows a structured layout to promote separation of concerns and maintainability.

```
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── controllers/            # Handles incoming requests and returns responses (API endpoints)
│   │   ├── auth_controller.py
│   │   └── user_controller.py
│   ├── core/                   # Core components like configuration and database connection
│   │   ├── config.py
│   │   └── database.py
│   ├── middleware/             # Custom middleware
│   │   └── auth.py
│   ├── models/                 # Database models (Beanie ODM)
│   │   └── user.py
│   ├── repositories/           # Data access layer, interacts with the database
│   │   └── user_repository.py
│   ├── schemas/                # Pydantic schemas for data validation and serialization
│   │   ├── auth_schema.py
│   │   └── user_schema.py
│   ├── services/               # Business logic layer
│   │   ├── auth_service.py
│   │   └── user_service.py
│   └── utils/                  # Utility functions and helper modules
│       ├── auth.py
│       └── helpers.py
├── .env                        # Environment variables for configuration (create from .env.example)
├── .gitignore                  # Files and directories to be ignored by Git
├── API_DOCS.md                 # Detailed API documentation
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker configuration for the application
├── requirements.txt            # Python dependencies
├── start.bat                   # Batch script to run the development server on Windows
├── start.sh                    # Shell script to run the development server on Linux/macOS
└── test_auth.py                # Script to test the authentication system
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Docker (optional, for containerized setup)
- A running MongoDB instance

### 1. Clone the Repository

```bash
git clone https://github.com/knightempire/fastapi-mvc-baseauth.git
cd fastapi-mvc-baseauth
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory by copying the example:

```bash
cp .env.example .env
```

Update the `.env` file with your configuration, especially the `MONGODB_URL` and `JWT_SECRET_KEY`.

### 3. Running the Application

#### Without Docker

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2.  **Activate the virtual environment:**
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the development server:**
    - On Windows:
      ```bash
      ./start.bat
      ```
    - On macOS/Linux:
      ```bash
      ./start.sh
      ```

The application will be available at `http://localhost:8000`.

#### With Docker

1.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```

The application will be available at `http://localhost:8000`.

## Interactive API Documentation

Once the application is running, you can access the interactive API documentation at:

-   **Swagger UI**: `http://localhost:8000/docs`
-   **ReDoc**: `http://localhost:8000/redoc`

## 📖 API Endpoints

The following are the main API endpoints available:

### Authentication (`/api/v1/auth`)

-   `POST /register`: Register a new user.
-   `POST /login`: Log in a user and receive JWT tokens.
-   `GET /me`: Get the profile of the currently authenticated user (protected).
-   `GET /verify-token`: Verify the validity of an access token (protected).

### User Management (`/api/v1/users`)

-   `GET /`: Get a list of all users.
-   `GET /{user_id}`: Get a specific user by their ID.
-   `PUT /{user_id}`: Update a user's information.
-   `DELETE /{user_id}`: Delete a user.

For more details on request and response models, please refer to the interactive documentation.

## 🧪 Testing

To test the authentication system, ensure the server is running and execute the following command:

```bash
python test_auth.py
```

This script will perform a series of tests, including user registration, login, and accessing protected endpoints.
