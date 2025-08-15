from telebot import TeleBot
from dotenv import load_dotenv
import os, json
from keyboards import vip_package_keyboard, payment_keyboard, admin_approve_keyboard

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS").split(",")]
VIP_IMAGE_PATH = os.path.join("assets", "vip_temp.jpg")
VIP_JSON_PATH = os.path.join("vip_accounts.json")

bot = TeleBot(BOT_TOKEN)
pending_payments = {}

# Load VIP accounts
def load_vip_accounts():
    with open(VIP_JSON_PATH, "r") as f:
        return json.load(f)

def save_vip_accounts(accounts):
    with open(VIP_JSON_PATH, "w") as f:
        json.dump(accounts, f, indent=4)

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "🤩 **N4 VPN PRO** 🤩\n"
        "**⭕️ VIP စျေးနှုန်းများ ⭕️**\n"
        "💰 တလ 8,000  💰 သုံးလ 22,000  💰 ခြောက်လ 40,000  💰 ၁ နှစ် 80,000\n\n"
        "အောက်က Button မှာ သင်လိုချင်တဲ့ Package ကို ရွေးပါ"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=vip_package_keyboard())

# Handle package selection
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_package(call):
    packages = {
        "buy_1month": 8000,
        "buy_3month": 22000,
        "buy_6month": 40000,
        "buy_12month": 80000
    }
    amount = packages.get(call.data)
    pending_payments[call.from_user.id] = {"amount": amount, "username": call.from_user.username}
    bot.send_message(
        call.message.chat.id,
        f"💰 ငွေလွဲရန် Amount: {amount} MMK\nအောက်က Payment Button နှိပ်ပြီး ငွေလွဲပါ",
        reply_markup=payment_keyboard(amount)
    )

# Handle Paid click
@bot.callback_query_handler(func=lambda call: call.data == "paid")
def handle_paid(call):
    user_id = call.from_user.id
    for admin_id in ADMIN_IDS:
        bot.send_message(
            admin_id,
            f"💰 User @{call.from_user.username} (ID:{user_id}) က ငွေလွဲပြီးပြီ။ Approve လုပ်ပါ။",
            reply_markup=admin_approve_keyboard(user_id)
        )
    bot.send_message(call.message.chat.id, "✅ သင့်ငွေလွဲ အတည်ပြုရန် Admin ကို notify လုပ်ပြီးပါပြီ")

# Admin approve handler
@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def handle_approve(call):
    admin_id = call.from_user.id
    if admin_id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ သင် Admin မဟုတ်ပါ")
        return

    user_id = int(call.data.split("_")[1])
    if user_id not in pending_payments:
        bot.answer_callback_query(call.id, "❌ Pending payment မတွေ့ပါ")
        return

    # Assign VIP account dynamically
    accounts = load_vip_accounts()
    vip_account = None
    for acc in accounts:
        if not acc["used"]:
            vip_account = acc
            acc["used"] = True
            save_vip_accounts(accounts)
            break

    if not vip_account:
        bot.send_message(user_id, "❌ VIP account မရှိတော့ပါ")
        return

    # Send VIP account
    caption = f"""
🎉 VIP အကောင့် အသစ်
━━━━━━━━━━━━━━━
📌 Username: {vip_account['username']}
🔑 Password: {vip_account['password']}
🌐 Server: {vip_account['server']}
📆 Expiry: {vip_account['expiry']}
━━━━━━━━━━━━━━━
✅ ချက်ချင်း အသုံးပြုနိုင်ပါသည်။
"""
    if os.path.exists(VIP_IMAGE_PATH):
        bot.send_photo(user_id, open(VIP_IMAGE_PATH, 'rb'), caption=caption)
    else:
        bot.send_message(user_id, caption)

    bot.send_message(admin_id, f"✅ VIP account @{vip_account['username']} ကို User ကို ပို့ပြီးပါပြီ")
    pending_payments.pop(user_id)

if __name__ == "__main__":
    print("🚀 N4 VIP Bot လည်ပတ်နေပါပြီ...")
    bot.infinity_polling()