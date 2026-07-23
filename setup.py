from setuptools import setup, find_packages

setup(
    name="nexora3bot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot==20.7",
        "requests==2.31.0",
        "Pillow==10.1.0",
        "python-dotenv==1.0.0",
        "aiohttp==3.9.1",
    ],
)
