from pydantic import BaseModel, Field, model_validator


class GeneratedQuestion(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    options: list[str] = Field(min_length=2, max_length=6)
    correct_answer: int
    explanation: str = Field(min_length=1, max_length=2000)

    @model_validator(mode="after")
    def validate_correct_answer(self):
        if self.correct_answer < 0 or self.correct_answer >= len(self.options):
            raise ValueError("correct_answer must reference an existing option.")

        cleaned_options = [option.strip() for option in self.options]
        if any(not option for option in cleaned_options):
            raise ValueError("Quiz options cannot be empty.")

        self.options = cleaned_options
        return self


class GeneratedQuiz(BaseModel):
    questions: list[GeneratedQuestion] = Field(min_length=1, max_length=20)
