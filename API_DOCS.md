# FastAPI MVC Project - API Documentation

## Overview

This FastAPI application demonstrates a complete implementation of the Model-View-Controller (MVC) architectural pattern with comprehensive CRUD operations for Users, Products, and Orders.

## Base URL

- **Development**: `http://localhost:8000`
- **API Version**: `v1`
- **API Base Path**: `/api/v1`

## Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Authentication

Currently, the API does not implement authentication middleware, but the user service includes password hashing and authentication methods ready for integration with JWT or OAuth2.

## API Endpoints

### System Endpoints

#### Health Check
- **GET** `/health`
  - Description: Check API health status
  - Response: JSON with status and timestamp

#### Root
- **GET** `/`
  - Description: Welcome message with API information

### User Management (`/api/v1/users`)

#### Create User
- **POST** `/api/v1/users/`
  - Description: Create a new user account
  - Request Body: `UserCreate`
  - Response: `UserResponse` (201 Created)
  - Validations:
    - Email must be valid and unique
    - Username must be alphanumeric and unique
    - Password must be at least 8 characters with uppercase, digit

#### Get All Users
- **GET** `/api/v1/users/`
  - Description: Retrieve all users with pagination
  - Query Parameters:
    - `page` (int, default: 1): Page number
    - `size` (int, default: 50, max: 100): Items per page
    - `active_only` (bool, default: true): Filter active users only
  - Response: `UserListResponse`

#### Get User by ID
- **GET** `/api/v1/users/{user_id}`
  - Description: Retrieve a specific user
  - Path Parameters:
    - `user_id` (int): User ID
  - Response: `UserResponse`

#### Update User
- **PUT** `/api/v1/users/{user_id}`
  - Description: Update user information
  - Path Parameters:
    - `user_id` (int): User ID
  - Request Body: `UserUpdate`
  - Response: `UserResponse`

#### Delete User
- **DELETE** `/api/v1/users/{user_id}`
  - Description: Soft delete user (sets is_active to False)
  - Path Parameters:
    - `user_id` (int): User ID
  - Response: 204 No Content
  - Note: Cannot delete the last admin user

#### Search Users
- **GET** `/api/v1/users/search/`
  - Description: Search users by name, email, or username
  - Query Parameters:
    - `q` (string, min: 2): Search query
    - `page` (int, default: 1): Page number
    - `size` (int, default: 50): Items per page
  - Response: `List[UserResponse]`

#### User Actions
- **POST** `/api/v1/users/{user_id}/activate` - Activate user
- **POST** `/api/v1/users/{user_id}/deactivate` - Deactivate user
- **POST** `/api/v1/users/{user_id}/make-admin` - Grant admin privileges
- **POST** `/api/v1/users/{user_id}/remove-admin` - Remove admin privileges

### Product Management (`/api/v1/products`)

#### Create Product
- **POST** `/api/v1/products/`
  - Description: Create a new product
  - Request Body: `ProductCreate`
  - Response: `ProductResponse` (201 Created)
  - Validations:
    - SKU must be unique
    - Price must be positive
    - Stock quantity must be non-negative

#### Get All Products
- **GET** `/api/v1/products/`
  - Description: Retrieve all products with pagination
  - Query Parameters:
    - `page` (int, default: 1): Page number
    - `size` (int, default: 50, max: 100): Items per page
    - `active_only` (bool, default: true): Filter active products only
  - Response: `ProductListResponse`

#### Get Product by ID
- **GET** `/api/v1/products/{product_id}`
  - Description: Retrieve a specific product
  - Path Parameters:
    - `product_id` (int): Product ID
  - Response: `ProductResponse`

#### Get Product by SKU
- **GET** `/api/v1/products/sku/{sku}`
  - Description: Retrieve product by SKU
  - Path Parameters:
    - `sku` (string): Product SKU
  - Response: `ProductResponse`

#### Update Product
- **PUT** `/api/v1/products/{product_id}`
  - Description: Update product information
  - Path Parameters:
    - `product_id` (int): Product ID
  - Request Body: `ProductUpdate`
  - Response: `ProductResponse`

#### Delete Product
- **DELETE** `/api/v1/products/{product_id}`
  - Description: Soft delete product
  - Path Parameters:
    - `product_id` (int): Product ID
  - Response: 204 No Content

