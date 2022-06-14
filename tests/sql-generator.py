from uuid import uuid4

sql = open("./test1.sql", "w")
test_id = str(uuid4())
query = f"INSERT INTO tests (\"id\", \"name\", \"description\") VALUES ('{test_id}', 'Тест на тревожность', 'Внимательно прочитайте каждое утверждение и выберите 1 ответ, который наиболее соответствует вашему состоянию за последнюю неделю.');\n\n"
sql.write(query)

with open("./test1.txt", "r") as file:
    for line in file:
        question_id = uuid4()

        line = line.split(";")
        line.pop()
        query = f"INSERT INTO questions (\"id\", \"test_id\", \"text\") VALUES ('{question_id}', '{test_id}', '{line[0]}');\n"
        sql.write(query)

        answers = []
        for idx in range(2):
            line = file.readline().split(";")
            line.pop()
            line = [obj.strip() for obj in line]
            answers.append(line)

        for idx in range(len(answers[0])):
            answer_id = uuid4()
            query = f"INSERT INTO proposed_answers (\"id\", \"quiestion_id\", \"text\", \"score\") VALUES ('{answer_id}', '{question_id}', '{answers[0][idx]}', '{answers[1][idx]}');\n"
            sql.write(query)
        sql.write("\n")

file.close()
sql.close()
