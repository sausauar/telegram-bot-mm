# RAG Evaluation

Эта папка нужна для ручной проверки качества ответов RAG-бота.

- `questions.md` — список вопросов для проверки.
- `answers/` — сюда складываем ответы бота после прогонов.

Рекомендуемый формат файла ответа:

```text
question: Чем занимается компания?
answer: ...
used_llm: true/false
sources: ...
notes: ...
```

Быстрая проверка одного вопроса через локальный сервис:

```powershell
C:\Users\Admin\miniconda3\envs\kaspi-rag\python.exe -c "import asyncio; from app.main import app; async def main(): r=await app.state.rag_service.answer(123, 'Чем занимается компания?'); print(r.text); print('used_llm=', r.used_llm); print('sources=', [s.title for s in r.sources]); asyncio.run(main())"
```
