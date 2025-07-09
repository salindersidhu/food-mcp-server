
# Food MCP Server

[![Contributors](https://img.shields.io/github/contributors/salindersidhu/food-mcp-server?style=for-the-badge)](https://github.com/salindersidhu/food-mcp-server/graphs/contributors)
[![License](https://img.shields.io/badge/license-Apache%202.0-brightgreen.svg?style=for-the-badge)](/LICENSE)

## Overview

A FastAPI-based MCP server that exposes endpoints for searching meals, fetching meal details, categories, and regional dishes using TheMealDB API. Built using Python and other open source technologies.

<p float="left">
    <img src="https://hub.docker.com/api/media/repos_logo/v1/library%2Fpython?type=logo" height="150" width="150">
    <img src="https://cdn.worldvectorlogo.com/logos/fastapi.svg" height="150" width="150">
    <img src="https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/mcp.png" height="150" width="150">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2n9vMsjdx7gIMP96b-5GAxAWyExZlLkX4blsM5ywS54T8leQlRkMh6BhvXVIWcZGoYJQ&usqp=CAU" height="150" width="150">
</p>

## Prerequisite Software

| Software | Version  |
| :------- | :------- |
| Git      | 2.20.1+  |
| Python   | 3.11+    |

## Getting Started

1. Clone the repository:

```bash
git clone git@github.com:salindersidhu/food-mcp-server.git
cd food-mcp-server
```

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:


```bash
pip install -U pip
pip install -e .
```

4. (Optional) Add to Claude Desktop as a tool:

   - Run the following command to register this server as a tool in Claude Desktop:

     ```bash
     uv run mcp install main.py
     ```

## Running

To start the MCP server locally:

```bash
mcp run main.py
```

## Production

1. Merge your changes into the main branch.
2. Deploy using your preferred Python hosting or container solution.

## Project Structure

    .
    ├── main.py              # MCP server entry point
    ├── pyproject.toml       # Project metadata and dependencies
    ├── LICENSE              # License file
    ├── README.md            # This file
    └── ...

## License

This project is licensed under the Apache License 2.0.

