E-Commerce API
This project is a simple E-Commerce API builty with Flask, SQLAlchemy, 
and Marshmallow. It allows users to manage users, orders and products.
It also allows enabling basic CRUD operations for each resource.
Data is stored in a MySQL database (titled ecom_api) and is designed to run in
a Python virtual environment (titled venv)

-- FEATURES --
- User Management: Create, read, update and delete users
- Order Management: Create orders, add or remove products
    to/from orders and read order details
- Product Management: Create, read, update and delete products
- Database: Data storage using MySQL with SQLAlchemy ORM
- Validation: Input validation handled using
    Marshmallow schemas

-- Tools and Dependencies --
- Python: main language for the project
- Flask: framework for handling routes and HTTP methods
- MySQL: Database for storing data
- SQLAlchemy: ORM (Object Relational Mapping) for
    database interaction
- mysql-connector-python: MySQL database driver

-- Installation Instructions -- 
1. Clone the Repository
git clone https://github.com/codenamehenny/ecommerce_api
cd ecommerce_api

2. Set up a Virtual Environment:
python3 -m venv venv
source venv/bin/activate     # macOS and Linux
venv\Scripts\activate       # Windows

3. Install Dependencies:
pip install Flask Flask-SQLAlchemy Flask-Marshmallow marshmallow-sqlalchemy mysql-connector-python

4. Set up MySQL Database:
- Create a MySQL database named ecommerce_api
- Update the database URI in app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 
    'mysql+mysqlconnector://<username>:<password>@127.0.0.1:3306/ecommerce_api'

5. Run Database Migrations:
Initialize the database schema:
flask run

-- Usage -- 
1. Start the Flask Server:
flask run

2. Interact with the API:
Use  tools like Postman to test endpoints

-- API Endpoints --
User Endpoints:
GET /users: Retrieve all users
GET /users/<id>: Retrieve a user by ID
POST /users: Create a new user
PUT /users/<id>: Update a user by ID
DELETE /users/<id>: Delete a user by ID

Product Endpoints:
GET /products: Retrieve all products
GET /products/<id>: Retrieve a product by ID
POST /products: Create a new product
PUT /products/<id>: Update a product by ID
DELETE /products/<id>: Delete a product by ID

Order Endpoints:
POST /orders: Create a new order (requires user ID and order date)
GET /orders/<order_id>/add_product/<product_id>: Add a product to an order (prevent duplicates)
DELETE /orders/<order_id>/remove_product: Remove a product from an order
GET /orders/user/<user_id>: Get all orders for a user
GET /orders/<order_id>/products: Get all products for an order

-- Contributing -- 
1. Fork the Repository:
Fork the project repository using the Github interface

2. Clone Your Fork:
git clone <your-forked-repo-url>

3. Create a New Branch:
git checkout -b feature/your-feature-name

4. Install Dependencies:
Once in the virtual environment, run:
pip install Flask Flask-SQLAlchemy Flask-Marshmallow marshmallow-sqlalchemy mysql-connector-python

5. Make Changes:
Modify the code and ensure your changes follow best 
    practices and are tested

6. Test Your Changes:
flask run

7. Commit Your Changes:
git add .
git commit -m "Add your message here"

8. Push and Create a Pull Request
git push origin feature/your-feature-name

Open a pull request on the original repository

-- Questions/Feedback --
Please send to genesis09m@hotmail.com