import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

_client = None


def get_client():
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            return None
        _client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    return _client


def save_score(nickname, score):
    client = get_client()
    if client is None:
        print("[ledaerboard] .env에 SUPABASE_URL / SUPABASE_ANON_KEY가 없어 저장을 건너뜁니다.")
        return False
    try:
        client.table("scores").insert({"nickname" : nickname, "score" : score}).execute()
        return True
    except Exception as e:
        print("[leaderboard] 저장 실패:", e)
        return False


def get_top10():
    client = get_client()
    if client is None:
        return []

    try:
        response = (
            client.table("scores")
            .select("nickname, score")
            .order("score", desc = True)
            .order("created_at", desc = False)
            .limit(10)
            .execute()
        )
        return response.data
    except Exception as e:
        print("[leaderboard] 조회 실패:", e)
        return []