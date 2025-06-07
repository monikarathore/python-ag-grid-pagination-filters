Project Description:

This project is a Python-based REST API built with FastAPI that integrates seamlessly with AG Grid on the frontend. It supports advanced grid functionalities such as conditional text filtering, multiple filter operators (contains, equals, starts with, ends with, blank, not blank, etc.), and logical operators (AND, OR) for combined filter conditions. The API also includes efficient pagination and dynamic sorting capabilities to handle large datasets with ease.

Key features include:

Robust support for AG Grid’s complex filter models

Flexible text filtering with multiple operators

Support for combining filter conditions using AND/OR logic

Server-side pagination and sorting for optimized data retrieval

Modular and reusable filter construction functions for easy maintenance and extension

This setup ensures a powerful, scalable backend API to serve dynamic grid-based data tables with rich user interaction and filtering capabilities.

# FastAPI Project with AG-Grid Filters, Sorting, and Pagination

This project is a Python FastAPI backend API that supports AG-Grid conditional filters, text filters, sorting (ascending and descending), and pagination.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-project-folder>


## Setting Up the Project Locally

### 1. Create and activate a Python virtual environment

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload