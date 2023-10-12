from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import db_models as models
from db_setup import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
# this line creates all the Tables/Columns from modules file in PostgreSQL:
models.Base.metadata.create_all(bind=engine)


class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]


# opening and closing database:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# annotation for dependency injection :
db_dependency = Annotated[Session, Depends(get_db)]  # ?????


# getting questions api:
@app.get("/questions/{question_id}")
async def read_question_and_its_choices(question_id: int, db: db_dependency):
    question_result = (
        db.query(models.Questions).filter(models.Questions.id == question_id).first()
    )
    choices_result = (
        db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    )
    print(choices_result)
    if not question_result:
        raise HTTPException(status_code=404, detail="Question was not found!")
    else:
        return {"question": question_result, "choices": choices_result}


# creating question api:
@app.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):  # ?????
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id,
        )
        db.add(db_choice)
    db.commit()
