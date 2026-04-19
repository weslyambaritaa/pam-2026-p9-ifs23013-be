from app.extensions import SessionLocal
from app.models.football import Football
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

def create_football_clubs(league: str, total: int):
    session = SessionLocal()

    try:
        prompt = f"""
        Berikan jawaban dalam format JSON saja.
        Daftar {total} klub sepak bola dari liga "{league}".
        Format:
        {{
            "clubs": [
                {{"name": "Nama Klub"}}
            ]
        }}
        """

        result = generate_from_llm(prompt)
        footballs = parse_llm_response(result)

        # Ganti 'theme' menjadi 'league' saat menyimpan log
        # Asumsi model RequestLog masih menggunakan kolom 'theme'
        req_log = RequestLog(theme=league) 
        session.add(req_log)
        session.commit()

        saved = []

        for item in footballs:
            # Ambil "name" dari JSON, bukan "text"
            club_name = item.get("name") 

            m = Football(
                name=club_name,   # Sesuaikan dengan model Football
                league=league,    # Simpan juga data liganya
                request_id=req_log.id
            )
            session.add(m)
            saved.append(club_name)

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
                "name": m.name,       # Diubah dari m.text
                "league": m.league,   # Tambahkan kembalian liga
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