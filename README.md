# ShopEase - Django + MySQL E-commerce Project

A beginner-friendly e-commerce project built with HTML, CSS, JavaScript, Django and MySQL.

## Features
- Product listing, search and category filtering
- Product details
- Customer registration, login and logout
- Session-based shopping cart (add, update, remove)
- Checkout and order processing
- Stock validation and stock reduction after a successful order
- Customer order history
- Django admin for managing products and orders

**Payment note:** This learning project records orders but does not integrate a real payment gateway.

## Requirements
- Python 3.10+
- MySQL Server 8.x (or compatible)
- VS Code (recommended)

## Setup on Windows PowerShell

1. Extract the ZIP file and open the `ShopEase` folder in VS Code.
2. Open Terminal > New Terminal.
3. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this in the same terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

4. Install packages:

```powershell
python -m pip install -r requirements.txt
```

5. Create the MySQL database in MySQL Workbench:

```sql
CREATE DATABASE shopease_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. Copy `.env.example` to a new file named `.env`. Update `DB_PASSWORD` with your MySQL password. Keep the database name, user, host and port consistent with your MySQL setup.

7. Create database tables:

```powershell
python manage.py makemigrations
python manage.py migrate
```

8. Create an admin account:

```powershell
python manage.py createsuperuser
```

9. Start the website:

```powershell
python manage.py runserver
```

Open:
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Add products
Log in to the admin panel, open Products, and add products. The `Image URL` field is optional; use a publicly accessible image URL. Add a name, description, price, category and stock.

## Test the application
1. Add at least two products in the admin panel.
2. Register a customer account from the website.
3. Log in, open a product and add it to the cart.
4. Update quantity or remove a product.
5. Proceed to checkout and enter a delivery address.
6. Place the order and open My Orders.
7. In MySQL Workbench, inspect `store_product`, `store_order` and `store_orderitem`.

## Database configuration
The project reads MySQL credentials from `.env`. Do not upload `.env` or real credentials to GitHub. `PyMySQL` is used as a pure-Python MySQL driver to simplify setup on Windows.

## Common issues
- **Access denied for user:** check `DB_USER` and `DB_PASSWORD` in `.env`.
- **Can't connect to MySQL server:** start the MySQL service and confirm `DB_HOST` and `DB_PORT`.
- **Unknown database:** create `shopease_db` in MySQL Workbench.
- **No products shown:** add products through `/admin/`.
- **Template not found:** check that the `templates/store/` folders and filenames match this project.
