from database import get_db

def get_db_by_domain(domain: str):
    def _get_db():
        return next(get_db(domain))
    return _get_db