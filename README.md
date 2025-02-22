# COMP0035 Coursework 02 reassessment starter repository

1. Create a project in VS Code, PyCharm or other Python IDE
2. Create and activate a virtual Python environment.
3. The coursework code should have the following structure:

    ```text
     my_project/
     ├── .gitignore             # Git ignore file
     ├── README.md              # Project description and instructions
     ├── requirements.txt       # List of dependencies
     ├── pyproject.toml         # Installation and package details
     ├── src/                   # Main code directory
     │   ├── traffic/               # Traffic package directory
     │      ├── __init__.py        # Makes this directory a package
     │      ├── traffic.db         # SQLite database with some of the traffic data
     │      ├── trafficdata.py     # Python class that creates and instance of the data with methods
     ├── tests/                 # Test suite
     │   ├── conftest.py        # Tests for main module
     │   ├── test_hello.py      # Example tests
     └── ...                    # Add module for your tests

      ```
4. Install the project code using `pip install -e .`.

   If you use this command you should not also need to use the `requirements.txt` file. If this step fails, then install
   the required packages by entering `pip install -r requirements.txt` in the IDE's terminal window.

5. Run the tests in `test_hello.py`. These should pass if your project files are structured as above and you completed
   `pip install -e .`