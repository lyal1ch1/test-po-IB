from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import pandas as pd
import os
JSON_FILE = 'user_answers.json'

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех запросов

# Загружаем вопросы из файла
with open('data.json', 'r', encoding='utf-8') as file:
    questions = json.load(file)

# Путь к CSV файлу
CSV_FILE = 'user_answers.csv'

# Функция для подсчета правильных ответов и баллов
def calculate_score(answers):
    score = 0
    results = []
    for question in questions:
        q_id = question['id']
        if q_id in answers:
            user_answer = answers[q_id]['answer']
            correct_answer = question.get('correct', None)
            if question['type'] == 'single':
                is_correct = user_answer == correct_answer
                score += 1 if is_correct else 0
            elif question['type'] == 'multiple':
                correct_answers = set(correct_answer)
                user_answers = set(user_answer)
                is_correct = correct_answers == user_answers
                score += 1 if is_correct else 0
            
            # Запись результатов в список
            results.append({
                'user_name': answers[q_id]['user_name'],
                'question_id': q_id,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'score': 1 if is_correct else 0
            })
    
    return score, results

# Функция для записи ответов в CSV
def save_answers_to_csv(results):
    df = pd.DataFrame(results)
    # print("Saving data to CSV:", df)  # Добавляем вывод для проверки
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(CSV_FILE, mode='w', header=True, index=False)

# Маршрут для получения вопросов
@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify(questions)

# Маршрут для записи ответов и подсчета баллов
# @app.route('/submit-answers', methods=['POST'])
# def submit_answers():
#     data = request.json
#     # print(data)

#     answers = data.get('answers', {})
#     user_name = data.get('user_name', '')
#     formatted_answers = {}
    
#     # Форматируем ответы
#     for q_id, ans in answers.items():
#         formatted_answers[q_id] = {
#             'answer': ans,
#             'user_name': user_name
#         }
    
#     print("Formatted Answers:", formatted_answers)
#     score, results = calculate_score(formatted_answers)
#     save_answers_to_csv(results)
#     return jsonify({"message": "Ответы сохранены!", "score": score})


# Путь к JSON файлу

# Функция для загрузки данных из JSON
def load_json_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Функция для записи данных в JSON
def save_json_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Функция для обработки и сохранения ответов
@app.route('/submit-answers', methods=['POST'])
# def submit_answers():
#     data = request.json
#     print(data)
#     answers = data.get('answers', {})
#     user_name = data.get('user_name', '')

#     # Загружаем существующие данные из JSON файла
#     existing_data = load_json_data()

#     # Если данные являются словарем (например, если файл пуст или содержит неправильную структуру),
#     # преобразуем их в список.
#     if not isinstance(existing_data, list):
#         existing_data = []

#     # Форматируем вопросы и ответы в требуемый вид
#     formatted_questions = []
#     total_score = 0

#     for question in questions:
#         q_id = str(question['id'])
#         if q_id in answers:
#             user_answer = answers[q_id]

#             # Проверяем, правильно ли пользователь ответил
#             correct_answer = question.get('correct', [])
#             score = 0
#             if question['type'] == 'single':
#                 score = 1 if user_answer == correct_answer else 0
#             elif question['type'] == 'multiple':
#                 score = 1 if set(user_answer) == set(correct_answer) else 0
            
#             # Добавляем баллы за вопрос к общему баллу
#             total_score += score

#             # Форматируем вопрос в нужном виде
#             formatted_questions.append({
#                 "quest": question['question'],
#                 "answers": question['choices'],
#                 "correct": correct_answer,
#                 "type": question['type'],
#                 "score": score
#             })

#     # Формируем запись для текущего пользователя
#     new_entry = {
#         "ФИО": user_name,
#         "questions": formatted_questions,
#         "sum-score": total_score
#     }

#     # Добавляем запись в существующие данные
#     existing_data.append(new_entry)

#     # Сохраняем обновленные данные в JSON файл
#     save_json_data(existing_data)

