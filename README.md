# Intro
This repo contain a Behavior-Driven Development (BDD) test automation project written in `Python` using `pytest-bdd` framework.
I suggest reading `pytest-bdd` docs to understand how it utilizes fixtures.
[pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/en/stable/)


The project utilize `https://jsonplaceholder.typicode.com` **fake** API service.
Please note that this API doesn't persist data changes, limiting the test assertions in `@then` steps.

# Installation
The project has been tested and verified with `Python 3.7` on `MacOS - Sonoma`.
To start installation, create a `Python` virtual environment and activate it:
```bash
python -m venv venv-e2e
source venv-e2e/bin/activate
```

Install all packages from requirements file.

``` bash
pip install -r requirements.txt
```

# Files Relationships
`pytest-bdd` links Gherkin feature file scenarios to Python test implementations using the `scenarios()` function, enabling associations via step definitions and markers.

``` python
# Content of steps/posts/test_posts.py

scenarios('../../features/posts.feature')
```

`pytest-bdd` has limitation to share steps between features, unlike other BDD framework where it works out of the box.
To share steps between feature files, in `test_x.py` you will need to import step functions from `steps/feature_y_steps/steps.py`.

You can see example in how posts steps are imported in `steps/comments_steps/test_comments.py` and being used in `features/comments.feature`.
- It is also possible to import steps in `conftest.py` to make steps available across all feature files.

The project structure is organized as follows:

```
Pytest-BDD-Project
|___features
     |___posts.feature
|___steps
|    |___posts_steps
|        |___test_posts.py
|        |___steps.py
|___conftest.py
```
In the table bellow I will explain the meaning behind the structure, I will use `posts.feature` as an example:

| Name                            | Info                                                                                                                                               |
|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| posts.feature                   | Contains scenarios related to posts API and verifies data associated with posts responses.                                                         | 
| steps/posts_steps               | Includes relevant steps for handling posts and can be shared across multiple feature files.                                                        | 
| steps/posts_steps/steps.py      | Houses @given and `@when` steps specifically for posts, available to be imported and use in any feature file.                                      | 
| steps/posts_steps/test_posts.py | Contains `@the`n steps solely for the `posts.feature`, it is possible to import steps from other features if needed to be used in `posts.feature`. | 
| conftest.py                     | Holds standard Pytest configurations, including fixtures applicable to the entire project (e.g., Client).                                          | 

* **Note**: Avoid importing steps from `test_*.py` files to prevent test duplication and failures.


## Reporting
The project uses the standard `pytest-html` report with the `pytest-bdd-html` plugin for BDD reporting.

You can find more information about these plugins at:
* [pytest-html](https://pypi.org/project/pytest-html)
* [pytest-bdd-html](https://pypi.org/project/pytest-bdd-html/0.1.6rc0)


* **Note**: I am modifying the "Link" default column and cell values of the HTML report to highlight the failed step in `conftest.py`.

![img.png](utils%2Freadme_screenshots%2Fimg.png)

## Run Commands
| Command                                                                 | Info                                                                                                  |
|-------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| ```pytest```                                                            | Executes all tests.                                                                                   | 
| `pytest -vv`                                                            | Displays verbose terminal reports.                                                                    | 
| `pytest -m "posts"`                                                     | Runs tests marked with `@posts`.                                                                      | 
| `pytest -m "comments" --html=reports/report.html --self-contained-html` | Executes `@posts` tests and generate an HTML report.                                                  | 
| `pytest --worker 5`                                                     | Runs tests in parallel using the `pytest-parallel` library with 5 processes.                          | 
| `pytest --tenv="jsonplaceholder"`                                       | Uses a custom `pytest` command option for domain prefix. **Note**: No real QA/Dev environment exists. | 