#### Search Products
- **GET** `/api/v1/products/search/`
  - Description: Search products by name, description, category, brand, or SKU
  - Query Parameters:
    - `q` (string, min: 2): Search query
    - `page` (int, default: 1): Page number
    - `size` (int, default: 50): Items per page
  - Response: `List[ProductResponse]`

#### Filter Products
- **POST** `/api/v1/products/filter`
  - Description: Filter products with multiple criteria
  - Request Body: `ProductSearchFilter`
  - Query Parameters:
    - `page` (int, default: 1): Page number
    - `size` (int, default: 50): Items per page
  - Response: `ProductListResponse`

#### Stock Management
- **PUT** `/api/v1/products/{product_id}/stock`
  - Description: Update product stock quantity
  - Request Body: `ProductStockUpdate`
  - Response: `ProductResponse`

- **GET** `/api/v1/products/{product_id}/stock-check`
  - Description: Check stock availability
  - Query Parameters:
    - `quantity` (int): Requested quantity
  - Response: JSON with availability status

#### Product Categories
- **GET** `/api/v1/products/category/{category}`
  - Description: Get products by category
  - Path Parameters:
    - `category` (string): Product category
  - Response: `ProductListResponse`

#### Low Stock Alert
- **GET** `/api/v1/products/low-stock/`
  - Description: Get products with low stock
  - Query Parameters:
    - `threshold` (int, default: 10): Stock threshold
  - Response: `List[ProductResponse]`

#### Product Actions
- **POST** `/api/v1/products/{product_id}/activate` - Activate product
- **POST** `/api/v1/products/{product_id}/deactivate` - Deactivate product

### Order Management (`/api/v1/orders`)

#### Create Order
- **POST** `/api/v1/orders/`
  - Description: Create a new order
  - Request Body: `OrderCreate`
  - Response: `OrderResponse` (201 Created)
  - Business Logic:
    - Validates user and product existence
    - Checks stock availability
    - Automatically calculates prices
    - Reserves stock

#### Get All Orders
- **GET** `/api/v1/orders/`
  - Description: Retrieve all orders with pagination
  - Query Parameters:
    - `page` (int, default: 1): Page number
    - `size` (int, default: 50, max: 100): Items per page
  - Response: `OrderListResponse`

#### Get Order by ID
- **GET** `/api/v1/orders/{order_id}`
  - Description: Retrieve detailed order information
  - Path Parameters:
    - `order_id` (int): Order ID
  - Response: `OrderDetailResponse`

#### Update Order
- **PUT** `/api/v1/orders/{order_id}`
  - Description: Update order information
  - Path Parameters:
    - `order_id` (int): Order ID
  - Request Body: `OrderUpdate`
  - Response: `OrderResponse`
  - Note: Cannot update cancelled, delivered, or refunded orders

#### Update Order Status
- **PATCH** `/api/v1/orders/{order_id}/status`
  - Description: Update order status with validation
  - Path Parameters:
    - `order_id` (int): Order ID
  - Request Body: `OrderStatusUpdate`
  - Response: `OrderResponse`
  - Valid Transitions:
    - PENDING → CONFIRMED, CANCELLED
    - CONFIRMED → PROCESSING, CANCELLED
    - PROCESSING → SHIPPED, CANCELLED
    - SHIPPED → DELIVERED
    - DELIVERED → REFUNDED

#### Cancel Order
- **POST** `/api/v1/orders/{order_id}/cancel`
  - Description: Cancel an order
  - Path Parameters:
    - `order_id` (int): Order ID
  - Response: `OrderResponse`
  - Effect: Releases reserved stock

#### Delete Order
- **DELETE** `/api/v1/orders/{order_id}`
  - Description: Delete an order
  - Path Parameters:
    - `order_id` (int): Order ID
  - Response: 204 No Content
  - Note: Only cancelled orders can be deleted

#### Get User Orders
- **GET** `/api/v1/orders/user/{user_id}`
  - Description: Get all orders for a specific user
  - Path Parameters:
    - `user_id` (int): User ID
  - Response: `OrderListResponse`

#### Get Product Orders
- **GET** `/api/v1/orders/product/{product_id}`
  - Description: Get all orders for a specific product
  - Path Parameters:
    - `product_id` (int): Product ID
  - Response: `OrderListResponse`

#### Filter Orders
- **POST** `/api/v1/orders/filter`
  - Description: Filter orders with multiple criteria
  - Request Body: `OrderFilter`
  - Response: `OrderListResponse`

