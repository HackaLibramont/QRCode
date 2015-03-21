#!/bin/env python

from model import create_all, drop_all

if __name__ == "__main__":
    drop_all()
    create_all()
