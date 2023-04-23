#!/usr/bin/env python3

"""Module for the card reading database entity. Used to insert tarot card readings in a relational database."""

from datetime import datetime

from sqlalchemy import Column, Float, Integer, String, Text, TIMESTAMP

from .. tarot import CardReading
from . base import Base


# pylint: disable=C0103,R0902,R0903
class CardReadingEntity(Base):
    """Entity object for the CardReading class."""
    __tablename__ = "reading"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    openai_id = Column(String(64), nullable=False)
    card_one = Column(Integer, nullable=False)
    card_two = Column(Integer, nullable=True)
    card_three = Column(Integer, nullable=True)
    card_four = Column(Integer, nullable=True)
    card_five = Column(Integer, nullable=True)
    subject = Column(String(64), nullable=True)
    teller = Column(String(64), nullable=True)
    prompt = Column(String(256), nullable=False)
    response = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    model = Column(String(64), nullable=True)
    created_ts = Column(TIMESTAMP, nullable=True)
    response_ms = Column(Integer, nullable=True)
    max_tokens = Column(Integer, nullable=True)
    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    temperature = Column(Float, nullable=True)
    top_p = Column(Float, nullable=True)

    def __init__(self, dto: CardReading):
        self.card_one = dto.spread[0].value
        if len(dto.spread) > 1:
            self.card_two = dto.spread[1].value
        if len(dto.spread) > 2:
            self.card_three = dto.spread[2].value
        if len(dto.spread) > 3:
            self.card_four = dto.spread[3].value
        if len(dto.spread) > 4:
            self.card_five = dto.spread[4].value
        self.subject = dto.subject
        self.teller = dto.teller
        self.prompt = dto.prompt
        self.response = dto.response
        self.summary = dto.summary
        self.openai_id = dto.metadata.openai_id
        self.model = dto.metadata.model
        self.created_ts = datetime.fromtimestamp(dto.metadata.created_ts)
        self.response_ms = dto.metadata.response_ms
        self.max_tokens = dto.metadata.max_tokens
        self.prompt_tokens = dto.metadata.prompt_tokens
        self.completion_tokens = dto.metadata.completion_tokens
        self.total_tokens = dto.metadata.total_tokens
        self.temperature = dto.metadata.temperature
        self.top_p = dto.metadata.top_p
# pylint: enable=C0103,R0902,R0903
