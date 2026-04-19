from app.extensions import SessionLocal
from app.models.football import Football
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

def create_football_clubs(league: str, total: int):
    session = SessionLocal()

    try:
        prompt = f"""
        Dalam format JSON, buat {total} daftar klub sepak bola dari liga "{league}".
        Format:
        {{
            "clubs": [
                {{"name": "..."}}
            ]
        }}
        """

        result = generate_from_llm(prompt)
        footballs = parse_llm_response(result)

        # save request log
        req_log = RequestLog(theme=theme)
        session.add(req_log)
        session.commit()

        saved = []

        for item in footballs:
            text = item.get("text")

            m = Football(
                text=text,
                request_id=req_log.id
            )
            session.add(m)
            saved.append(text)

        session.commit()

        return saved

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def get_all_footballs(page: int = 1, per_page: int = 100):
    session = SessionLocal()

    try:
        query = session.query(Football)

        total = query.count()

        data = (
            query
            .order_by(Football.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        result = [
            {
                "id": m.id,
                "text": m.text,
                "created_at": m.created_at.isoformat()
            }
            for m in data
        ]

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "data": result
        }

    finally:
        session.close()