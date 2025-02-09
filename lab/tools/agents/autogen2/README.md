Demo Autogen project that plan and execute tasks

## Installation

### Prerequisites
Ensure you have the following installed:
- [Git](https://git-scm.com/)
- [Poetry](https://python-poetry.org/)
- Python (version required by the project)

### Clone the Repository
```sh
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### Install Dependencies
```sh
poetry install
```

## Usage

### Set Up Environment Variables
You need to set the `OPENAI_API_KEY` before running the project:

- **On macOS/Linux**
  ```sh
  export OPENAI_API_KEY="your-api-key"
  ```
- **On Windows (PowerShell)**
  ```powershell
  $env:OPENAI_API_KEY="your-api-key"
  ```

### Run the Application
```sh
poetry run python main.py
```









