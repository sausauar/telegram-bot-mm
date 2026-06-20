from __future__ import annotations

from enum import Enum


class Intent(str, Enum):
    GREETING = "greeting"
    COMPANY_OVERVIEW = "company_overview"
    PRODUCTS = "products"
    BRANDS = "brands"
    SERVICES = "services"
    DESIGNERS = "designers"
    BUILDERS = "builders"
    DELIVERY = "delivery"
    CONTACTS = "contacts"
    PRICE = "price"
    STOCK = "stock"
    PROMOTIONS = "promotions"
    VACANCIES = "vacancies"
    CLIENTS = "clients"
    SENSITIVE_UNKNOWN = "sensitive_unknown"
    OUT_OF_SCOPE = "out_of_scope"
    INTERNAL_PROMPT = "internal_prompt"
    UNKNOWN_PRODUCT = "unknown_product"
    GENERAL_RAG = "general_rag"
