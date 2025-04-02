#!/usr/bin/env bash

# Install Python deps
pip install -r requirements.txt

# Install Playwright browser binaries (no root access needed)
playwright install chromium
