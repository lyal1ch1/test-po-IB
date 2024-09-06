import React, { useState, useEffect } from "react";

const Question = ({ questionData, handleAnswer }) => {
  const [selectedAnswers, setSelectedAnswers] = useState([]);
  const [textAnswer, setTextAnswer] = useState("");
  const [singleAnswer, setSingleAnswer] = useState(null);

  // Передаем начальные данные в родительский компонент
  useEffect(() => {
    handleAnswer(questionData.id, getAnswer());
  }, []); // Запускаем только при монтировании

  const handleMultipleChange = (event) => {
    const index = parseInt(event.target.value);
    const updatedAnswers = event.target.checked
      ? [...selectedAnswers, index]
      : selectedAnswers.filter((answer) => answer !== index);
    setSelectedAnswers(updatedAnswers);
    handleAnswer(questionData.id, updatedAnswers);
  };

  const handleTextChange = (event) => {
    const updatedAnswer = event.target.value;
    setTextAnswer(updatedAnswer);
    handleAnswer(questionData.id, updatedAnswer);
  };

  const handleSingleChange = (event) => {
    const updatedAnswer = parseInt(event.target.value);
    setSingleAnswer(updatedAnswer);
    handleAnswer(questionData.id, updatedAnswer);
  };

  const getAnswer = () => {
    if (questionData.type === "text") {
      return textAnswer;
    } else if (questionData.type === "multiple") {
      return selectedAnswers;
    } else if (questionData.type === "single") {
      return singleAnswer;
    }
  };

  return (
    <div>
      <h3>{questionData.question}</h3>
      {questionData.type === "text" ? (
        <input type="text" value={textAnswer} onChange={handleTextChange} />
      ) : questionData.type === "multiple" ? (
        <ul>
          {questionData.choices.map((choice, index) => (
            <li key={index}>
              <input
                type="checkbox"
                value={index}
                checked={selectedAnswers.includes(index)}
                onChange={handleMultipleChange}
              />
              {choice}
            </li>
          ))}
        </ul>
      ) : questionData.type === "single" ? (
        <ul>
          {questionData.choices.map((choice, index) => (
            <li key={index}>
              <input
                type="radio"
                name={`question-${questionData.id}`}
                value={index}
                checked={singleAnswer === index}
                onChange={handleSingleChange}
              />
              {choice}
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
};

export default Question;
