import os

__all__ = []

for folder in os.listdir(os.path.dirname(__file__)):
    if os.path.isdir(folder):
        __all__.append(folder)

if __name__ == "__main__":
    print(__all__)
