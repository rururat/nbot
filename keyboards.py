from telebot import types

def vip_package_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("တစ်လ - 8,000 MMK", callback_data="buy_1month"),
        types.InlineKeyboardButton("သုံးလ - 22,000 MMK", callback_data="buy_3month"),
        types.InlineKeyboardButton("ခြောက်လ - 40,000 MMK", callback_data="buy_6month"),
        types.InlineKeyboardButton("၁ နှစ် - 80,000 MMK", callback_data="buy_12month")
    )
    return markup

def payment_keyboard(amount):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💸 KPay", url="kpay://transfer/09682115890"),
        types.InlineKeyboardButton("💸 WavePay", url="https://wavepay.me/09682115890"),
        types.InlineKeyboardButton("✅ ငွေလွဲပြီးပြီ", callback_data="paid")
    )
    return markup

def admin_approve_keyboard(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Approve Payment", callback_data=f"approve_{user_id}")
    )
    return markup