#### Order Statistics
- **GET** `/api/v1/orders/stats/overview`
  - Description: Get overall order statistics
  - Response: `OrderStats`

- **GET** `/api/v1/orders/stats/user/{user_id}`
  - Description: Get order statistics for a specific user
  - Path Parameters:
    - `user_id` (int): User ID
  - Response: `UserOrderStats`

#### Recent Orders
- **GET** `/api/v1/orders/recent/`
  - Description: Get most recent orders
  - Query Parameters:
    - `limit` (int, default: 10, max: 50): Number of orders
  - Response: `List[OrderResponse]`

#### Orders by Status
- **GET** `/api/v1/orders/status/{status}`
  - Description: Get orders by status
  - Path Parameters:
    - `status` (OrderStatus): Order status
  - Response: `OrderListResponse`

## Data Models

### User Models

#### UserCreate
```json
{
  "email": "user@example.com",
  "username": "username",
  "first_name": "First",
  "last_name": "Last",
  "password": "Password123",
  "is_admin": false
}
```

#### UserUpdate
```json
{
  "email": "newemail@example.com",
  "username": "newusername",
  "first_name": "NewFirst",
  "last_name": "NewLast",
  "is_active": true,
  "is_admin": false
}
```

#### UserResponse
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "First",
  "last_name": "Last",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Product Models

#### ProductCreate
```json
{
  "name": "Product Name",
  "description": "Product description",
  "price": 99.99,
  "sku": "PROD-001",
  "stock_quantity": 100,
  "category": "Electronics",
  "brand": "BrandName",
  "weight": 1.5,
  "dimensions": "10x5x3 cm",
  "is_active": true
}
```

#### ProductResponse
```json
{
  "id": 1,
  "name": "Product Name",
  "description": "Product description",
  "price": 99.99,
  "sku": "PROD-001",
  "stock_quantity": 100,
  "is_active": true,
  "category": "Electronics",
  "brand": "BrandName",
  "weight": 1.5,
  "dimensions": "10x5x3 cm",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Order Models

#### OrderCreate
```json
{
  "user_id": 1,
  "product_id": 1,
  "quantity": 2,
  "shipping_address": "123 Main St, City, State 12345",
  "notes": "Special instructions"
}
```

#### OrderResponse
```json
{
  "id": 1,
  "user_id": 1,
  "product_id": 1,
  "quantity": 2,
  "unit_price": 99.99,
  "total_price": 199.98,
  "status": "pending",
  "shipping_address": "123 Main St, City, State 12345",
  "notes": "Special instructions",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## Order Statuses

- `pending` - Order created, awaiting confirmation
- `confirmed` - Order confirmed, ready for processing
- `processing` - Order being prepared
- `shipped` - Order shipped to customer
- `delivered` - Order delivered successfully
- `cancelled` - Order cancelled
- `refunded` - Order refunded

## Error Responses

All endpoints return standardized error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `400 Bad Request` - Invalid input data
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server errors

## Business Rules

### Users
- Email addresses must be unique
- Usernames must be alphanumeric and unique
- Passwords must be at least 8 characters with uppercase and digit
- Cannot delete the last admin user
- Cannot remove admin privileges from the last admin

### Products
- SKUs must be unique
- Prices must be positive
- Stock quantities cannot be negative

### Orders
- Users and products must exist and be active
- Cannot order more than available stock
- Order status transitions follow business logic
- Stock is automatically reserved/released based on order changes
- Cannot update cancelled, delivered, or refunded orders
- Only cancelled orders can be deleted

## Sample Usage

### Create a User
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "password": "JohnPassword123"
  }'
```

### Create a Product
```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Headphones",
    "description": "High-quality wireless headphones",
    "price": 199.99,
    "sku": "WH-001",
    "stock_quantity": 50,
    "category": "Electronics"
  }'
```

### Create an Order
```bash
curl -X POST "http://localhost:8000/api/v1/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "product_id": 1,
    "quantity": 1,
    "shipping_address": "123 Main St, Anytown, AT 12345"
  }'
```

## Development Tips

1. Use the interactive documentation at `/docs` for testing
2. Check the `/health` endpoint to verify API status
3. Use pagination parameters to limit response sizes
4. Filter endpoints accept various criteria for flexible queries
5. Order status transitions are strictly enforced
6. Stock management is automatically handled by the system
