# Contributing

Use feature branches and pull requests. Keep fixtures synthetic and private data out of git.

Before a PR:
- python -m unittest discover -s tests -v
- verify any primary-source URL and licenses
- include tests for data unavailable, stale timestamp and source mismatch
- preserve research_only and orders_enabled=false
- do not add order endpoints or real brokerage statements
