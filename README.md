# Hackathon_HCL_project - Smart Banking System

## overview
This project is a modular backend system for smart banking. It provides secure user registration, user login  and kyc verification while following best practices like authentication, authorization, input validation and testing.

This system designed  for **frontend UI rendering using Django templates** to be scalable ,secured and maintainable using **Django** (Django Rest Framework) as a backend framework.

--- 

## Features

### **core features**
- **User Registration**
    - Submit personal details like : Username, Emailid, PhoneNumber, Address, etc.
    - Upload KYC documents: Government ID Proof, Address Proof 
    - Input validation and sanitization
    - Password hashing with **bcrypt** algorithm
    - Email uniqueness among different users and email format validation

- **User Login**
  - Authenticate using email/username and password
  - JWT-based authentication for session handling (optional if frontend uses server-side sessions)
  - Rate-limiting to prevent brute-force login attacks

- **KYC Verification**
    - Automatic system validation for document format and required fields
    - Status tracking: Pending, Approved, Rejected

- **Admin Dashboard**
    - To monitor the user accounts and their profile
    - To review the kyc document and update the status by approv/reject.

### **Security Features**

- **Password Hashing**
  - Using **bcrypt** for secure password storage

  **Rate Limiting**
  - Using Ratelimit from **django-ratelimiter** which protects against brute force attacks.

- **Role-Based Access Control (RBAC)**
  - Roles: `admin`, `customer`
  - Permissions based on role for sensitive endpoints

- **Input Validation & Sanitization**
  - Validation of user inputs (emailid, phonenumber, password strength/weak)
  - Protection against SQL injection/XSS attacks

  - **JWT-based Authentication**
  - Access and refresh tokens
  - Token expiration handling

### **Testing**
- **Unit Tests**
  - Test individual business logic (e.g., password hashing, KYC validation rules)
- **Integration Tests**
  - Test API endpoints and workflows (registration, document upload, token generation)
- **Test Coverage**
  - Generate coverage reports using `pytest` and `pytest-cov`

---

## Frontend Integration (Django Templates)

- The **frontend forms** are rendered using Django templates (`.html`)  
- Example pages:
  - `register.html` → User registration form
  - `login.html` → Login form
  - `kyc_submit.html` → Upload KYC documents
- Form handling:
  - Backend receives form submission via POST request
  - Django forms handle validation and sanitization
  - Upon success, redirect user to the appropriate page
- KYC verification:
  - Admin reviews submitted documents via Django Admin panel

## API Endpoints (Example)

| Endpoint                      | Method | Description                             | AuthRequired |
|-------------------------------|--------|-----------------------------------------|--------------|
| `/register/`            | POST   | User registration                       |No            |
| `/login/`               | POST   | JWT login                               |No            |
| `/kyc/`                 | POST   | Submit KYC documents                    |Yes           |
| `/admin/users/`             | GET    | Fetch user profile                      |Yes           |
| `/admin/kyc/`           | GET    | List KYC submissions (Admin only)       |Admin         |

---

## Security Implementation

### 1. Session-based & JWT Authentication
- Use `djangorestframework-simplejwt` for access/refresh tokens
- Protect sensitive endpoints with JWT verification

### 2. Password Hashing
- Store hashed passwords using `bcrypt`
- Ensure strong password policy: min length, alphanumeric, special characters

### 3. Role-Based Access Control
- Decorators or DRF permission classes
- Example roles: `admin`, `customer`
- Sensitive APIs restricted to specific roles

### 4. Input Validation & Sanitization
- Validate email, phone, and document types
- Sanitize inputs to prevent XSS/SQL injection

### 5. Rate limiting
 - Protects important endpoints against bruteforce attack from repetetive access.

---

## Dependencies
- Python >= 3.11
- Django >= 4.2
- Django REST Framework
- bcrypt
- django-ratelimit
- pytest-django, coverage

## Running the project

## Install all dependencies
- pip install -r requirements.txt

## Activate virtual environment
- venv\Source\activate

## Apply migrations
- python manage.py migrate

## Run development server
- python manage.py runserver

## Run test coverage
 - coverage run --source='users' manage.py test users
 - coverage report -m
 - coverage html

## Conclusion

This Smart Banking System provides a secure and modular backend for user registration, login, and KYC submission. It includes:

- Role-based access for customers and admins
- Input validation and sanitization
- Rate limiting to prevent abuse
- Session-based & JWT-based authentication (stateless)
- Unit and integration tests for code coverage

The system demonstrates a robust foundation for building more complex banking features in the future.

## Future Enhancements

Potential improvements for the system include:

- Integration with real banking APIs for transactions
- Multi-factor authentication (MFA) for stronger security
- Improved KYC verification workflow with admin notifications
- Detailed audit logs for all user activities
- Automated deployment and CI/CD pipelines
