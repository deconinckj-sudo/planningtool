#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Thiry Planning Tool - Start hier!
"""

import sys
import os

# Voeg root directory toe aan Python path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == '__main__':
    from src.main import main
    main()