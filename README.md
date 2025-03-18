# Nexu Fullstack Project

This repository contains a fullstack project consisting of:

- **Backend** (FastAPI, MongoDB via Motor, Docker): Provides endpoints to manage brands and models.
- **Frontend** (React, Axios, React Router): A user interface that consumes the backend endpoints.

---

## Table of Contents

- [Nexu Fullstack Project](#nexu-fullstack-project)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Requirements](#requirements)
  - [Backend](#backend)
    - [Installation and Running the Backend](#installation-and-running-the-backend)
    - [Main Endpoints](#main-endpoints)
    - [Testing](#testing)
    - [Docker](#docker)
      - [Building and Running Locally](#building-and-running-locally)
      - [Pushing to AWS ECR](#pushing-to-aws-ecr)
  - [Frontend](#frontend)
    - [Installation and Running the Frontend](#installation-and-running-the-frontend)
    - [Production Build](#production-build)
    - [Deployment Options](#deployment-options)
  - [Environment Variables](#environment-variables)
    - [Backend](#backend-1)
    - [Frontend](#frontend-1)
  - [GitHub Actions](#github-actions)
    - [To configure GitHub Actions:](#to-configure-github-actions)
  - [License](#license)

---

## Project Structure

```
nexu-backend-test/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── ... (other backend files)
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   │   ├── Header.js
    │   │   ├── BrandList.js
    │   │   ├── BrandForm.js
    │   │   ├── ModelList.js
    │   │   ├── ModelForm.js
    │   │   └── FilteredModelList.js
    │   ├── services/
    │   │   └── api.js
    │   ├── App.js
    │   ├── App.css
    │   └── index.js
    ├── package.json
    └── ... (other frontend files)
```

---

## Requirements

- **Backend:**
  - Python 3.12+
  - Poetry for dependency management
  - MongoDB (local or hosted, e.g., Mongo Atlas)
  - Docker (optional, for containerizing the backend)
  - AWS CLI (optional, if using ECR for Docker images)

- **Frontend:**
  - Node.js 14+ and npm (or yarn)
  - Create React App

---

## Backend

### Installation and Running the Backend

1. **Clone the repository and navigate to the backend folder:**

   ```bash
   git clone https://github.com/your-username/nexu-backend-test.git
   cd nexu-backend-test/backend
   ```

2. **Install dependencies using Poetry:**

   ```bash
   poetry install
   ```

3. **Set the required environment variables** (see [Environment Variables](#environment-variables)).

4. **Run the FastAPI server:**

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

   The API will be available at [http://localhost:8000](http://localhost:8000).

### Main Endpoints

- **GET /brands**: List all brands.
- **POST /brands**: Create a new brand.
- **GET /brands/:id/models**: List models for a specific brand.
- **POST /brands/:id/models**: Create a new model for a specific brand.
- **GET /models?greater=&lower=**: Filter models by price.
- **PUT /models/:id**: Update the average price of a model.

### Testing

We use **pytest** and **pytest-asyncio** for testing.

To run tests, execute:

```bash
cd backend
poetry run pytest
```

### Docker

#### Building and Running Locally

1. **Build the Docker image:**

   ```bash
   docker build -t nexu-backend:latest .
   ```

2. **Run the container:**

   ```bash
   docker run -p 8000:8000 nexu-backend:latest
   ```

   The API will be accessible at [http://localhost:8000](http://localhost:8000).

#### Pushing to AWS ECR

1. **Log in to ECR:**

   ```bash
   aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<your-region>.amazonaws.com
   ```

2. **Tag and push the image:**

   ```bash
   docker tag nexu-backend:latest <account-id>.dkr.ecr.<your-region>.amazonaws.com/nexu-backend:latest
   docker push <account-id>.dkr.ecr.<your-region>.amazonaws.com/nexu-backend:latest
   ```

---

## Frontend

### Installation and Running the Frontend

1. **Navigate to the frontend folder:**

   ```bash
   cd ../frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```
   or
   ```bash
   yarn
   ```

3. **Start the development server:**

   ```bash
   npm start
   ```
   The app will be available at [http://localhost:3000](http://localhost:3000).

4. **Configure the API Base URL:**

   In `src/services/api.js`, ensure the baseURL points to your backend API:
   ```javascript
   import axios from 'axios';
   
   const API = axios.create({
     baseURL: 'http://localhost:8000', // or your production URL
   });
   
   export default API;
   ```

### Production Build

To build the frontend for production, run:

```bash
npm run build
```

This creates a `build/` directory with optimized static files.

### Deployment Options

- **Netlify**: Set the publish directory to `build`.
- **Vercel**: It automatically detects a Create React App project.
- **AWS Amplify**: Set the base directory to `frontend` and output directory to `build`.
- **S3 + CloudFront**: Upload the contents of `build/` to an S3 bucket configured for static website hosting.

---

## Environment Variables

### Backend

- **MONGO_DETAILS**: MongoDB connection string (e.g., `mongodb+srv://<user>:<password>@cluster0.mongodb.net/<db>?retryWrites=true&w=majority`).
- **Other backend-specific variables** as needed.

### Frontend

- In `frontend/.env` (which should not be committed), you can define:
  - `REACT_APP_API_URL=http://localhost:8000` (or your production URL).

---

## GitHub Actions

We have workflows set up for:
- Running pre-commit checks.
- Building and pushing Docker images to AWS ECR.

Workflows are located in the `.github/workflows/` folder.

### To configure GitHub Actions:

1. **Add the following repository secrets** in GitHub:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`
   - `ECR_REPOSITORY` (e.g., `123456789012.dkr.ecr.<your-region>.amazonaws.com/nexu-backend`)

2. **The workflow (e.g., `.github/workflows/ecr-deploy.yml`) will automatically build and push the Docker image** on every push to the `main` branch.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.