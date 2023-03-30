from setuptools import find_packages, setup

setup(
    name="Caster Modules",
    version="0.1",
    packages=find_packages(exclude=('tests*',)),
    python_requires=">=3.9",
    install_requires=[
        'PyChromecast',
        'pytube',
        'ntfpy',
        'beautifulsoup4',
        'selenium',
        'pyTelegramBotAPI',
        'dacite',
        # Dev tools
        'pylint',
        'autopep8',
        # isort
    ]
)
