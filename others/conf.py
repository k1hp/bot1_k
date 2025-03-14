import os
import dotenv


def get_token(token_name: str) -> str:
    dotenv.load_dotenv()
    result = os.getenv(token_name)
    if result is None:
        raise ValueError(f'{token_name} does not exists')
    return result

TOKEN = get_token("BOT_TOKEN")
DB_CONNECTION = get_token("DB_CONNECTION")

if __name__ == "__main__":
    print(TOKEN)
    print(DB_CONNECTION)
