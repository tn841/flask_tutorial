#-*- coding: utf-8 -*-

# 데이터 모델 클래스들이 상속받아 사용할 기반(base)클래스 생성
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

__all__ = ["user"]