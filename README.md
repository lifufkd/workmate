
# Скрипт подсчёта зарплаты сотрудников

Скрипт позволяет формировать отчёты по зарплате сотрудников на основе одного или нескольких CSV-файлов.

## 📌 Возможности

- Поддержка CSV-файлов с разным порядком колонок и разными названиями ставки (`hourly_rate`, `rate`, `salary`).
- Генерация отчёта по зарплатам (`--report payout`).
- Вывод отчёта в консоль.
- Экспорт отчетов в json (`--export-file-name report.json --export-type JSON`).
- Расширяемая архитектура: добавление новых **типов отчётов** и **форматов экспорта** без переписывания основной логики.
- Полное покрытие тестами с использованием `pytest`.

## 🚀 Пример запуска

```bash
python3 main.py data1.csv data2.csv --report payout --export-file-name report.json --export-type JSON
```

## 📊 Пример отчёта

```
Design
name                 hours  rate   payout
-------------------- -----  -----  --------
Bob Smith             150   40     $6,000
Carol Williams        170   60     $10,200
                      320          $16,200
```

## ⚙️ Как добавить новый отчёт

1. **Создай новый класс отчёта**, унаследованный от базового интерфейса `Report`:
    ```python
    class AvgRateReport(BaseReport):
        def process_data(self, employees_data: list[dict]) -> dict:
            ...
    ```

2. **Используйте класс отчёта**:
    ```python
    def process_data(report_mode: str, raw_employees_data: list[dict]) -> dict:
    match report_mode:
        case "avg_rate":
            processed_data = AvgRateReport().process_data(raw_employees_data)
    ```

3. **Добавь обработку нового параметра** `--report` в `argparse`.

## ✅ Требования

- Python 3.7+

## 🧪 Тестирование

```bash
python -m pytest --cov src
```

## 📁 Структура проекта

```
workmate/
├── src/
│   ├── report_handlers/
│        ├── base.py
│        └── payout.py
│   ├── file_managers/
│        ├── csv_manager.py
│        └── json_manager.py
│   └── main.py
├── tests/
│   ├── test_csv_manager.py
│   ├── test_json_manager.py
│   ├── test_main.py
│   └── test_payout.py
├── docs/
│   ├── examples/
│   └── screenshots/
└── README.md
```
