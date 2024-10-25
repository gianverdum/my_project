# src/test_imports.py
import sys

from src.models.member import Member

print("\n".join(sys.path))


print("Imported Member from:", Member.__module__)
