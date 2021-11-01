from dataclasses import dataclass
from tinydb import TinyDB, where
from datetime import date
today = date.today()
DB_PATH = 'mvc-history-db.json'
db = TinyDB(DB_PATH)
history_cat_table = db.table('history')


@dataclass
class history:
    """
    represent commands history
    """
    category_lst: list
    date: date


class HistoryModelWrapper:
    """
    warpped class to handle request history and store it in the db
    """

    @classmethod
    def get_by_date(cls, date) -> history:
        """
        return the category that fits date
        :return: record from the db by date
        """
        return history_cat_table.search(where('date') == date)

    @classmethod
    def create(cls, cat: int):
        """
        insert the db new category or update the category list if the number already exists
        """
        if cls.get_by_date(str(date.today())):
            if cat not in cls.get_by_date(str(date.today()))[0]['category_lst']:
                cat_lst =cls.get_by_date(str(date.today()))[0]['category_lst']+[cat]
                history_cat_table.update({'category_lst': cat_lst}, where('date') == str(date.today()))
            else:
                return True
        else:
            history_cat_table.insert({'category_lst': [cat], 'date': str(date.today())})
        return False


