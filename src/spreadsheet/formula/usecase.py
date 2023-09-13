from spreadsheet.formula.repository import FormulaRepo


class FormulaCrudUsecase:
    def __init__(self, repo: FormulaRepo):
        self._repo = repo

    def create_plan_items(self):
        pass
