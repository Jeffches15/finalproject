# 📦 Project Setup

## GitHub Actions successful run screenshot:

## Screenshots of successful Docker image deployment:


## Docker Hub repository link:
https://hub.docker.com/r/jeffches15/finalproject

## How to run the application:
- After setting up the project and getting all the files situated, do these steps:
   1. docker compose up --build
   2. open a browser tab and go to http://localhost:8000/
   3. open a different tab and go to http://localhost:5050/ (pgAdmin)
      - sign in using account details in docker-compose.yml file
      - create a new server using information in docker-compose.yml file
      - make sure users and calculations tables are in the schema
   4. click register and create an account
   5. log into new account
   6. begin creating new calculations and seeing them display in the calculation history
   7. experiment with "view", "edit", and "delete" features

- When done using the app:
   1. run docker compose down -v
      -  this removes the pgAdmin server and all data created (start again with fresh slate)

## How to run tests locally
In order to run these pytests, the first command to run is: docker compose up -d --build. This command builds the image if its not already there, and starts the containers and it in the background. This "unlocks" the terminal, allowing pytest commands to be entered. We need to run this docker command because we are interacting with a PostgreSQL database and a server to connect to.

Running 'pytest' runs every test function in every test file, but I split this up into several commands. I ran pytest file by file in this order:

- pytest -v -s tests/integration/test_user.py
- pytest -v -s tests/integration/test_user.py --preserve-db (check data in PostgreSQL database)
- pytest -v -s tests/integration/test_calculation.py
   - testing Calculation model
- pytest -v -s tests/integration/test_schema_base.py
- pytest -v -s tests/integration/test_calculation_schema.py
   - testing CalculationCreate and CalculationRead
- pytest -v -s tests/integration/test_user_auth.py
- pytest -v -s tests/integration/test_user_auth.py --preserve-db (check data in PostgreSQL)
- pytest -v -s tests/integration/test_dependencies.py
- pytest -v -s tests/integration/test_database.py
- pytest -v -s tests/e2e/test_fastapi_calculator.py
   - testing Playwright tests and other calculator endpoints
- pytest -s -s tests/e2e/test_bread_operations.py**
   - testing Playwright tests for:
      - **Positive Scenarios:** Successful creation, retrieval, updating, and deletion of calculations.
      - **Negative Scenarios:** Handling invalid inputs, unauthorized access, and error responses.
- pytest -v -s tests/unit/test_calculator.py 

**Note:** -s: show print/log output: tells pytest not to capture stdout/sterr, so print() statements and logging messages are shown immediately in the terminal -v: verbose output: shows the full name and their individual results (e.g., PASSED, FAILED) of each test function instead of just a dot (.)


# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
