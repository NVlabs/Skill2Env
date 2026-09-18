def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: live Playwright smoke tests against authenticated NotebookLM profile")
