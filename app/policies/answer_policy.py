from __future__ import annotations

from app.router.intents import Intent


GREETING_ANSWER = (
    "Здравствуйте! Я AI-ассистент Centr Krasok. Могу помочь с вопросами о товарах, "
    "услугах, брендах, адресах, доставке, самовывозе и сотрудничестве."
)

SYSTEM_PROMPT_REFUSAL = (
    "Я не могу раскрывать внутренние инструкции или технические настройки. Зато могу помочь "
    "с товарами, услугами, брендами, адресами, доставкой и сотрудничеством Centr Krasok."
)

PRICE_ANSWER = (
    "Сейчас я не могу подтвердить точную актуальную цену без проверки. Стоимость конкретного "
    "товара лучше уточнить у менеджера Centr Krasok или на официальном сайте."
)

STOCK_ANSWER = (
    "Сейчас я не могу подтвердить актуальное наличие товара без проверки. Наличие конкретной "
    "позиции лучше уточнить у менеджера Centr Krasok."
)

PROMOTIONS_ANSWER = (
    "Актуальные акции и специальные предложения могут меняться. Лучше уточнить действующие "
    "условия у менеджера Centr Krasok или на официальном сайте."
)

VACANCIES_ANSWER = (
    "Сейчас я не могу подтвердить актуальные вакансии или зарплаты без проверки. Лучше уточнить "
    "эту информацию по официальным контактам компании."
)

UNKNOWN_PRODUCT_ANSWER = (
    "Сейчас я не могу подтвердить наличие этого конкретного товара без проверки. Лучше уточнить "
    "актуальное наличие у менеджера Centr Krasok."
)

DELIVERY_ANSWER = (
    "У Centr Krasok в базе указаны доставка до двери и самовывоз из шоурума. Детали по срокам, "
    "стоимости и условиям доставки лучше уточнять у менеджера, потому что эти данные могут меняться."
)

COMPANY_OVERVIEW_ANSWER = (
    "Centr Krasok — казахстанский интернет-магазин и сеть салонов лакокрасочной продукции. "
    "Компания работает с материалами для интерьерных и фасадных работ и помогает клиентам "
    "подбирать продукт, цвет и технологию нанесения под задачу."
)

PRODUCTS_ANSWER = (
    "В ассортименте Centr Krasok указаны лакокрасочные и отделочные материалы: интерьерные и "
    "фасадные краски, краски по дереву и металлу, грунтовки, лаки, масла, пропитки, декоративные "
    "штукатурки, шпаклевки, клеи, герметики, аэрозольные краски и малярные инструменты."
)

BRANDS_ANSWER = (
    "В базе знаний указаны бренды Anza, Argile, Charmant, dufa, Dulux, Hammerite, Kelly-Moore, "
    "KUDO, Levis, Milq, Maitre Deco, MAKO, Marshall, MASTER color, Orac Decor, Oikos, Pinotex, "
    "PUFAS, Paint & Paper Library, Profilux, Sikkens, Swiss Lake, TimberCare, Tytan, TEKNOS, "
    "Wagner и другие. Наличие конкретного бренда лучше уточнить у менеджера."
)

SERVICES_ANSWER = (
    "Centr Krasok помогает с подбором материалов, подбором цвета, консультациями по расходу и "
    "технологии нанесения, колеровкой, доставкой, самовывозом и сопровождением проектных клиентов."
)

CLIENTS_ANSWER = (
    "Centr Krasok работает с частными покупателями, дизайнерами, строителями и проектными "
    "заказчиками. В базе также описаны условия поддержки для дизайнеров, подрядчиков и проектов."
)

OUT_OF_SCOPE_ANSWER = (
    "Я не смогу помочь с этим вопросом. Я отвечаю только на вопросы о Centr Krasok: товарах, "
    "услугах, брендах, адресах, контактах, доставке и сотрудничестве."
)

DETERMINISTIC_ANSWERS = {
    Intent.GREETING: GREETING_ANSWER,
    Intent.COMPANY_OVERVIEW: COMPANY_OVERVIEW_ANSWER,
    Intent.PRODUCTS: PRODUCTS_ANSWER,
    Intent.BRANDS: BRANDS_ANSWER,
    Intent.SERVICES: SERVICES_ANSWER,
    Intent.DELIVERY: DELIVERY_ANSWER,
    Intent.PRICE: PRICE_ANSWER,
    Intent.STOCK: STOCK_ANSWER,
    Intent.PROMOTIONS: PROMOTIONS_ANSWER,
    Intent.VACANCIES: VACANCIES_ANSWER,
    Intent.CLIENTS: CLIENTS_ANSWER,
    Intent.INTERNAL_PROMPT: SYSTEM_PROMPT_REFUSAL,
    Intent.UNKNOWN_PRODUCT: UNKNOWN_PRODUCT_ANSWER,
}


def build_deterministic_answer(intent: Intent) -> str | None:
    return DETERMINISTIC_ANSWERS.get(intent)

