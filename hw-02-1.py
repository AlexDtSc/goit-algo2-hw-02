def find_min_max(arr):
    # Якщо масив порожній, повертаємо помилку або None
    if not arr:
        return None

    # Допоміжна рекурсивна функція
    def get_min_max(low, high):
        # Базовий випадок 1: Якщо залишився лише 1 елемент
        if low == high:
            return arr[low], arr[low]

        # Базовий випадок 2: Якщо залишилося 2 елементи (пара)
        if high == low + 1:
            if arr[low] < arr[high]:
                return arr[low], arr[high]
            else:
                return arr[high], arr[low]

        # Стадія "Розділяй": знаходимо середину
        mid = (low + high) // 2

        # Стадія "Володарюй": рекурсивно шукаємо в лівій і правій половинах
        left_min, left_max = get_min_max(low, mid)
        right_min, right_max = get_min_max(mid + 1, high)

        # Стадія "Об'єднуй": порівнюємо переможців половин
        final_min = left_min if left_min < right_min else right_min
        final_max = left_max if left_max > right_max else right_max

        return final_min, final_max

    # Запускаємо процес для всього масиву (від 0 до останнього індексу)
    return get_min_max(0, len(arr) - 1)

# Тестування
if __name__ == "__main__":
    test_array = [38, 27, 43, 3, 9, 82, 10]
    result = find_min_max(test_array)
    print(f"Масив: {test_array}")
    print(f"(Мінімум, Максимум): {result}")