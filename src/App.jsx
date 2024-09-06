import React, { useState, useEffect } from "react";
import Question from "./Question";

const App = () => {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [score, setScore] = useState(null);
  const [userName, setUserName] = useState(""); // Добавляем состояние для ФИО

  useEffect(() => {
    fetch("http://localhost:5000/questions")
      .then((response) => response.json())
      .then((data) => setQuestions(data));
  }, []);

  const handleAnswer = (questionId, answer) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: answer,
    }));
  };

  const handleSubmitAll = () => {
    fetch("http://localhost:5000/submit-answers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ answers, user_name: userName }),
    })
      .then((response) => response.json())
      .then((data) => {
        setScore(data.score);
        alert("Ответы сохранены! Ваши баллы: " + data.score);
      });
  };

  return (
    <div>
      <h1>Тестирование</h1>
      <input
        type="text"
        placeholder="Введите ваше ФИО"
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />
      {questions.map((question) => (
        <Question
          key={question.id}
          questionData={question}
          handleAnswer={handleAnswer}
        />
      ))}
      <button onClick={handleSubmitAll}>Отправить ответы</button>
      {score !== null && <h2>Ваши баллы: {score}</h2>}
    </div>
  );
};

export default App;
