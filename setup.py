from setuptools import setup, find_packages
import pathlib

base_path = pathlib.Path(__file__).parent.resolve()
long_description = (base_path / "README.md").read_text(encoding="utf-8")

setup(
    name="pyg",
    version="0.0.1",
    description="Simple OpenGL-based graphics library for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Talendar/pyg",
    author="Gabriel Nogueira (Talendar)",
    keywords="graphics, opengl, draw",
    python_requires=">=3.9, <4",
    install_requires=[
        "numpy==1.22.3",
        "PyGLM==2.5.7",
        "PyOpenGL==3.1.6",
        "PyOpenGL-accelerate==3.1.5",
        "glfw==2.5.1",
        "Pillow==9.1.1",
    ],
    extras_require={
        "dev": [
            "mypy~=0.942",
            "pylint~=2.13.5",
        ]
    }
)