#     return jsonify({"message": "Ответы сохранены!", "score": total_score})
# def submit_answers():
#     data = request.json
#     print(data)
#     answers = data.get('answers', {})
#     user_name = data.get('user_name', '')

#     # Загружаем существующие данные из JSON файла
#     existing_data = load_json_data()

#     # Если данные являются словарем (например, если файл пуст или содержит неправильную структуру),
#     # преобразуем их в список.
#     if not isinstance(existing_data, list):
#         existing_data = []

#     # Форматируем вопросы и ответы в требуемый вид
#     formatted_questions = []
#     total_score = 0

#     for question in questions:
#         q_id = str(question['id'])
#         if q_id in answers:
#             user_answer = answers[q_id]

#             # Проверяем, правильно ли пользователь ответил
#             correct_answer = question.get('correct', [])
#             score = 0
#             if question['type'] == 'single':
#                 score = 1 if user_answer == correct_answer else 0
#             elif question['type'] == 'multiple':
#                 score = 1 if set(user_answer) == set(correct_answer) else 0
            
#             # Добавляем баллы за вопрос к общему баллу
#             total_score += score

#             # Форматируем вопрос в нужном виде
#             formatted_questions.append({
#                 "quest": question['question'],
#                 "answers": question['choices'],
#                 "correct": correct_answer,
#                 "user_answer": user_answer,  # Сохраняем ответ пользователя
#                 "type": question['type'],
#                 "score": score
#             })

#     # Формируем запись для текущего пользователя
#     new_entry = {
#         "ФИО": user_name,
#         "questions": formatted_questions,
#         "sum-score": total_score
#     }

#     # Добавляем запись в существующие данные
#     existing_data.append(new_entry)

#     # Сохраняем обновленные данные в JSON файл
#     save_json_data(existing_data)

#     return jsonify({"message": "Ответы сохранены!", "score": total_score})

def submit_answers():
    data = request.json
    answers = data.get('answers', {})
    user_name = data.get('user_name', '')

    # Загружаем существующие данные из JSON файла
    existing_data = load_json_data()

    # Если данные являются словарем (например, если файл пуст или содержит неправильную структуру),
    # преобразуем их в список.
    if not isinstance(existing_data, list):
        existing_data = []

    # Форматируем вопросы и ответы в требуемый вид
    formatted_questions = []
    total_score = 0

    for question in questions:
        q_id = str(question['id'])
        if q_id in answers:
            user_answer = answers[q_id]

            # Проверяем, правильно ли пользователь ответил
            correct_answer = question.get('correct', [])
            score = 0

            if question['type'] == 'single':
                # Для одиночного выбора оценка дается за правильный ответ
                score = 1 if user_answer == correct_answer else 0

            elif question['type'] == 'multiple':
                # Для множественного выбора:
                # - Баллы за каждый правильный вариант.
                # - Вычитание за каждый неправильный вариант.
                correct_set = set(correct_answer)
                user_set = set(user_answer)

                correct_choices = correct_set.intersection(user_set)
                incorrect_choices = user_set.difference(correct_set)

                # Доля баллов за каждый правильный вариант
                score += len(correct_choices) / len(correct_set)
                # Вычитаем за каждый неправильный вариант
                score -= len(incorrect_choices) / len(correct_set)
                
                # Убедимся, что итоговый балл не отрицательный
                score = max(score, 0)

            # Добавляем баллы за вопрос к общему баллу
            total_score += score

            # Форматируем вопрос в нужном виде
            formatted_questions.append({
                "quest": question['question'],
                "answers": question['choices'],
                "correct": correct_answer,
                "user_answer": user_answer,  # Сохраняем ответ пользователя
                "type": question['type'],
                "score": score
            })

    # Формируем запись для текущего пользователя
    new_entry = {
        "ФИО": user_name,
        "questions": formatted_questions,
        "sum-score": total_score
    }

    # Добавляем запись в существующие данные
    existing_data.append(new_entry)

    # Сохраняем обновленные данные в JSON файл
    save_json_data(existing_data)

    return jsonify({"message": "Ответы сохранены!", "score": total_score})

if __name__ == '__main__':
    app.run(debug=True)
