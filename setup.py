from setuptools import setup , find_packages
setup(
    author = "Jack Shen",
    description = "A package for NDU student to do NLP",
    name = "ndu_nlp",
    version = '0.1.0',
    packages = find_packages(include=['ndu_nlp','ndu_nlp.*'])
)