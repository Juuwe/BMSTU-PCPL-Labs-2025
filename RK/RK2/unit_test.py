import pytest
from database import *

@pytest.fixture
def database():
    test_langs = [
    # ID: 1, 2, 3, 4, 5
    Language("Python", "3.12"),
    Language("Java", "21"),
    Language("Rust", "1.74"),
    Language("Go", "1.21"),
    Language("C#", "12"),
    # ID: 6, 7, 8, 9, 10
    Language("JavaScript", "ES2023"),
    Language("TypeScript", "5.2"),
    Language("Swift", "5.9"),
    Language("Kotlin", "1.9"),
    Language("PHP", "8.3"),
    ]

    database = Database()
    database.add_languages(test_langs)
    return database

@pytest.fixture(autouse=True)
def reset_database():
    DatabaseEntity.reset_id_counter()

def test_first_query(database: Database):
    test_ides = [
        IDE("PyCharm", 1),  # Python
        IDE("VS Code", 1),
        IDE("Sublime Text", 1)
    ]

    database.add_ides(test_ides)

    result = database.first_query()
    assert result == [("PyCharm", "Python"), ("Sublime Text", "Python"), ("VS Code", "Python")]

def test_second_query(database: Database):
    test_ides = [
        IDE("PyCharm", 1),  # Python
        IDE("VS Code", 1),
        IDE("Sublime Text", 1),

        IDE("IntelliJ", 2),  # Java
        IDE("Eclipse", 2)
    ]

    database.add_ides(test_ides)

    result = database.second_query()
    assert result == [("Python", 3), ("Java", 2)]

def test_third_query(database: Database):
    test_ides = [IDE("PyCharm"), IDE("IntelliJ")]
    database.add_ides(test_ides)

    relations = [LanguageIDE(language_id=1, IDE_id=1), LanguageIDE(language_id=2, IDE_id=2)]
    database.add_lang_ide_relations(relations)

    result = database.third_query("PyCham")
    assert len(result) > 0
    assert result[0][0] == "PyCharm"
    assert "Python" in result[0][1]
