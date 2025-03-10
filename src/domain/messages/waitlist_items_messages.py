
from aiogram import types
from aiogram.utils import formatting


# ATOMS
def _hello_message(message: types.Message) -> formatting.Text:
    return formatting.Text(
        "🪐 Хэй, ", formatting.Bold(message.from_user.full_name), "\n",
    )


def _please_do_not_block_bot(message: types.Message) -> formatting.Text:
    return formatting.Text(
        formatting.BlockQuote(
            "Мы свяжемся с вами, когда OctoVerse выйдет в бета-тестирование. \n",
            "Поэтому убедительно просим вас не блокировать бота.",
        ),
        "\n",
    )


def _internal_ads(message: types.Message) -> formatting.Text:
    return formatting.Text(
        "А пока ждете...", "\n",
        formatting.TextLink("🚀 Следите за развитием", url="https://t.me/OctoVerseWorld"), "\n",
        formatting.TextLink("💭 Присоединяйтесь к обсуждению ", url="https://t.me/OctoVerseGroup"), "\n",
        formatting.TextLink("📚 Подробнее о проекте", url="https://octoverse.world"), "\n",
    )


def succesfully_joined_waitlist(message: types.Message, *, item_id: int) -> formatting.Text:
    return formatting.Text(
        _hello_message(message),
        "Ваша позиция в листе ожидания: ", formatting.Spoiler(item_id), "\n",
        "Спасибо за ожидание!", "\n",
        _please_do_not_block_bot(message),
        _internal_ads(message),
    )


def already_in_waitlist(message: types.Message) -> formatting.Text:
    return formatting.Text(
        _hello_message(message),
        "Вы уже добавлены в лист ожидания.", "\n",
        _please_do_not_block_bot(message),
        _internal_ads(message),
    )


# MOLECULES
def waitlist_items_count(message: types.Message, *, count: int) -> formatting.Text:
    return formatting.Text(
        _hello_message(message),
        "Людей в ожидании: ", formatting.Text(count), "\n",
        _please_do_not_block_bot(message),
        _internal_ads(message),
    )
