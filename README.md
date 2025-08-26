![Random picture from my walk](sky.png)

*To see things as they are. Substance, cause and purpose. - Marcus Aurelius*

## Summary

A simple project, based on Astral's uv, for testing a subset of the GitHub API
using REST requests. It's implemented in Python with requests and pytest. The
test results are in Allure format.

### Local setup

- Add `github-pat`="<your-github-pat>" to `tests/resources/config.toml`
- Run `uv run pytest --alluredir allure-results tests/` to execute the tests
- Run `uv run allure serve allure-results` to view Allure report
