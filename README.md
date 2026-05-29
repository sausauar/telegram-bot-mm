# telegram-bot-mm

Telegram AI assistant MVP for Centr Krasok.

## What is included

- FastAPI webhook endpoint for Telegram updates.
- Clean service boundaries: Telegram API, RAG, retrieval, LLM and guardrails are separated.
- Markdown knowledge base loaded through a repository.
- Lexical retrieval baseline for MVP.
- Intent router with deterministic answers for greetings, prices, stock, promotions, vacancies and prompt-safety requests.
- Short in-memory dialog history per Telegram chat.
- Company voice polishing for generated answers.
- Guardrails that block answers when relevant context is missing.
- Optional OpenAI-compatible and Amvera integrations with deterministic offline fallback.

## Run locally

```powershell
Copy-Item .env.example .env
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Telegram webhook endpoint:

```text
POST /telegram/webhook
```

Healthcheck:

```text
GET /health
```

Required production variables:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_URL`
- `TELEGRAM_WEBHOOK_SECRET`
- `AI_PROVIDER`, one of `auto`, `openai`, `amvera`, `offline`
- `OPENAI_API_KEY` for OpenAI-compatible providers
- `AMVERA_API_TOKEN` for Amvera

If no AI provider token is configured, the bot uses an offline fact-based answer from retrieved context.

## Connect Telegram webhook

Telegram requires a public HTTPS URL. Local `http://127.0.0.1:8000` is only enough for backend tests.

```powershell
python scripts/set_telegram_webhook.py --drop-pending-updates
```

The script reads:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_URL`, for example `https://your-domain.com/telegram/webhook`
- `TELEGRAM_WEBHOOK_SECRET`

## Check RAG locally

```powershell
python scripts/check_rag.py
```

## Run tests

```powershell
pytest
```

## Docker

```powershell
docker build -t centr-krasok-telegram-bot .
docker run --env-file .env -p 8000:8000 centr-krasok-telegram-bot
```

## Architecture

```text
app/
  api/
    telegram_webhook.py
  core/
    config.py
    logging.py
  services/
    telegram_service.py
    llm_service.py
    retriever.py
    rag_service.py
    guardrails.py
    dialog_memory.py
  router/
    router.py
    intents.py
  policies/
    answer_policy.py
    voice.py
  schemas/
    telegram.py
    rag.py
  repositories/
    knowledge_repository.py
  prompts/
    assistant_prompt.py
  workers/
    ingestion.py
  main.py
```
