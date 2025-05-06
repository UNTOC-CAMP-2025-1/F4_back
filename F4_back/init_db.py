from database import engines, bases

def create_all_tables():
    for domain in engines:
        print(f"[{domain}] 스키마에 테이블 생성 중...")
        base = bases[domain]
        engine = engines[domain]
        base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_all_tables()
