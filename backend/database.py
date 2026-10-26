from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# 使用 SQLite 作為本地端資料庫
SQLALCHEMY_DATABASE_URL = "sqlite:///math_tutor.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 定義題庫的資料表
class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)      # 分類，例如 "國一下-1-1重點一"
    question_text = Column(Text, nullable=False)       # 題目純文字
    image_path = Column(String(200), nullable=False)   # 圖片檔案路徑
    detailed_solution = Column(Text, nullable=True)    # 預留給你的標準詳解

# 建立資料表
Base.metadata.create_all(bind=engine)