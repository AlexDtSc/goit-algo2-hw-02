from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    # 1. Перетворюємо звичайні словники (Dict) на об'єкти Dataclass
    jobs = [PrintJob(**job) for job in print_jobs]
    printer_limits = PrinterConstraints(**constraints)

    # 2. Сортуємо завдання за пріоритетом (1 - найвищий, тому сортуємо за зростанням)
    # Python сортує "стабільно", тобто якщо пріоритети однакові, порядок збережеться
    jobs.sort(key=lambda j: j.priority)

    print_order = []
    total_time = 0

    current_batch = []
    current_volume = 0

    # 3. Жадібний алгоритм: формуємо групи (партії) для друку
    for job in jobs:
        # Перевіряємо, чи влізе ця деталь у поточну партію за кількістю та об'ємом
        if len(current_batch) < printer_limits.max_items and current_volume + job.volume <= printer_limits.max_volume:
            current_batch.append(job)
            current_volume += job.volume
        else:
            # Деталь не влізла! Відправляємо поточну партію на друк
            print_order.extend([j.id for j in current_batch])
            total_time += max([j.print_time for j in current_batch])
            
            # Створюємо нову партію, куди одразу кладемо деталь, що не влізла
            current_batch = [job]
            current_volume = job.volume

    # 4. Після циклу у нас могла залишитися остання партія, яку теж треба "надрукувати"
    if current_batch:
        print_order.extend([j.id for j in current_batch])
        total_time += max([j.print_time for j in current_batch])

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()