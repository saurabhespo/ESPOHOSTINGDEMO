from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains.llm import LLMChain
from sqlalchemy import text

import llmutils


class NewQuery(BaseModel):
    """Creates new rewritten question"""

    question: str = Field(
        ...,
        description="use this field for new question",
    )


class NL2SQL(BaseModel):
    """Creates a MS SQL Query"""

    sql_query: str = Field(
        ...,
        description="use this field for ms sql query",
    )


def get_sql_query(query,table_info):

    parser = JsonOutputParser(pydantic_object=NL2SQL)
    prompt = PromptTemplate(
        template=llmutils.get_prompt("NL2SQL_PROMPT"),
        input_variables=["input"],
        partial_variables={"format_instructions": parser.get_format_instructions},
    )
    prompt=prompt.partial(table_info=table_info)
    model = llmutils.get_model(temperature=0)
    chain = prompt | model | parser
    result = chain.invoke({"input": query})

    return result["sql_query"]


def query_rewriter(query, session_history):

    model = llmutils.get_model(temperature=0)
    parser = JsonOutputParser(pydantic_object=NewQuery)
    prompt = PromptTemplate(
        template=llmutils.get_prompt("QUERY_REWRITING_PROMPT"),
        input_variables=["input"],
        partial_variables={"format_instructions": parser.get_format_instructions},
    )
    prompt = prompt.partial(session_history=str(session_history))
    chain = prompt | model | parser
    response = chain.invoke({"input": query})

    return response["question"]


def execute_sql_query(query, db):
    sql_query = text(query)
    print(sql_query)
    results = db.execute(sql_query).fetchall()
    results = str(results)
    print(results)
    return results

def generate_qna_ans(user_query, answer):

    model = llmutils.get_model(temperature=0)
    prompt = PromptTemplate(
        template=llmutils.get_prompt("QnA_PROMPT"),
        input_variables=["user_query"],
    )

    prompt=prompt.partial(answer=answer)
    chain = prompt | model 
    response = chain.invoke({"user_query": user_query})

    return response.content
def generate_qna_followup(user_query):

    model = llmutils.get_model(temperature=0)
    prompt = PromptTemplate(
        template=llmutils.get_prompt("QUERY_FOR_FOLLOWUP_PROMPT"),
        input_variables=["input"],
    )

    
    chain = prompt | model 
    response = chain.invoke({"input": user_query})

    return response.content
