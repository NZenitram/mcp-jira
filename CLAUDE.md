# MCP-JIRA Project Guidelines

## Development Commands
- Setup environment: `/opt/homebrew/bin/python3.10 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- Run tests: `source venv/bin/activate && python -m pytest`
- Run single test: `source venv/bin/activate && python -m pytest tests/test_file.py::test_function`
- Test JIRA connection: `source venv/bin/activate && python -m pytest tests/test_jira_connection.py -v`
- Run application: `source venv/bin/activate && python -m src.main`
- Install dependencies: `source venv/bin/activate && pip install -r requirements.txt`

## Code Style
- Imports: Group standard library, third-party, and local imports (separated by blank line)
- Docstrings: Use """triple quotes""" for all functions, classes, and modules
- Type hints: Use for function parameters and return values
- Naming: snake_case for variables/functions, PascalCase for classes
- Error handling: Use try/except blocks with specific exceptions
- Environment variables: Access via os.getenv() after load_dotenv()
- FastMCP tools: Place in src/tools/ directory using appropriate decorators

## Project Structure
- src/main.py: Application entry point
- src/tools/: FastMCP tool implementations
- tests/: Test files (prefix with test_)