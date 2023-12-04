# Flask Auth Project

## Description

This project is a Flask application for authentication and authorization.

## Getting Started

To run this project locally, make sure you have Docker installed on your machine.

### Prerequisites

- Docker installed on your machine

### Build and Run

Build the Docker container:

```bash
docker build -t flask-auth-app .
```

Run the conainter:

```bash
docker run -p 5000:5000 flask-auth-app
```

# Routes

## Empty Page
GET /

An empty page.

## Get CSRF Token
GET /csrf

Endpoint to get a CSRF token.

## Login
POST /login

Endpoint for user login.

## Protected Page
GET /protected

A protected page that requires authentication.