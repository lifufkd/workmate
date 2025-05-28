from src.report_handlers.base import BaseReport


class PayoutHandler(BaseReport):
    def __init__(self):
        pass

    def _calculate_payout(self, employee_data: dict) -> int | None:

        # Trying to find existing filed name
        rate = employee_data.get("hourly_rate") or employee_data.get("rate") or employee_data.get("salary") or None
        if not rate:
            return None

        try:
            # Calculate payout with ValueError exception on case if field in error format or null
            payout = int(employee_data["hours_worked"]) * int(rate)
        except ValueError:
            return None
        else:
            return payout

    def _sort_and_aggregate_by_payout(self, departments_data: dict) -> dict:

        # Sort departments alphabetically
        sorted_departments = dict(
            sorted(departments_data.items(), key=lambda d: d[0], reverse=False)
        )

        # Sorting employees by salary
        for department, data in sorted_departments.items():
            employees = data.get("employees", [])
            data["employees"] = sorted(employees, key=lambda e: e["payout"], reverse=False)

        # Adding summary information to each department
        for department in sorted_departments.keys():
            employees_worked_hours = 0
            employees_payout = 0
            for employee in sorted_departments[department]['employees']:
                employees_worked_hours += int(employee['hours_worked'])
                employees_payout += int(employee['payout'])

            sorted_departments[department]["summary"] = {"worked_hours": employees_worked_hours, "payout": employees_payout}

        return sorted_departments

    def process_data(self, employees_data: list[dict]) -> dict:
        result = dict()
        # Create copy of employees_data for avoid changing object in outer scope
        employees_data_copy = employees_data.copy()

        for employee in employees_data_copy:

            # Calculate payout
            payout = self._calculate_payout(employee_data=employee)
            if not payout:
                continue
            # Set payout
            employee.update({"payout": payout})

            # Create output obj structer & fill with employees
            if result.get(employee["department"]):
                if result[employee["department"]].get("employees"):
                    result[employee["department"]]["employees"].append(employee)
                else:
                    result[employee["department"]]["employees"] = [employee]
            else:
                result[employee["department"]] = {
                    "employees": [employee]
                }

        # Sort & aggregate employees
        result = self._sort_and_aggregate_by_payout(departments_data=result)

        return result
