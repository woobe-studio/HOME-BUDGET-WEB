import unittest
from datetime import datetime
from scripts.custom_scripts import is_leap_year, get_years, get_months, get_days, get_day_names

class TestLeapYear(unittest.TestCase):

    def test_leap_year_divide_by_4(self):
        # Sprawdza czy rok 2024 jest przestępny 2024 dzieli sie przez 4
        self.assertTrue(is_leap_year(2024))

    def test_not_leap_year_not_divide_by_4(self):
        # Sprawdza czy rok 2023 jest przestępny, 2023 nie dzieli się przez 4
        self.assertFalse(is_leap_year(2023))

    def test_leap_year_divide_by_100(self):
        # Sprawdza czy rok 1900 jest przestępny, jest podzielny przez 100
        self.assertFalse(is_leap_year(1900))

    def test_leap_year_divide_by_400(self):
        # Sprawdza czy rok 2000 jest przestępny, jest podzielny przez 400
        self.assertTrue(is_leap_year(2000))

    def test_leap_year_invalid_input(self):
        # Sprawdza poprawność przyjmowania parametrów do funkcji
        # Aktualnie funkcja nie sprawdza poprawnosci parametrów więc jest FALSE !!!!!!
        for value in ["2024", None, 2024.5]:
            with self.assertRaises(TypeError):
                is_leap_year(value)



class TestGetYears(unittest.TestCase):

    def test_get_years(self):
        # Sprawdza czy funkcja get_years()
        # - zwraca 11 lat
        # - czy pierwszy wynik jest równy obecny rok - 10 i jest stringem
        # - czy ostatni rekord jest równy obecnemu rokowi
        current_year = datetime.now().year

        self.assertEqual(len(get_years()), 11)
        self.assertEqual(get_years()[0], str(current_year - 10))
        self.assertEqual(get_years()[-1], str(current_year))

    def test_get_years_are_strings(self):
        # Sprawdza czy lata są instancjami stringa
        for year in get_years():
            self.assertIsInstance(year,str)
        
    def test_get_years_with_parameter(self):
        # Sprawdza czy funkcja wyrzuci błąd przy podaniu parametru
        with self.assertRaises(TypeError):
            get_years(2026)

    def test_get_years_sorted_output(self):
        # Sprawdza czy wynik jest w porządku rosnacym
        self.assertEqual(get_years(), sorted(get_years()))


class TestGetMonths(unittest.TestCase):

    def test_get_months_length(self):
        # Sprawdza czy fukcja zwróci długość 12 równą ilości miesięcy
        self.assertEqual(len(get_months()), 12)

    def test_get_months_expected_keys(self):
        # Sprawdza czy wszystkie miesiace są obecne
        expected_keys = ['January', 'February', 'March', 'April', 'May', 'June','July','August','September','October','November','December']

        for key in expected_keys:
            self.assertIn(key, get_months())

    def test_get_months_assigned_values(self):
        # Sprawdza czy każdy miesiąc ma poprawnie przypisaną wartość
        expected_values = {
            'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 
            'May' : 5, 'June' : 6,'July' : 7,'August' : 8,'September' : 9,
            'October' : 10,'November' : 11,'December' : 12
        }

        self.assertEqual(get_months(),expected_values)

    def test_get_months_output_type(self):
        # Sprawdza czy wynik funkcji jest słownikiem
        self.assertIsInstance(get_months(),dict)

    def test_get_months_order(self):
        # Sprawdza czy kolejność miesięcy jest poprawna
        expected_keys = [
            'January', 'February', 'March', 
            'April', 'May', 'June','July','August',
            'September','October','November','December'
        ]

        for i in range(0,12):
            self.assertEqual(list(get_months().keys())[i], list(expected_keys)[i])

    def test_get_months_no_arguments(self):
        # Sprawdza czy funkcja nie przyjmuje parametrów
        for value in ["13", 11, None]:
            with self.assertRaises(TypeError):
                get_months(value)

    
class TestGetDays(unittest.TestCase):

    def test_get_days_february_leap_year(self):
        # Sprawdza czy dla lutego roku przestępnego ma 29 dni
        self.assertEqual(len(get_days(2024,2)), 29)

    def test_get_days_february_not_leap_year(self):
        # Sprawdza czy dla lutego roku nie przestępnego ma 28 dni
        self.assertEqual(len(get_days(2023,2)), 28)

    def test_get_days_invalid_parameter(self):
        # Sprawdza czy funkcja obsługuje niepoprawne parametry
        with self.assertRaises(TypeError):
            get_days("2026","10")
            get_days(2026,30)
            get_days(None, 2)

    
class TestGetDayNames(unittest.TestCase):

    def test_get_day_names_number_of_days(self):
        # Sprawdza czy funkcja zwraca 7 elementów
        self.assertEqual(len(get_day_names()), 7)

    def test_get_day_names_all_days_are_present(self):
        # Sprawdza czy wszystkie dni tygodnia są obecne
        expected_days = [
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ]

        for day in expected_days:
            self.assertIn(day, get_day_names())

    def test_get_day_names_order(self):
        # Sprawdza poprawną kolejność dni tygodnia
        expected_days = [
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ]

        self.assertEqual(get_day_names(), expected_days)

    def test_get_day_names_output_type(self):
        # Sprawdza czy wynik funkcji jest listą
        self.assertIsInstance(get_day_names(), list)

    def test_get_day_names_invalid_parameter(self):
        # Sprawdza czy funkcja obsługuje parametry
        with self.assertRaises(TypeError):
            get_day_names("1")
            get_day_names(1)
            get_day_names(None)

    def test_get_day_names_are_strings(self):
        # Sprawdza czy wszystkie elementy sa stringami
        for day in get_day_names():
            self.assertIsInstance(day, str)


if __name__ == "__main__":
    unittest.main()