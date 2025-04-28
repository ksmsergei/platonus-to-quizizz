import pandas as pd

# Функция для обработки текстового файла и создания DataFrame
def process_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Разделение вопросов по тегу <question>
    questions = [q.strip() for q in content.split('<question>') if q.strip()]

    # Пустой список для хранения данных
    data = []

    print("Найдено вопросов: ", len(questions))

    for question in questions:
        lines = [line.strip() for line in question.split('\n') if line.strip()]

        # Инициализация переменных
        question_text = ''
        options = []
        correct_answer = ''

        # Определяем, является ли первая строка вопросом или сразу идет вариант ответа
        if lines and not (lines[0].startswith('<variant>') or lines[0].startswith('<variantright>')):
            question_text = lines[0]
            option_lines = lines[1:]
        else:
            question_text = '<EMPTY>'  # Нет явного текста вопроса
            option_lines = lines

        # Обработка вариантов ответов
        for line in option_lines:
            if line.startswith('<variant>'):
                variant_text = line.replace('<variant>', '').strip() or '<EMPTY>'
                options.append(variant_text)
            elif line.startswith('<variantright>'):
                variant_text = line.replace('<variantright>', '').strip() or '<EMPTY>'
                options.append(variant_text)
                correct_answer = str(len(options))  # Номер правильного ответа

        # Заполнение пропущенных вариантов до 5 штук
        while len(options) < 5:
            options.append('<EMPTY>')

        # Заполнение строки
        row = {
            'Question Text': question_text if question_text else '<EMPTY>',
            'Question Type': 'Multiple Choice',
            'Option 1': options[0],
            'Option 2': options[1],
            'Option 3': options[2],
            'Option 4': options[3],
            'Option 5': options[4],
            'Correct Answer': correct_answer if correct_answer else '1',  # Если правильный вариант не указан
            'Time in seconds': 900,
            'Image Link': '',
            'Answer explanation': ''
        }
        data.append(row)

    # Создание DataFrame
    df = pd.DataFrame(data)
    return df

# Чтение файла и создание Excel
input_file = 'questions.txt'  # Замените на путь к вашему txt-файлу
output_file = 'quiz.xlsx'

df = process_questions(input_file)
df.to_excel(output_file, index=False)

print(f"Excel-файл успешно создан: {output_file}")
