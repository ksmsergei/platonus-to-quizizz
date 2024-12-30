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
        lines = question.split('\n')
        question_text = lines[0].strip()
        
        # Инициализация переменных для вариантов ответов и правильного ответа
        options = []
        correct_answer = ''

        # Обработка строк для извлечения вариантов ответов
        for i, line in enumerate(lines[1:]):
            line = line.strip()
            if line.startswith('<variant>'):
                options.append(line.replace('<variant>', '').strip())
            elif line.startswith('<variantright>'):
                options.append(line.replace('<variantright>', '').strip())
                correct_answer = str(len(options))  # Номер правильного ответа

        # Заполнение данных
        row = {
            'Question Text': question_text,
            'Question Type': 'Multiple Choice',
            'Option 1': options[0] if len(options) > 0 else '',
            'Option 2': options[1] if len(options) > 1 else '',
            'Option 3': options[2] if len(options) > 2 else '',
            'Option 4': options[3] if len(options) > 3 else '',
            'Option 5': options[4] if len(options) > 4 else '',
            'Correct Answer': correct_answer,
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