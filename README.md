# Intro
A BDD test automation project written in `Python` using `pytest-bdd` framework.
I suggest reading `pytest-bdd` docs to understand how it utilizes fixtures.
https://pytest-bdd.readthedocs.io/en/stable/


The project utilize `https://jsonplaceholder.typicode.com` **fake** API service.
* **Note**: the API does not really create resources, so the test assertions are limited in `@then` steps.

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
`pytest-bdd` utilizes feature files to define the scenarios.
Each feature file has a `pytest` `test_*.py` file connected to it, so pytest will collect at it as test.
The connection is done by this line:

``` python
# Content of steps/posts/test_posts.py

scenarios('../../features/posts.feature')
```

`pytest-bdd` has limitation to share steps between features, unlike other BDD framework where it works out of the box.
To share steps between feature files, in `test_x.py` you will need to import step functions from `steps/feature_y_steps/steps.py`.
You can see example in `/steps/comments_steps/test_comments.py`.

The project structured as the following:
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

| Name                            | Info                                                                                                                                                                                                                                                                                                                              |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| posts.feature                   | Only scenarios that are related to posts API, it will also verify data that related to posts response.                                                                                                                                                                                                                            | 
| steps/posts_steps               | Relevant steps to posts, can be shared in any feature file by importing them.                                                                                                                                                                                                                                                     | 
| steps/posts_steps/steps.py      | Only has `@given` and `@when` relevant posts steps, these steps can be used on any feature file.                                                                                                                                                                                                                                  | 
| steps/posts_steps/test_posts.py | Only has `@then` steps. These steps are available only on the feature file defined in `scenarios("path/to/posts.feature")`. Here we also import steps from other feature, so they will be available in `posts.feature` file. It will also contain only`@then` steps, to maintain clean seperation between assertions and actions. | 
| conftest.py                     | Pytest standard configuration file. Contain fixtures that are relevant to the whole project, such as `Client`.                                                                                                                                                                                                                    | 

* **Note**: Never import steps from `test_*.py` - it cause test duplication and failures.


## Reporting
I am using the standard `pytest-html` report with a plugin that enable bdd reporting called `pytest-bdd-html`. You can read more about these plugins on:
https://pypi.org/project/pytest-html/ and https://pypi.org/project/pytest-bdd-html/0.1.6rc0/.


* **Note**: I am modifying the "Link" default column and cell values of the HTML report to highlight the failed step in `conftest.py`.

![img.png](utils%2Freadme_screenshots%2Fimg.png)

## Run Commands
| Command                                                                 | Info                                                                                                                       |
|-------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| ```pytest```                                                            | Will run all tests.                                                                                                        | 
| `pytest -vv`                                                            | Verbose terminal report.                                                                                                   | 
| `pytest -m "posts"`                                                     | Run tests only with `@posts` marker. Find available markers in `pytest.ini`.                                               | 
| `pytest -m "comments" --html=reports/report.html --self-contained-html` | Run `@posts` marked tests with HTML report.                                                                                | 
| `pytest --worker 5`                                                     | Parallel executing using `pytest-parallel` library on 5 processes.                                                         | 
| `pytest --tenv="jsonplaceholder"`                                       | Custom `pytest` command option for domain prefix. Search for `env` fixture. **Note**: there is no real QA/Dev environment. | 
