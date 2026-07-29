# Публикация на GitHub

## 1. Создать пустой публичный репозиторий

Рекомендуемое имя:

```text
stalem-bot-showcase
```

Не добавляйте README, `.gitignore` или лицензию через интерфейс GitHub: они уже
есть в архиве.

## 2. Инициализировать Git

```powershell
git init
git add .
git commit -m "Add STALEM public architecture showcase"
git branch -M main
git remote add origin https://github.com/exzoe/stalem-bot-showcase.git
git push -u origin main
```

## 3. Проверить после публикации

- GitHub Actions завершился успешно;
- в репозитории нет `.env`, баз, логов и архивов;
- Mermaid-схема корректно отображается в README;
- ссылка на Telegram-бота открывается;
- GitHub Secret Scanning не показывает предупреждений.

## Важно

Не переносите в этот репозиторий коммиты из production-проекта и не объединяйте
их Git-истории. Любой новый фрагмент production-кода сначала должен пройти
ручную проверку границы безопасности и `python scripts/check.py`.
