from aiogram import Bot, Dispatcher, types, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from pathlib import Path
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from datetime import datetime
from aiogram import Router
from datetime import timezone
import asyncio, random, string, time, re
import aiosqlite
import asyncio
import os
import json
import yt_dlp
import aiohttp

# === Reklama uchun holatlar (state) ===
class ReklamaForm(StatesGroup):
    name = State()
    contact = State()
    content = State()

BOT_TOKEN = "8319503755:AAEBlDMEjpiJcDm9BELgqFH2tVDKO08ypvU"
ADMIN_ID = 6760161876
ADMINS = [6760161876]
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

CHANNELS = ["@Kuvond1kov", "@osmondagi_janglar_rasmiy", "@taxt_muhri_uzb"]

# ===================== DATABASE =====================
DB = "subscribers.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        user_id INTEGER PRIMARY KEY,
        first_seen_ts INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_new_user(user_id: int):
    ts = int(datetime.now(timezone.utc).timestamp())
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    INSERT OR IGNORE INTO subscribers (user_id, first_seen_ts)
    VALUES (?, ?)
    """, (user_id, ts))
    conn.commit()
    conn.close()

def count_month_users(year: int, month: int):
    import calendar
    start = datetime(year, month, 1, tzinfo=timezone.utc).timestamp()
    end = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59,
                   tzinfo=timezone.utc).timestamp()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM subscribers WHERE first_seen_ts BETWEEN ? AND ?", (start, end))
    (count,) = cur.fetchone()
    conn.close()
    return count

VIDEOS_PER_PAGE = 10

# === Obuna tekshirish funksiyasi ===
async def check_user_subscriptions(user_id: int):
    not_subscribed = []
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, user_id)
            if member.status == "left":
                not_subscribed.append(ch)
        except Exception:
            not_subscribed.append(ch)
    return not_subscribed


# === /start buyrug‘i ===
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    not_subscribed = await check_user_subscriptions(message.from_user.id)
    if not_subscribed:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanal 1", url="https://t.me/Kuvond1kov")],
            [InlineKeyboardButton(text="📺 Kanal 2", url="https://t.me/osmondagi_janglar_rasmiy")],
            [InlineKeyboardButton(text="🎬 Kanal 3", url="https://t.me/taxt_muhri_uzb")],
            [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub")]
        ])
        await message.answer("Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling 👇", reply_markup=keyboard)
        return

    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📜 Mundareja 1-qism")],
            [KeyboardButton(text="📜 Mundareja 2-qism")],
            [KeyboardButton(text="📜 Mundareja 3-qism")],
            [KeyboardButton(text="📜 Mundareja 4-qism")],
            [KeyboardButton(text="📜 Mundareja 5-qism")],
            [KeyboardButton(text="📜 KINOLAR")],
            [KeyboardButton(text="📢 Reklama va homiylik")],
            [KeyboardButton(text="📥 Video yuklab olish")],
            [KeyboardButton(text="📈 Statistika")],
            [KeyboardButton(text="👤 Admin")],
        ],
        resize_keyboard=True
    )
    await message.answer("🎉 Botga xush kelibsiz!\nKerakli bo‘limni tanlang:", reply_markup=main_menu)


# === "✅ Obunani tekshirish" tugmasi ===
@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub_callback(callback: types.CallbackQuery):
    not_subscribed = await check_user_subscriptions(callback.from_user.id)
    if not_subscribed:
        await callback.answer("❌ Hali barcha kanallarga obuna bo‘lmadingiz!", show_alert=True)
    else:
        main_menu = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📜 Mundareja 1-qism")],
                [KeyboardButton(text="📜 Mundareja 2-qism")],
                [KeyboardButton(text="📜 Mundareja 3-qism")],
                [KeyboardButton(text="📜 Mundareja 4-qism")],
                [KeyboardButton(text="📜 Mundareja 5-qism")],
                [KeyboardButton(text="📜 KINOLAR")],
                [KeyboardButton(text="📢 Reklama va homiylik")],
                [KeyboardButton(text="📥 Video yuklab olish")],
                [KeyboardButton(text="📈 Statistika")],
                [KeyboardButton(text="👤 Admin")],
            ],
            resize_keyboard=True
        )
        await callback.message.edit_text("✅ Obuna tasdiqlandi! Endi botdan foydalanishingiz mumkin.")
        await callback.message.answer("🎉 Asosiy menyu:", reply_markup=main_menu)

# ============= 📜 Mundareja 1-qism =============
@dp.message(F.text == "📜 Mundareja 1-qism")
async def mundareja_1_handler(message: types.Message):
    mundareja_1_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="TAXT MUHRI")],
            [KeyboardButton(text="RENEGADE O‘LMAS")],
            [KeyboardButton(text="MUKAMMAL DUNYO")],
            [KeyboardButton(text="OSMONDAGI JANGLAR")],
            [KeyboardButton(text="ZULMATDAGI YULDUZ")],
            [KeyboardButton(text="JANGOVAR QIT'A")],
            [KeyboardButton(text="OLOV JANG USTASI")],
            [KeyboardButton(text="HUKUMDORLAR YULI")],
            [KeyboardButton(text="SAMODAGI QIRG'IN")],
            [KeyboardButton(text="JANG KOINOTI")],
            [KeyboardButton(text="⬅️ Orqaga")],
        ],
        resize_keyboard=True
    )
    await message.answer("📜 Mundareja 1-qism bo‘limi:", reply_markup=mundareja_1_menu)

# ⬅️ Orqaga
@dp.message(F.text == "⬅️ Orqaga")
async def back_to_main(message: types.Message):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📜 Mundareja 1-qism")],
            [KeyboardButton(text="📜 Mundareja 2-qism")],
            [KeyboardButton(text="📜 Mundareja 3-qism")],
            [KeyboardButton(text="📜 Mundareja 4-qism")],
            [KeyboardButton(text="📜 Mundareja 5-qism")],
            [KeyboardButton(text="📢 Reklama / Homiylik")],
            [KeyboardButton(text="📊 Ko‘rishlar soni")],
            [KeyboardButton(text="👤 Admin")],
        ],
        resize_keyboard=True
    )
    await message.answer("🔙 Asosiy menyuga qaytdingiz", reply_markup=main_menu)

# ==============🎥 RENEGADE O‘LMAS=================
@dp.message(F.text == "RENEGADE O‘LMAS")
async def renegade_olmas_handler(message: types.Message):
    await message.answer("👑 RENEGADE O‘LMAS qismlarini tanlang:", reply_markup=get_page_renegade_keyboard(1))


# 📄 RENEGADE sahifa almashtirish
@dp.callback_query(F.data.regexp(r"^renegade_page_\d+$"))
async def change_page_renegade(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_page_renegade_keyboard(page))
    await callback.answer()


# 🎬 RENEGADE video yuborish
@dp.callback_query(F.data.regexp(r"^renegade_olmas_\d+$"))
async def send_renegade_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = renegade_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🎬 Nomi: RENEGADE O‘LMAS\n"
        "───────────────────────────────\n"
        f"🎞 Janr: Fantastika, Jangovar, Romantika, Sarguzasht\n"
        f"📺 Qismi: {qism_raqami}\n"
        "💿 Sifati: 1080p HD\n"
        "🌐 Til: O‘zbek\n"
        "───────────────────────────────\n"
        "👑 Kanal: @AniMania_rasmiy\n"
        "#renegade_olmas_animania\n\n"
        "💬 “Haqiqiy kuch — yurakdagi qat’iyat va hech qachon taslim bo‘lmaslikda.” ⚡"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True
    )
    await callback.answer()


# 🔘 RENEGADE sahifalangan tugmalar
def get_page_renegade_keyboard(page: int):
    VIDEOS_PER_PAGE = 10
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(renegade_videolar.keys())[start:end]

    buttons = [
        [InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=key)]
        for i, key in enumerate(keys, start=start)
    ]

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"renegade_page_{page-1}"))
    if end < len(renegade_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"renegade_page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎞 RENEGADE O'LMAS videolar ro'yxati:
renegade_videolar = {
    "renegade_olmas_1": "https://t.me/dhsaidqhndi/492",
    "renegade_olmas_2": "https://t.me/dhsaidqhndi/493",
    "renegade_olmas_3": "https://t.me/dhsaidqhndi/494",
    "renegade_olmas_4": "https://t.me/dhsaidqhndi/495",
    "renegade_olmas_5": "https://t.me/dhsaidqhndi/496",
    "renegade_olmas_6": "https://t.me/dhsaidqhndi/497",
    "renegade_olmas_7": "https://t.me/dhsaidqhndi/498",
    "renegade_olmas_8": "https://t.me/dhsaidqhndi/499",
    "renegade_olmas_9": "https://t.me/dhsaidqhndi/500",
    "renegade_olmas_10": "https://t.me/dhsaidqhndi/501",
    "renegade_olmas_11": "https://t.me/dhsaidqhndi/502",
    "renegade_olmas_12": "https://t.me/dhsaidqhndi/503",
    "renegade_olmas_13": "https://t.me/dhsaidqhndi/504",
    "renegade_olmas_14": "https://t.me/dhsaidqhndi/505",
    "renegade_olmas_15": "https://t.me/dhsaidqhndi/506",
    "renegade_olmas_16": "https://t.me/dhsaidqhndi/507",
    "renegade_olmas_17": "https://t.me/dhsaidqhndi/508",
    "renegade_olmas_18": "https://t.me/dhsaidqhndi/509",
    "renegade_olmas_19": "https://t.me/dhsaidqhndi/510",
    "renegade_olmas_20": "https://t.me/dhsaidqhndi/511",
    "renegade_olmas_21": "https://t.me/dhsaidqhndi/512",
    "renegade_olmas_22": "https://t.me/dhsaidqhndi/513",
    "renegade_olmas_23": "https://t.me/dhsaidqhndi/514",
    "renegade_olmas_24": "https://t.me/dhsaidqhndi/515",
    "renegade_olmas_25": "https://t.me/dhsaidqhndi/516",
    "renegade_olmas_26": "https://t.me/dhsaidqhndi/517",
    "renegade_olmas_27": "https://t.me/dhsaidqhndi/518",
    "renegade_olmas_28": "https://t.me/dhsaidqhndi/519",
    "renegade_olmas_29": "https://t.me/dhsaidqhndi/520",
    "renegade_olmas_30": "https://t.me/dhsaidqhndi/521",
    "renegade_olmas_31": "https://t.me/dhsaidqhndi/522",
    "renegade_olmas_32": "https://t.me/dhsaidqhndi/523",
    "renegade_olmas_33": "https://t.me/dhsaidqhndi/524",
    "renegade_olmas_34": "https://t.me/dhsaidqhndi/525",
    "renegade_olmas_35": "https://t.me/dhsaidqhndi/526",
    "renegade_olmas_36": "https://t.me/dhsaidqhndi/527",
    "renegade_olmas_37": "https://t.me/dhsaidqhndi/528",
    "renegade_olmas_38": "https://t.me/dhsaidqhndi/529",
    "renegade_olmas_39": "https://t.me/dhsaidqhndi/530",
    "renegade_olmas_40": "https://t.me/dhsaidqhndi/531",
    "renegade_olmas_41": "https://t.me/dhsaidqhndi/532",
    "renegade_olmas_42": "https://t.me/dhsaidqhndi/533",
    "renegade_olmas_43": "https://t.me/dhsaidqhndi/534",
    "renegade_olmas_44": "https://t.me/dhsaidqhndi/535",
    "renegade_olmas_45": "https://t.me/dhsaidqhndi/536",
    "renegade_olmas_46": "https://t.me/dhsaidqhndi/537",
    "renegade_olmas_47": "https://t.me/dhsaidqhndi/538",
    "renegade_olmas_48": "https://t.me/dhsaidqhndi/539",
    "renegade_olmas_49": "https://t.me/dhsaidqhndi/540",
    "renegade_olmas_50": "https://t.me/dhsaidqhndi/541",
    "renegade_olmas_51": "https://t.me/dhsaidqhndi/542",
    "renegade_olmas_52": "https://t.me/dhsaidqhndi/543",
    "renegade_olmas_53": "https://t.me/dhsaidqhndi/544",
    "renegade_olmas_54": "https://t.me/dhsaidqhndi/545",
    "renegade_olmas_55": "https://t.me/dhsaidqhndi/546",
    "renegade_olmas_56": "https://t.me/dhsaidqhndi/547",
    "renegade_olmas_57": "https://t.me/dhsaidqhndi/548",
    "renegade_olmas_58": "https://t.me/dhsaidqhndi/549",
    "renegade_olmas_59": "https://t.me/dhsaidqhndi/550",
    "renegade_olmas_60": "https://t.me/dhsaidqhndi/551",
    "renegade_olmas_61": "https://t.me/dhsaidqhndi/552",
    "renegade_olmas_62": "https://t.me/dhsaidqhndi/553",
    "renegade_olmas_63": "https://t.me/dhsaidqhndi/554",
    "renegade_olmas_64": "https://t.me/dhsaidqhndi/555",
    "renegade_olmas_65": "https://t.me/dhsaidqhndi/556",
    "renegade_olmas_66": "https://t.me/dhsaidqhndi/557",
    "renegade_olmas_67": "https://t.me/dhsaidqhndi/558",
    "renegade_olmas_68": "https://t.me/dhsaidqhndi/559",
    "renegade_olmas_69": "https://t.me/dhsaidqhndi/560",
    "renegade_olmas_70": "https://t.me/dhsaidqhndi/561",
    "renegade_olmas_71": "https://t.me/dhsaidqhndi/562",
    "renegade_olmas_72": "https://t.me/dhsaidqhndi/563",
    "renegade_olmas_73": "https://t.me/dhsaidqhndi/564",
    "renegade_olmas_74": "https://t.me/dhsaidqhndi/565",
    "renegade_olmas_75": "https://t.me/dhsaidqhndi/566",
    "renegade_olmas_76": "https://t.me/dhsaidqhndi/567",
    "renegade_olmas_77": "https://t.me/dhsaidqhndi/568",
    "renegade_olmas_78": "https://t.me/dhsaidqhndi/569",
    "renegade_olmas_79": "https://t.me/dhsaidqhndi/570",
    "renegade_olmas_80": "https://t.me/dhsaidqhndi/571",
    "renegade_olmas_81": "https://t.me/dhsaidqhndi/572",
    "renegade_olmas_82": "https://t.me/dhsaidqhndi/573",
    "renegade_olmas_83": "https://t.me/dhsaidqhndi/574",
    "renegade_olmas_84": "https://t.me/dhsaidqhndi/575",
    "renegade_olmas_85": "https://t.me/dhsaidqhndi/576",
    "renegade_olmas_86": "https://t.me/dhsaidqhndi/577",
    "renegade_olmas_87": "https://t.me/dhsaidqhndi/578",
    "renegade_olmas_88": "https://t.me/dhsaidqhndi/579",
    "renegade_olmas_89": "https://t.me/dhsaidqhndi/580",
    "renegade_olmas_90": "https://t.me/dhsaidqhndi/581",
    "renegade_olmas_91": "https://t.me/dhsaidqhndi/582",
    "renegade_olmas_92": "https://t.me/dhsaidqhndi/583",
    "renegade_olmas_93": "https://t.me/dhsaidqhndi/584",
    "renegade_olmas_94": "https://t.me/dhsaidqhndi/585",
    "renegade_olmas_95": "https://t.me/dhsaidqhndi/586",
    "renegade_olmas_96": "https://t.me/dhsaidqhndi/587",
    "renegade_olmas_97": "https://t.me/dhsaidqhndi/588",
    "renegade_olmas_98": "https://t.me/dhsaidqhndi/589",
    "renegade_olmas_99": "https://t.me/dhsaidqhndi/923",
    "renegade_olmas_100": "https://t.me/dhsaidqhndi/924",
    "renegade_olmas_101": "https://t.me/dhsaidqhndi/590",
    "renegade_olmas_102": "https://t.me/dhsaidqhndi/925",
    "renegade_olmas_103": "https://t.me/dhsaidqhndi/926",
    "renegade_olmas_104": "https://t.me/dhsaidqhndi/601",
    "renegade_olmas_105": "https://t.me/dhsaidqhndi/591",
    "renegade_olmas_106": "https://t.me/dhsaidqhndi/592",
    "renegade_olmas_107": "https://t.me/dhsaidqhndi/593",
    "renegade_olmas_108": "https://t.me/dhsaidqhndi/594",
    "renegade_olmas_109": "https://t.me/dhsaidqhndi/595",
    "renegade_olmas_110": "https://t.me/dhsaidqhndi/596",
    "renegade_olmas_111": "https://t.me/dhsaidqhndi/930",
    "renegade_olmas_112": "https://t.me/dhsaidqhndi/1313",
    "renegade_olmas_113": "https://t.me/dhsaidqhndi/1959",
    "renegade_olmas_114": "https://t.me/dhsaidqhndi/2234",
    "renegade_olmas_115": "https://t.me/dhsaidqhndi/2323",
    "renegade_olmas_116": "https://t.me/dhsaidqhndi/2412",
    "renegade_olmas_117": "https://t.me/dhsaidqhndi/2413",
    "renegade_olmas_118": "https://t.me/dhsaidqhndi/2504",
    "renegade_olmas_119": "https://t.me/dhsaidqhndi/2524",
    "renegade_olmas_120": "https://t.me/dhsaidqhndi/2605",
    "renegade_olmas_121": "https://t.me/dhsaidqhndi/2664",
}

# ==================== JANGOVAR QIT'A ====================
@dp.message(F.text == "JANGOVAR QIT'A")
async def qita_handler(message: types.Message):
    await message.answer(
        "🔥 *Jangovar Qit’a* qismlarini tanlang:",
        reply_markup=get_qita_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^qita_page_\d+$"))
async def change_qita_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_qita_page_keyboard(page))
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^qita_\d+$"))
async def send_qita_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = qita_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return
    qism = key.split("_")[-1]
    caption = (
        "🎬 <b>Nomi:</b> JANGOVAR QIT'A\n"
        "🎞 <b>Janr:</b> Jang, Fantastika, Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@uzdubgo</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @uzdubgo | @bananatv_uz\n"
        "#jangovar_qita"
    )
    await bot.send_video(callback.from_user.id, video_link, caption=caption, parse_mode="HTML", protect_content=True)

def get_qita_page_keyboard(page: int):
    per_page = 20
    start = (page-1)*per_page
    end = start+per_page
    keys = list(qita_videolar.keys())[start:end]

    buttons = [[InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"qita_{i+1}")] for i, _ in enumerate(keys, start=start)]
    nav = []

    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"qita_page_{page-1}"))
    if end < len(qita_videolar):
        nav.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"qita_page_{page+1}"))
    if nav:
        buttons.append(nav)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎞 JANGOVAR QIT'A videolar ro'yxati
qita_videolar = {
    "qita_1": "https://t.me/dhsaidqhndi/2043",
    "qita_2": "https://t.me/dhsaidqhndi/2044",
    "qita_3": "https://t.me/dhsaidqhndi/2045",
    "qita_4": "https://t.me/dhsaidqhndi/2046",
    "qita_5": "https://t.me/dhsaidqhndi/2047",
    "qita_6": "https://t.me/dhsaidqhndi/2048",
    "qita_7": "https://t.me/dhsaidqhndi/2049",
    "qita_8": "https://t.me/dhsaidqhndi/2050",
    "qita_9": "https://t.me/dhsaidqhndi/2051",
    "qita_10": "https://t.me/dhsaidqhndi/2052",
    "qita_11": "https://t.me/dhsaidqhndi/2053",
    "qita_12": "https://t.me/dhsaidqhndi/2054",
    "qita_13": "https://t.me/dhsaidqhndi/2055",
    "qita_14": "https://t.me/dhsaidqhndi/2056",
    "qita_15": "https://t.me/dhsaidqhndi/2057",
    "qita_16": "https://t.me/dhsaidqhndi/2058",
}

# ==================== TAXT MUHRI ====================
# 🎥 TAXT MUHRI — Asosiy menyu
@dp.message(F.text == "TAXT MUHRI")
async def taxt_muhri_handler(message: types.Message):
    await message.answer(
        "👑 *Taxt Muhri* qismlarini tanlang:",
        reply_markup=get_taxt_page_keyboard(1),
        parse_mode="Markdown"
    )


# 📄 Sahifa almashtirish (pagination)
@dp.callback_query(F.data.regexp(r"^taxt_page_\d+$"))
async def change_taxt_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_taxt_page_keyboard(page))
    await callback.answer()


# 🎬 Video yuborish (ma’lumotli tarzda)
@dp.callback_query(F.data.regexp(r"^taxt_muhri_\d+$"))
async def send_taxt_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = taxt_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> Taxt Muhri\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Sehrli, Jangovar, Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (Uzdubgo)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @Uzdubgo | @bananatv_uz\n"
        "#taxt_muhri_animania\n\n"
        "💬 “Taxt — kuch, kuch esa mas’uliyat. Haqiqiy shoh yuragida rahm bilan hukm yuritadi.” ⚔️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption.replace("*", "").replace("_", ""),  # xavfsizlik uchun
        protect_content=True,
        parse_mode="HTML"
    )

# 🔘 Sahifalangan tugmalar — 20 ta per page
def get_taxt_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20  # Har sahifada 20 ta qism chiqadi
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(taxt_videolar.keys())[start:end]

    buttons = []
    for i, key in enumerate(keys, start=start):
        buttons.append([
            InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"taxt_muhri_{i+1}")
        ])

    # Navigatsiya tugmalari
    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"taxt_page_{page-1}"))
    if end < len(taxt_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"taxt_page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎞 1–182 gacha “TAXT MUHRI” videolari
taxt_videolar = {
    "taxt_muhri_1": "http://t.me/dhsaidqhndi/15",
    "taxt_muhri_2": "https://t.me/dhsaidqhndi/16",
    "taxt_muhri_3": "https://t.me/dhsaidqhndi/17",
    "taxt_muhri_4": "https://t.me/dhsaidqhndi/19",
    "taxt_muhri_5": "https://t.me/dhsaidqhndi/18",
    "taxt_muhri_6": "https://t.me/dhsaidqhndi/20",
    "taxt_muhri_7": "https://t.me/dhsaidqhndi/21",
    "taxt_muhri_8": "https://t.me/dhsaidqhndi/23",
    "taxt_muhri_9": "https://t.me/dhsaidqhndi/24",
    "taxt_muhri_10": "https://t.me/dhsaidqhndi/22",
    "taxt_muhri_11": "https://t.me/dhsaidqhndi/25",
    "taxt_muhri_12": "https://t.me/dhsaidqhndi/27",
    "taxt_muhri_13": "https://t.me/dhsaidqhndi/26",
    "taxt_muhri_14": "https://t.me/dhsaidqhndi/28",
    "taxt_muhri_15": "https://t.me/dhsaidqhndi/29",
    "taxt_muhri_16": "https://t.me/dhsaidqhndi/31",
    "taxt_muhri_17": "https://t.me/dhsaidqhndi/32",
    "taxt_muhri_18": "https://t.me/dhsaidqhndi/30",
    "taxt_muhri_19": "https://t.me/dhsaidqhndi/34",
    "taxt_muhri_20": "https://t.me/dhsaidqhndi/35",
    "taxt_muhri_21": "https://t.me/dhsaidqhndi/33",
    "taxt_muhri_22": "https://t.me/dhsaidqhndi/36",
    "taxt_muhri_23": "https://t.me/dhsaidqhndi/37",
    "taxt_muhri_24": "https://t.me/dhsaidqhndi/38",
    "taxt_muhri_25": "https://t.me/dhsaidqhndi/39",
    "taxt_muhri_26": "https://t.me/dhsaidqhndi/40",
    "taxt_muhri_27": "https://t.me/dhsaidqhndi/41",
    "taxt_muhri_28": "https://t.me/dhsaidqhndi/44",
    "taxt_muhri_29": "https://t.me/dhsaidqhndi/43",
    "taxt_muhri_30": "https://t.me/dhsaidqhndi/42",
    "taxt_muhri_31": "https://t.me/dhsaidqhndi/46",
    "taxt_muhri_32": "https://t.me/dhsaidqhndi/47",
    "taxt_muhri_33": "https://t.me/dhsaidqhndi/49",
    "taxt_muhri_34": "https://t.me/dhsaidqhndi/45",
    "taxt_muhri_35": "https://t.me/dhsaidqhndi/50",
    "taxt_muhri_36": "https://t.me/dhsaidqhndi/48",
    "taxt_muhri_37": "https://t.me/dhsaidqhndi/51",
    "taxt_muhri_38": "https://t.me/dhsaidqhndi/55",
    "taxt_muhri_39": "https://t.me/dhsaidqhndi/52",
    "taxt_muhri_40": "https://t.me/dhsaidqhndi/54",
    "taxt_muhri_41": "https://t.me/dhsaidqhndi/53",
    "taxt_muhri_42": "https://t.me/dhsaidqhndi/57",
    "taxt_muhri_43": "https://t.me/dhsaidqhndi/59",
    "taxt_muhri_44": "https://t.me/dhsaidqhndi/56",
    "taxt_muhri_45": "https://t.me/dhsaidqhndi/58",
    "taxt_muhri_46": "https://t.me/dhsaidqhndi/60",
    "taxt_muhri_47": "https://t.me/dhsaidqhndi/62",
    "taxt_muhri_48": "https://t.me/dhsaidqhndi/61",
    "taxt_muhri_49": "https://t.me/dhsaidqhndi/63",
    "taxt_muhri_50": "https://t.me/dhsaidqhndi/64",
    "taxt_muhri_51": "https://t.me/dhsaidqhndi/90",
    "taxt_muhri_52": "https://t.me/dhsaidqhndi/91",
    "taxt_muhri_53": "https://t.me/dhsaidqhndi/92",
    "taxt_muhri_54": "https://t.me/dhsaidqhndi/94",
    "taxt_muhri_55": "https://t.me/dhsaidqhndi/95",
    "taxt_muhri_56": "https://t.me/dhsaidqhndi/96",
    "taxt_muhri_57": "https://t.me/dhsaidqhndi/97",
    "taxt_muhri_58": "https://t.me/dhsaidqhndi/99",
    "taxt_muhri_59": "https://t.me/dhsaidqhndi/100",
    "taxt_muhri_60": "https://t.me/dhsaidqhndi/101",
    "taxt_muhri_61": "https://t.me/dhsaidqhndi/102",
    "taxt_muhri_62": "https://t.me/dhsaidqhndi/103",
    "taxt_muhri_63": "https://t.me/dhsaidqhndi/104",
    "taxt_muhri_64": "https://t.me/dhsaidqhndi/105",
    "taxt_muhri_65": "https://t.me/dhsaidqhndi/106",
    "taxt_muhri_66": "https://t.me/dhsaidqhndi/107",
    "taxt_muhri_67": "https://t.me/dhsaidqhndi/108",
    "taxt_muhri_68": "https://t.me/dhsaidqhndi/109",
    "taxt_muhri_69": "https://t.me/dhsaidqhndi/110",
    "taxt_muhri_70": "https://t.me/dhsaidqhndi/111",
    "taxt_muhri_71": "https://t.me/dhsaidqhndi/112",
    "taxt_muhri_72": "https://t.me/dhsaidqhndi/113",
    "taxt_muhri_73": "https://t.me/dhsaidqhndi/114",
    "taxt_muhri_74": "https://t.me/dhsaidqhndi/115",
    "taxt_muhri_75": "https://t.me/dhsaidqhndi/116",
    "taxt_muhri_76": "https://t.me/dhsaidqhndi/117",
    "taxt_muhri_77": "https://t.me/dhsaidqhndi/118",
    "taxt_muhri_78": "https://t.me/dhsaidqhndi/119",
    "taxt_muhri_79": "https://t.me/dhsaidqhndi/120",
    "taxt_muhri_80": "https://t.me/dhsaidqhndi/121",
    "taxt_muhri_81": "https://t.me/dhsaidqhndi/122",
    "taxt_muhri_82": "https://t.me/dhsaidqhndi/123",
    "taxt_muhri_83": "https://t.me/dhsaidqhndi/124",
    "taxt_muhri_84": "https://t.me/dhsaidqhndi/125",
    "taxt_muhri_85": "https://t.me/dhsaidqhndi/126",
    "taxt_muhri_86": "https://t.me/dhsaidqhndi/127",
    "taxt_muhri_87": "https://t.me/dhsaidqhndi/128",
    "taxt_muhri_88": "https://t.me/dhsaidqhndi/129",
    "taxt_muhri_89": "https://t.me/dhsaidqhndi/130",
    "taxt_muhri_90": "https://t.me/dhsaidqhndi/131",
    "taxt_muhri_91": "https://t.me/dhsaidqhndi/132",
    "taxt_muhri_92": "https://t.me/dhsaidqhndi/133",
    "taxt_muhri_93": "https://t.me/dhsaidqhndi/134",
    "taxt_muhri_94": "https://t.me/dhsaidqhndi/135",
    "taxt_muhri_95": "https://t.me/dhsaidqhndi/136",
    "taxt_muhri_96": "https://t.me/dhsaidqhndi/137",
    "taxt_muhri_97": "https://t.me/dhsaidqhndi/138",
    "taxt_muhri_98": "https://t.me/dhsaidqhndi/139",
    "taxt_muhri_99": "https://t.me/dhsaidqhndi/140",
    "taxt_muhri_100": "https://t.me/dhsaidqhndi/141",
    "taxt_muhri_101": "https://t.me/dhsaidqhndi/142",
    "taxt_muhri_102": "https://t.me/dhsaidqhndi/143",
    "taxt_muhri_103": "https://t.me/dhsaidqhndi/144",
    "taxt_muhri_104": "https://t.me/dhsaidqhndi/145",
    "taxt_muhri_105": "https://t.me/dhsaidqhndi/146",
    "taxt_muhri_106": "https://t.me/dhsaidqhndi/147",
    "taxt_muhri_107": "https://t.me/dhsaidqhndi/148",
    "taxt_muhri_108": "https://t.me/dhsaidqhndi/149",
    "taxt_muhri_109": "https://t.me/dhsaidqhndi/150",
    "taxt_muhri_110": "https://t.me/dhsaidqhndi/151",
    "taxt_muhri_111": "https://t.me/dhsaidqhndi/154",
    "taxt_muhri_112": "https://t.me/dhsaidqhndi/155",
    "taxt_muhri_113": "https://t.me/dhsaidqhndi/156",
    "taxt_muhri_114": "https://t.me/dhsaidqhndi/157",
    "taxt_muhri_115": "https://t.me/dhsaidqhndi/158",
    "taxt_muhri_116": "https://t.me/dhsaidqhndi/159",
    "taxt_muhri_117": "https://t.me/dhsaidqhndi/160",
    "taxt_muhri_118": "https://t.me/dhsaidqhndi/161",
    "taxt_muhri_119": "https://t.me/dhsaidqhndi/162",
    "taxt_muhri_120": "https://t.me/dhsaidqhndi/163",
    "taxt_muhri_121": "https://t.me/dhsaidqhndi/164",
    "taxt_muhri_122": "https://t.me/dhsaidqhndi/165",
    "taxt_muhri_123": "https://t.me/dhsaidqhndi/166",
    "taxt_muhri_124": "https://t.me/dhsaidqhndi/167",
    "taxt_muhri_125": "https://t.me/dhsaidqhndi/168",
    "taxt_muhri_126": "https://t.me/dhsaidqhndi/169",
    "taxt_muhri_127": "https://t.me/dhsaidqhndi/170",
    "taxt_muhri_128": "https://t.me/dhsaidqhndi/171",
    "taxt_muhri_129": "https://t.me/dhsaidqhndi/172",
    "taxt_muhri_130": "https://t.me/dhsaidqhndi/173",
    "taxt_muhri_131": "https://t.me/dhsaidqhndi/174",
    "taxt_muhri_132": "https://t.me/dhsaidqhndi/175",
    "taxt_muhri_133": "https://t.me/dhsaidqhndi/176",
    "taxt_muhri_134": "https://t.me/dhsaidqhndi/177",
    "taxt_muhri_135": "https://t.me/dhsaidqhndi/178",
    "taxt_muhri_136": "https://t.me/dhsaidqhndi/179",
    "taxt_muhri_137": "https://t.me/dhsaidqhndi/180",
    "taxt_muhri_138": "https://t.me/dhsaidqhndi/181",
    "taxt_muhri_139": "https://t.me/dhsaidqhndi/182",
    "taxt_muhri_140": "https://t.me/dhsaidqhndi/183",
    "taxt_muhri_141": "https://t.me/dhsaidqhndi/184",
    "taxt_muhri_142": "https://t.me/dhsaidqhndi/185",
    "taxt_muhri_143": "https://t.me/dhsaidqhndi/186",
    "taxt_muhri_144": "https://t.me/dhsaidqhndi/187",
    "taxt_muhri_145": "https://t.me/dhsaidqhndi/188",
    "taxt_muhri_146": "https://t.me/dhsaidqhndi/189",
    "taxt_muhri_147": "https://t.me/dhsaidqhndi/190",
    "taxt_muhri_148": "https://t.me/dhsaidqhndi/191",
    "taxt_muhri_149": "https://t.me/dhsaidqhndi/192",
    "taxt_muhri_150": "https://t.me/dhsaidqhndi/193",
    "taxt_muhri_151": "https://t.me/dhsaidqhndi/194",
    "taxt_muhri_152": "https://t.me/dhsaidqhndi/195",
    "taxt_muhri_153": "https://t.me/dhsaidqhndi/196",
    "taxt_muhri_154": "https://t.me/dhsaidqhndi/197",
    "taxt_muhri_155": "https://t.me/dhsaidqhndi/198",
    "taxt_muhri_156": "https://t.me/dhsaidqhndi/199",
    "taxt_muhri_157": "https://t.me/dhsaidqhndi/200",
    "taxt_muhri_158": "https://t.me/dhsaidqhndi/201",
    "taxt_muhri_159": "https://t.me/dhsaidqhndi/202",
    "taxt_muhri_160": "https://t.me/dhsaidqhndi/203",
    "taxt_muhri_161": "https://t.me/dhsaidqhndi/204",
    "taxt_muhri_162": "https://t.me/dhsaidqhndi/205",
    "taxt_muhri_163": "https://t.me/dhsaidqhndi/206",
    "taxt_muhri_164": "https://t.me/dhsaidqhndi/207",
    "taxt_muhri_165": "https://t.me/dhsaidqhndi/208",
    "taxt_muhri_166": "https://t.me/dhsaidqhndi/209",
    "taxt_muhri_167": "https://t.me/dhsaidqhndi/210",
    "taxt_muhri_168": "https://t.me/dhsaidqhndi/211",
    "taxt_muhri_169": "https://t.me/dhsaidqhndi/212",
    "taxt_muhri_170": "https://t.me/dhsaidqhndi/213",
    "taxt_muhri_171": "https://t.me/dhsaidqhndi/214",
    "taxt_muhri_172": "https://t.me/dhsaidqhndi/215",
    "taxt_muhri_173": "https://t.me/dhsaidqhndi/216",
    "taxt_muhri_174": "https://t.me/dhsaidqhndi/217",
    "taxt_muhri_175": "https://t.me/dhsaidqhndi/218",
    "taxt_muhri_176": "https://t.me/dhsaidqhndi/219",
    "taxt_muhri_177": "https://t.me/dhsaidqhndi/220",
    "taxt_muhri_178": "https://t.me/dhsaidqhndi/221",
    "taxt_muhri_179": "https://t.me/dhsaidqhndi/222",
    "taxt_muhri_180": "https://t.me/dhsaidqhndi/223",
    "taxt_muhri_181": "https://t.me/dhsaidqhndi/879",
    "taxt_muhri_182": "https://t.me/dhsaidqhndi/931",
    "taxt_muhri_183": "https://t.me/dhsaidqhndi/2374",
    "taxt_muhri_184": "https://t.me/dhsaidqhndi/2375",
    "taxt_muhri_185": "https://t.me/dhsaidqhndi/2376",
    "taxt_muhri_186": "https://t.me/dhsaidqhndi/2377",
    "taxt_muhri_187": "https://t.me/dhsaidqhndi/2478",
    "taxt_muxri_188": "https://t.me/dhsaidqhndi/2506",
    "taxt_muhri_189": "https://t.me/dhsaidqhndi/2503",
    "taxt_muxri_190": "https://t.me/dhsaidqhndi/2604",
    "taxt_muhri_191": "https://t.me/dhsaidqhndi/2665",
}

#====================MUKAMMAL DUNYO===================
# 🎥 MUKAMMAL DUNYO — Asosiy menyu
@dp.message(F.text == "MUKAMMAL DUNYO")
async def mukammal_dunyo_handler(message: types.Message):
    await message.answer(
        "🌌 *Mukammal Dunyo* qismlarini tanlang:",
        reply_markup=get_mukammal_page_keyboard(1),
        parse_mode="Markdown"
    )

# 📄 Sahifa almashtirish (pagination)
@dp.callback_query(F.data.regexp(r"^mukammal_page_\d+$"))
async def change_mukammal_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_mukammal_page_keyboard(page))
    await callback.answer()

# 🎬 Video yuborish (ma’lumotli tarzda)
@dp.callback_query(F.data.regexp(r"^mukammal_dunyo_\d+$"))
async def send_mukammal_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = mukammal_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        f"🎬 <b>Nomi:</b> Mukammal Dunyo\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Sehrli, Jangovar, Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniMajicUz)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @animajicuz\n"
        "💬 “Har doim biron nimaga suyanib yashama!” ☁️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

    await callback.answer()

# 🔘 Inline tugmalar — har betda 20 ta qism
def get_mukammal_page_keyboard(page: int):
    per_page = 20
    total = 250
    start = (page - 1) * per_page + 1
    end = min(start + per_page - 1, total)

    buttons = []
    for i in range(start, end + 1):
        buttons.append(
            [InlineKeyboardButton(text=f"{i}-qism", callback_data=f"mukammal_dunyo_{i}")]
        )

    # Navigatsiya tugmalari
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"mukammal_page_{page - 1}"))
    if end < total:
        nav.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"mukammal_page_{page + 1}"))
    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Mukammal Dunyo videolar ro'yxati:
mukammal_videolar = {
    "mukammal_dunyo_1": "https://t.me/dhsaidqhndi/600",
    "mukammal_dunyo_2": "https://t.me/dhsaidqhndi/601",
    "mukammal_dunyo_3": "https://t.me/dhsaidqhndi/602",
    "mukammal_dunyo_4": "https://t.me/dhsaidqhndi/603",
    "mukammal_dunyo_5": "https://t.me/dhsaidqhndi/604",
    "mukammal_dunyo_6": "https://t.me/dhsaidqhndi/605",
    "mukammal_dunyo_7": "https://t.me/dhsaidqhndi/606",
    "mukammal_dunyo_8": "https://t.me/dhsaidqhndi/607",
    "mukammal_dunyo_9": "https://t.me/dhsaidqhndi/608",
    "mukammal_dunyo_10": "https://t.me/dhsaidqhndi/609",
    "mukammal_dunyo_11": "https://t.me/dhsaidqhndi/610",
    "mukammal_dunyo_12": "https://t.me/dhsaidqhndi/611",
    "mukammal_dunyo_13": "https://t.me/dhsaidqhndi/612",
    "mukammal_dunyo_14": "https://t.me/dhsaidqhndi/613",
    "mukammal_dunyo_15": "https://t.me/dhsaidqhndi/614",
    "mukammal_dunyo_16": "https://t.me/dhsaidqhndi/615",
    "mukammal_dunyo_17": "https://t.me/dhsaidqhndi/616",
    "mukammal_dunyo_18": "https://t.me/dhsaidqhndi/617",
    "mukammal_dunyo_19": "https://t.me/dhsaidqhndi/618",
    "mukammal_dunyo_20": "https://t.me/dhsaidqhndi/619",
    "mukammal_dunyo_21": "https://t.me/dhsaidqhndi/620",
    "mukammal_dunyo_22": "https://t.me/dhsaidqhndi/621",
    "mukammal_dunyo_23": "https://t.me/dhsaidqhndi/622",
    "mukammal_dunyo_24": "https://t.me/dhsaidqhndi/623",
    "mukammal_dunyo_25": "https://t.me/dhsaidqhndi/624",
    "mukammal_dunyo_26": "https://t.me/dhsaidqhndi/625",
    "mukammal_dunyo_27": "https://t.me/dhsaidqhndi/626",
    "mukammal_dunyo_28": "https://t.me/dhsaidqhndi/627",
    "mukammal_dunyo_29": "https://t.me/dhsaidqhndi/628",
    "mukammal_dunyo_30": "https://t.me/dhsaidqhndi/629",
    "mukammal_dunyo_31": "https://t.me/dhsaidqhndi/630",
    "mukammal_dunyo_32": "https://t.me/dhsaidqhndi/631",
    "mukammal_dunyo_33": "https://t.me/dhsaidqhndi/632",
    "mukammal_dunyo_34": "https://t.me/dhsaidqhndi/633",
    "mukammal_dunyo_35": "https://t.me/dhsaidqhndi/634",
    "mukammal_dunyo_36": "https://t.me/dhsaidqhndi/635",
    "mukammal_dunyo_37": "https://t.me/dhsaidqhndi/636",
    "mukammal_dunyo_38": "https://t.me/dhsaidqhndi/637",
    "mukammal_dunyo_39": "https://t.me/dhsaidqhndi/638",
    "mukammal_dunyo_40": "https://t.me/dhsaidqhndi/639",
    "mukammal_dunyo_41": "https://t.me/dhsaidqhndi/640",
    "mukammal_dunyo_42": "https://t.me/dhsaidqhndi/641",
    "mukammal_dunyo_43": "https://t.me/dhsaidqhndi/642",
    "mukammal_dunyo_44": "https://t.me/dhsaidqhndi/643",
    "mukammal_dunyo_45": "https://t.me/dhsaidqhndi/644",
    "mukammal_dunyo_46": "https://t.me/dhsaidqhndi/645",
    "mukammal_dunyo_47": "https://t.me/dhsaidqhndi/646",
    "mukammal_dunyo_48": "https://t.me/dhsaidqhndi/647",
    "mukammal_dunyo_49": "https://t.me/dhsaidqhndi/648",
    "mukammal_dunyo_50": "https://t.me/dhsaidqhndi/649",
    "mukammal_dunyo_51": "https://t.me/dhsaidqhndi/749",
    "mukammal_dunyo_52": "https://t.me/dhsaidqhndi/750",
    "mukammal_dunyo_53": "https://t.me/dhsaidqhndi/751",
    "mukammal_dunyo_54": "https://t.me/dhsaidqhndi/752",
    "mukammal_dunyo_55": "https://t.me/dhsaidqhndi/753",
    "mukammal_dunyo_56": "https://t.me/dhsaidqhndi/754",
    "mukammal_dunyo_57": "https://t.me/dhsaidqhndi/755",
    "mukammal_dunyo_58": "https://t.me/dhsaidqhndi/756",
    "mukammal_dunyo_59": "https://t.me/dhsaidqhndi/757",
    "mukammal_dunyo_60": "https://t.me/dhsaidqhndi/758",
    "mukammal_dunyo_61": "https://t.me/dhsaidqhndi/759",
    "mukammal_dunyo_62": "https://t.me/dhsaidqhndi/760",
    "mukammal_dunyo_63": "https://t.me/dhsaidqhndi/761",
    "mukammal_dunyo_64": "https://t.me/dhsaidqhndi/762",
    "mukammal_dunyo_65": "https://t.me/dhsaidqhndi/763",
    "mukammal_dunyo_66": "https://t.me/dhsaidqhndi/764",
    "mukammal_dunyo_67": "https://t.me/dhsaidqhndi/765",
    "mukammal_dunyo_68": "https://t.me/dhsaidqhndi/766",
    "mukammal_dunyo_69": "https://t.me/dhsaidqhndi/767",
    "mukammal_dunyo_70": "https://t.me/dhsaidqhndi/768",
    "mukammal_dunyo_71": "https://t.me/dhsaidqhndi/769",
    "mukammal_dunyo_72": "https://t.me/dhsaidqhndi/770",
    "mukammal_dunyo_73": "https://t.me/dhsaidqhndi/771",
    "mukammal_dunyo_74": "https://t.me/dhsaidqhndi/772",
    "mukammal_dunyo_75": "https://t.me/dhsaidqhndi/773",
    "mukammal_dunyo_76": "https://t.me/dhsaidqhndi/774",
    "mukammal_dunyo_77": "https://t.me/dhsaidqhndi/775",
    "mukammal_dunyo_78": "https://t.me/dhsaidqhndi/776",
    "mukammal_dunyo_79": "https://t.me/dhsaidqhndi/777",
    "mukammal_dunyo_80": "https://t.me/dhsaidqhndi/778",
    "mukammal_dunyo_81": "https://t.me/dhsaidqhndi/779",
    "mukammal_dunyo_82": "https://t.me/dhsaidqhndi/780",
    "mukammal_dunyo_83": "https://t.me/dhsaidqhndi/781",
    "mukammal_dunyo_84": "https://t.me/dhsaidqhndi/782",
    "mukammal_dunyo_85": "https://t.me/dhsaidqhndi/783",
    "mukammal_dunyo_86": "https://t.me/dhsaidqhndi/784",
    "mukammal_dunyo_87": "https://t.me/dhsaidqhndi/785",
    "mukammal_dunyo_88": "https://t.me/dhsaidqhndi/786",
    "mukammal_dunyo_89": "https://t.me/dhsaidqhndi/787",
    "mukammal_dunyo_90": "https://t.me/dhsaidqhndi/788",
    "mukammal_dunyo_91": "https://t.me/dhsaidqhndi/789",
    "mukammal_dunyo_92": "https://t.me/dhsaidqhndi/790",
    "mukammal_dunyo_93": "https://t.me/dhsaidqhndi/791",
    "mukammal_dunyo_94": "https://t.me/dhsaidqhndi/792",
    "mukammal_dunyo_95": "https://t.me/dhsaidqhndi/793",
    "mukammal_dunyo_96": "https://t.me/dhsaidqhndi/794",
    "mukammal_dunyo_97": "https://t.me/dhsaidqhndi/795",
    "mukammal_dunyo_98": "https://t.me/dhsaidqhndi/796",
    "mukammal_dunyo_99": "https://t.me/dhsaidqhndi/797",
    "mukammal_dunyo_100": "https://t.me/dhsaidqhndi/798",
    "mukammal_dunyo_101": "https://t.me/dhsaidqhndi/799",
    "mukammal_dunyo_102": "https://t.me/dhsaidqhndi/800",
    "mukammal_dunyo_103": "https://t.me/dhsaidqhndi/801",
    "mukammal_dunyo_104": "https://t.me/dhsaidqhndi/802",
    "mukammal_dunyo_105": "https://t.me/dhsaidqhndi/803",
    "mukammal_dunyo_106": "https://t.me/dhsaidqhndi/804",
    "mukammal_dunyo_107": "https://t.me/dhsaidqhndi/805",
    "mukammal_dunyo_108": "https://t.me/dhsaidqhndi/806",
    "mukammal_dunyo_109": "https://t.me/dhsaidqhndi/807",
    "mukammal_dunyo_110": "https://t.me/dhsaidqhndi/808",
    "mukammal_dunyo_111": "https://t.me/dhsaidqhndi/809",
    "mukammal_dunyo_112": "https://t.me/dhsaidqhndi/810",
    "mukammal_dunyo_113": "https://t.me/dhsaidqhndi/811",
    "mukammal_dunyo_114": "https://t.me/dhsaidqhndi/812",
    "mukammal_dunyo_115": "https://t.me/dhsaidqhndi/813",
    "mukammal_dunyo_116": "https://t.me/dhsaidqhndi/814",
    "mukammal_dunyo_117": "https://t.me/dhsaidqhndi/815",
    "mukammal_dunyo_118": "https://t.me/dhsaidqhndi/816",
    "mukammal_dunyo_119": "https://t.me/dhsaidqhndi/817",
    "mukammal_dunyo_120": "https://t.me/dhsaidqhndi/818",
    "mukammal_dunyo_121": "https://t.me/dhsaidqhndi/819",
    "mukammal_dunyo_122": "https://t.me/dhsaidqhndi/820",
    "mukammal_dunyo_123": "https://t.me/dhsaidqhndi/821",
    "mukammal_dunyo_124": "https://t.me/dhsaidqhndi/822",
    "mukammal_dunyo_125": "https://t.me/dhsaidqhndi/823",
    "mukammal_dunyo_126": "https://t.me/dhsaidqhndi/824",
    "mukammal_dunyo_127": "https://t.me/dhsaidqhndi/825",
    "mukammal_dunyo_128": "https://t.me/dhsaidqhndi/826",
    "mukammal_dunyo_129": "https://t.me/dhsaidqhndi/827",
    "mukammal_dunyo_130": "https://t.me/dhsaidqhndi/828",
    "mukammal_dunyo_131": "https://t.me/dhsaidqhndi/829",
    "mukammal_dunyo_132": "https://t.me/dhsaidqhndi/830",
    "mukammal_dunyo_133": "https://t.me/dhsaidqhndi/831",
    "mukammal_dunyo_134": "https://t.me/dhsaidqhndi/832",
    "mukammal_dunyo_135": "https://t.me/dhsaidqhndi/833",
    "mukammal_dunyo_136": "https://t.me/dhsaidqhndi/834",
    "mukammal_dunyo_137": "https://t.me/dhsaidqhndi/835",
    "mukammal_dunyo_138": "https://t.me/dhsaidqhndi/836",
    "mukammal_dunyo_139": "https://t.me/dhsaidqhndi/837",
    "mukammal_dunyo_140": "https://t.me/dhsaidqhndi/838",
    "mukammal_dunyo_141": "https://t.me/dhsaidqhndi/839",
    "mukammal_dunyo_142": "https://t.me/dhsaidqhndi/840",
    "mukammal_dunyo_143": "https://t.me/dhsaidqhndi/841",
    "mukammal_dunyo_144": "https://t.me/dhsaidqhndi/842",
    "mukammal_dunyo_145": "https://t.me/dhsaidqhndi/843",
    "mukammal_dunyo_146": "https://t.me/dhsaidqhndi/844",
    "mukammal_dunyo_147": "https://t.me/dhsaidqhndi/845",
    "mukammal_dunyo_148": "https://t.me/dhsaidqhndi/846",
    "mukammal_dunyo_149": "https://t.me/dhsaidqhndi/847",
    "mukammal_dunyo_150": "https://t.me/dhsaidqhndi/848",
    "mukammal_dunyo_151": "https://t.me/dhsaidqhndi/849",
    "mukammal_dunyo_152": "https://t.me/dhsaidqhndi/850",
    "mukammal_dunyo_153": "https://t.me/dhsaidqhndi/851",
    "mukammal_dunyo_154": "https://t.me/dhsaidqhndi/852",
    "mukammal_dunyo_155": "https://t.me/dhsaidqhndi/853",
    "mukammal_dunyo_156": "https://t.me/dhsaidqhndi/854",
    "mukammal_dunyo_157": "https://t.me/dhsaidqhndi/855",
    "mukammal_dunyo_158": "https://t.me/dhsaidqhndi/856",
    "mukammal_dunyo_159": "https://t.me/dhsaidqhndi/857",
    "mukammal_dunyo_160": "https://t.me/dhsaidqhndi/858",
    "mukammal_dunyo_161": "https://t.me/dhsaidqhndi/859",
    "mukammal_dunyo_162": "https://t.me/dhsaidqhndi/860",
    "mukammal_dunyo_163": "https://t.me/dhsaidqhndi/861",
    "mukammal_dunyo_164": "https://t.me/dhsaidqhndi/862",
    "mukammal_dunyo_165": "https://t.me/dhsaidqhndi/863",
    "mukammal_dunyo_166": "https://t.me/dhsaidqhndi/864",
    "mukammal_dunyo_167": "https://t.me/dhsaidqhndi/865",
    "mukammal_dunyo_168": "https://t.me/dhsaidqhndi/866",
    "mukammal_dunyo_169": "https://t.me/dhsaidqhndi/867",
    "mukammal_dunyo_170": "https://t.me/dhsaidqhndi/868",
    "mukammal_dunyo_171": "https://t.me/dhsaidqhndi/869",
    "mukammal_dunyo_172": "https://t.me/dhsaidqhndi/870",
    "mukammal_dunyo_173": "https://t.me/dhsaidqhndi/871",
    "mukammal_dunyo_174": "https://t.me/dhsaidqhndi/872",
    "mukammal_dunyo_175": "https://t.me/dhsaidqhndi/873",
    "mukammal_dunyo_176": "https://t.me/dhsaidqhndi/874",
    "mukammal_dunyo_177": "https://t.me/dhsaidqhndi/875",
    "mukammal_dunyo_178": "https://t.me/dhsaidqhndi/876",
    "mukammal_dunyo_179": "https://t.me/dhsaidqhndi/877",
    "mukammal_dunyo_180": "https://t.me/dhsaidqhndi/878",
    "mukammal_dunyo_181": "https://t.me/dhsaidqhndi/879",
    "mukammal_dunyo_182": "https://t.me/dhsaidqhndi/880",
    "mukammal_dunyo_183": "https://t.me/dhsaidqhndi/881",
    "mukammal_dunyo_184": "https://t.me/dhsaidqhndi/882",
    "mukammal_dunyo_185": "https://t.me/dhsaidqhndi/883",
    "mukammal_dunyo_186": "https://t.me/dhsaidqhndi/884",
    "mukammal_dunyo_187": "https://t.me/dhsaidqhndi/885",
    "mukammal_dunyo_188": "https://t.me/dhsaidqhndi/886",
    "mukammal_dunyo_189": "https://t.me/dhsaidqhndi/887",
    "mukammal_dunyo_190": "https://t.me/dhsaidqhndi/888",
    "mukammal_dunyo_191": "https://t.me/dhsaidqhndi/889",
    "mukammal_dunyo_192": "https://t.me/dhsaidqhndi/890",
    "mukammal_dunyo_193": "https://t.me/dhsaidqhndi/891",
    "mukammal_dunyo_194": "https://t.me/dhsaidqhndi/892",
    "mukammal_dunyo_195": "https://t.me/dhsaidqhndi/893",
    "mukammal_dunyo_196": "https://t.me/dhsaidqhndi/894",
    "mukammal_dunyo_197": "https://t.me/dhsaidqhndi/895",
    "mukammal_dunyo_198": "https://t.me/dhsaidqhndi/896",
    "mukammal_dunyo_199": "https://t.me/dhsaidqhndi/897",
    "mukammal_dunyo_200": "https://t.me/dhsaidqhndi/898",
    "mukammal_dunyo_201": "https://t.me/dhsaidqhndi/899",
    "mukammal_dunyo_202": "https://t.me/dhsaidqhndi/900",
    "mukammal_dunyo_203": "https://t.me/dhsaidqhndi/901",
    "mukammal_dunyo_204": "https://t.me/dhsaidqhndi/902",
    "mukammal_dunyo_205": "https://t.me/dhsaidqhndi/903",
    "mukammal_dunyo_206": "https://t.me/dhsaidqhndi/904",
    "mukammal_dunyo_207": "https://t.me/dhsaidqhndi/905",
    "mukammal_dunyo_208": "https://t.me/dhsaidqhndi/906",
    "mukammal_dunyo_209": "https://t.me/dhsaidqhndi/907",
    "mukammal_dunyo_210": "https://t.me/dhsaidqhndi/908",
    "mukammal_dunyo_211": "https://t.me/dhsaidqhndi/909",
    "mukammal_dunyo_212": "https://t.me/dhsaidqhndi/910",
    "mukammal_dunyo_213": "https://t.me/dhsaidqhndi/911",
    "mukammal_dunyo_214": "https://t.me/dhsaidqhndi/912",
    "mukammal_dunyo_215": "https://t.me/dhsaidqhndi/913",
    "mukammal_dunyo_216": "https://t.me/dhsaidqhndi/914",
    "mukammal_dunyo_217": "https://t.me/dhsaidqhndi/915",
    "mukammal_dunyo_218": "https://t.me/dhsaidqhndi/916",
    "mukammal_dunyo_219": "https://t.me/dhsaidqhndi/917",
    "mukammal_dunyo_220": "https://t.me/dhsaidqhndi/918",
    "mukammal_dunyo_221": "https://t.me/dhsaidqhndi/919",
    "mukammal_dunyo_222": "https://t.me/dhsaidqhndi/920",
    "mukammal_dunyo_223": "https://t.me/dhsaidqhndi/927",
    "mukammal_dunyo_224": "https://t.me/dhsaidqhndi/928",
    "mukammal_dunyo_225": "https://t.me/dhsaidqhndi/1256",
    "mukammal_dunyo_226": "https://t.me/dhsaidqhndi/1257",
    "mukammal_dunyo_227": "https://t.me/dhsaidqhndi/1601",
    "mukammal_dunyo_228": "https://t.me/dhsaidqhndi/1867",
    "mukammal_dunyo_229": "https://t.me/dhsaidqhndi/2126",
    "mukammal_dunyo_230": "https://t.me/dhsaidqhndi/2132",
    "mukammal_dunyo_231": "https://t.me/dhsaidqhndi/2252",
    "mukammal_dunyo_232": "https://t.me/dhsaidqhndi/2305",
    "mukammal_dunyo_233": "https://t.me/dhsaidqhndi/2328",
    "mukammal_dunyo_234": "https://t.me/dhsaidqhndi/2414",
    "mukammal_dunyo_235": "https://t.me/dhsaidqhndi/2415",
    "mukammal_dunyo_236": "https://t.me/dhsaidqhndi/2416",
    "mukammal_dunyo_237": "https://t.me/dhsaidqhndi/2507",
    "mukammal_dunyo_238": "https://t.me/dhsaidqhndi/2508",
    "mukammal_dunyo_239": "https://t.me/dhsaidqhndi/2606",
    "mukammal_dunyo_240": "https://t.me/dhsaidqhndi/2607",
    "mukammal_dunyo_241": "https://t.me/dhsaidqhndi/2667",
}

# ==================== OSMONDAGI JANGLAR ====================
# 🌌 OSMONDAGI JANGLAR menyusi
@dp.message(F.text == "OSMONDAGI JANGLAR")
async def osmon_menu(message: types.Message):
    fasllar = list(osmon_videolar.keys())
    buttons = [
        [InlineKeyboardButton(text=fasl, callback_data=f"osmon_fasl_{fasl}")]
        for fasl in fasllar
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("⚔️ Osmondagi janglar faslini tanlang:", reply_markup=keyboard)


# 🔹 FASL TANLANGANDA
@dp.callback_query(F.data.startswith("osmon_fasl_"))
async def osmon_fasl_tanlandi(callback: types.CallbackQuery):
    fasl = callback.data.replace("osmon_fasl_", "")
    await callback.message.edit_text(
        f"☁️ Osmondagi janglar — {fasl}\n\nQuyidagi qismlardan birini tanlang 👇",
        reply_markup=generate_osmon_keyboard(fasl, 1)
    )


# 🔹 SAHIFALASH FUNKSIYASI
def generate_osmon_keyboard(fasl: str, page: int = 1):
    per_page = 30 if fasl == "5-fasl" else 50
    all_items = list(osmon_videolar[fasl].items())  # [(qism, url), ...]
    start = (page - 1) * per_page
    end = start + per_page
    items = all_items[start:end]

    keyboard = []
    for name, url in items:
        keyboard.append([InlineKeyboardButton(text=name, callback_data=f"osmon_video_{fasl}:{name}")])

    nav_buttons = []
    if start > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"osmon_page_{fasl}_{page-1}"))
    if end < len(all_items):
        nav_buttons.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"osmon_page_{fasl}_{page+1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# 🔹 SAHIFA ALMASHTIRILGANDA
@dp.callback_query(F.data.startswith("osmon_page_"))
async def osmon_page(callback: types.CallbackQuery):
    data = callback.data[len("osmon_page_"):]  # "5-fasl_2"
    fasl, page_str = data.rsplit("_", 1)
    page = int(page_str)

    await callback.message.edit_text(
        f"☁️ Osmondagi janglar — {fasl}\n\nQuyidagi qismlardan birini tanlang 👇",
        reply_markup=generate_osmon_keyboard(fasl, page)
    )


# 🔹 VIDEO YUBORISH
@dp.callback_query(F.data.startswith("osmon_video_"))
async def osmon_video_yubor(callback: types.CallbackQuery):
    # callback.data misol: osmon_video_5-fasl:231-qism
    data = callback.data[len("osmon_video_"):]  # "5-fasl:231-qism"
    if ":" not in data:
        await callback.answer("❌ Xato formatdagi video identifikator!", show_alert=True)
        return

    fasl, qism = data.split(":", 1)

    # Ma'lumotni tekshirish
    if fasl not in osmon_videolar or qism not in osmon_videolar[fasl]:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    video_link = osmon_videolar[fasl][qism]

    caption = (
        f"🎬 <b>Nomi:</b> Osmondagi Janglar\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Sehrli, Jangovar, Sarguzasht\n"
        f"📺 <b>Fasl:</b> {fasl}\n"
        f"🎞 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniMania_rasmiy | @uzdubgo | @aniconbo\n"
        "💬 “Osmonda g‘alaba qilganlarning yuragida jasorat yashaydi.” ⚔️"
    )
    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"  # <b> format uchun HTML qo‘llanildi
    )

    await callback.answer()

# 🎞 1–200 gacha “Osmondagi janglar” videolari
osmon_videolar = {
    "1-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/224",
        "2-qism": "https://t.me/dhsaidqhndi/225",
        "3-qism": "https://t.me/dhsaidqhndi/226",
    },
    "2-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/227",
        "2-qism": "https://t.me/dhsaidqhndi/228",
        "3-qism": "https://t.me/dhsaidqhndi/229",
        "4-qism": "https://t.me/dhsaidqhndi/230",
        "5-qism": "https://t.me/dhsaidqhndi/1361",
        "6-qism": "https://t.me/dhsaidqhndi/231",
        "7-qism": "https://t.me/dhsaidqhndi/232",
        "8-qism": "https://t.me/dhsaidqhndi/233",
        "9-qism": "https://t.me/dhsaidqhndi/234",
        "10-qism": "https://t.me/dhsaidqhndi/235",
        "11-qism": "https://t.me/dhsaidqhndi/236",
        "12-qism": "https://t.me/dhsaidqhndi/237",
        "13-qism": "https://t.me/dhsaidqhndi/238",
        "14-qism": "https://t.me/dhsaidqhndi/239",
        "15-qism": "https://t.me/dhsaidqhndi/240",
        "16-qism": "https://t.me/dhsaidqhndi/241",
        "17-qism": "https://t.me/dhsaidqhndi/242",
    },
    "3-fasl": {
        "1-qism":  "https://t.me/dhsaidqhndi/243",
        "2-qism":  "https://t.me/dhsaidqhndi/244",
        "3-qism":  "https://t.me/dhsaidqhndi/245",
        "4-qism":  "https://t.me/dhsaidqhndi/246",
        "5-qism":  "https://t.me/dhsaidqhndi/247",
        "6-qism":  "https://t.me/dhsaidqhndi/248",
        "7-qism":  "https://t.me/dhsaidqhndi/249",
        "8-qism":  "https://t.me/dhsaidqhndi/250",
        "9-qism":  "https://t.me/dhsaidqhndi/251",
        "10-qism": "https://t.me/dhsaidqhndi/252",
        "11-qism": "https://t.me/dhsaidqhndi/253",
        "12-qism": "https://t.me/dhsaidqhndi/254",
    },
    "4-fasl": {
        "1-qism":  "https://t.me/dhsaidqhndi/255",
        "2-qism":  "https://t.me/dhsaidqhndi/256",
        "3-qism":  "https://t.me/dhsaidqhndi/257",
        "4-qism":  "https://t.me/dhsaidqhndi/258",
        "5-qism":  "https://t.me/dhsaidqhndi/259",
        "6-qism":  "https://t.me/dhsaidqhndi/260",
        "7-qism":  "https://t.me/dhsaidqhndi/261",
        "8-qism":  "https://t.me/dhsaidqhndi/262",
        "9-qism":  "https://t.me/dhsaidqhndi/263",
        "10-qism": "https://t.me/dhsaidqhndi/264",
        "11-qism": "https://t.me/dhsaidqhndi/265",
        "12-qism": "https://t.me/dhsaidqhndi/266",
        "13-qism": "https://t.me/dhsaidqhndi/267",
        "14-qism": "https://t.me/dhsaidqhndi/268",
        "15-qism": "https://t.me/dhsaidqhndi/269",
        "16-qism": "https://t.me/dhsaidqhndi/270",
        "17-qism": "https://t.me/dhsaidqhndi/271",
        "18-qism": "https://t.me/dhsaidqhndi/272",
        "19-qism": "https://t.me/dhsaidqhndi/273",
        "20-qism": "https://t.me/dhsaidqhndi/274",
        "21-qism": "https://t.me/dhsaidqhndi/275",
        "22-qism": "https://t.me/dhsaidqhndi/276",
        "23-qism": "https://t.me/dhsaidqhndi/277",
        "24-qism": "https://t.me/dhsaidqhndi/278",
        "25-qism": "https://t.me/dhsaidqhndi/279",
        "26-qism": "https://t.me/dhsaidqhndi/280",
        "27-qism": "https://t.me/dhsaidqhndi/281",
        "28-qism": "https://t.me/dhsaidqhndi/282",
        "29-qism": "https://t.me/dhsaidqhndi/283",
        "30-qism": "https://t.me/dhsaidqhndi/284",
        "31-qism": "https://t.me/dhsaidqhndi/285",
        "32-qism": "https://t.me/dhsaidqhndi/286",
        "33-qism": "https://t.me/dhsaidqhndi/287",
        "34-qism": "https://t.me/dhsaidqhndi/288",
        "35-qism": "https://t.me/dhsaidqhndi/289",
        "36-qism": "https://t.me/dhsaidqhndi/290",
    },
    "5-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/291",
        "2-qism": "https://t.me/dhsaidqhndi/292",
        "3-qism": "https://t.me/dhsaidqhndi/293",
        "4-qism": "https://t.me/dhsaidqhndi/294",
        "5-qism": "https://t.me/dhsaidqhndi/295",
        "6-qism": "https://t.me/dhsaidqhndi/296",
        "7-qism": "https://t.me/dhsaidqhndi/297",
        "8-qism": "https://t.me/dhsaidqhndi/298",
        "9-qism": "https://t.me/dhsaidqhndi/299",
        "10-qism": "https://t.me/dhsaidqhndi/300",
        "11-qism": "https://t.me/dhsaidqhndi/301",
        "12-qism": "https://t.me/dhsaidqhndi/302",
        "13-qism": "https://t.me/dhsaidqhndi/303",
        "14-qism": "https://t.me/dhsaidqhndi/304",
        "15-qism": "https://t.me/dhsaidqhndi/305",
        "16-qism": "https://t.me/dhsaidqhndi/306",
        "17-qism": "https://t.me/dhsaidqhndi/307",
        "18-qism": "https://t.me/dhsaidqhndi/308",
        "19-qism": "https://t.me/dhsaidqhndi/309",
        "20-qism": "https://t.me/dhsaidqhndi/310",
        "21-qism": "https://t.me/dhsaidqhndi/311",
        "22-qism": "https://t.me/dhsaidqhndi/312",
        "23-qism": "https://t.me/dhsaidqhndi/313",
        "24-qism": "https://t.me/dhsaidqhndi/314",
        "25-qism": "https://t.me/dhsaidqhndi/315",
        "26-qism": "https://t.me/dhsaidqhndi/316",
        "27-qism": "https://t.me/dhsaidqhndi/317",
        "28-qism": "https://t.me/dhsaidqhndi/318",
        "29-qism": "https://t.me/dhsaidqhndi/319",
        "30-qism": "https://t.me/dhsaidqhndi/320",
        "31-qism": "https://t.me/dhsaidqhndi/321",
        "32-qism": "https://t.me/dhsaidqhndi/322",
        "33-qism": "https://t.me/dhsaidqhndi/323",
        "34-qism": "https://t.me/dhsaidqhndi/324",
        "35-qism": "https://t.me/dhsaidqhndi/325",
        "36-qism": "https://t.me/dhsaidqhndi/326",
        "37-qism": "https://t.me/dhsaidqhndi/327",
        "38-qism": "https://t.me/dhsaidqhndi/328",
        "39-qism": "https://t.me/dhsaidqhndi/329",
        "40-qism": "https://t.me/dhsaidqhndi/330",
        "41-qism": "https://t.me/dhsaidqhndi/331",
        "42-qism": "https://t.me/dhsaidqhndi/332",
        "43-qism": "https://t.me/dhsaidqhndi/333",
        "44-qism": "https://t.me/dhsaidqhndi/334",
        "45-qism": "https://t.me/dhsaidqhndi/335",
        "46-qism": "https://t.me/dhsaidqhndi/336",
        "47-qism": "https://t.me/dhsaidqhndi/337",
        "48-qism": "https://t.me/dhsaidqhndi/338",
        "49-qism": "https://t.me/dhsaidqhndi/339",
        "50-qism": "https://t.me/dhsaidqhndi/340",
        "51-qism": "https://t.me/dhsaidqhndi/341",
        "52-qism": "https://t.me/dhsaidqhndi/342",
        "53-qism": "https://t.me/dhsaidqhndi/343",
        "54-qism": "https://t.me/dhsaidqhndi/344",
        "55-qism": "https://t.me/dhsaidqhndi/345",
        "56-qism": "https://t.me/dhsaidqhndi/346",
        "57-qism": "https://t.me/dhsaidqhndi/347",
        "58-qism": "https://t.me/dhsaidqhndi/348",
        "59-qism": "https://t.me/dhsaidqhndi/349",
        "60-qism": "https://t.me/dhsaidqhndi/350",
        "61-qism": "https://t.me/dhsaidqhndi/351",
        "62-qism": "https://t.me/dhsaidqhndi/352",
        "63-qism": "https://t.me/dhsaidqhndi/353",
        "64-qism": "https://t.me/dhsaidqhndi/354",
        "65-qism": "https://t.me/dhsaidqhndi/355",
        "66-qism": "https://t.me/dhsaidqhndi/356",
        "67-qism": "https://t.me/dhsaidqhndi/357",
        "68-qism": "https://t.me/dhsaidqhndi/358",
        "69-qism": "https://t.me/dhsaidqhndi/359",
        "70-qism": "https://t.me/dhsaidqhndi/360",
        "71-qism": "https://t.me/dhsaidqhndi/361",
        "72-qism": "https://t.me/dhsaidqhndi/362",
        "73-qism": "https://t.me/dhsaidqhndi/363",
        "74-qism": "https://t.me/dhsaidqhndi/922",
        "75-qism": "https://t.me/dhsaidqhndi/364",
        "76-qism": "https://t.me/dhsaidqhndi/365",
        "77-qism": "https://t.me/dhsaidqhndi/366",
        "78-qism": "https://t.me/dhsaidqhndi/367",
        "79-qism": "https://t.me/dhsaidqhndi/368",
        "80-qism": "https://t.me/dhsaidqhndi/369",
        "81-qism": "https://t.me/dhsaidqhndi/370",
        "82-qism": "https://t.me/dhsaidqhndi/371",
        "83-qism": "https://t.me/dhsaidqhndi/372",
        "84-qism": "https://t.me/dhsaidqhndi/373",
        "85-qism": "https://t.me/dhsaidqhndi/374",
        "86-qism": "https://t.me/dhsaidqhndi/375",
        "87-qism": "https://t.me/dhsaidqhndi/376",
        "88-qism": "https://t.me/dhsaidqhndi/377",
        "89-qism": "https://t.me/dhsaidqhndi/378",
        "90-qism": "https://t.me/dhsaidqhndi/379",
        "91-qism": "https://t.me/dhsaidqhndi/380",
        "92-qism": "https://t.me/dhsaidqhndi/381",
        "93-qism": "https://t.me/dhsaidqhndi/382",
        "94-qism": "https://t.me/dhsaidqhndi/383",
        "95-qism": "https://t.me/dhsaidqhndi/384",
        "96-qism": "https://t.me/dhsaidqhndi/385",
        "97-qism": "https://t.me/dhsaidqhndi/386",
        "98-qism": "https://t.me/dhsaidqhndi/387",
        "99-qism": "https://t.me/dhsaidqhndi/388",
        "100-qism": "https://t.me/dhsaidqhndi/389",
        "101-qism": "https://t.me/dhsaidqhndi/390",
        "102-qism": "https://t.me/dhsaidqhndi/391",
        "103-qism": "https://t.me/dhsaidqhndi/392",
        "104-qism": "https://t.me/dhsaidqhndi/393",
        "105-qism": "https://t.me/dhsaidqhndi/394",
        "106-qism": "https://t.me/dhsaidqhndi/395",
        "107-qism": "https://t.me/dhsaidqhndi/396",
        "108-qism": "https://t.me/dhsaidqhndi/397",
        "109-qism": "https://t.me/dhsaidqhndi/398",
        "110-qism": "https://t.me/dhsaidqhndi/399",
        "111-qism": "https://t.me/dhsaidqhndi/400",
        "112-qism": "https://t.me/dhsaidqhndi/401",
        "113-qism": "https://t.me/dhsaidqhndi/402",
        "114-qism": "https://t.me/dhsaidqhndi/403",
        "115-qism": "https://t.me/dhsaidqhndi/404",
        "116-qism": "https://t.me/dhsaidqhndi/405",
        "117-qism": "https://t.me/dhsaidqhndi/406",
        "118-qism": "https://t.me/dhsaidqhndi/407",
        "119-qism": "https://t.me/dhsaidqhndi/408",
        "120-qism": "https://t.me/dhsaidqhndi/409",
        "121-qism": "https://t.me/dhsaidqhndi/410",
        "122-qism": "https://t.me/dhsaidqhndi/411",
        "123-qism": "https://t.me/dhsaidqhndi/412",
        "124-qism": "https://t.me/dhsaidqhndi/413",
        "125-qism": "https://t.me/dhsaidqhndi/414",
        "126-qism": "https://t.me/dhsaidqhndi/415",
        "127-qism": "https://t.me/dhsaidqhndi/416",
        "128-qism": "https://t.me/dhsaidqhndi/417",
        "129-qism": "https://t.me/dhsaidqhndi/418",
        "130-qism": "https://t.me/dhsaidqhndi/419",
        "131-qism": "https://t.me/dhsaidqhndi/420",
        "132-qism": "https://t.me/dhsaidqhndi/421",
        "133-qism": "https://t.me/dhsaidqhndi/422",
        "134-qism": "https://t.me/dhsaidqhndi/423",
        "135-qism": "https://t.me/dhsaidqhndi/424",
        "136-qism": "https://t.me/dhsaidqhndi/425",
        "137-qism": "https://t.me/dhsaidqhndi/426",
        "138-qism": "https://t.me/dhsaidqhndi/427",
        "139-qism": "https://t.me/dhsaidqhndi/428",
        "140-qism": "https://t.me/dhsaidqhndi/429",
        "141-qism": "https://t.me/dhsaidqhndi/430",
        "142-qism": "https://t.me/dhsaidqhndi/431",
        "143-qism": "https://t.me/dhsaidqhndi/432",
        "144-qism": "https://t.me/dhsaidqhndi/433",
        "145-qism": "https://t.me/dhsaidqhndi/434",
        "146-qism": "https://t.me/dhsaidqhndi/435",
        "147-qism": "https://t.me/dhsaidqhndi/436",
        "148-qism": "https://t.me/dhsaidqhndi/437",
        "149-qism": "https://t.me/dhsaidqhndi/438",
        "150-qism": "https://t.me/dhsaidqhndi/439",
        "151-qism": "https://t.me/dhsaidqhndi/440",
        "152-qism": "https://t.me/dhsaidqhndi/441",
        "153-qism": "https://t.me/dhsaidqhndi/442",
        "154-qism": "https://t.me/dhsaidqhndi/443",
        "155-qism": "https://t.me/dhsaidqhndi/444",
        "156-qism": "https://t.me/dhsaidqhndi/445",
        "157-qism": "https://t.me/dhsaidqhndi/452",
        "158-qism": "https://t.me/dhsaidqhndi/453",
        "159-qism": "https://t.me/dhsaidqhndi/454",
        "160-qism": "https://t.me/dhsaidqhndi/455",
        "161-qism": "https://t.me/dhsaidqhndi/456",
        "162-qism": "https://t.me/dhsaidqhndi/457",
        "163-qism": "https://t.me/dhsaidqhndi/458",
        "164-qism": "https://t.me/dhsaidqhndi/459",
        "165-qism": "https://t.me/dhsaidqhndi/460",
        "166-qism": "https://t.me/dhsaidqhndi/461",
        "167-qism": "https://t.me/dhsaidqhndi/462",
        "168-qism": "https://t.me/dhsaidqhndi/490",
        "169-qism": "https://t.me/dhsaidqhndi/921",
        "170-qism": "https://t.me/dhsaidqhndi/1258",
        "171-qism": "https://t.me/dhsaidqhndi/1259",
        "172-qism": "https://t.me/dhsaidqhndi/2123",
        "173-qism": "https://t.me/dhsaidqhndi/2417",
        "174-qism": "https://t.me/dhsaidqhndi/2418",
        "175-qism": "https://t.me/dhsaidqhndi/2419",
        "176-qism": "https://t.me/dhsaidqhndi/2495",
        "177-qism": "https://t.me/dhsaidqhndi/2540",
        "178-qism": "https://t.me/dhsaidqhndi/2611",
        "179-qism": "https://t.me/dhsaidqhndi/2621",
    }
}

# ==================== ZULMATDAGI YULDUZ ====================
# 🎥 ZULMATDAGI YULDUZ — Asosiy menyu
@dp.message(F.text == "ZULMATDAGI YULDUZ")
async def zulmatdagi_yulduz_handler(message: types.Message):
    await message.answer(
        "👑 *Zulmatdagi Yulduz* qismlarini tanlang:",
        reply_markup=get_yulduz_page_keyboard(1),
        parse_mode="Markdown"
    )


# 📄 Sahifa almashtirish (pagination)
@dp.callback_query(F.data.regexp(r"^yulduz_page_\d+$"))
async def change_yulduz_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_yulduz_page_keyboard(page))
    await callback.answer()


# 🎬 Video yuborish (ma’lumotli tarzda)
@dp.callback_query(F.data.regexp(r"^zulmatdagi_yulduz_\d+$"))
async def send_yulduz_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = yulduz_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> Zulmatdagi Yulduz\n"
        "───────────────\n"
        f"🎞 <b>Janr:</b> Fantastika, Robot, Jangovar, Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (Uzdubgo)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @Uzdubgo | @bananatv_uz\n"
        "#taxt_muhri_animania\n\n"
        "💬 “Taxt — kuch, kuch esa mas’uliyat. Haqiqiy shoh yuragida rahm bilan hukm yuritadi.” ⚔️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

# 🔘 Sahifalangan tugmalar — 20 ta per page
def get_yulduz_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20  # Har sahifada 20 ta qism chiqadi
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(yulduz_videolar.keys())[start:end]

    buttons = []
    for i, key in enumerate(keys, start=start):
        buttons.append([
            InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"zulmatdagi_yulduz_{i+1}")
        ])

    # Navigatsiya tugmalari
    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"yulduz_page_{page-1}"))
    if end < len(yulduz_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"yulduz_page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Zulmatdagi Yulduz videolar ro'yxati
yulduz_videolar = {
    "zulmatdagi_yulduz_1": "https://t.me/dhsaidqhndi/966",
    "zulmatdagi_yulduz_2": "https://t.me/dhsaidqhndi/967",
    "zulmatdagi_yulduz_3": "https://t.me/dhsaidqhndi/968",
    "zulmatdagi_yulduz_4": "https://t.me/dhsaidqhndi/969",
    "zulmatdagi_yulduz_5": "https://t.me/dhsaidqhndi/970",
    "zulmatdagi_yulduz_6": "https://t.me/dhsaidqhndi/971", 
    "zulmatdagi_yulduz_7": "https://t.me/dhsaidqhndi/972",
    "zulmatdagi_yulduz_8": "https://t.me/dhsaidqhndi/973",
    "zulmatdagi_yulduz_9": "https://t.me/dhsaidqhndi/974",
    "zulmatdagi_yulduz_10": "https://t.me/dhsaidqhndi/975",
    "zulmatdagi_yulduz_11": "https://t.me/dhsaidqhndi/976", 
    "zulmatdagi_yulduz_12": "https://t.me/dhsaidqhndi/977",
    "zulmatdagi_yulduz_13": "https://t.me/dhsaidqhndi/978",
    "zulmatdagi_yulduz_14": "https://t.me/dhsaidqhndi/979",
    "zulmatdagi_yulduz_15": "https://t.me/dhsaidqhndi/980",
    "zulmatdagi_yulduz_16": "https://t.me/dhsaidqhndi/981",
    "zulmatdagi_yulduz_17": "https://t.me/dhsaidqhndi/982",
    "zulmatdagi_yulduz_18": "https://t.me/dhsaidqhndi/983",
    "zulmatdagi_yulduz_19": "https://t.me/dhsaidqhndi/984",
    "zulmatdagi_yulduz_20": "https://t.me/dhsaidqhndi/985",
    "zulmatdagi_yulduz_21": "https://t.me/dhsaidqhndi/986",
    "zulmatdagi_yulduz_22": "https://t.me/dhsaidqhndi/987",
    "zulmatdagi_yulduz_23": "https://t.me/dhsaidqhndi/988",
    "zulmatdagi_yulduz_24": "https://t.me/dhsaidqhndi/989",
    "zulmatdagi_yulduz_25": "https://t.me/dhsaidqhndi/990",
    "zulmatdagi_yulduz_26": "https://t.me/dhsaidqhndi/991",
    "zulmatdagi_yulduz_27": "https://t.me/dhsaidqhndi/992",
    "zulmatdagi_yulduz_28": "https://t.me/dhsaidqhndi/1093",
    "zulmatdagi_yulduz_29": "https://t.me/dhsaidqhndi/1094",
    "zulmatdagi_yulduz_30": "https://t.me/dhsaidqhndi/1095",
    "zulmatdagi_yulduz_31": "https://t.me/dhsaidqhndi/1096",
    "zulmatdagi_yulduz_32": "https://t.me/dhsaidqhndi/1097",
    "zulmatdagi_yulduz_33": "https://t.me/dhsaidqhndi/1098",
    "zulmatdagi_yulduz_34": "https://t.me/dhsaidqhndi/1099",
    "zulmatdagi_yulduz_35": "https://t.me/dhsaidqhndi/1100",
    "zulmatdagi_yulduz_36": "https://t.me/dhsaidqhndi/1101",
    "zulmatdagi_yulduz_37": "https://t.me/dhsaidqhndi/1102",
    "zulmatdagi_yulduz_38": "https://t.me/dhsaidqhndi/1103",
    "zulmatdagi_yulduz_39": "https://t.me/dhsaidqhndi/1104",
    "zulmatdagi_yulduz_40": "https://t.me/dhsaidqhndi/1105",
    "zulmatdagi_yulduz_41": "https://t.me/dhsaidqhndi/1106",
    "zulmatdagi_yulduz_42": "https://t.me/dhsaidqhndi/1107",
    "zulmatdagi_yulduz_43": "https://t.me/dhsaidqhndi/1108",
    "zulmatdagi_yulduz_44": "https://t.me/dhsaidqhndi/1109",
    "zulmatdagi_yulduz_45": "https://t.me/dhsaidqhndi/1110",
    "zulmatdagi_yulduz_46": "https://t.me/dhsaidqhndi/1111",
    "zulmatdagi_yulduz_47": "https://t.me/dhsaidqhndi/1112",
    "zulmatdagi_yulduz_48": "https://t.me/dhsaidqhndi/1113",
    "zulmatdagi_yulduz_49": "https://t.me/dhsaidqhndi/1114",
    "zulmatdagi_yulduz_50": "https://t.me/dhsaidqhndi/1115",
    "zulmatdagi_yulduz_51": "https://t.me/dhsaidqhndi/1116",
    "zulmatdagi_yulduz_52": "https://t.me/dhsaidqhndi/1117",
    "zulmatdagi_yulduz_53": "https://t.me/dhsaidqhndi/1118",
    "zulmatdagi_yulduz_54": "https://t.me/dhsaidqhndi/1119",
    "zulmatdagi_yulduz_55": "https://t.me/dhsaidqhndi/1120",
    "zulmatdagi_yulduz_56": "https://t.me/dhsaidqhndi/1121",
    "zulmatdagi_yulduz_57": "https://t.me/dhsaidqhndi/1122",
    "zulmatdagi_yulduz_58": "https://t.me/dhsaidqhndi/1123",
    "zulmatdagi_yulduz_59": "https://t.me/dhsaidqhndi/1124",
    "zulmatdagi_yulduz_60": "https://t.me/dhsaidqhndi/1125",
    "zulmatdagi_yulduz_61": "https://t.me/dhsaidqhndi/1126",
    "zulmatdagi_yulduz_62": "https://t.me/dhsaidqhndi/1127",
    "zulmatdagi_yulduz_63": "https://t.me/dhsaidqhndi/1128",
    "zulmatdagi_yulduz_64": "https://t.me/dhsaidqhndi/1129",
    "zulmatdagi_yulduz_65": "https://t.me/dhsaidqhndi/1130",
    "zulmatdagi_yulduz_66": "https://t.me/dhsaidqhndi/1131",
    "zulmatdagi_yulduz_67": "https://t.me/dhsaidqhndi/1132",
    "zulmatdagi_yulduz_68": "https://t.me/dhsaidqhndi/1133",
    "zulmatdagi_yulduz_69": "https://t.me/dhsaidqhndi/1134",
    "zulmatdagi_yulduz_70": "https://t.me/dhsaidqhndi/1135",
    "zulmatdagi_yulduz_71": "https://t.me/dhsaidqhndi/1136",
    "zulmatdagi_yulduz_72": "https://t.me/dhsaidqhndi/1137",
    "zulmatdagi_yulduz_73": "https://t.me/dhsaidqhndi/1138",
    "zulmatdagi_yulduz_74": "https://t.me/dhsaidqhndi/1139",
    "zulmatdagi_yulduz_75": "https://t.me/dhsaidqhndi/1140",
    "zulmatdagi_yulduz_76": "https://t.me/dhsaidqhndi/1141",
    "zulmatdagi_yulduz_77": "https://t.me/dhsaidqhndi/1142",
    "zulmatdagi_yulduz_78": "https://t.me/dhsaidqhndi/1143",
    "zulmatdagi_yulduz_79": "https://t.me/dhsaidqhndi/1144",
    "zulmatdagi_yulduz_80": "https://t.me/dhsaidqhndi/1145",
    "zulmatdagi_yulduz_81": "https://t.me/dhsaidqhndi/1146",
    "zulmatdagi_yulduz_82": "https://t.me/dhsaidqhndi/1147",
    "zulmatdagi_yulduz_83": "https://t.me/dhsaidqhndi/1148",
    "zulmatdagi_yulduz_84": "https://t.me/dhsaidqhndi/1149",
    "zulmatdagi_yulduz_85": "https://t.me/dhsaidqhndi/1150",
    "zulmatdagi_yulduz_86": "https://t.me/dhsaidqhndi/1151",
    "zulmatdagi_yulduz_87": "https://t.me/dhsaidqhndi/1152",
    "zulmatdagi_yulduz_88": "https://t.me/dhsaidqhndi/1153",
    "zulmatdagi_yulduz_89": "https://t.me/dhsaidqhndi/1154",
    "zulmatdagi_yulduz_90": "https://t.me/dhsaidqhndi/1155",
    "zulmatdagi_yulduz_91": "https://t.me/dhsaidqhndi/1156",
    "zulmatdagi_yulduz_92": "https://t.me/dhsaidqhndi/1157",
    "zulmatdagi_yulduz_93": "https://t.me/dhsaidqhndi/1158",
    "zulmatdagi_yulduz_94": "https://t.me/dhsaidqhndi/1159",
    "zulmatdagi_yulduz_95": "https://t.me/dhsaidqhndi/1160",
    "zulmatdagi_yulduz_96": "https://t.me/dhsaidqhndi/1161",
    "zulmatdagi_yulduz_97": "https://t.me/dhsaidqhndi/1162",
    "zulmatdagi_yulduz_98": "https://t.me/dhsaidqhndi/1163",
    "zulmatdagi_yulduz_99": "https://t.me/dhsaidqhndi/1164",
    "zulmatdagi_yulduz_100": "https://t.me/dhsaidqhndi/1165",
    "zulmatdagi_yulduz_101": "https://t.me/dhsaidqhndi/1166",
    "zulmatdagi_yulduz_102": "https://t.me/dhsaidqhndi/1167",
    "zulmatdagi_yulduz_103": "https://t.me/dhsaidqhndi/1168",
    "zulmatdagi_yulduz_104": "https://t.me/dhsaidqhndi/1169",
    "zulmatdagi_yulduz_105": "https://t.me/dhsaidqhndi/1170",
    "zulmatdagi_yulduz_106": "https://t.me/dhsaidqhndi/1171",
    "zulmatdagi_yulduz_107": "https://t.me/dhsaidqhndi/1172",
    "zulmatdagi_yulduz_108": "https://t.me/dhsaidqhndi/1173",
    "zulmatdagi_yulduz_109": "https://t.me/dhsaidqhndi/1174",
    "zulmatdagi_yulduz_110": "https://t.me/dhsaidqhndi/1175",
    "zulmatdagi_yulduz_111": "https://t.me/dhsaidqhndi/1176",
    "zulmatdagi_yulduz_112": "https://t.me/dhsaidqhndi/1177",
    "zulmatdagi_yulduz_113": "https://t.me/dhsaidqhndi/1178",
    "zulmatdagi_yulduz_114": "https://t.me/dhsaidqhndi/1179",
    "zulmatdagi_yulduz_115": "https://t.me/dhsaidqhndi/1180",
    "zulmatdagi_yulduz_116": "https://t.me/dhsaidqhndi/1181",
    "zulmatdagi_yulduz_117": "https://t.me/dhsaidqhndi/1182",
    "zulmatdagi_yulduz_118": "https://t.me/dhsaidqhndi/1183",
    "zulmatdagi_yulduz_119": "https://t.me/dhsaidqhndi/1184",
    "zulmatdagi_yulduz_120": "https://t.me/dhsaidqhndi/1185",
    "zulmatdagi_yulduz_121": "https://t.me/dhsaidqhndi/1186",
    "zulmatdagi_yulduz_122": "https://t.me/dhsaidqhndi/1187",
    "zulmatdagi_yulduz_123": "https://t.me/dhsaidqhndi/1188",
    "zulmatdagi_yulduz_124": "https://t.me/dhsaidqhndi/1189",
    "zulmatdagi_yulduz_125": "https://t.me/dhsaidqhndi/1190",
    "zulmatdagi_yulduz_126": "https://t.me/dhsaidqhndi/1191",
    "zulmatdagi_yulduz_127": "https://t.me/dhsaidqhndi/1192",
    "zulmatdagi_yulduz_128": "https://t.me/dhsaidqhndi/1193",
    "zulmatdagi_yulduz_129": "https://t.me/dhsaidqhndi/1194",
    "zulmatdagi_yulduz_130": "https://t.me/dhsaidqhndi/1195",
    "zulmatdagi_yulduz_131": "https://t.me/dhsaidqhndi/1196",
    "zulmatdagi_yulduz_132": "https://t.me/dhsaidqhndi/1197",
    "zulmatdagi_yulduz_133": "https://t.me/dhsaidqhndi/1198",
    "zulmatdagi_yulduz_134": "https://t.me/dhsaidqhndi/1199",
    "zulmatdagi_yulduz_135": "https://t.me/dhsaidqhndi/1200",
    "zulmatdagi_yulduz_136": "https://t.me/dhsaidqhndi/1201",
    "zulmatdagi_yulduz_137": "https://t.me/dhsaidqhndi/1202",
    "zulmatdagi_yulduz_138": "https://t.me/dhsaidqhndi/1203",
    "zulmatdagi_yulduz_139": "https://t.me/dhsaidqhndi/1204",
    "zulmatdagi_yulduz_140": "https://t.me/dhsaidqhndi/1205",
    "zulmatdagi_yulduz_141": "https://t.me/dhsaidqhndi/1206",
    "zulmatdagi_yulduz_142": "https://t.me/dhsaidqhndi/1207",
    "zulmatdagi_yulduz_143": "https://t.me/dhsaidqhndi/1208",
    "zulmatdagi_yulduz_144": "https://t.me/dhsaidqhndi/1209",
    "zulmatdagi_yulduz_145": "https://t.me/dhsaidqhndi/1210",
    "zulmatdagi_yulduz_146": "https://t.me/dhsaidqhndi/1211",
    "zulmatdagi_yulduz_147": "https://t.me/dhsaidqhndi/1212",
    "zulmatdagi_yulduz_148": "https://t.me/dhsaidqhndi/1213",
    "zulmatdagi_yulduz_149": "https://t.me/dhsaidqhndi/1214",
    "zulmatdagi_yulduz_150": "https://t.me/dhsaidqhndi/1215",
    "zulmatdagi_yulduz_151": "https://t.me/dhsaidqhndi/1216",
    "zulmatdagi_yulduz_152": "https://t.me/dhsaidqhndi/1217",
    "zulmatdagi_yulduz_153": "https://t.me/dhsaidqhndi/1218",
    "zulmatdagi_yulduz_154": "https://t.me/dhsaidqhndi/1219",
    "zulmatdagi_yulduz_155": "https://t.me/dhsaidqhndi/1220",
    "zulmatdagi_yulduz_156": "https://t.me/dhsaidqhndi/1221",
    "zulmatdagi_yulduz_157": "https://t.me/dhsaidqhndi/1222",
    "zulmatdagi_yulduz_158": "https://t.me/dhsaidqhndi/1223",
    "zulmatdagi_yulduz_159": "https://t.me/dhsaidqhndi/1224",
    "zulmatdagi_yulduz_160": "https://t.me/dhsaidqhndi/1225",
    "zulmatdagi_yulduz_161": "https://t.me/dhsaidqhndi/1226",
    "zulmatdagi_yulduz_162": "https://t.me/dhsaidqhndi/1227",
    "zulmatdagi_yulduz_163": "https://t.me/dhsaidqhndi/1228",
    "zulmatdagi_yulduz_164": "https://t.me/dhsaidqhndi/1229",
    "zulmatdagi_yulduz_165": "https://t.me/dhsaidqhndi/1230",
    "zulmatdagi_yulduz_166": "https://t.me/dhsaidqhndi/1231",
    "zulmatdagi_yulduz_167": "https://t.me/dhsaidqhndi/1232",
    "zulmatdagi_yulduz_168": "https://t.me/dhsaidqhndi/1233",
    "zulmatdagi_yulduz_169": "https://t.me/dhsaidqhndi/1234",
    "zulmatdagi_yulduz_170": "https://t.me/dhsaidqhndi/1235",
    "zulmatdagi_yulduz_171": "https://t.me/dhsaidqhndi/1236",
    "zulmatdagi_yulduz_172": "https://t.me/dhsaidqhndi/1237",
    "zulmatdagi_yulduz_173": "https://t.me/dhsaidqhndi/1238",
    "zulmatdagi_yulduz_174": "https://t.me/dhsaidqhndi/1239",
    "zulmatdagi_yulduz_175": "https://t.me/dhsaidqhndi/1240",
    "zulmatdagi_yulduz_176": "https://t.me/dhsaidqhndi/1241",
    "zulmatdagi_yulduz_177": "https://t.me/dhsaidqhndi/1242",
    "zulmatdagi_yulduz_178": "https://t.me/dhsaidqhndi/1243",
    "zulmatdagi_yulduz_179": "https://t.me/dhsaidqhndi/1244",
    "zulmatdagi_yulduz_180": "https://t.me/dhsaidqhndi/1245",
    "zulmatdagi_yulduz_181": "https://t.me/dhsaidqhndi/1246",
    "zulmatdagi_yulduz_182": "https://t.me/dhsaidqhndi/1247",
    "zulmatdagi_yulduz_183": "https://t.me/dhsaidqhndi/1248",
    "zulmatdagi_yulduz_184": "https://t.me/dhsaidqhndi/1249",
    "zulmatdagi_yulduz_185": "https://t.me/dhsaidqhndi/1250",
    "zulmatdagi_yulduz_186": "https://t.me/dhsaidqhndi/1251",
    "zulmatdagi_yulduz_187": "https://t.me/dhsaidqhndi/1252",
    "zulmatdagi_yulduz_188": "https://t.me/dhsaidqhndi/1253",
    "zulmatdagi_yulduz_189": "https://t.me/dhsaidqhndi/1254",
    "zulmatdagi_yulduz_190": "https://t.me/dhsaidqhndi/1255",
    "zulmatdagi_yulduz_191": "https://t.me/dhsaidqhndi/2127",
    "zulmatdagi_yulduz_192": "https://t.me/dhsaidqhndi/2253",
    "zulmatdagi_yulduz_193": "https://t.me/dhsaidqhndi/2355",
    "zulmatdagi_yulduz_194": "https://t.me/dhsaidqhndi/2356",
    "zulmatdagi_yulduz_195": "https://t.me/dhsaidqhndi/2360",
    "zulmatdagi_yulduz_196": "https://t.me/dhsaidqhndi/2362",
    "zulmatdagi_yulduz_197": "https://t.me/dhsaidqhndi/2371",
    "zulmatdagi_yulduz_198": "https://t.me/dhsaidqhndi/2372",
    "zulmatdagi_yulduz_199": "https://t.me/dhsaidqhndi/2471",
    "zulmatdagi_yulduz_200": "https://t.me/dhsaidqhndi/2472",
    "zulmatdagi_yulduz_201": "https://t.me/dhsaidqhndi/2509",
    "zulmatdagi_yulduz_202": "https://t.me/dhsaidqhndi/2608",
}

# ==================== HUKUMDORLAR YO‘LI ====================
# ⚔️ HUKUMDORLAR YO‘LI menyusi
@dp.message(F.text == "HUKUMDORLAR YULI")
async def hukmdorlar_menu(message: types.Message):
    fasllar = list(hukmdorlar_videolar.keys())
    buttons = [
        [InlineKeyboardButton(text=fasl, callback_data=f"hukmdor_fasl_{fasl}")]
        for fasl in fasllar
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("⚔️ Hukumdorlar Yo‘li faslini tanlang:", reply_markup=keyboard)


# 🔹 FASL TANLANGANDA
@dp.callback_query(F.data.startswith("hukmdor_fasl_"))
async def hukmdor_fasl_tanlandi(callback: types.CallbackQuery):
    fasl = callback.data.replace("hukmdor_fasl_", "")
    await callback.message.edit_text(
        f"⚔️ Hukumdorlar Yo‘li — {fasl}\n\nQuyidagi qismlardan birini tanlang 👇",
        reply_markup=generate_hukmdor_keyboard(fasl, 1)
    )


# 🔹 SAHIFALASH FUNKSIYASI (orqaga tugmasi bilan)
def generate_hukmdor_keyboard(fasl: str, page: int = 1):
    per_page = 20
    all_items = list(hukmdorlar_videolar[fasl].items())
    start = (page - 1) * per_page
    end = start + per_page
    items = all_items[start:end]

    keyboard = []
    for name, url in items:
        keyboard.append([InlineKeyboardButton(text=name, callback_data=f"hukmdor_video_{fasl}:{name}")])

    nav_buttons = []
    if start > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"hukmdor_page_{fasl}_{page-1}"))
    if end < len(all_items):
        nav_buttons.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"hukmdor_page_{fasl}_{page+1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)

    # 🔙 Orqaga (fasllarga qaytish)
    keyboard.append([InlineKeyboardButton(text="🔙 Fasllarga qaytish", callback_data="hukmdor_back_fasllar")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# 🔹 SAHIFA ALMASHTIRILGANDA
@dp.callback_query(F.data.startswith("hukmdor_page_"))
async def hukmdor_page(callback: types.CallbackQuery):
    data = callback.data[len("hukmdor_page_"):]
    fasl, page_str = data.rsplit("_", 1)
    page = int(page_str)

    await callback.message.edit_text(
        f"⚔️ Hukumdorlar Yo‘li — {fasl}\n\nQuyidagi qismlardan birini tanlang 👇",
        reply_markup=generate_hukmdor_keyboard(fasl, page)
    )


# 🔙 FASLLARGA QAYTISH
@dp.callback_query(F.data == "hukmdor_back_fasllar")
async def hukmdor_back_to_fasllar(callback: types.CallbackQuery):
    fasllar = list(hukmdorlar_videolar.keys())
    buttons = [
        [InlineKeyboardButton(text=fasl, callback_data=f"hukmdor_fasl_{fasl}")]
        for fasl in fasllar
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text("⚔️ Hukumdorlar Yo‘li faslini tanlang:", reply_markup=keyboard)


# 🔹 VIDEO YUBORISH
@dp.callback_query(F.data.startswith("hukmdor_video_"))
async def hukmdor_video_yubor(callback: types.CallbackQuery):
    data = callback.data[len("hukmdor_video_"):]
    if ":" not in data:
        await callback.answer("❌ Xato formatdagi video identifikator!", show_alert=True)
        return

    fasl, qism = data.split(":", 1)

    if fasl not in hukmdorlar_videolar or qism not in hukmdorlar_videolar[fasl]:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    video_link = hukmdorlar_videolar[fasl][qism]

    caption = (
        f"🎬 <b>Nomi:</b> Hukumdorlar Yo‘li\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Jang, Sarguzasht\n"
        f"📺 <b>Fasl:</b> {fasl}\n"
        f"🎞 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniManhwa3D)\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniManhwa3D</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D\n"
        "#hukmdorlar_yuli\n\n"
        "💬 “Faqat eng qat’iy yuraklar taqdir yo‘lini o‘zgartira oladi.” ⚔️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

    await callback.answer()

# Hukumdorlar Yuli videolar ro'yxati:
hukmdorlar_videolar = {
    "1-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/1362",
        "2-qism": "https://t.me/dhsaidqhndi/1363",
        "3-qism": "https://t.me/dhsaidqhndi/1364",
        "4-qism": "https://t.me/dhsaidqhndi/1365",
        "5-qism": "https://t.me/dhsaidqhndi/1366",
        "6-qism": "https://t.me/dhsaidqhndi/1367",
        "7-qism": "https://t.me/dhsaidqhndi/1368",
        "8-qism": "https://t.me/dhsaidqhndi/1369",
        "9-qism": "https://t.me/dhsaidqhndi/1370",
        "10-qism": "https://t.me/dhsaidqhndi/1371",
        "11-qism": "https://t.me/dhsaidqhndi/1372",
        "12-qism": "https://t.me/dhsaidqhndi/1373",
        "13-qism": "https://t.me/dhsaidqhndi/1374",
        "14-qism": "https://t.me/dhsaidqhndi/1375",
        "15-qism": "https://t.me/dhsaidqhndi/1376",
        "16-qism": "https://t.me/dhsaidqhndi/1377",
        "17-qism": "https://t.me/dhsaidqhndi/1418",
        "18-qism": "https://t.me/dhsaidqhndi/1378",
        "19-qism": "https://t.me/dhsaidqhndi/1379",
        "20-qism": "https://t.me/dhsaidqhndi/1380",
        "21-qism": "https://t.me/dhsaidqhndi/1381",
        "22-qism": "https://t.me/dhsaidqhndi/1382",
        "23-qism": "https://t.me/dhsaidqhndi/1383",
        "24-qism": "https://t.me/dhsaidqhndi/1384",
        "25-qism": "https://t.me/dhsaidqhndi/1385",
        "26-qism": "https://t.me/dhsaidqhndi/1386",
        "27-qism": "https://t.me/dhsaidqhndi/1387",
        "28-qism": "https://t.me/dhsaidqhndi/1388",
        "29-qism": "https://t.me/dhsaidqhndi/1389",
        "30-qism": "https://t.me/dhsaidqhndi/1390",
        "31-qism": "https://t.me/dhsaidqhndi/1391",
        "32-qism": "https://t.me/dhsaidqhndi/1392",
        "33-qism": "https://t.me/dhsaidqhndi/1393",
        "34-qism": "https://t.me/dhsaidqhndi/1394",
        "35-qism": "https://t.me/dhsaidqhndi/1395",
        "36-qism": "https://t.me/dhsaidqhndi/1396",
        "37-qism": "https://t.me/dhsaidqhndi/1397",
        "38-qism": "https://t.me/dhsaidqhndi/1398",
        "39-qism": "https://t.me/dhsaidqhndi/1399",
        "40-qism": "https://t.me/dhsaidqhndi/1400",
        "41-qism": "https://t.me/dhsaidqhndi/1401",
        "42-qism": "https://t.me/dhsaidqhndi/1402",
        "43-qism": "https://t.me/dhsaidqhndi/1403",
        "44-qism": "https://t.me/dhsaidqhndi/1404",
        "45-qism": "https://t.me/dhsaidqhndi/1405",
        "46-qism": "https://t.me/dhsaidqhndi/1406",
        "47-qism": "https://t.me/dhsaidqhndi/1407",
        "48-qism": "https://t.me/dhsaidqhndi/1408",
        "49-qism": "https://t.me/dhsaidqhndi/1409",
        "50-qism": "https://t.me/dhsaidqhndi/1410",
        "51-qism": "https://t.me/dhsaidqhndi/1411",
        "52-qism": "https://t.me/dhsaidqhndi/1412",
    },

    "2-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/1413",
        "2-qism": "https://t.me/dhsaidqhndi/1414",
        "3-qism": "https://t.me/dhsaidqhndi/1415",
        "4-qism": "https://t.me/dhsaidqhndi/1416",
        "5-qism": "https://t.me/dhsaidqhndi/1417",
        "6-qism": "https://t.me/dhsaidqhndi/1907",
        "7-qism": "https://t.me/dhsaidqhndi/1909",
        "8-qism": "https://t.me/dhsaidqhndi/2241",
        "9-qism": "https://t.me/dhsaidqhndi/2315",
        "10-qism": "https://t.me/dhsaidqhndi/2373",
        "11-qism": "https://t.me/dhsaidqhndi/2405",
        "12-qism": "https://t.me/dhsaidqhndi/2515",
        "13-qism": "https://t.me/dhsaidqhndi/2516",
        "14-qism": "https://t.me/dhsaidqhndi/2520",
        "15-qism": "https://t.me/dhsaidqhndi/2521",
        "16-qism": "https://t.me/dhsaidqhndi/2522",
        "17-qism": "https://t.me/dhsaidqhndi/2525",
        "18-qism": "https://t.me/dhsaidqhndi/2526",
        "19-qism": "https://t.me/dhsaidqhndi/2539",
        "20-qism": "https://t.me/dhsaidqhndi/2632",
        "21-qism": "https://t.me/dhsaidqhndi/2633",
    }
}

# ==================== OLOV JANG USTASI ====================
@dp.message(F.text == "OLOV JANG USTASI")
async def olov_jang_ustasi_handler(message: types.Message):
    await message.answer(
        "🔥 *Olov Jang Ustasi* qismlarini tanlang:",
        reply_markup=get_olov_page_keyboard(1),
        parse_mode="Markdown"
    )

# 📄 Sahifa almashtirish (pagination)
@dp.callback_query(F.data.regexp(r"^olov_page_\d+$"))
async def change_olov_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_olov_page_keyboard(page))
    await callback.answer()

# 🎬 Video yuborish
@dp.callback_query(F.data.regexp(r"^olov_qism_\d+$"))
async def send_olov_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = olov_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🔥 <b>Nomi:</b> Olov Jang Ustasi\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Sehrli, Jangovar\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniManhwa3D)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "#olov_jang_ustasi_animania\n\n"
        "💬 “Har bir olovning markazida yurak bor — kuchni his et, nazorat qil va yondir.” 🔥"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

# 🔘 Sahifalangan tugmalar
def get_olov_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 10  # har sahifada 10 qism
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(olov_videolar.keys())[start:end]

    buttons = []
    for key in keys:
        qism_raqami = key.split("_")[-1]
        buttons.append([InlineKeyboardButton(
            text=f"🎬 {qism_raqami}-qism",
            callback_data=key
        )])

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"olov_page_{page-1}"))
    if end < len(olov_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"olov_page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Olov Jang Ustasi videolar ro'yxati:
olov_videolar = {
    "olov_qism_1": "https://t.me/dhsaidqhndi/1464",
    "olov_qism_2": "https://t.me/dhsaidqhndi/1465",
    "olov_qism_3": "https://t.me/dhsaidqhndi/1466",
    "olov_qism_4": "https://t.me/dhsaidqhndi/1467",
    "olov_qism_5": "https://t.me/dhsaidqhndi/1468",
    "olov_qism_6": "https://t.me/dhsaidqhndi/1469",
    "olov_qism_7": "https://t.me/dhsaidqhndi/1470",
    "olov_qism_8": "https://t.me/dhsaidqhndi/1471",
    "olov_qism_9": "https://t.me/dhsaidqhndi/1472",
    "olov_qism_10": "https://t.me/dhsaidqhndi/1473",
    "olov_qism_11": "https://t.me/dhsaidqhndi/1474",
    "olov_qism_12": "https://t.me/dhsaidqhndi/1475",
    "olov_qism_13": "https://t.me/dhsaidqhndi/1476",
    "olov_qism_14": "https://t.me/dhsaidqhndi/1477",
    "olov_qism_15": "https://t.me/dhsaidqhndi/1478",
    "olov_qism_16": "https://t.me/dhsaidqhndi/1479",
    "olov_qism_17": "https://t.me/dhsaidqhndi/1480",
    "olov_qism_18": "https://t.me/dhsaidqhndi/1481",
    "olov_qism_19": "https://t.me/dhsaidqhndi/1482",
    "olov_qism_20": "https://t.me/dhsaidqhndi/1483",
    "olov_qism_21": "https://t.me/dhsaidqhndi/1484",
    "olov_qism_22": "https://t.me/dhsaidqhndi/1485",
    "olov_qism_23": "https://t.me/dhsaidqhndi/1486",
    "olov_qism_24": "https://t.me/dhsaidqhndi/1487",
    "olov_qism_25": "https://t.me/dhsaidqhndi/1488",
    "olov_qism_26": "https://t.me/dhsaidqhndi/1489",
    "olov_qism_27": "https://t.me/dhsaidqhndi/1490",
    "olov_qism_28": "https://t.me/dhsaidqhndi/1491",
    "olov_qism_29": "https://t.me/dhsaidqhndi/1492",
    "olov_qism_30": "https://t.me/dhsaidqhndi/1493",
    "olov_qism_31": "https://t.me/dhsaidqhndi/1494",
    "olov_qism_32": "https://t.me/dhsaidqhndi/1495",
    "olov_qism_33": "https://t.me/dhsaidqhndi/1496",
    "olov_qism_34": "https://t.me/dhsaidqhndi/1497",
    "olov_qism_35": "https://t.me/dhsaidqhndi/1498",
    "olov_qism_36": "https://t.me/dhsaidqhndi/1499",
    "olov_qism_37": "https://t.me/dhsaidqhndi/1500",
    "olov_qism_38": "https://t.me/dhsaidqhndi/1501",
    "olov_qism_39": "https://t.me/dhsaidqhndi/1502",
    "olov_qism_40": "https://t.me/dhsaidqhndi/1503",
    "olov_qism_41": "https://t.me/dhsaidqhndi/1504",
    "olov_qism_42": "https://t.me/dhsaidqhndi/1505",
    "olov_qism_43": "https://t.me/dhsaidqhndi/1506",
    "olov_qism_44": "https://t.me/dhsaidqhndi/1507",
    "olov_qism_45": "https://t.me/dhsaidqhndi/1508",
    "olov_qism_46": "https://t.me/dhsaidqhndi/1509",
    "olov_qism_47": "https://t.me/dhsaidqhndi/1510",
    "olov_qism_48": "https://t.me/dhsaidqhndi/1511",
    "olov_qism_49": "https://t.me/dhsaidqhndi/1512",
    "olov_qism_50": "https://t.me/dhsaidqhndi/1513",
    "olov_qism_51": "https://t.me/dhsaidqhndi/1514",
    "olov_qism_52": "https://t.me/dhsaidqhndi/1515",
    "olov_qism_53": "https://t.me/dhsaidqhndi/1516",
    "olov_qism_54": "https://t.me/dhsaidqhndi/1517",
    "olov_qism_55": "https://t.me/dhsaidqhndi/1518",
    "olov_qism_56": "https://t.me/dhsaidqhndi/1519",
    "olov_qism_57": "https://t.me/dhsaidqhndi/1520",
    "olov_qism_58": "https://t.me/dhsaidqhndi/1521",
    "olov_qism_59": "https://t.me/dhsaidqhndi/1522",
    "olov_qism_60": "https://t.me/dhsaidqhndi/1523",
    "olov_qism_61": "https://t.me/dhsaidqhndi/1524",
    "olov_qism_62": "https://t.me/dhsaidqhndi/1525",
    "olov_qism_63": "https://t.me/dhsaidqhndi/1526",
    "olov_qism_64": "https://t.me/dhsaidqhndi/1527",
    "olov_qism_65": "https://t.me/dhsaidqhndi/1528",
    "olov_qism_66": "https://t.me/dhsaidqhndi/1529",
    "olov_qism_67": "https://t.me/dhsaidqhndi/1530",
    "olov_qism_68": "https://t.me/dhsaidqhndi/1531",
    "olov_qism_69": "https://t.me/dhsaidqhndi/1532",
    "olov_qism_70": "https://t.me/dhsaidqhndi/1533",
    "olov_qism_71": "https://t.me/dhsaidqhndi/1534",
    "olov_qism_72": "https://t.me/dhsaidqhndi/1535",
    "olov_qism_73": "https://t.me/dhsaidqhndi/1536",
    "olov_qism_74": "https://t.me/dhsaidqhndi/1537",
    "olov_qism_75": "https://t.me/dhsaidqhndi/1538",
    "olov_qism_76": "https://t.me/dhsaidqhndi/1539",
    "olov_qism_77": "https://t.me/dhsaidqhndi/1540",
    "olov_qism_78": "https://t.me/dhsaidqhndi/1541",
    "olov_qism_79": "https://t.me/dhsaidqhndi/1542",
    "olov_qism_80": "https://t.me/dhsaidqhndi/1543",
    "olov_qism_81": "https://t.me/dhsaidqhndi/1544",
    "olov_qism_82": "https://t.me/dhsaidqhndi/1545",
    "olov_qism_83": "https://t.me/dhsaidqhndi/1546",
    "olov_qism_84": "https://t.me/dhsaidqhndi/1547",
    "olov_qism_85": "https://t.me/dhsaidqhndi/1548",
    "olov_qism_86": "https://t.me/dhsaidqhndi/1549",
    "olov_qism_87": "https://t.me/dhsaidqhndi/1550",
    "olov_qism_88": "https://t.me/dhsaidqhndi/1551",
    "olov_qism_89": "https://t.me/dhsaidqhndi/1552",
    "olov_qism_90": "https://t.me/dhsaidqhndi/1553",
    "olov_qism_91": "https://t.me/dhsaidqhndi/1554",
    "olov_qism_92": "https://t.me/dhsaidqhndi/1555",
    "olov_qism_93": "https://t.me/dhsaidqhndi/1556",
    "olov_qism_94": "https://t.me/dhsaidqhndi/1557",
    "olov_qism_95": "https://t.me/dhsaidqhndi/1558",
    "olov_qism_96": "https://t.me/dhsaidqhndi/1559",
    "olov_qism_97": "https://t.me/dhsaidqhndi/1560",
    "olov_qism_98": "https://t.me/dhsaidqhndi/1561",
    "olov_qism_99": "https://t.me/dhsaidqhndi/1562",
    "olov_qism_100": "https://t.me/dhsaidqhndi/1563",
    "olov_qism_101": "https://t.me/dhsaidqhndi/1564",
    "olov_qism_102": "https://t.me/dhsaidqhndi/1565",
    "olov_qism_103": "https://t.me/dhsaidqhndi/1566",
    "olov_qism_104": "https://t.me/dhsaidqhndi/1567",
    "olov_qism_105": "https://t.me/dhsaidqhndi/1568",
    "olov_qism_106": "https://t.me/dhsaidqhndi/1569",
    "olov_qism_107": "https://t.me/dhsaidqhndi/1570",
    "olov_qism_108": "https://t.me/dhsaidqhndi/1571",
    "olov_qism_109": "https://t.me/dhsaidqhndi/1572",
    "olov_qism_110": "https://t.me/dhsaidqhndi/1573",
    "olov_qism_111": "https://t.me/dhsaidqhndi/1574",
    "olov_qism_112": "https://t.me/dhsaidqhndi/1575",
    "olov_qism_113": "https://t.me/dhsaidqhndi/1576",
    "olov_qism_114": "https://t.me/dhsaidqhndi/1577",
    "olov_qism_115": "https://t.me/dhsaidqhndi/1578",
    "olov_qism_116": "https://t.me/dhsaidqhndi/1579",
    "olov_qism_117": "https://t.me/dhsaidqhndi/1580",
    "olov_qism_118": "https://t.me/dhsaidqhndi/1581",
    "olov_qism_119": "https://t.me/dhsaidqhndi/1582",
    "olov_qism_120": "https://t.me/dhsaidqhndi/1583",
    "olov_qism_121": "https://t.me/dhsaidqhndi/1584",
    "olov_qism_122": "https://t.me/dhsaidqhndi/1585",
    "olov_qism_123": "https://t.me/dhsaidqhndi/1586",
    "olov_qism_124": "https://t.me/dhsaidqhndi/1587",
    "olov_qism_125": "https://t.me/dhsaidqhndi/1588",
    "olov_qism_126": "https://t.me/dhsaidqhndi/1589",
    "olov_qism_127": "https://t.me/dhsaidqhndi/1590",
    "olov_qism_128": "https://t.me/dhsaidqhndi/1591",
    "olov_qism_129": "https://t.me/dhsaidqhndi/1592",
    "olov_qism_130": "https://t.me/dhsaidqhndi/1593",
    "olov_qism_131": "https://t.me/dhsaidqhndi/1594",
    "olov_qism_132": "https://t.me/dhsaidqhndi/1595",
    "olov_qism_133": "https://t.me/dhsaidqhndi/1596",
    "olov_qism_134": "https://t.me/dhsaidqhndi/1597",
    "olov_qism_135": "https://t.me/dhsaidqhndi/1598",
    "olov_qism_136": "https://t.me/dhsaidqhndi/1599",
    "olov_qism_137": "https://t.me/dhsaidqhndi/1600",
    "olov_qism_138": "https://t.me/dhsaidqhndi/1765",
    "olov_qism_139": "https://t.me/dhsaidqhndi/1962",
    "olov_qism_140": "https://t.me/dhsaidqhndi/2242",
    "olov_qism_141": "https://t.me/dhsaidqhndi/2254",
    "olov_qism_142": "https://t.me/dhsaidqhndi/2326",
    "olov_qism_143": "https://t.me/dhsaidqhndi/2402",
    "olov_qism_144": "https://t.me/dhsaidqhndi/2482",
    "olov_qism_145": "https://t.me/dhsaidqhndi/2612",
    "olov_qism_146": "https://t.me/dhsaidqhndi/2613",
    "olov_qism_147": "",
    "olov_qism_148": "",
    "olov_qism_149": "",
    "olov_qism_150": "",
    "olov_qism_151": "",
}

# ==================== SAMODAGI QIRG'IN ====================
@dp.message(F.text == "SAMODAGI QIRG'IN")
async def samodagi_qirgin_handler(message: types.Message):
    await message.answer(
        "👑 *Samodagi Qirg'in* qismlarini tanlang:",
        reply_markup=get_page_samodagi_keyboard(1),
        parse_mode="Markdown"
    )


@dp.callback_query(F.data.regexp(r"^samodagi_page_\d+$"))
async def change_page_samodagi(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(
        reply_markup=get_page_samodagi_keyboard(page)
    )
    await callback.answer()


@dp.callback_query(F.data.regexp(r"^samodagi_\d+$"))
async def send_samodagi_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = samodagi_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[1]

    caption = (
        "🎬 <b>Nomi:</b> SAMODAGI QIRG'IN\n"
        "🎞 <b>Janr:</b> Fantastika | Harakat | Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "📌 <b>Premyera:</b> @AniMania_rasmiy\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniMania_rasmiy | @aust1n_griffin\n"
        "🏷 #samodagi_qirgin_animania\n"
        "───────────────\n"
        "💬 <i>“Faqat jasorat va qat’iyat bilan barcha to‘siqlar yengiladi.”</i> ⚡"
    )

    await bot.send_video(
        callback.from_user.id,
        video_link,
        caption=caption,
        parse_mode="HTML",
        protect_content=True
    )

def get_page_samodagi_keyboard(page: int):
    PER_PAGE = 10
    keys = sorted(samodagi_videolar.keys(), key=lambda x: int(x.split("_")[1]))
    total_pages = (len(keys) + PER_PAGE - 1) // PER_PAGE

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    page_keys = keys[start:end]

    # 🎬 Sahifadagi qismlar tugmalari
    buttons = [
        [InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=key)]
        for i, key in enumerate(page_keys, start=start)
    ]

    # ▶️ Navigatsiya tugmalari
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"samodagi_page_{page-1}"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"samodagi_page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Samodagi Qirg'in videolar ro'yxati:
samodagi_videolar = {
    "samodagi_1": "https://t.me/dhsaidqhndi/2142",
    "samodagi_2": "https://t.me/dhsaidqhndi/2143",
    "samodagi_3": "https://t.me/dhsaidqhndi/2144",
    "samodagi_4": "https://t.me/dhsaidqhndi/2145",
    "samodagi_5": "https://t.me/dhsaidqhndi/2146",
    "samodagi_6": "https://t.me/dhsaidqhndi/2147",
    "samodagi_7": "https://t.me/dhsaidqhndi/2148",
    "samodagi_8": "https://t.me/dhsaidqhndi/2149",
    "samodagi_9": "https://t.me/dhsaidqhndi/2150",
    "samodagi_10": "https://t.me/dhsaidqhndi/2151",
    "samodagi_11": "https://t.me/dhsaidqhndi/2152",
    "samodagi_12": "https://t.me/dhsaidqhndi/2153",
    "samodagi_13": "https://t.me/dhsaidqhndi/2154",
    "samodagi_14": "https://t.me/dhsaidqhndi/2155",
    "samodagi_15": "https://t.me/dhsaidqhndi/2156",
    "samodagi_16": "https://t.me/dhsaidqhndi/2157",
    "samodagi_17": "https://t.me/dhsaidqhndi/2158",
    "samodagi_18": "https://t.me/dhsaidqhndi/2159",
    "samodagi_19": "https://t.me/dhsaidqhndi/2160",
    "samodagi_20": "https://t.me/dhsaidqhndi/2161",
    "samodagi_21": "https://t.me/dhsaidqhndi/2162",
    "samodagi_22": "https://t.me/dhsaidqhndi/2163",
    "samodagi_23": "https://t.me/dhsaidqhndi/2164",
    "samodagi_24": "https://t.me/dhsaidqhndi/2165",
    "samodagi_25": "https://t.me/dhsaidqhndi/2166",
    "samodagi_26": "https://t.me/dhsaidqhndi/2167",
    "samodagi_27": "https://t.me/dhsaidqhndi/2168",
    "samodagi_28": "https://t.me/dhsaidqhndi/2169",
    "samodagi_29": "https://t.me/dhsaidqhndi/2170",
    "samodagi_30": "https://t.me/dhsaidqhndi/2171",
    "samodagi_31": "https://t.me/dhsaidqhndi/2172",
    "samodagi_32": "https://t.me/dhsaidqhndi/2173",
    "samodagi_33": "https://t.me/dhsaidqhndi/2174",
    "samodagi_34": "https://t.me/dhsaidqhndi/2175",
    "samodagi_35": "https://t.me/dhsaidqhndi/2176",
    "samodagi_36": "https://t.me/dhsaidqhndi/2177",
    "samodagi_37": "https://t.me/dhsaidqhndi/2178",
    "samodagi_38": "https://t.me/dhsaidqhndi/2179",
    "samodagi_39": "https://t.me/dhsaidqhndi/2180",
    "samodagi_40": "https://t.me/dhsaidqhndi/2181",
    "samodagi_41": "https://t.me/dhsaidqhndi/2182",
    "samodagi_42": "https://t.me/dhsaidqhndi/2183",
    "samodagi_43": "https://t.me/dhsaidqhndi/2184",
    "samodagi_44": "https://t.me/dhsaidqhndi/2185",
    "samodagi_45": "https://t.me/dhsaidqhndi/2186",
    "samodagi_46": "https://t.me/dhsaidqhndi/2187",
    "samodagi_47": "https://t.me/dhsaidqhndi/2188",
    "samodagi_48": "https://t.me/dhsaidqhndi/2189",
    "samodagi_49": "https://t.me/dhsaidqhndi/2190",
    "samodagi_50": "https://t.me/dhsaidqhndi/2191",
    "samodagi_51": "https://t.me/dhsaidqhndi/2192",
    "samodagi_52": "https://t.me/dhsaidqhndi/2193",
    "samodagi_53": "https://t.me/dhsaidqhndi/2194",
    "samodagi_54": "https://t.me/dhsaidqhndi/2195",
    "samodagi_55": "https://t.me/dhsaidqhndi/2196",
    "samodagi_56": "https://t.me/dhsaidqhndi/2197",
    "samodagi_57": "https://t.me/dhsaidqhndi/2198",
    "samodagi_58": "https://t.me/dhsaidqhndi/2199",
    "samodagi_59": "https://t.me/dhsaidqhndi/2200",
    "samodagi_60": "https://t.me/dhsaidqhndi/2201",
    "samodagi_61": "https://t.me/dhsaidqhndi/2202",
    "samodagi_62": "https://t.me/dhsaidqhndi/2203",
    "samodagi_63": "https://t.me/dhsaidqhndi/2204",
    "samodagi_64": "https://t.me/dhsaidqhndi/2205",
    "samodagi_65": "https://t.me/dhsaidqhndi/2206",
    "samodagi_66": "https://t.me/dhsaidqhndi/2207",
    "samodagi_67": "https://t.me/dhsaidqhndi/2208",
    "samodagi_68": "https://t.me/dhsaidqhndi/2209",
    "samodagi_69": "https://t.me/dhsaidqhndi/2210",
    "samodagi_70": "https://t.me/dhsaidqhndi/2211",
    "samodagi_71": "https://t.me/dhsaidqhndi/2212",
    "samodagi_72": "https://t.me/dhsaidqhndi/2213",
    "samodagi_73": "https://t.me/dhsaidqhndi/2214",
    "samodagi_74": "https://t.me/dhsaidqhndi/2215",
    "samodagi_75": "https://t.me/dhsaidqhndi/2216",
    "samodagi_76": "https://t.me/dhsaidqhndi/2217",
    "samodagi_77": "https://t.me/dhsaidqhndi/2218",
    "samodagi_78": "https://t.me/dhsaidqhndi/2219",
    "samodagi_79": "https://t.me/dhsaidqhndi/2220",
    "samodagi_80": "https://t.me/dhsaidqhndi/2221",
    "samodagi_81": "https://t.me/dhsaidqhndi/2222",
    "samodagi_82": "https://t.me/dhsaidqhndi/2223",
    "samodagi_83": "https://t.me/dhsaidqhndi/2224",
    "samodagi_84": "https://t.me/dhsaidqhndi/2225",
    "samodagi_85": "https://t.me/dhsaidqhndi/2226",
    "samodagi_86": "https://t.me/dhsaidqhndi/2227",
    "samodagi_87": "https://t.me/dhsaidqhndi/2228",
    "samodagi_88": "https://t.me/dhsaidqhndi/2229",
    "samodagi_89": "https://t.me/dhsaidqhndi/2230",
    "samodagi_90": "https://t.me/dhsaidqhndi/2231",
    "samodagi_91": "https://t.me/dhsaidqhndi/2232",
}

# ==================== JANG KOINOTI ====================
@dp.message(F.text == "JANG KOINOTI")
async def jang_koinoti_menu(message: types.Message):
    fasllar = list(jang_koinoti_videolar.keys())
    buttons = [
        [InlineKeyboardButton(text=fasl, callback_data=f"jang_koinoti_fasl_{fasl}")]
        for fasl in fasllar
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("⚔️ Jang Koinoti faslini tanlang:", reply_markup=keyboard)

# 🔹 FASL TANLANGANDA
@dp.callback_query(F.data.startswith("jang_koinoti_fasl_"))
async def jang_fasl_tanlandi(callback: types.CallbackQuery):
    fasl = callback.data.replace("jang_koinoti_fasl_", "")
    await callback.message.edit_text(
        f"🪐 Jang Koinoti — {fasl}\n\nQuyidagi qismlardan birini tanlang 👇",
        reply_markup=generate_jang_koinoti_keyboard(fasl, 1)
    )

# 🔹 SAHIFALASH FUNKSIYASI
def generate_jang_koinoti_keyboard(fasl: str, page: int = 1):
    per_page = 12
    all_items = list(jang_koinoti_videolar[fasl].items())
    start = (page - 1) * per_page
    end = start + per_page
    items = all_items[start:end]

    keyboard = []
    for name, url in items:
        keyboard.append([
            InlineKeyboardButton(
                text=name,
                callback_data=f"jang_koinoti_video_{fasl}:{name}"
            )
        ])

    nav_buttons = []
    if start > 0:
        nav_buttons.append(
            InlineKeyboardButton("⬅️ Oldingi", callback_data=f"jang_koinoti_page_{fasl}_{page-1}")
        )
    if end < len(all_items):
        nav_buttons.append(
            InlineKeyboardButton("➡️ Keyingi", callback_data=f"jang_koinoti_page_{fasl}_{page+1}")
        )

    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# 🔹 SAHIFA ALMASHTIRILGANDA
@dp.callback_query(F.data.startswith("jang_koinoti_page_"))
async def jang_page(callback: types.CallbackQuery):
    data = callback.data.replace("jang_koinoti_page_", "")
    fasl, page_str = data.rsplit("_", 1)
    page = int(page_str)

    await callback.message.edit_text(
        f"🪐 Jang Koinoti — {fasl}\n\nQuyidagi qismlardan birini tanlang 👇",
        reply_markup=generate_jang_koinoti_keyboard(fasl, page)
    )

# 🔹 VIDEO YUBORISH
@dp.callback_query(F.data.startswith("jang_koinoti_video_"))
async def jang_video_yubor(callback: types.CallbackQuery):
    data = callback.data.replace("jang_koinoti_video_", "")
    fasl, qism = data.split(":", 1)

    # Ma'lumotni tekshirish
    if fasl not in jang_koinoti_videolar or qism not in jang_koinoti_videolar[fasl]:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    video_link = jang_koinoti_videolar[fasl][qism]

    caption = (
        f"🎬 <b>Nomi:</b> Jang Koinoti\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Jangovar, Sarguzasht\n"
        f"📺 <b>Fasl:</b> {fasl}\n"
        f"🎞 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniMania_rasmiy | @aust1n_griffin\n"
        "#jang_koinoti\n\n"
        "💬 “Koinotdagi har bir jang — g‘alaba sari bir qadam.” ⚔️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

# Jang Koinoti videolar ro'yxati:
jang_koinoti_videolar = {
    "1-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/1613",
        "2-qism": "https://t.me/dhsaidqhndi/1614",
        "3-qism": "https://t.me/dhsaidqhndi/1615",
        "4-qism": "https://t.me/dhsaidqhndi/1616",
        "5-qism": "https://t.me/dhsaidqhndi/1617",
        "6-qism": "https://t.me/dhsaidqhndi/1618",
        "7-qism": "https://t.me/dhsaidqhndi/1619",
        "8-qism": "https://t.me/dhsaidqhndi/1620",
        "9-qism": "https://t.me/dhsaidqhndi/1621",
        "10-qism": "https://t.me/dhsaidqhndi/1622",
        "11-qism": "https://t.me/dhsaidqhndi/1623",
        "12-qism": "https://t.me/dhsaidqhndi/1624",
    },
    "2-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/1625",
        "2-qism": "https://t.me/dhsaidqhndi/1626",
        "3-qism": "https://t.me/dhsaidqhndi/1627",
        "4-qism": "https://t.me/dhsaidqhndi/1628",
        "5-qism": "https://t.me/dhsaidqhndi/1629",
        "6-qism": "https://t.me/dhsaidqhndi/1630",
        "7-qism": "https://t.me/dhsaidqhndi/1631",
        "8-qism": "https://t.me/dhsaidqhndi/1632",
        "9-qism": "https://t.me/dhsaidqhndi/1633",
        "10-qism": "https://t.me/dhsaidqhndi/1634",
        "11-qism": "https://t.me/dhsaidqhndi/1635",
        "12-qism": "https://t.me/dhsaidqhndi/1636",
    },
    "3-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/1637",
        "2-qism": "https://t.me/dhsaidqhndi/1638",
        "3-qism": "https://t.me/dhsaidqhndi/1639",
        "4-qism": "https://t.me/dhsaidqhndi/1640",
        "5-qism": "https://t.me/dhsaidqhndi/1641",
        "6-qism": "https://t.me/dhsaidqhndi/1642",
        "7-qism": "https://t.me/dhsaidqhndi/1643",
        "8-qism": "https://t.me/dhsaidqhndi/1644",
        "9-qism": "https://t.me/dhsaidqhndi/1645",
        "10-qism": "https://t.me/dhsaidqhndi/1646",
        "11-qism": "https://t.me/dhsaidqhndi/1647",
        "12-qism": "https://t.me/dhsaidqhndi/1648",
    },
    "4-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/1649",
        "2-qism": "https://t.me/dhsaidqhndi/1650",
        "3-qism": "https://t.me/dhsaidqhndi/1651",
        "4-qism": "https://t.me/dhsaidqhndi/1652",
        "5-qism": "https://t.me/dhsaidqhndi/1653",
        "6-qism": "https://t.me/dhsaidqhndi/1654",
        "7-qism": "https://t.me/dhsaidqhndi/1655",
        "8-qism": "https://t.me/dhsaidqhndi/1656",
        "9-qism": "https://t.me/dhsaidqhndi/1657",
        "10-qism": "https://t.me/dhsaidqhndi/1658",
        "11-qism": "https://t.me/dhsaidqhndi/1659",
        "12-qism": "https://t.me/dhsaidqhndi/1660",
    },
    "5-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/1661",
        "2-qism": "https://t.me/dhsaidqhndi/1662",
        "3-qism": "https://t.me/dhsaidqhndi/1663",
        "4-qism": "https://t.me/dhsaidqhndi/1664",
        "5-qism": "https://t.me/dhsaidqhndi/1665",
        "6-qism": "https://t.me/dhsaidqhndi/1666",
        "7-qism": "https://t.me/dhsaidqhndi/1667",
        "8-qism": "https://t.me/dhsaidqhndi/1668",
        "9-qism": "https://t.me/dhsaidqhndi/1669",
        "10-qism": "https://t.me/dhsaidqhndi/1670",
        "11-qism": "https://t.me/dhsaidqhndi/1671",
        "12-qism": "https://t.me/dhsaidqhndi/1672",
    },
    "6-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/2634",
        "2-qism": "https://t.me/dhsaidqhndi/2635",
        "3-qism": "https://t.me/dhsaidqhndi/2636",
        "4-qism": "https://t.me/dhsaidqhndi/2637",
        "5-qism": "https://t.me/dhsaidqhndi/2638",
    }
}

# ============= 📜 Mundareja 2-qism =============
@dp.message(F.text == "📜 Mundareja 2-qism")
async def mundareja_2_handler(message: types.Message):
    mundareja_2_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="100 MING YILLIK PAST DARAJADAGI YETISHTIRISH")],
            [KeyboardButton(text="JADE SULOLASI")],
            [KeyboardButton(text="ASRAB OLINGAN BOLA")],
            [KeyboardButton(text="VAYRONALAR ICHRA")],
            [KeyboardButton(text="MABUTLAR MAQBARASI")],
            [KeyboardButton(text="LINGVU QIT'ASI")],
            [KeyboardButton(text="KUCHLI SHOGIRDLAR")],
            [KeyboardButton(text="JANG SAN'ATI CHO'QQISI")],
            [KeyboardButton(text="YE FENNING SHONLI QASOSI")],
            [KeyboardButton(text="YAN CHEN AFSONASI")],
            [KeyboardButton(text="⬅️ Orqaga")],
        ],
        resize_keyboard=True
    )
    await message.answer("📜 Mundareja 2-qism bo‘limi:", reply_markup=mundareja_2_menu)

# ⬅️ Orqaga
@dp.message(F.text == "⬅️ Orqaga")
async def back_to_main(message: types.Message):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📜 Mundareja 1-qism")],
            [KeyboardButton(text="📜 Mundareja 2-qism")],
            [KeyboardButton(text="📜 Mundareja 3-qism")],
            [KeyboardButton(text="📜 Mundareja 4-qism")],
            [KeyboardButton(text="📜 Mundareja 5-qism")],
            [KeyboardButton(text="📢 Reklama va homiylik")],
            [KeyboardButton(text="📥 Video yuklab olish")],
            [KeyboardButton(text="📈 Statistika")],
            [KeyboardButton(text="👤 Admin")],
        ],
        resize_keyboard=True
    )
    await message.answer("🔙 Asosiy menyuga qaytdingiz", reply_markup=main_menu)

# ==================== 100 MING YILLIK PAST DARAJADAGI YETISHTIRISH ====================
@dp.message(F.text == "100 MING YILLIK PAST DARAJADAGI YETISHTIRISH")
async def yillik_handler(message: types.Message):
    await message.answer(
        "💠 *100 Ming Yillik Past Darajadagi Yetishtirish* qismlarini tanlang:",
        reply_markup=get_yillik_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^yillik_\d+$"))
async def send_yillik_video(callback: types.CallbackQuery):
    key = callback.data
    link = yillik_videolar.get(key)

    if not link:
        await callback.answer("❌ Bu qism mavjud emas!", show_alert=True)
        return

    qism = int(key.split("_")[1])

    caption = (
        f"🎬 <b>Nomi:</b> 100 Ming Yillik Past Darajadagi Yetishtirish\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniMania_rasmiy</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniMania_rasmiy | @aust1n_griffin\n"
    )

    await bot.send_video(
        callback.from_user.id, 
        link,
        caption=caption,
        parse_mode="HTML",
        protect_content=True
    )

@dp.callback_query(F.data.regexp(r"^yillik_page_\d+$"))
async def change_yillik_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(
        reply_markup=get_yillik_page_keyboard(page)
    )
    await callback.answer()

def get_yillik_page_keyboard(page: int):
    PER_PAGE = 20
    keys = sorted(yillik_videolar.keys(), key=lambda x: int(x.split("_")[1]))
    total_pages = (len(keys) + PER_PAGE - 1) // PER_PAGE

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    page_keys = keys[start:end]

    # Videolar tugmalari
    buttons = [
        [InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=key)]
        for i, key in enumerate(page_keys, start=start)
    ]

    # Navigatsiya tugmalari
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"yillik_page_{page-1}"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"yillik_page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎞 100 MING YILLIK PAST DARAJADAGI YETISHTIRISH videolar ro'yxati
yillik_videolar = {
    "yillik_1": "https://t.me/dhsaidqhndi/2008",
    "yillik_2": "https://t.me/dhsaidqhndi/2009",
    "yillik_3": "https://t.me/dhsaidqhndi/2010",
    "yillik_4": "https://t.me/dhsaidqhndi/2011",
    "yillik_5": "https://t.me/dhsaidqhndi/2012",
    "yillik_6": "https://t.me/dhsaidqhndi/2013",
    "yillik_7": "https://t.me/dhsaidqhndi/2014",
    "yillik_8": "https://t.me/dhsaidqhndi/2015",
    "yillik_9": "https://t.me/dhsaidqhndi/2016",
    "yillik_10": "https://t.me/dhsaidqhndi/2017",
    "yillik_11": "https://t.me/dhsaidqhndi/2018",
    "yillik_12": "https://t.me/dhsaidqhndi/2019",
    "yillik_13": "https://t.me/dhsaidqhndi/2020",
    "yillik_14": "https://t.me/dhsaidqhndi/2021",
    "yillik_15": "https://t.me/dhsaidqhndi/2022",
    "yillik_16": "https://t.me/dhsaidqhndi/2023",
    "yillik_17": "https://t.me/dhsaidqhndi/2024",
    "yillik_18": "https://t.me/dhsaidqhndi/2025",
    "yillik_19": "https://t.me/dhsaidqhndi/2026",
    "yillik_20": "https://t.me/dhsaidqhndi/2027",
    "yillik_21": "https://t.me/dhsaidqhndi/2028",
    "yillik_22": "https://t.me/dhsaidqhndi/2029",
    "yillik_23": "https://t.me/dhsaidqhndi/2030",
    "yillik_24": "https://t.me/dhsaidqhndi/2031",
    "yillik_25": "https://t.me/dhsaidqhndi/2032",
    "yillik_26": "https://t.me/dhsaidqhndi/2033",
    "yillik_27": "https://t.me/dhsaidqhndi/2034",
    "yillik_28": "https://t.me/dhsaidqhndi/2035",
    "yillik_29": "https://t.me/dhsaidqhndi/2036",
    "yillik_30": "https://t.me/dhsaidqhndi/2037",
    "yillik_31": "https://t.me/dhsaidqhndi/2038",
    "yillik_32": "https://t.me/dhsaidqhndi/2039",
    "yillik_33": "https://t.me/dhsaidqhndi/2040",
    "yillik_34": "https://t.me/dhsaidqhndi/2041",
    "yillik_35": "https://t.me/dhsaidqhndi/2042",
}

# ==================== JADE SULOLASI ====================
# 💎 JADE SULOLASI — Asosiy menyu
@dp.message(F.text == "JADE SULOLASI")
async def jade_handler(message: types.Message):
    await message.answer(
        "💎 *Jade Sulolasi* faslini tanlang:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1-fasl", callback_data="jade_fasl_1")],
            [InlineKeyboardButton(text="2-fasl", callback_data="jade_fasl_2")],
            [InlineKeyboardButton(text="3-fasl", callback_data="jade_fasl_3")],
        ]),
        parse_mode="Markdown"
    )

# 📄 Fasl tanlanganda
@dp.callback_query(F.data.startswith("jade_fasl_"))
async def jade_fasl(callback: types.CallbackQuery):
    fasl = callback.data.split("_")[-1]
    await callback.message.edit_text(
        f"💎 *Jade Sulolasi — {fasl}-fasl* qismini tanlang:",
        reply_markup=get_jade_page_keyboard(fasl, 1),
        parse_mode="Markdown"
    )

# 🎬 Video yuborish
@dp.callback_query(F.data.regexp(r"^jade_\d+_\d+$"))
async def send_jade_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = jade_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    fasl, qism = key.split("_")[1], key.split("_")[2]
    caption = (
        "🎬 <b>Nomi:</b> Jade Sulolasi\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Tarixiy, Jangovar\n"
        f"📺 <b>Fasl:</b> {fasl}\n"
        f"🎞 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniMania)\n"
        "────────────────\n"
        "👑 <b>Kanal:</b> @AniMania_Rasmiy\n"
        "#jade_sulolasi\n\n"
        "💬 “Har bir toshda o‘tgan avlodlarning izlari bor. Ammo haqiqiy kuch yurakda yashaydi.”"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

# 🔘 Sahifalangan tugmalar
def get_jade_page_keyboard(fasl: str, page: int):
    per_page = 26
    prefix = f"jade_{fasl}_"
    keys = [k for k in jade_videolar.keys() if k.startswith(prefix)]
    start = (page - 1) * per_page
    end = start + per_page
    sub_keys = keys[start:end]

    buttons = [[InlineKeyboardButton(text=f"🎬 {k.split('_')[-1]}-qism", callback_data=k)] for k in sub_keys]

    nav = []
    if start > 0:
        nav.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"jade_page_{fasl}_{page-1}"))
    if end < len(keys):
        nav.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"jade_page_{fasl}_{page+1}"))
    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Jade Sulolasi videolar ro'yxati:
jade_videolar = {
    # ==================== 1-FASL ====================
    "jade_1_1": "https://t.me/dhsaidqhndi/1768",
    "jade_1_2": "https://t.me/dhsaidqhndi/1769",
    "jade_1_3": "https://t.me/dhsaidqhndi/1770",
    "jade_1_4": "https://t.me/dhsaidqhndi/1771",
    "jade_1_5": "https://t.me/dhsaidqhndi/1772",
    "jade_1_6": "https://t.me/dhsaidqhndi/1773",
    "jade_1_7": "https://t.me/dhsaidqhndi/1774",
    "jade_1_8": "https://t.me/dhsaidqhndi/1775",
    "jade_1_9": "https://t.me/dhsaidqhndi/1776",
    "jade_1_10": "https://t.me/dhsaidqhndi/1777",
    "jade_1_11": "https://t.me/dhsaidqhndi/1778",
    "jade_1_12": "https://t.me/dhsaidqhndi/1779",
    "jade_1_13": "https://t.me/dhsaidqhndi/1780",
    "jade_1_14": "https://t.me/dhsaidqhndi/1781",
    "jade_1_15": "https://t.me/dhsaidqhndi/1782",
    "jade_1_16": "https://t.me/dhsaidqhndi/1783",
    "jade_1_17": "https://t.me/dhsaidqhndi/1784",
    "jade_1_18": "https://t.me/dhsaidqhndi/1785",
    "jade_1_19": "https://t.me/dhsaidqhndi/1786",
    "jade_1_20": "https://t.me/dhsaidqhndi/1787",
    "jade_1_21": "https://t.me/dhsaidqhndi/1788",
    "jade_1_22": "https://t.me/dhsaidqhndi/1789",
    "jade_1_23": "https://t.me/dhsaidqhndi/1790",
    "jade_1_24": "https://t.me/dhsaidqhndi/1791",
    "jade_1_25": "https://t.me/dhsaidqhndi/1792",
    "jade_1_26": "https://t.me/dhsaidqhndi/1793",

    # ==================== 2-FASL ====================
    "jade_2_1": "https://t.me/dhsaidqhndi/1794",
    "jade_2_2": "https://t.me/dhsaidqhndi/1795",
    "jade_2_3": "https://t.me/dhsaidqhndi/1796",
    "jade_2_4": "https://t.me/dhsaidqhndi/1797",
    "jade_2_5": "https://t.me/dhsaidqhndi/1798",
    "jade_2_6": "https://t.me/dhsaidqhndi/1799",
    "jade_2_7": "https://t.me/dhsaidqhndi/1800",
    "jade_2_8": "https://t.me/dhsaidqhndi/1801",
    "jade_2_9": "https://t.me/dhsaidqhndi/1802",
    "jade_2_10": "https://t.me/dhsaidqhndi/1803",
    "jade_2_11": "https://t.me/dhsaidqhndi/1804",
    "jade_2_12": "https://t.me/dhsaidqhndi/1805",
    "jade_2_13": "https://t.me/dhsaidqhndi/1806",
    "jade_2_14": "https://t.me/dhsaidqhndi/1807",
    "jade_2_15": "https://t.me/dhsaidqhndi/1808",
    "jade_2_16": "https://t.me/dhsaidqhndi/1809",
    "jade_2_17": "https://t.me/dhsaidqhndi/1810",
    "jade_2_18": "https://t.me/dhsaidqhndi/1811",
    "jade_2_19": "https://t.me/dhsaidqhndi/1812",
    "jade_2_20": "https://t.me/dhsaidqhndi/1813",
    "jade_2_21": "https://t.me/dhsaidqhndi/1814",
    "jade_2_22": "https://t.me/dhsaidqhndi/1815",
    "jade_2_23": "https://t.me/dhsaidqhndi/1816",
    "jade_2_24": "https://t.me/dhsaidqhndi/1817",
    "jade_2_25": "https://t.me/dhsaidqhndi/1818",
    "jade_2_26": "https://t.me/dhsaidqhndi/1819",

    # ==================== 3-FASL ====================
    "jade_3_1": "https://t.me/dhsaidqhndi/1820",
    "jade_3_2": "https://t.me/dhsaidqhndi/1821",
    "jade_3_3": "https://t.me/dhsaidqhndi/2249",
    "jade_3_4": "https://t.me/dhsaidqhndi/2249",
    "jade_3_5": "https://t.me/dhsaidqhndi/2350",
    "jade_3_6": "https://t.me/dhsaidqhndi/2428",
    "jade_3_7": "https://t.me/dhsaidqhndi/2429",
    "jade_3_8": "https://t.me/dhsaidqhndi/2430",
}

# ============🎥 ASRAB OLINGAN BOLA ============
@dp.message(F.text == "ASRAB OLINGAN BOLA")
async def asrab_olingan_bola_handler(message: types.Message):
    await message.answer("👶 'ASRAB OLINGAN BOLA' qismlarini tanlang:", reply_markup=get_page_asrab_keyboard(1))


# 📄 Sahifa almashtirish
@dp.callback_query(F.data.regexp(r"^asrab_page_\d+$"))
async def change_page_asrab(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_page_asrab_keyboard(page))
    await callback.answer()


# 🎬 Video yuborish
@dp.callback_query(F.data.regexp(r"^asrab_qism_\d+$"))
async def send_asrab_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = asrab_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🎬 Nomi: ASRAB OLINGAN BOLA\n"
        "───────────────\n"
        "🎞 Janr: Drama, Hayotiy, Oilaviy\n"
        f"📺 Qismi: {qism_raqami}\n"
        "💿 Sifati: 480p HD\n"
        "🌐 Til: O‘zbek(EgoSama)\n"
        "───────────────\n"
        "👑 Kanal: @AniMania_rasmiy, @EgoSama\n"
        "#asrab_olingan_bola_animania\n\n"
        "💬 “Ba’zan eng katta kuch — mehrdan keladi.” 💖"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True
    )
    await callback.answer()


# 🔘 Sahifalangan tugmalar
def get_page_asrab_keyboard(page: int):
    VIDEOS_PER_PAGE = 10
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(asrab_videolar.keys())[start:end]

    buttons = [
        [InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=key)]
        for i, key in enumerate(keys, start=start)
    ]

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"asrab_page_{page-1}"))
    if end < len(asrab_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"asrab_page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎞 ASRAB OLINGAN BOLA videolari ro‘yxati
asrab_videolar = {
    "asrab_qism_1": "https://t.me/dhsaidqhndi/1260",
    "asrab_qism_2": "https://t.me/dhsaidqhndi/1261",
    "asrab_qism_3": "https://t.me/dhsaidqhndi/1262",
    "asrab_qism_4": "https://t.me/dhsaidqhndi/1263",
    "asrab_qism_5": "https://t.me/dhsaidqhndi/1264",
    "asrab_qism_6": "https://t.me/dhsaidqhndi/1265",
    "asrab_qism_7": "https://t.me/dhsaidqhndi/1266",
    "asrab_qism_8": "https://t.me/dhsaidqhndi/1267",
    "asrab_qism_9": "https://t.me/dhsaidqhndi/1268",
    "asrab_qism_10": "https://t.me/dhsaidqhndi/1269",
    "asrab_qism_11": "https://t.me/dhsaidqhndi/1270",
    "asrab_qism_12": "https://t.me/dhsaidqhndi/1271",
    "asrab_qism_13": "https://t.me/dhsaidqhndi/1272",
    "asrab_qism_14": "https://t.me/dhsaidqhndi/1273",
    "asrab_qism_15": "https://t.me/dhsaidqhndi/1274",
    "asrab_qism_16": "https://t.me/dhsaidqhndi/1275",
    "asrab_qism_17": "https://t.me/dhsaidqhndi/1276",
    "asrab_qism_18": "https://t.me/dhsaidqhndi/1277",
    "asrab_qism_19": "https://t.me/dhsaidqhndi/1278",
    "asrab_qism_20": "https://t.me/dhsaidqhndi/1279",
    "asrab_qism_21": "https://t.me/dhsaidqhndi/1280",
    "asrab_qism_22": "https://t.me/dhsaidqhndi/1281",
    "asrab_qism_23": "https://t.me/dhsaidqhndi/1282",
    "asrab_qism_24": "https://t.me/dhsaidqhndi/1283",
    "asrab_qism_25": "https://t.me/dhsaidqhndi/1284",
    "asrab_qism_26": "https://t.me/dhsaidqhndi/1285",
    "asrab_qism_27": "https://t.me/dhsaidqhndi/1286",
    "asrab_qism_28": "https://t.me/dhsaidqhndi/1287",
    "asrab_qism_29": "https://t.me/dhsaidqhndi/1288",
    "asrab_qism_30": "https://t.me/dhsaidqhndi/1289",
    "asrab_qism_31": "https://t.me/dhsaidqhndi/1290",
    "asrab_qism_32": "https://t.me/dhsaidqhndi/1291",
    "asrab_qism_33": "https://t.me/dhsaidqhndi/1292",
    "asrab_qism_34": "https://t.me/dhsaidqhndi/1293",
    "asrab_qism_35": "https://t.me/dhsaidqhndi/1294",
    "asrab_qism_36": "https://t.me/dhsaidqhndi/1295",
    "asrab_qism_37": "https://t.me/dhsaidqhndi/1296",
    "asrab_qism_38": "https://t.me/dhsaidqhndi/1297",
    "asrab_qism_39": "https://t.me/dhsaidqhndi/1298",
    "asrab_qism_40": "https://t.me/dhsaidqhndi/1299",
    "asrab_qism_41": "https://t.me/dhsaidqhndi/1300",
    "asrab_qism_42": "https://t.me/dhsaidqhndi/1301",
    "asrab_qism_43": "https://t.me/dhsaidqhndi/1302",
    "asrab_qism_44": "https://t.me/dhsaidqhndi/1303",
    "asrab_qism_45": "https://t.me/dhsaidqhndi/1304",
    "asrab_qism_46": "https://t.me/dhsaidqhndi/1305",
    "asrab_qism_47": "https://t.me/dhsaidqhndi/1306",
    "asrab_qism_48": "https://t.me/dhsaidqhndi/1307",
    "asrab_qism_49": "https://t.me/dhsaidqhndi/1308",
    "asrab_qism_50": "https://t.me/dhsaidqhndi/1309",
    "asrab_qism_51": "https://t.me/dhsaidqhndi/1310",
    "asrab_qism_52": "https://t.me/dhsaidqhndi/1311",
    "asrab_qism_53": "https://t.me/dhsaidqhndi/1312",
    "asrab_qism_54": "https://t.me/dhsaidqhndi/2122",
    "asrab_qism_55": "https://t.me/dhsaidqhndi/2329",
    "asrab_qism_56": "https://t.me/dhsaidqhndi/2330",
    "asrab_qism_57": "https://t.me/dhsaidqhndi/2437",
    "asrab_qism_58": "https://t.me/dhsaidqhndi/2527",
    "asrab_qism_59": "https://t.me/dhsaidqhndi/2510",
}

# ==================== VAYRONALAR ICHRA ====================
@dp.message(F.text == "VAYRONALAR ICHRA")
async def vayronalar_handler(message: types.Message):
    await message.answer(
        "🏯 *Vayronalar Ichra* qismlarini tanlang:",
        reply_markup=get_vayronalar_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^vayronalar_page_\d+$"))
async def change_vayronalar_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(
        reply_markup=get_vayronalar_page_keyboard(page)
    )
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^vayronalar_\d+$"))
async def send_vayronalar_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = vayronalar_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> VAYRONALAR ICHRA\n"
        "🎞 <b>Janr:</b> Sehrli, Jangovar, Falsafiy\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@uzdubgo</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @uzdubgo | @aust1n_griffin\n"
    )

    await bot.send_video(
        callback.from_user.id,
        video_link,
        caption=caption,
        parse_mode="HTML",
        protect_content=True
    )

def get_vayronalar_page_keyboard(page: int):
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page

    keys = list(vayronalar_videolar.keys())[start:end]

    buttons = [
    [
        InlineKeyboardButton(
            text=f"🎬 {i+1}-qism",
            callback_data=f"vayronalar_{i+1}"
        )
    ]
    for i, _ in enumerate(keys, start=start)
]
    
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"vayronalar_page_{page-1}"))
    if end < len(vayronalar_videolar):
        nav.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"vayronalar_page_{page+1}"))
    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎞 VAYRONALAR ICHRA videolar ro'yxati
vayronalar_videolar = {
    "vayronalar_1": "https://t.me/dhsaidqhndi/2059",
    "vayronalar_2": "https://t.me/dhsaidqhndi/2060",
    "vayronalar_3": "https://t.me/dhsaidqhndi/2061",
    "vayronalar_4": "https://t.me/dhsaidqhndi/2062",
    "vayronalar_5": "https://t.me/dhsaidqhndi/2063",
    "vayronalar_6": "https://t.me/dhsaidqhndi/2064",
    "vayronalar_7": "https://t.me/dhsaidqhndi/2132",
    "vayronalar_8": "https://t.me/dhsaidqhndi/2134",
    "vayronalar_9": "https://t.me/dhsaidqhndi/2133",
    "vayronalar_10": "https://t.me/dhsaidqhndi/2334",
    "vayronalar_11": "https://t.me/dhsaidqhndi/2335",
    "vayronalar_12": "https://t.me/dhsaidqhndi/2336",
    "vayronalar_13": "https://t.me/dhsaidqhndi/2337",
    "vayronalar_14": "https://t.me/dhsaidqhndi/2439",
    "vayronalar_15": "https://t.me/dhsaidqhndi/2440",
}

# ==================== MABUTLAR MAQBARASI ====================
# 🏛️ MABUTLAR MAQBARASI menyusi
@dp.message(F.text == "MABUTLAR MAQBARASI")
async def mabutlar_menu(message: types.Message):
    fasllar = list(mabut_videolar.keys())
    buttons = [
        [InlineKeyboardButton(text=fasl, callback_data=f"mabut_fasl_{fasl}")]
        for fasl in fasllar
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("🏛️ Mabutlar Maqbarasi faslini tanlang:", reply_markup=keyboard)


# 🔹 FASL TANLANGANDA
@dp.callback_query(F.data.startswith("mabut_fasl_"))
async def mabut_fasl_tanlandi(callback: types.CallbackQuery):
    fasl = callback.data.replace("mabut_fasl_", "")
    await callback.message.edit_text(
        f"🏛️ Mabutlar Maqbarasi — {fasl}\n\nQuyidagi qismlardan birini tanlang 👇",
        reply_markup=generate_mabut_keyboard(fasl, 1)
    )


# 🔹 SAHIFALASH FUNKSIYASI
def generate_mabut_keyboard(fasl: str, page: int = 1):
    per_page = 20  # har faslda bitta sahifada nechta video ko‘rsatiladi
    all_items = list(mabut_videolar[fasl].items())  # [(qism, url), ...]
    start = (page - 1) * per_page
    end = start + per_page
    items = all_items[start:end]

    keyboard = []
    for name, url in items:
        keyboard.append([InlineKeyboardButton(text=name, callback_data=f"mabut_video_{fasl}:{name}")])

    nav_buttons = []
    if start > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"mabut_page_{fasl}_{page-1}"))
    if end < len(all_items):
        nav_buttons.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"mabut_page_{fasl}_{page+1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# 🔹 SAHIFA ALMASHTIRILGANDA
@dp.callback_query(F.data.startswith("mabut_page_"))
async def mabut_page(callback: types.CallbackQuery):
    data = callback.data[len("mabut_page_"):] 
    fasl, page_str = data.rsplit("_", 1)
    page = int(page_str)

    await callback.message.edit_text(
        f"🏛️ Mabutlar Maqbarasi — {fasl}\n\nQuyidagi qismlardan birini tanlang 👇",
        reply_markup=generate_mabut_keyboard(fasl, page)
    )


# 🔹 VIDEO YUBORISH
@dp.callback_query(F.data.startswith("mabut_video_"))
async def mabut_video_yubor(callback: types.CallbackQuery):
    data = callback.data[len("mabut_video_"):]  
    if ":" not in data:
        await callback.answer("❌ Xato formatdagi video identifikator!", show_alert=True)
        return

    fasl, qism = data.split(":", 1)

    # Ma'lumotni tekshirish
    if fasl not in mabut_videolar or qism not in mabut_videolar[fasl]:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    video_link = mabut_videolar[fasl][qism]

    caption = (
        f"🎬 <b>Nomi:</b> Mabutlar Maqbarasi\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Sarguzasht, Drama\n"
        f"📺 <b>Fasl:</b> {fasl}\n"
        f"🎞 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniManhwa3D)\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniManhwa3D</b>\n"
        "───────────────\n" 
        "👑 <b>Kanal:</b> @AniMAnhwa3D\n"
        "#mabut_maqbara\n\n"
        "💬 “Maqbaraning sirli derazalari faqat jasoratga ochiladi.” 🏛️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

    await callback.answer()

# 🎞 Mabudlar Maqbarasi videolari ro‘yxati
mabut_videolar = {
    "1-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/1314",
        "2-qism": "https://t.me/dhsaidqhndi/1315",
        "3-qism": "https://t.me/dhsaidqhndi/1316",
        "4-qism": "https://t.me/dhsaidqhndi/1317",
        "5-qism": "https://t.me/dhsaidqhndi/1318",
        "6-qism": "https://t.me/dhsaidqhndi/1319",
        "7-qism": "https://t.me/dhsaidqhndi/1320",
        "8-qism": "https://t.me/dhsaidqhndi/1321",
        "9-qism": "https://t.me/dhsaidqhndi/1322",
        "10-qism": "https://t.me/dhsaidqhndi/1323",
        "11-qism": "https://t.me/dhsaidqhndi/1324",
        "12-qism": "https://t.me/dhsaidqhndi/1325",
        "13-qism": "https://t.me/dhsaidqhndi/1326",
        "14-qism": "https://t.me/dhsaidqhndi/1327",
        "15-qism": "https://t.me/dhsaidqhndi/1328",
        "16-qism": "https://t.me/dhsaidqhndi/1329"
    },
    "2-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/1330",
        "2-qism": "https://t.me/dhsaidqhndi/1331",
        "3-qism": "https://t.me/dhsaidqhndi/1332",
        "4-qism": "https://t.me/dhsaidqhndi/1333",
        "5-qism": "https://t.me/dhsaidqhndi/1334",
        "6-qism": "https://t.me/dhsaidqhndi/1335",
        "7-qism": "https://t.me/dhsaidqhndi/1336",
        "8-qism": "https://t.me/dhsaidqhndi/1337",
        "9-qism": "https://t.me/dhsaidqhndi/1338",
        "10-qism": "https://t.me/dhsaidqhndi/1339",
        "11-qism": "https://t.me/dhsaidqhndi/1340",
        "12-qism": "https://t.me/dhsaidqhndi/1341",
        "13-qism": "https://t.me/dhsaidqhndi/1342",
        "14-qism": "https://t.me/dhsaidqhndi/1343",
        "15-qism": "https://t.me/dhsaidqhndi/1344",
        "16-qism": "https://t.me/dhsaidqhndi/1345",
        "17-qism": "https://t.me/dhsaidqhndi/1346",
        "18-qism": "https://t.me/dhsaidqhndi/1347",
        "19-qism": "https://t.me/dhsaidqhndi/1348",
        "20-qism": "https://t.me/dhsaidqhndi/1349",
        "21-qism": "https://t.me/dhsaidqhndi/1350",
        "22-qism": "https://t.me/dhsaidqhndi/1351",
        "23-qism": "https://t.me/dhsaidqhndi/1352",
        "24-qism": "https://t.me/dhsaidqhndi/1353",
        "25-qism": "https://t.me/dhsaidqhndi/1361",
        "26-qism": "https://t.me/dhsaidqhndi/1354",
        "27-qism": "https://t.me/dhsaidqhndi/1355",
    },
    "3-fasl": {
        "1-qism": "https://t.me/dhsaidqhndi/1356",
        "2-qism": "https://t.me/dhsaidqhndi/1357",
        "3-qism": "https://t.me/dhsaidqhndi/1359",
        "4-qism": "https://t.me/dhsaidqhndi/1360",
        "5-qism": "https://t.me/dhsaidqhndi/1463",
        "6-qism": "https://t.me/dhsaidqhndi/2239",
        "7-qism": "https://t.me/dhsaidqhndi/2240",
        "8-qism": "https://t.me/dhsaidqhndi/2303",
        "9-qism": "https://t.me/dhsaidqhndi/2421",
        "10-qism": "https://t.me/dhsaidqhndi/2380",
        "11-qism": "https://t.me/dhsaidqhndi/2403",
        "12-qism": "https://t.me/dhsaidqhndi/2511",
        "13-qism": "https://t.me/dhsaidqhndi/2512",
        "14-qism": "https://t.me/dhsaidqhndi/2513",
        "15-qism": "https://t.me/dhsaidqhndi/2615",
        "16-qism": "https://t.me/dhsaidqhndi/2627",
    }
}

# ================= LINGVU QIT'ASI ====================
# 🌊 LINGVU QIT'ASI — Asosiy menyu
@dp.message(F.text == "LINGVU QIT'ASI")
async def lingvu_qitasi_handler(message: types.Message):
    await message.answer(
        "🌊 *Lingvu Qit'asi* qismlarini tanlang:",
        reply_markup=get_lingvu_page_keyboard(1),
        parse_mode="Markdown"
    )

# 📄 Sahifa almashtirish (pagination)
@dp.callback_query(F.data.regexp(r"^lingvu_page_\d+$"))
async def change_lingvu_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_lingvu_page_keyboard(page))
    await callback.answer()

# 🎬 Video yuborish
@dp.callback_query(F.data.regexp(r"^lingvu_qism_\d+$"))
async def send_lingvu_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = lingvu_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🌊 <b>Nomi:</b> Lingvu Qit'asi\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Sehrli, Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniMAnhwa3D)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "#lingvu_qitasi_animania\n\n"
        "💬 “Sokin suv ham chuqur sirlarni yashiradi — ularni faqat jasurlar anglay oladi.” 🌊"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption.replace("*", "").replace("_", ""),
        protect_content=True,
        parse_mode="HTML"
    )

# 🔘 Sahifalangan tugmalar — 20 ta per page
def get_lingvu_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(lingvu_videolar.keys())[start:end]

    buttons = []
    for i, key in enumerate(keys, start=start):
        buttons.append([
            InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"lingvu_qism_{i+1}")
        ])

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"lingvu_page_{page-1}"))
    if end < len(lingvu_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"lingvu_page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Lingvu Qit'asi videolar ro'yxati:
lingvu_videolar = {
    "lingvu_qism_1": "https://t.me/dhsaidqhndi/1435",
    "lingvu_qism_2": "https://t.me/dhsaidqhndi/1436",
    "lingvu_qism_3": "https://t.me/dhsaidqhndi/1437",
    "lingvu_qism_4": "https://t.me/dhsaidqhndi/1438",
    "lingvu_qism_5": "https://t.me/dhsaidqhndi/1439",
    "lingvu_qism_6": "https://t.me/dhsaidqhndi/1440",
    "lingvu_qism_7": "https://t.me/dhsaidqhndi/1441",
    "lingvu_qism_8": "https://t.me/dhsaidqhndi/1442",
    "lingvu_qism_9": "https://t.me/dhsaidqhndi/1443",
    "lingvu_qism_10": "https://t.me/dhsaidqhndi/1444",
    "lingvu_qism_11": "https://t.me/dhsaidqhndi/1445",
    "lingvu_qism_12": "https://t.me/dhsaidqhndi/1446",
    "lingvu_qism_13": "https://t.me/dhsaidqhndi/1447",
    "lingvu_qism_14": "https://t.me/dhsaidqhndi/1448",
    "lingvu_qism_15": "https://t.me/dhsaidqhndi/1449",
    "lingvu_qism_16": "https://t.me/dhsaidqhndi/1450",
    "lingvu_qism_17": "https://t.me/dhsaidqhndi/1451",
    "lingvu_qism_18": "https://t.me/dhsaidqhndi/1452",
    "lingvu_qism_19": "https://t.me/dhsaidqhndi/1453",
    "lingvu_qism_20": "https://t.me/dhsaidqhndi/1455",
    "lingvu_qism_21": "https://t.me/dhsaidqhndi/1456",
    "lingvu_qism_22": "https://t.me/dhsaidqhndi/1457",
    "lingvu_qism_23": "https://t.me/dhsaidqhndi/1459",
    "lingvu_qism_24": "https://t.me/dhsaidqhndi/1460",
    "lingvu_qism_25": "https://t.me/dhsaidqhndi/1461",
    "lingvu_qism_26": "https://t.me/dhsaidqhndi/1462",
    "lingvu_qism_27": "https://t.me/dhsaidqhndi/1676",
    "lingvu_qism_28": "https://t.me/dhsaidqhndi/2243",
    "lingvu_qism_29": "https://t.me/dhsaidqhndi/2244",
    "lingvu_qism_30": "https://t.me/dhsaidqhndi/2245",
    "lingvu_qism_31": "https://t.me/dhsaidqhndi/2299",
    "lingvu_qism_32": "https://t.me/dhsaidqhndi/2300",
    "lingvu_qism_33": "https://t.me/dhsaidqhndi/2316",
    "lingvu_qism_34": "https://t.me/dhsaidqhndi/2322",
    "lingvu_qism_35": "https://t.me/dhsaidqhndi/2347",
    "lingvu_qism_36": "https://t.me/dhsaidqhndi/2378",
    "lingvu_qism_37": "https://t.me/dhsaidqhndi/2379",
    "lingvu_qism_38": "https://t.me/dhsaidqhndi/2423",
    "lingvu_qism_39": "https://t.me/dhsaidqhndi/2424",
    "lingvu_qism_40": "https://t.me/dhsaidqhndi/2401",
    "lingvu_qism_41": "https://t.me/dhsaidqhndi/2404",
    "lingvu_qism_42": "https://t.me/dhsaidqhndi/2408",
    "lingvu_qism_43": "https://t.me/dhsaidqhndi/2517",
    "lingvu_qism_44": "https://t.me/dhsaidqhndi/2528",
    "lingvu_qism_45": "https://t.me/dhsaidqhndi/2532",
    "lingvu_qism_46": "https://t.me/dhsaidqhndi/2533",
    "lingvu_qism_47": "https://t.me/dhsaidqhndi/2617",
    "lingvu_qism_48": "https://t.me/dhsaidqhndi/2644",
    "lingvu_qism_49": "https://t.me/dhsaidqhndi/2618",
    "lingvu_qism_50": "https://t.me/dhsaidqhndi/2619",
    "lingvu_qism_51": "https://t.me/dhsaidqhndi/2620",
    "lingvu_qism_52": "https://t.me/dhsaidqhndi/2631",
    "lingvu_qism_53": "https://t.me/dhsaidqhndi/2673",
}

# ==================== KUCHLI SHOGIRDLAR ====================
@dp.message(F.text == "KUCHLI SHOGIRDLAR")
async def shogird_handler(message: types.Message):
    await message.answer(
        "💪 *Kuchli Shogirdlar* qismlarini tanlang:",
        reply_markup=get_shogird_page_keyboard(1),
        parse_mode="Markdown"
    )


@dp.callback_query(F.data.regexp(r"^shogird_page_\d+$"))
async def change_shogird_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(
        reply_markup=get_shogird_page_keyboard(page)
    )
    await callback.answer()


@dp.callback_query(F.data.regexp(r"^shogird_\d+$"))
async def send_shogird_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = shogird_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[1]

    caption = (
        "🎬 <b>Nomi:</b> KUCHLI SHOGIRDLAR\n"
        "🎞 <b>Janr:</b> Jangovar, Komediya, Sehrli\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniManhwa3D</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
    )

    await bot.send_video(
        callback.from_user.id,
        video_link,
        caption=caption,
        parse_mode="HTML",
        protect_content=True
    )

def get_shogird_page_keyboard(page: int):
    PER_PAGE = 20
    keys = sorted(shogird_videolar.keys(), key=lambda x: int(x.split("_")[1]))
    total_pages = (len(keys) + PER_PAGE - 1) // PER_PAGE

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    page_keys = keys[start:end]

    # Videolar tugmalari
    buttons = [
        [InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=key)]
        for i, key in enumerate(page_keys, start=start)
    ]

    # Navigatsiya tugmalari
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"shogird_page_{page-1}"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"shogird_page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎞 KUCHLI SHOGIRDLAR videolar ro'yxati
shogird_videolar = {
    "shogird_1": "https://t.me/dhsaidqhndi/2067",
    "shogird_2": "https://t.me/dhsaidqhndi/2068",
    "shogird_3": "https://t.me/dhsaidqhndi/2069",
    "shogird_4": "https://t.me/dhsaidqhndi/2070",
    "shogird_5": "https://t.me/dhsaidqhndi/2071",
    "shogird_6": "https://t.me/dhsaidqhndi/2072",
    "shogird_7": "https://t.me/dhsaidqhndi/2073",
    "shogird_8": "https://t.me/dhsaidqhndi/2074",
    "shogird_9": "https://t.me/dhsaidqhndi/2075",
    "shogird_10": "https://t.me/dhsaidqhndi/2076",
    "shogird_11": "https://t.me/dhsaidqhndi/2077",
    "shogird_12": "https://t.me/dhsaidqhndi/2078",
    "shogird_13": "https://t.me/dhsaidqhndi/2079",
    "shogird_14": "https://t.me/dhsaidqhndi/2080",
    "shogird_15": "https://t.me/dhsaidqhndi/2081",
    "shogird_16": "https://t.me/dhsaidqhndi/2082",
    "shogird_17": "https://t.me/dhsaidqhndi/2083",
    "shogird_18": "https://t.me/dhsaidqhndi/2084",
    "shogird_19": "https://t.me/dhsaidqhndi/2085",
    "shogird_20": "https://t.me/dhsaidqhndi/2086",
    "shogird_21": "https://t.me/dhsaidqhndi/2087",
    "shogird_22": "https://t.me/dhsaidqhndi/2088",
}

# ==================== JANG SAN’ATI CHO‘QQISI ====================
# 🥋 JANG SAN’ATI CHO‘QQISI — Asosiy menyu
@dp.message(F.text == "JANG SAN'ATI CHO'QQISI")
async def jang_sanati_handler(message: types.Message):
    await message.answer(
        "🥋 *Jang San’ati Cho‘qqisi* qismlarini tanlang:",
        reply_markup=get_jang_page_keyboard(1),
        parse_mode="Markdown"
    )


# 📄 Sahifa almashtirish (pagination)
@dp.callback_query(F.data.regexp(r"^jang_page_\d+$"))
async def change_jang_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_jang_page_keyboard(page))
    await callback.answer()


# 🎬 Video yuborish (qismni tanlanganda)
@dp.callback_query(F.data.regexp(r"^jang_sanati_\d+$"))
async def send_jang_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = jang_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> Jang San’ati Cho‘qqisi\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Jang, Fantastika, Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniManhwa3D))\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniManhwa3D</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "💬 “Jangchi hech qachon to‘xtamaydi — u doimo cho‘qqiga intiladi.” ⚔️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption.replace("*", "").replace("_", ""),
        protect_content=True,
        parse_mode="HTML"
    )

# 🔘 Sahifalangan tugmalar — 20 ta per sahifa
def get_jang_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(jang_videolar.keys())[start:end]

    buttons = []
    for i, key in enumerate(keys, start=start):
        buttons.append([
            InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"jang_sanati_{i+1}")
        ])

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"jang_page_{page-1}"))
    if end < len(jang_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"jang_page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Jang San'ati Cho'qqisi videolar ro'yxati:
jang_videolar = {
    "jang_sanati_1": "https://t.me/dhsaidqhndi/1713",
    "jang_sanati_2": "https://t.me/dhsaidqhndi/1714",
    "jang_sanati_3": "https://t.me/dhsaidqhndi/1715",
    "jang_sanati_4": "https://t.me/dhsaidqhndi/1716",
    "jang_sanati_5": "https://t.me/dhsaidqhndi/1717",
    "jang_sanati_6": "https://t.me/dhsaidqhndi/1718",
    "jang_sanati_7": "https://t.me/dhsaidqhndi/1719",
    "jang_sanati_8": "https://t.me/dhsaidqhndi/1720",
    "jang_sanati_9": "https://t.me/dhsaidqhndi/1721",
    "jang_sanati_10": "https://t.me/dhsaidqhndi/1722",
    "jang_sanati_11": "https://t.me/dhsaidqhndi/1723",
    "jang_sanati_12": "https://t.me/dhsaidqhndi/1724",
    "jang_sanati_13": "https://t.me/dhsaidqhndi/1725",
    "jang_sanati_14": "https://t.me/dhsaidqhndi/1726",
    "jang_sanati_15": "https://t.me/dhsaidqhndi/1727",
    "jang_sanati_16": "https://t.me/dhsaidqhndi/1728",
    "jang_sanati_17": "https://t.me/dhsaidqhndi/1729",
    "jang_sanati_18": "https://t.me/dhsaidqhndi/1730",
    "jang_sanati_19": "https://t.me/dhsaidqhndi/1731",
    "jang_sanati_20": "https://t.me/dhsaidqhndi/1732",
    "jang_sanati_21": "https://t.me/dhsaidqhndi/1733",
    "jang_sanati_22": "https://t.me/dhsaidqhndi/1734",
    "jang_sanati_23": "https://t.me/dhsaidqhndi/1735",
    "jang_sanati_24": "https://t.me/dhsaidqhndi/1736",
    "jang_sanati_25": "https://t.me/dhsaidqhndi/1737",
    "jang_sanati_26": "https://t.me/dhsaidqhndi/1738",
    "jang_sanati_27": "https://t.me/dhsaidqhndi/1739",
    "jang_sanati_28": "https://t.me/dhsaidqhndi/1740",
    "jang_sanati_29": "https://t.me/dhsaidqhndi/1741",
    "jang_sanati_30": "https://t.me/dhsaidqhndi/1742",
    "jang_sanati_31": "https://t.me/dhsaidqhndi/1743",
    "jang_sanati_32": "https://t.me/dhsaidqhndi/1744",
    "jang_sanati_33": "https://t.me/dhsaidqhndi/1745",
    "jang_sanati_34": "https://t.me/dhsaidqhndi/1746",
    "jang_sanati_35": "https://t.me/dhsaidqhndi/1747",
    "jang_sanati_36": "https://t.me/dhsaidqhndi/1748",
    "jang_sanati_37": "https://t.me/dhsaidqhndi/1749",
    "jang_sanati_38": "https://t.me/dhsaidqhndi/1750",
    "jang_sanati_39": "https://t.me/dhsaidqhndi/1751",
    "jang_sanati_40": "https://t.me/dhsaidqhndi/1752",
    "jang_sanati_41": "https://t.me/dhsaidqhndi/1753",
    "jang_sanati_42": "https://t.me/dhsaidqhndi/1754",
    "jang_sanati_43": "https://t.me/dhsaidqhndi/1755",
    "jang_sanati_44": "https://t.me/dhsaidqhndi/1756",
    "jang_sanati_45": "https://t.me/dhsaidqhndi/1757",
    "jang_sanati_46": "https://t.me/dhsaidqhndi/1758",
    "jang_sanati_47": "https://t.me/dhsaidqhndi/1759",
    "jang_sanati_48": "https://t.me/dhsaidqhndi/1760",
}

# ==================== YE FENNING SHONLI QASOSI ====================
@dp.message(F.text == "YE FENNING SHONLI QASOSI")
async def yefen_handler(message: types.Message):
    await message.answer(
        "🔥 *Ye Fenning Shonli Qasosi* qismlarini tanlang:",
        reply_markup=get_yefen_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^yefen_\d+$"))
async def send_yefen_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = yefen_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[1]
    caption = (
        "🎬 <b>Nomi:</b> Ye Fenning Shonli Qasosi\n"
        "🔥 <b>Janr:</b> Jang, Fantastika, Qi, Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniManhwa3D</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D\n"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^yefen_page_\d+$"))
async def change_yefen_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(
        reply_markup=get_yefen_page_keyboard(page)
    )
    await callback.answer()

def get_yefen_page_keyboard(page: int):
    keys = sorted(yefen_videolar.keys(), key=lambda x: int(x.split("_")[1]))
    total_pages = (len(keys) + VIDEOS_PER_PAGE - 1) // VIDEOS_PER_PAGE

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    page_keys = keys[start:end]

    buttons = [[InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=key)]
               for i, key in enumerate(page_keys, start=start)]

    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"yefen_page_{page-1}"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"yefen_page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Ye Fen videolar ro'yxati (misol)
yefen_videolar = {
    "yefen_1": "https://t.me/dhsaidqhndi/1910",
    "yefen_2": "https://t.me/dhsaidqhndi/1911",
    "yefen_3": "https://t.me/dhsaidqhndi/1912",
    "yefen_4": "https://t.me/dhsaidqhndi/1913",
    "yefen_5": "https://t.me/dhsaidqhndi/1914",
    "yefen_6": "https://t.me/dhsaidqhndi/1915",
    "yefen_7": "https://t.me/dhsaidqhndi/1916",
    "yefen_8": "https://t.me/dhsaidqhndi/1917",
    "yefen_9": "https://t.me/dhsaidqhndi/1918",
    "yefen_10": "https://t.me/dhsaidqhndi/1919",
    "yefen_11": "https://t.me/dhsaidqhndi/1920",
    "yefen_12": "https://t.me/dhsaidqhndi/1921",
    "yefen_13": "https://t.me/dhsaidqhndi/1922",
    "yefen_14": "https://t.me/dhsaidqhndi/1923",
    "yefen_15": "https://t.me/dhsaidqhndi/1924",
    "yefen_16": "https://t.me/dhsaidqhndi/1925",
    "yefen_17": "https://t.me/dhsaidqhndi/1926",
    "yefen_18": "https://t.me/dhsaidqhndi/1927",
    "yefen_19": "https://t.me/dhsaidqhndi/1928",
    "yefen_20": "https://t.me/dhsaidqhndi/1929",
    "yefen_21": "https://t.me/dhsaidqhndi/1930",
    "yefen_22": "https://t.me/dhsaidqhndi/1931",
    "yefen_23": "https://t.me/dhsaidqhndi/1932",
    "yefen_24": "https://t.me/dhsaidqhndi/1933",
    "yefen_25": "https://t.me/dhsaidqhndi/1934",
    "yefen_26": "https://t.me/dhsaidqhndi/1935",
    "yefen_27": "https://t.me/dhsaidqhndi/1936",
    "yefen_28": "https://t.me/dhsaidqhndi/1937",
    "yefen_29": "https://t.me/dhsaidqhndi/1938",
    "yefen_30": "https://t.me/dhsaidqhndi/1939",
    "yefen_31": "https://t.me/dhsaidqhndi/1940",
    "yefen_32": "https://t.me/dhsaidqhndi/1941",
    "yefen_33": "https://t.me/dhsaidqhndi/1942",
    "yefen_34": "https://t.me/dhsaidqhndi/1943",
    "yefen_35": "https://t.me/dhsaidqhndi/1944",
    "yefen_36": "https://t.me/dhsaidqhndi/1945",
    "yefen_37": "https://t.me/dhsaidqhndi/1946",
    "yefen_38": "https://t.me/dhsaidqhndi/1947",
    "yefen_39": "https://t.me/dhsaidqhndi/1948",
    "yefen_40": "https://t.me/dhsaidqhndi/1949",
    "yefen_41": "https://t.me/dhsaidqhndi/1950",
    "yefen_42": "https://t.me/dhsaidqhndi/1951",
    "yefen_43": "https://t.me/dhsaidqhndi/1952",
    "yefen_44": "https://t.me/dhsaidqhndi/1953",
}

# ==================== YAN CHEN AFSONASI ====================
# 🕊️ YAN CHEN AFSONASI — Asosiy menyu
@dp.message(F.text == "YAN CHEN AFSONASI")
async def yan_handler(message: types.Message):
    await message.answer(
        "🕊️ *Yan Chen Afsonasi* qismlarini tanlang:",
        reply_markup=get_yan_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^yan_page_\d+$"))
async def change_yan_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_yan_page_keyboard(page))
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^yan_\d+$"))
async def send_yan_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = yan_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]
    caption = (
        "🎬 <b>Nomi:</b> Yan Chen Afsonasi\n"
        "⚔️ <b>Janr:</b> Jang, Fantastika, Afsona\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @aust1n_griffin\n"
    )
    await bot.send_video(chat_id=callback.from_user.id, video=video_link, caption=caption, protect_content=True, parse_mode="HTML")

def get_yan_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(yan_videolar.keys())[start:end]
    buttons = [[InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"yan_{i+1}")] for i, key in enumerate(keys, start=start)]
    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"yan_page_{page-1}"))
    if end < len(yan_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"yan_page_{page+1}"))
    if navigation:
        buttons.append(navigation)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Yan Chen Afsonasi videolar ro'yxati:
yan_videolar = {
    "yan_1": "https://t.me/dhsaidqhndi/1868",
    "yan_2": "https://t.me/dhsaidqhndi/1869",
    "yan_3": "https://t.me/dhsaidqhndi/1870",
    "yan_4": "https://t.me/dhsaidqhndi/1871",
    "yan_5": "https://t.me/dhsaidqhndi/1872",
    "yan_6": "https://t.me/dhsaidqhndi/1873",
    "yan_7": "https://t.me/dhsaidqhndi/1874",
    "yan_8": "https://t.me/dhsaidqhndi/1875",
    "yan_9": "https://t.me/dhsaidqhndi/1876",
    "yan_10": "https://t.me/dhsaidqhndi/1877",
    "yan_11": "https://t.me/dhsaidqhndi/1878",
    "yan_12": "https://t.me/dhsaidqhndi/1879",
    "yan_13": "https://t.me/dhsaidqhndi/1880",
    "yan_14": "https://t.me/dhsaidqhndi/1881",
    "yan_15": "https://t.me/dhsaidqhndi/1882",
    "yan_16": "https://t.me/dhsaidqhndi/1883",
    "yan_17": "https://t.me/dhsaidqhndi/1884",
    "yan_18": "https://t.me/dhsaidqhndi/1885",
    "yan_19": "https://t.me/dhsaidqhndi/1886",
    "yan_20": "https://t.me/dhsaidqhndi/1887",
    "yan_21": "https://t.me/dhsaidqhndi/1888",
    "yan_22": "https://t.me/dhsaidqhndi/1889",
    "yan_23": "https://t.me/dhsaidqhndi/1890",
    "yan_24": "https://t.me/dhsaidqhndi/1891",
    "yan_25": "https://t.me/dhsaidqhndi/1892",
    "yan_26": "https://t.me/dhsaidqhndi/1893",
    "yan_27": "https://t.me/dhsaidqhndi/1894",
    "yan_28": "https://t.me/dhsaidqhndi/1895",
    "yan_29": "https://t.me/dhsaidqhndi/1896",
    "yan_30": "https://t.me/dhsaidqhndi/1897",
    "yan_31": "https://t.me/dhsaidqhndi/1898",
    "yan_32": "https://t.me/dhsaidqhndi/1899",
    "yan_33": "https://t.me/dhsaidqhndi/1900",
    "yan_34": "https://t.me/dhsaidqhndi/1901",
    "yan_35": "https://t.me/dhsaidqhndi/1902",
    "yan_36": "https://t.me/dhsaidqhndi/1903",
    "yan_37": "https://t.me/dhsaidqhndi/1904",
    "yan_38": "https://t.me/dhsaidqhndi/1905",
    "yan_39": "https://t.me/dhsaidqhndi/1906",
}

# ============= 📜 Mundareja 3-qism =============
@dp.message(F.text == "📜 Mundareja 3-qism")
async def mundareja_3_handler(message: types.Message):
    mundareja_3_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="O'LMASLAR DUNYOSI")],
            [KeyboardButton(text="YULDUZLI ILOHIY SAN'AT SIRLARI")],
            [KeyboardButton(text="AJDARHO SHAHZODA YUAN")],
            [KeyboardButton(text="BULUTLAR OG'USHIDAGI SAROBLAR")],
            [KeyboardButton(text="TUSHDAGI ILLUZIYA")],
            [KeyboardButton(text="QILICH USTASINING QAYTA TUG'ILISHI")],
            [KeyboardButton(text="ZI CHUAN AFSONASI")],
            [KeyboardButton(text="ILOHIY NAMOYON BO'LISH")],
            [KeyboardButton(text="DUNYOGA QARSHI TURGAN")],
            [KeyboardButton(text="ILOHIY OLAMLAR USTIDA")],
            [KeyboardButton(text="⬅️ Orqaga")],
        ],
        resize_keyboard=True
    )
    await message.answer("📜 Mundareja 3-qism bo‘limi:", reply_markup=mundareja_3_menu)

# ⬅️ Orqaga
@dp.message(F.text == "⬅️ Orqaga")
async def back_to_main(message: types.Message):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📜 Mundareja 1-qism")],
            [KeyboardButton(text="📜 Mundareja 2-qism")],
            [KeyboardButton(text="📜 Mundareja 3-qism")],
            [KeyboardButton(text="📜 Mundareja 4-qism")],
            [KeyboardButton(text="📜 Mundareja 5-qism")],
            [KeyboardButton(text="📜 KINOLAR")],
            [KeyboardButton(text="📢 Reklama va homiylik")],
            [KeyboardButton(text="📥 Video yuklab olish")],
            [KeyboardButton(text="📈 Statistika")],
            [KeyboardButton(text="👤 Admin")],
        ],
        resize_keyboard=True
    )
    await message.answer("🔙 Asosiy menyuga qaytdingiz", reply_markup=main_menu)

# ================== O'LMASLAR DUNYOSI ====================
@dp.message(F.text == "O'LMASLAR DUNYOSI")
async def olmaslar_handler(message: types.Message):
    await message.answer(
        "💀 *O‘lm aslar Dunnyosi* qismlarini tanlang:",
        reply_markup=get_olmas_page_keyboard(1),
        parse_mode="Markdown"
    )

# 📄 Sahifa almashtirish
@dp.callback_query(F.data.regexp(r"^olmas_page_\d+$"))
async def change_olmas_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_olmas_page_keyboard(page))
    await callback.answer()

# 🎬 Video yuborish
@dp.callback_query(F.data.regexp(r"^olmas_qism_\d+$"))
async def send_olmas_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = olmas_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "💀 <b>Nomi:</b> O‘lmaslar Dunnyosi\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Jangovar, Sehrli\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniManhwa3D)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "#olmaslar_dunyosi_animania\n\n"
        "💬 “Ba'zan kuch — qorong‘ulikda yashiringan haqiqatdir.” ⚔️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

# 🔘 Sahifalangan tugmalar
def get_olmas_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 10
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(olmas_videolar.keys())[start:end]

    buttons = []
    for key in keys:
        qism_raqami = key.split("_")[-1]
        buttons.append([
            InlineKeyboardButton(
                text=f"🎬 {qism_raqami}-qism",
                callback_data=key
            )
        ])

    navigation = []
    if page > 1:
        navigation.append(
            InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"olmas_page_{page-1}")
        )
    if end < len(olmas_videolar):
        navigation.append(
            InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"olmas_page_{page+1}")
        )

    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

olmas_videolar = {
    "olmas_qism_1": "https://t.me/dhsaidqhndi/2094",
    "olmas_qism_2": "https://t.me/dhsaidqhndi/2095",
    "olmas_qism_3": "https://t.me/dhsaidqhndi/2096",
    "olmas_qism_4": "https://t.me/dhsaidqhndi/2097",
    "olmas_qism_5": "https://t.me/dhsaidqhndi/2098",
    "olmas_qism_6": "https://t.me/dhsaidqhndi/2099",
    "olmas_qism_7": "https://t.me/dhsaidqhndi/2100",
    "olmas_qism_8": "https://t.me/dhsaidqhndi/2101",
    "olmas_qism_9": "https://t.me/dhsaidqhndi/2102",
    "olmas_qism_10": "https://t.me/dhsaidqhndi/2103",
    "olmas_qism_11": "https://t.me/dhsaidqhndi/2104",
    "olmas_qism_12": "https://t.me/dhsaidqhndi/2105",
    "olmas_qism_13": "https://t.me/dhsaidqhndi/2106",
    "olmas_qism_14": "https://t.me/dhsaidqhndi/2107",
    "olmas_qism_15": "https://t.me/dhsaidqhndi/2108",
    "olmas_qism_16": "https://t.me/dhsaidqhndi/2109",
    "olmas_qism_17": "https://t.me/dhsaidqhndi/2110",
    "olmas_qism_18": "https://t.me/dhsaidqhndi/2111",
    "olmas_qism_19": "https://t.me/dhsaidqhndi/2112",
    "olmas_qism_20": "https://t.me/dhsaidqhndi/2113",
    "olmas_qism_21": "https://t.me/dhsaidqhndi/2114",
    "olmas_qism_22": "https://t.me/dhsaidqhndi/2115",
    "olmas_qism_23": "https://t.me/dhsaidqhndi/2116",
    "olmas_qism_24": "https://t.me/dhsaidqhndi/2117",
    "olmas_qism_25": "https://t.me/dhsaidqhndi/2118",
    "olmas_qism_26": "https://t.me/dhsaidqhndi/2119",
}

# ==================== YULDUZLI ILOHIY SAN'AT SIRLARI ====================
@dp.message(F.text == "YULDUZLI ILOHIY SAN'AT SIRLARI")
async def yulduzli_handler(message: types.Message):
    await message.answer(
        "✨ *Yulduzli Ilohiy San'at Sirlari* qismlarini tanlang:",
        reply_markup=get_yulduzli_page_keyboard(1),
        parse_mode="Markdown"
    )


# 📄 Sahifa almashtirish
@dp.callback_query(F.data.regexp(r"^yulduzli_page_\d+$"))
async def change_yulduzli_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(
        reply_markup=get_yulduzli_page_keyboard(page)
    )
    await callback.answer()


# 🎬 Qism yuborish
@dp.callback_query(F.data.regexp(r"^yulduzli_\d+$"))
async def send_yulduzli_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = yulduzli_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> Yulduzli Ilohiy San'at Sirlari\n"
        "✨ <b>Janr:</b> Fantastika | Sehr | Jang\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "📌 <b>Premyera:</b> @AniManhwa3D\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "🏷 #yulduzli_ilohiy_sanat"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        parse_mode="HTML",
        protect_content=True
    )

def get_yulduzli_page_keyboard(page: int):
    per_page = 20
    keys = sorted(yulduzli_videolar.keys(), key=lambda x: int(x.split("_")[1]))
    total_pages = (len(keys) + per_page - 1) // per_page

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    start = (page - 1) * per_page
    end = start + per_page
    page_keys = keys[start:end]

    # 🎬 Video qismlari tugmalari
    buttons = [
        [InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=key)]
        for i, key in enumerate(page_keys, start=start)
    ]

    # ▶️ Navigatsiya tugmalari
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"yulduzli_page_{page-1}"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"yulduzli_page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 📺 Yulduzli Ilohiy San'at Sirlari videolar ro'yxati
yulduzli_videolar = {
    "yulduzli_1": "https://t.me/dhsaidqhndi/2259",
    "yulduzli_2": "https://t.me/dhsaidqhndi/2260",
    "yulduzli_3": "https://t.me/dhsaidqhndi/2261",
    "yulduzli_4": "https://t.me/dhsaidqhndi/2262",
    "yulduzli_5": "https://t.me/dhsaidqhndi/2263",
    "yulduzli_6": "https://t.me/dhsaidqhndi/2264",
    "yulduzli_7": "https://t.me/dhsaidqhndi/2265",
    "yulduzli_8": "https://t.me/dhsaidqhndi/2266",
    "yulduzli_9": "https://t.me/dhsaidqhndi/2267",
    "yulduzli_10": "https://t.me/dhsaidqhndi/2268",
    "yulduzli_11": "https://t.me/dhsaidqhndi/2269",
    "yulduzli_12": "https://t.me/dhsaidqhndi/2270",
    "yulduzli_13": "https://t.me/dhsaidqhndi/2271",
    "yulduzli_14": "https://t.me/dhsaidqhndi/2272",
    "yulduzli_15": "https://t.me/dhsaidqhndi/2273",
    "yulduzli_16": "https://t.me/dhsaidqhndi/2274",
    "yulduzli_17": "https://t.me/dhsaidqhndi/2275",
    "yulduzli_18": "https://t.me/dhsaidqhndi/2276",
    "yulduzli_19": "https://t.me/dhsaidqhndi/2277",
    "yulduzli_20": "https://t.me/dhsaidqhndi/2278",
    "yulduzli_21": "https://t.me/dhsaidqhndi/2279",
    "yulduzli_22": "https://t.me/dhsaidqhndi/2280",
    "yulduzli_23": "https://t.me/dhsaidqhndi/2281",
}

# ==================== BULUTLAR OG‘USHIDAGI SAROBLAR ====================
# ☁️ BULUTLAR OG‘USHIDAGI SAROBLAR — Asosiy menyu
@dp.message(F.text == "BULUTLAR OG'USHIDAGI SAROBLAR")
async def bulut_handler(message: types.Message):
    await message.answer(
        "☁️ *Bulutlar Og‘ushidagi Saroblar* qismlarini tanlang:",
        reply_markup=get_bulut_page_keyboard(1),
        parse_mode="Markdown"
    )


@dp.callback_query(F.data.regexp(r"^bulut_page_\d+$"))
async def change_bulut_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_bulut_page_keyboard(page))
    await callback.answer()


@dp.callback_query(F.data.regexp(r"^bulut_\d+$"))
async def send_bulut_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = bulut_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[-1]
    caption = (
        "🎬 <b>Nomi:</b> Bulutlar Og‘ushidagi Saroblar\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Sarguzasht, Romantik\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (Uzdubgo)\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@Uzdubgo</b>\n"
        "───────────────\n"
        "☁️ <b>Kanal:</b> @Uzdubgo | @bananatv_uz\n"
        "#bulut_saroblari\n\n"
        "💬 “Ba’zan eng yorqin saroblar — yurakdagi eng chuqur haqiqatni yashiradi.”"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )


def get_bulut_page_keyboard(page: int):
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    keys = list(bulut_videolar.keys())[start:end]

    buttons = [[InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"bulut_{i+1}")] for i in range(start, end) if i < len(bulut_videolar)]
    nav = []
    if start > 0:
        nav.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"bulut_page_{page-1}"))
    if end < len(bulut_videolar):
        nav.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"bulut_page_{page+1}"))
    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Bulutlar Og'ushidagi Saroblar videolar ro'yxati:
bulut_videolar = {
    "bulut_1": "https://t.me/dhsaidqhndi/1823",
    "bulut_2": "https://t.me/dhsaidqhndi/1824",
    "bulut_3": "https://t.me/dhsaidqhndi/1826",
    "bulut_4": "https://t.me/dhsaidqhndi/1960",
    "bulut_5": "https://t.me/dhsaidqhndi/1961",
    "bulut_6": "https://t.me/dhsaidqhndi/2307",
    "bulut_7": "https://t.me/dhsaidqhndi/2308",
    "bulut_8": "https://t.me/dhsaidqhndi/2309",
    "bulut_9": "https://t.me/dhsaidqhndi/2310",
    "bulut_10": "https://t.me/dhsaidqhndi/2311",
    "bulut_11": "https://t.me/dhsaidqhndi/2312",
    "bulut_12": "https://t.me/dhsaidqhndi/2301",
    "bulut_13": "https://t.me/dhsaidqhndi/2302",
    "bulut_14": "https://t.me/dhsaidqhndi/2331",
    "bulut_15": "https://t.me/dhsaidqhndi/2332",
    "bulut_16": "https://t.me/dhsaidqhndi/2333",
    "bulut_17": "https://t.me/dhsaidqhndi/2431",
    "bulut_18": "https://t.me/dhsaidqhndi/2432",
    "bulut_19": "https://t.me/dhsaidqhndi/2433",
    "bulut_20": "https://t.me/dhsaidqhndi/2434",
    "bulut_21": "https://t.me/dhsaidqhndi/2435",
    "bulut_22": "https://t.me/dhsaidqhndi/2436",
    "bulut_23": "https://t.me/dhsaidqhndi/2530",
    "bulut_24": "https://t.me/dhsaidqhndi/2531",
}

# ==================== TUSHDAGI ILLUZIYA ====================
# 🌙 TUSHDAGI ILLUZIYA — Asosiy menyu
@dp.message(F.text == "TUSHDAGI ILLUZIYA")
async def tushdagi_handler(message: types.Message):
    await message.answer(
        "🌙 *Tushdagi Illuziya* qismlarini tanlang:",
        reply_markup=get_tush_page_keyboard(1),
        parse_mode="Markdown"
    )


@dp.callback_query(F.data.regexp(r"^tush_page_\d+$"))
async def change_tush_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_tush_page_keyboard(page))
    await callback.answer()


@dp.callback_query(F.data.regexp(r"^tush_\d+$"))
async def send_tush_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = tush_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[-1]
    caption = (
        "🎬 <b>Nomi:</b> Tushdagi Illuziya\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Sirli, Sehrli, Psixologik\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (Anix)\n"
        "───────────────\n"
        "👁 <b>Kanal:</b> @aust1n_griffin\n"
        "#tushdagi_illuziya\n\n"
        "💬 “Ba’zan eng haqiqatga yaqin joy – tushlar olamidir.”"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )


def get_tush_page_keyboard(page: int):
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    keys = list(tush_videolar.keys())[start:end]

    buttons = [[InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"tush_{i+1}")] for i in range(start, end) if i < len(tush_videolar)]
    nav = []
    if start > 0:
        nav.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"tush_page_{page-1}"))
    if end < len(tush_videolar):
        nav.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"tush_page_{page+1}"))
    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Tushdagi Illuziya videolar ro'yxati:
tush_videolar = {
    "tush_1": "https://t.me/dhsaidqhndi/1827",
    "tush_2": "https://t.me/dhsaidqhndi/1828",
    "tush_3": "https://t.me/dhsaidqhndi/1829",
    "tush_4": "https://t.me/dhsaidqhndi/1830",
    "tush_5": "https://t.me/dhsaidqhndi/1831",
    "tush_6": "https://t.me/dhsaidqhndi/1832",
    "tush_7": "https://t.me/dhsaidqhndi/1833",
    "tush_8": "https://t.me/dhsaidqhndi/1955",
    "tush_9": "https://t.me/dhsaidqhndi/1956",
    "tush_10": "https://t.me/dhsaidqhndi/1957",
    "tush_11": "https://t.me/dhsaidqhndi/1958",
}

# ==================== QILICH USTASINING QAYTA TUG'ILISHI ====================
@dp.message(F.text == "QILICH USTASINING QAYTA TUG'ILISHI")
async def qilich_handler(message: types.Message):
    await message.answer(
        "⚔️ *Qilich Ustasining Qayta Tug'ilishi* qismlarini tanlang:",
        reply_markup=get_qilich_page_keyboard(1),
        parse_mode="Markdown"
    )

# 📄 Sahifa almashtirish
@dp.callback_query(F.data.regexp(r"^qilich_page_\d+$"))
async def change_qilich_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(
        reply_markup=get_qilich_page_keyboard(page)
    )
    await callback.answer()

# 🎬 Qism yuborish
@dp.callback_query(F.data.regexp(r"^qilich_\d+$"))
async def send_qilich_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = qilich_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[-1]

    caption = (
        "⚔️ <b>Nomi:</b> Qilich Ustasining Qayta Tug'ilishi\n"
        "🔥 <b>Janr:</b> Harbiy | Sehr | Reinkarnatsiya | Jang\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "📌 <b>Premyera:</b> @AniManhwa3D\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "🏷 #qilich_ustasi"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        parse_mode="HTML",
        protect_content=True
    )

# 🔘 Tugmalar — sahifalash
def get_qilich_page_keyboard(page: int):
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page

    keys = list(qilich_videolar.keys())[start:end]

    buttons = [
        [
            InlineKeyboardButton(
                text=f"🎬 {key.split('_')[1]}-qism",
                callback_data=key
            )
        ]
        for key in keys
    ]

    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"qilich_page_{page-1}"))
    if end < len(qilich_videolar):
        nav.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"qilich_page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 📺 Qilich Ustasi videolar ro'yxati:
qilich_videolar = {
    "qilich_1": "https://t.me/dhsaidqhndi/2338",
    "qilich_2": "https://t.me/dhsaidqhndi/2339",
    "qilich_3": "https://t.me/dhsaidqhndi/2341",
    "qilich_4": "https://t.me/dhsaidqhndi/2343",
    "qilich_5": "https://t.me/dhsaidqhndi/2344",
    "qilich_6": "https://t.me/dhsaidqhndi/2345",
    "qilich_7": "https://t.me/dhsaidqhndi/2346",
    "qilich_8": "https://t.me/dhsaidqhndi/2395",
    "qilich_9": "https://t.me/dhsaidqhndi/2409",
    "qilich_10": "https://t.me/dhsaidqhndi/2534",
    "qilich_11": "https://t.me/dhsaidqhndi/2535",
    "qilich_12": "https://t.me/dhsaidqhndi/2536",
    "qilich_13": "https://t.me/dhsaidqhndi/2537",
    "qilich_14": "https://t.me/dhsaidqhndi/2538",
    "qilich_15": "https://t.me/dhsaidqhndi/2645",
    "qilich_16": "https://t.me/dhsaidqhndi/2646",
    "qilich_17": "https://t.me/dhsaidqhndi/2647",
    "qilich_18": "https://t.me/dhsaidqhndi/2648",
    "qilich_19": "https://t.me/dhsaidqhndi/2649",
    "qilich_20": "https://t.me/dhsaidqhndi/2650",
    "qilich_21": "https://t.me/dhsaidqhndi/2651",
    "qilich_22": "https://t.me/dhsaidqhndi/2652",
    "qilich_23": "https://t.me/dhsaidqhndi/2653",
    "qilich_24": "https://t.me/dhsaidqhndi/2671",
    "qilich_25": "https://t.me/dhsaidqhndi/2674",
    "qilich_26": "",
    "qilich_27": "",
}

# ==================== ZI CHUAN AFSONASI ====================
# 🎥 ZI CHUAN AFSONASI — Asosiy menyu
@dp.message(F.text == "ZI CHUAN AFSONASI")
async def zi_chuan_handler(message: types.Message):
    await message.answer(
        "🐉 *Zi Chuan Afsonasi* qismlarini tanlang:",
        reply_markup=get_zi_chuan_page_keyboard(1),
        parse_mode="Markdown"
    )


# 📄 Sahifa almashtirish (pagination)
@dp.callback_query(F.data.regexp(r"^zi_chuan_page_\d+$"))
async def change_zi_chuan_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[3])
    await callback.message.edit_reply_markup(reply_markup=get_zi_chuan_page_keyboard(page))
    await callback.answer()


# 🎬 Video yuborish (ma’lumotli tarzda)
@dp.callback_query(F.data.regexp(r"^zi_chuan_\d+$"))
async def send_zi_chuan_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = zi_chuan_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> Zi Chuan Afsonasi\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Sehrli, Jangovar, Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 480p\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @aust1n_griffin\n"
        "💬 “Har bir afsona orqasida haqiqat yotadi — uni anglaganlar kuchga ega bo‘ladi.” ⚔️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption.replace("*", "").replace("_", ""),
        protect_content=True,
        parse_mode="HTML"
    )


# 🔘 Sahifalangan tugmalar — 20 ta per page
def get_zi_chuan_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(zi_chuan_videolar.keys())[start:end]

    buttons = []
    for i, key in enumerate(keys, start=start):
        buttons.append([
            InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"zi_chuan_{i+1}")
        ])

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"zi_chuan_page_{page-1}"))
    if end < len(zi_chuan_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"zi_chuan_page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Zi Chuan Afsonasi videolar ro'yxati:
zi_chuan_videolar = {
    "zi_chuan_1": "https://t.me/dhsaidqhndi/1681",
    "zi_chuan_2": "https://t.me/dhsaidqhndi/1682",
    "zi_chuan_3": "https://t.me/dhsaidqhndi/1683",
    "zi_chuan_4": "https://t.me/dhsaidqhndi/1684",
    "zi_chuan_5": "https://t.me/dhsaidqhndi/1685",
    "zi_chuan_6": "https://t.me/dhsaidqhndi/1686",
    "zi_chuan_7": "https://t.me/dhsaidqhndi/1687",
    "zi_chuan_8": "https://t.me/dhsaidqhndi/1688",
    "zi_chuan_9": "https://t.me/dhsaidqhndi/1689",
    "zi_chuan_10": "https://t.me/dhsaidqhndi/1690",
    "zi_chuan_11": "https://t.me/dhsaidqhndi/1691",
    "zi_chuan_12": "https://t.me/dhsaidqhndi/1692",
    "zi_chuan_13": "https://t.me/dhsaidqhndi/1693",
    "zi_chuan_14": "https://t.me/dhsaidqhndi/1694",
    "zi_chuan_15": "https://t.me/dhsaidqhndi/1695",
    "zi_chuan_16": "https://t.me/dhsaidqhndi/1696",
    "zi_chuan_17": "https://t.me/dhsaidqhndi/1697",
    "zi_chuan_18": "https://t.me/dhsaidqhndi/1698",
}

# ==================== ILOHIY NAMOYON BO'LISH ====================
@dp.message(F.text == "ILOHIY NAMOYON BO'LISH")
async def ilohiy_handler(message: types.Message):
    await message.answer(
        "✨ *Ilohiy Namoyon Bo'lish* qismlarini tanlang:",
        reply_markup=get_ilohiy_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^ilohiy_page_\d+$"))
async def change_ilohiy_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_ilohiy_page_keyboard(page))
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^ilohiy_qism_\d+$"))
async def send_ilohiy_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = ilohiy_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[-1]

    caption = (
        "✨ <b>Nomi:</b> Ilohiy Namoyon Bo'lish\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Ilohiy kuch, Sehrli\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniManhwa3D)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "#ilohiy_namoyon_animania\n\n"
        "💬 “Ilohiy kuch qalbingda uyg‘onsa — taqdir yo‘lini sen belgilaysan.” ✨"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

def get_ilohiy_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 10
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(ilohiy_videolar.keys())[start:end]

    buttons = []
    for key in keys:
        qism = key.split("_")[-1]
        buttons.append([InlineKeyboardButton(
            text=f"🎬 {qism}-qism",
            callback_data=key
        )])

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"ilohiy_page_{page-1}"))
    if end < len(ilohiy_videolar):
        navigation.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"ilohiy_page_{page+1}"))

    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Ilohiy Namoyon Bo'lish videolar ro'yxati:
ilohiy_videolar = {
    "ilohiy_qism_1": "https://t.me/dhsaidqhndi/2406",
    "ilohiy_qism_2": "https://t.me/dhsaidqhndi/2410",
    "ilohiy_qism_3": "https://t.me/dhsaidqhndi/2475",
    "ilohiy_qism_4": "https://t.me/dhsaidqhndi/2476",
    "ilohiy_qism_5": "https://t.me/dhsaidqhndi/2654",
    "ilohiy_qism_6": "https://t.me/dhsaidqhndi/2655",
    "ilohiy_qism_7": "https://t.me/dhsaidqhndi/2656",
    "ilohiy_qism_8": "https://t.me/dhsaidqhndi/2657",
    "ilohiy_qism_9": "https://t.me/dhsaidqhndi/2658",
}

# ==================== DUNYOGA QARSHI TURGAN ====================
@dp.message(F.text == "DUNYOGA QARSHI TURGAN")
async def dunyoqarshi_handler(message: types.Message):
    await message.answer(
        "⚔️ *Dunyoga Qarshi Turgan* qismlarini tanlang:",
        reply_markup=get_dqt_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^dqt_page_\d+$"))
async def change_dqt_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_dqt_page_keyboard(page))
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^dqt_qism_\d+$"))
async def send_dqt_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = dqt_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[-1]

    caption = (
        "⚔️ <b>Nomi:</b> Dunyoga Qarshi Turgan\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Jangovar, Fantastika, Drama\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniManhwa3D)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "#dqt_animania\n\n"
        "💬 “Dunyo sening qarshingda bo‘lsa ham — kuching irodangdadir.” ⚔️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

def get_dqt_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 10
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(dqt_videolar.keys())[start:end]

    buttons = []
    for key in keys:
        qism = key.split("_")[-1]
        buttons.append([InlineKeyboardButton(
            text=f"🎬 {qism}-qism",
            callback_data=key
        )])

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"dqt_page_{page-1}"))
    if end < len(dqt_videolar):
        navigation.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"dqt_page_{page+1}"))

    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Dunyoga Qarshi Turgan videolar ro'yxati:
dqt_videolar = {
    "dqt_qism_1": "https://t.me/dhsaidqhndi/2407",
    "dqt_qism_2": "https://t.me/dhsaidqhndi/2473",
    "dqt_qism_3": "https://t.me/dhsaidqhndi/2484",
    "dqt_qism_4": "https://t.me/dhsaidqhndi/2669",
    "dqt_qism_5": "https://t.me/dhsaidqhndi/2670",
    "dqt_qism_6": "https://t.me/dhsaidqhndi/2672",
    "dqt_qism_7": "",
}

# ==================== ILOHIY OLAMLAR USTIDA ====================
# 🎥 ILOHIY OLAMLAR USTIDA — Asosiy menyu
@dp.message(F.text == "ILOHIY OLAMLAR USTIDA")
async def ilohiy_handler(message: types.Message):
    await message.answer(
        "🌌 *Ilohiy Olamlar Ustida* qismlarini tanlang:",
        reply_markup=get_ilohiy_page_keyboard(1),
        parse_mode="Markdown"
    )


# 📄 Sahifa almashtirish (pagination)
@dp.callback_query(F.data.regexp(r"^ilohiy_page_\d+$"))
async def change_ilohiy_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_ilohiy_page_keyboard(page))
    await callback.answer()


# 🎬 Video yuborish (ma’lumotli tarzda)
@dp.callback_query(F.data.regexp(r"^ilohiy_\d+$"))
async def send_ilohiy_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = ilohiy_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> Ilohiy Olamlar Ustida\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Sehrli, Jangovar, Ruhiy\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniManhwa)\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniManhwa3D</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManwha3D\n"
        "#ilohiy_olamlar_animania\n\n"
        "💬 “Ilohiy kuchni his qilgan yurak hech qachon qorong‘ilikda yo‘qolmaydi.” ✨"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption.replace("*", "").replace("_", ""),
        protect_content=True,
        parse_mode="HTML"
    )


# 🔘 Sahifalangan tugmalar — 20 ta per page
def get_ilohiy_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(ilohiy_videolar.keys())[start:end]

    buttons = []
    for i, key in enumerate(keys, start=start):
        buttons.append([
            InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"ilohiy_{i+1}")
        ])

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"ilohiy_page_{page-1}"))
    if end < len(ilohiy_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"ilohiy_page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Ilohiy Olamlar Ustida videolar ro'yxati:
ilohiy_videolar = {
    "ilohiy_1": "https://t.me/dhsaidqhndi/1699",
    "ilohiy_2": "https://t.me/dhsaidqhndi/1700",
    "ilohiy_3": "https://t.me/dhsaidqhndi/1701",
    "ilohiy_4": "https://t.me/dhsaidqhndi/1702",
    "ilohiy_5": "https://t.me/dhsaidqhndi/1703",
    "ilohiy_6": "https://t.me/dhsaidqhndi/1704",
    "ilohiy_7": "https://t.me/dhsaidqhndi/1705",
    "ilohiy_8": "https://t.me/dhsaidqhndi/1706",
    "ilohiy_9": "https://t.me/dhsaidqhndi/1707",
    "ilohiy_10": "https://t.me/dhsaidqhndi/1708",
    "ilohiy_11": "https://t.me/dhsaidqhndi/1709",
    "ilohiy_12": "https://t.me/dhsaidqhndi/1767",
    "ilohiy_13": "https://t.me/dhsaidqhndi/2120",
    "ilohiy_14": "https://t.me/dhsaidqhndi/2121",
    "ilohiy_15": "https://t.me/dhsaidqhndi/2246",
    "ilohiy_16": "https://t.me/dhsaidqhndi/2247",
    "ilohiy_17": "https://t.me/dhsaidqhndi/2304",
}

# ============= 📜 Mundareja 4-qism =============
@dp.message(F.text == "📜 Mundareja 4-qism")
async def mundareja_4_handler(message: types.Message):
    mundareja_4_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="O'LMAS IMPERATORNING QAYTISHI")],
            [KeyboardButton(text="JANGOVAR INVERSIYA")],
            [KeyboardButton(text="MALIKA CHON-GE HAQIDAGI AFSONA")],
            [KeyboardButton(text="OLTIN VUG")],
            [KeyboardButton(text="MABUDLAR QOTILI")],
            [KeyboardButton(text="BOQIYLIKKA SAYOHAT")],
            [KeyboardButton(text="TALABALAR KARTALARI")],
            [KeyboardButton(text="OSMON ILOHI")],
            [KeyboardButton(text="ASKAR AFSONASI")],
            [KeyboardButton(text="⬅️ Orqaga")],
        ],
        resize_keyboard=True
    )
    await message.answer("📜 Mundareja 4-qism bo‘limi:", reply_markup=mundareja_4_menu)

# ⬅️ Orqaga
@dp.message(F.text == "⬅️ Orqaga")
async def back_to_main(message: types.Message):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📜 Mundareja 1-qism")],
            [KeyboardButton(text="📜 Mundareja 2-qism")],
            [KeyboardButton(text="📜 Mundareja 3-qism")],
            [KeyboardButton(text="📜 Mundareja 4-qism")],
            [KeyboardButton(text="📜 Mundareja 5-qism")],
            [KeyboardButton(text="📜 KINOLAR")],
            [KeyboardButton(text="📢 Reklama va homiylik")],
            [KeyboardButton(text="📥 Video yuklab olish")],
            [KeyboardButton(text="📈 Statistika")],
            [KeyboardButton(text="👤 Admin")],
        ],
        resize_keyboard=True
    )
    await message.answer("🔙 Asosiy menyuga qaytdingiz", reply_markup=main_menu)

# ==================== O‘LMAS IMPERATORNING QAYTISHI ====================
@dp.message(F.text == "O'LMAS IMPERATORNING QAYTISHI")
async def olmas_imperator_handler(message: types.Message):
    await message.answer(
        "⚔️ *O‘lmas Imperatorning Qaytishi* qismlarini tanlang:",
        reply_markup=get_olmas_page_keyboard(1),
        parse_mode="Markdown"
    )


# 📄 Sahifa almashtirish
@dp.callback_query(F.data.regexp(r"^olmas_page_\d+$"))
async def change_olmas_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(
        reply_markup=get_olmas_page_keyboard(page)
    )
    await callback.answer()


# 🎬 Video yuborish
@dp.callback_query(F.data.regexp(r"^olmas_imperator_\d+$"))
async def send_olmas_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = olmas_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> O‘lmas Imperatorning Qaytishi\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Sehr, Jang, Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniManhwa3D)\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniManhwa3D</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "#olmas_imperator_animania\n\n"
        "💬 “Haqiqiy kuch o‘limdan qaytgan yurakda yashaydi.” ⚔️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

# 🔘 Sahifalangan tugmalar — 20ta per page
def get_olmas_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20
    keys = list(olmas_videolar.keys())

    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    page_keys = keys[start:end]

    buttons = []
    for key in page_keys:
        qism = key.split("_")[-1]
        buttons.append([
            InlineKeyboardButton(
                text=f"🎬 {qism}-qism",
                callback_data=key
            )
        ])

    # Navigatsiya tugmalari
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"olmas_page_{page-1}"))
    if end < len(keys):
        nav.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"olmas_page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# O'lmas Imperatorning Qaytishi videolar ro'yxati:
olmas_videolar = {
    "olmas_imperator_1": "https://t.me/dhsaidqhndi/1710",
    "olmas_imperator_2": "https://t.me/dhsaidqhndi/1711",
    "olmas_imperator_3": "https://t.me/dhsaidqhndi/1712",
    "olmas_imperator_4": "https://t.me/dhsaidqhndi/2248",
    "olmas_imperator_5": "https://t.me/dhsaidqhndi/2306",
    "olmas_imperator_6": "https://t.me/dhsaidqhndi/2314",
    "olmas_imperator_7": "https://t.me/dhsaidqhndi/2384",
    "olmas_imperator_8": "https://t.me/dhsaidqhndi/2427",
    "olmas_imperator_9": "https://t.me/dhsaidqhndi/2529",
    "olmas_imperator_10": "https://t.me/dhsaidqhndi/2639",
    "olmas_imperator_11": "https://t.me/dhsaidqhndi/2640",
}

# ==================== JANGOVAR INVERSIYA ====================
# ⚔️ JANGOVAR INVERSIYA — Asosiy menyu
@dp.message(F.text == "JANGOVAR INVERSIYA")
async def inversiya_handler(message: types.Message):
    await message.answer(
        "⚔️ *Jangovar Inversiya* qismlarini tanlang:",
        reply_markup=get_inversiya_page_keyboard(1),
        parse_mode="Markdown"
    )

# 📄 Sahifa almashtirish (pagination)
@dp.callback_query(F.data.regexp(r"^inversiya_page_\d+$"))
async def change_inversiya_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_inversiya_page_keyboard(page))
    await callback.answer()

# 🎬 Video yuborish
@dp.callback_query(F.data.regexp(r"^inversiya_\d+$"))
async def send_inversiya_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = inversiya_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> Jangovar Inversiya\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Jangovar, Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniManhwa)\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniManhwa3D</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManwha3D\n"
        "#jangovar_inversiya_animania\n\n"
        "💬 “Haqiqiy kuch — o‘z qo‘rquvingni yengishdan boshlanadi.” ⚔️"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )


# 🔘 Sahifalangan tugmalar — 20 ta per page
def get_inversiya_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(inversiya_videolar.keys())[start:end]

    buttons = []
    for i, key in enumerate(keys, start=start):
        buttons.append([
            InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"inversiya_{i+1}")
        ])

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"inversiya_page_{page-1}"))
    if end < len(inversiya_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"inversiya_page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎞 JANGOVAR INVERSIYA videolar ro'yxati
inversiya_videolar = {
    "inversiya_1": "https://t.me/dhsaidqhndi/1963",
    "inversiya_2": "https://t.me/dhsaidqhndi/1964",
    "inversiya_3": "https://t.me/dhsaidqhndi/1965",
    "inversiya_4": "https://t.me/dhsaidqhndi/1966",
    "inversiya_5": "https://t.me/dhsaidqhndi/1967",
    "inversiya_6": "https://t.me/dhsaidqhndi/1968",
    "inversiya_7": "https://t.me/dhsaidqhndi/1969",
    "inversiya_8": "https://t.me/dhsaidqhndi/1970",
    "inversiya_9": "https://t.me/dhsaidqhndi/1971",
    "inversiya_10": "https://t.me/dhsaidqhndi/1972",
    "inversiya_11": "https://t.me/dhsaidqhndi/1973",
    "inversiya_12": "https://t.me/dhsaidqhndi/1974",
    "inversiya_13": "https://t.me/dhsaidqhndi/1975",
    "inversiya_14": "https://t.me/dhsaidqhndi/1976",
    "inversiya_15": "https://t.me/dhsaidqhndi/1977",
    "inversiya_16": "https://t.me/dhsaidqhndi/1978",
}

# ==================== MALIKA CHON-GE HAQIDAGI AFSONA ====================
@dp.message(F.text == "MALIKA CHON-GE HAQIDAGI AFSONA")
async def malika_handler(message: types.Message):
    await message.answer(
        "👸 *Malika Chon-Ge haqidagi Afsona* qismlarini tanlang:",
        reply_markup=get_malika_page_keyboard(1),
        parse_mode="Markdown"
    )

# 📄 Sahifa almashtirish (pagination)
@dp.callback_query(F.data.regexp(r"^malika_page_\d+$"))
async def change_malika_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(
        reply_markup=get_malika_page_keyboard(page)
    )
    await callback.answer()

# 🎬 Video yuborish
@dp.callback_query(F.data.regexp(r"^malika_\d+$"))
async def send_malika_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = malika_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> Malika Chon-Ge haqidagi Afsona\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Sarguzasht, Sehrli, Tarixiy, Fantastik\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (Uzdubgo)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @Uzdubgo | @bananatv_uz\n"
        "#malika_chonge_animania\n\n"
        "💬 “Haqiqiy malika — jasorat va donolik bilan sinovlardan o‘tadi.” 👸✨"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption.replace("*", "").replace("_", ""),
        protect_content=True,
        parse_mode="HTML"
    )

# 🔘 Sahifalangan tugmalar — 20 ta per page
def get_malika_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE

    keys = list(malika_videolar.keys())[start:end]

    buttons = []
    for i, key in enumerate(keys, start=start):
        buttons.append([
            InlineKeyboardButton(
                text=f"🎬 {i+1}-qism",
                callback_data=f"malika_{i+1}"
            )
        ])

    # Navigatsiya tugmalari
    navigation = []
    if page > 1:
        navigation.append(
            InlineKeyboardButton("⬅️ Oldingi", callback_data=f"malika_page_{page-1}")
        )
    if end < len(malika_videolar):
        navigation.append(
            InlineKeyboardButton("➡️ Keyingi", callback_data=f"malika_page_{page+1}")
        )

    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Malika Chan-Ge haqidagi afsona videolar ro'yxati:
malika_videolar = {
    "malika_1": "https://t.me/dhsaidqhndi/2351",
    "malika_2": "https://t.me/dhsaidqhndi/2352",
    "malika_3": "https://t.me/dhsaidqhndi/2353",
}

# ==================== OLTIN VUG ====================
@dp.message(F.text == "OLTIN VUG")
async def oltinvug_handler(message: types.Message):
    await message.answer(
        "🏆 *Oltin Vug* qismlarini tanlang:",
        reply_markup=get_oltinvug_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^oltinvug_page_\d+$"))
async def change_oltinvug_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_oltinvug_page_keyboard(page))
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^oltinvug_\d+$"))
async def send_oltinvug_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = oltinvug_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[-1]
    caption = (
        "🎬 <b>Nomi:</b> Oltin Vug\n"
        "🏆 <b>Janr:</b> Sarguzasht | Qi | Fantastika\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "📌 <b>Premyera:</b> @AniManhwa3D\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "🏷 #oltin_vug"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        parse_mode="HTML",
        protect_content=True
    )

def get_oltinvug_page_keyboard(page: int):
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    keys = list(oltinvug_videolar.keys())[start:end]

    buttons = [
    [InlineKeyboardButton(text=f"🎬 {key.split('_')[-1]}-qism", callback_data=key)]
    for key in keys
]

    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"oltinvug_page_{page-1}"))
    if end < len(oltinvug_videolar):
        nav.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"oltinvug_page_{page+1}"))
    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Oltin Vug videolar ro'yxati:
oltinvug_videolar = {
    "oltinvug_1": "https://t.me/dhsaidqhndi/2282",
    "oltinvug_2": "https://t.me/dhsaidqhndi/2283",
    "oltinvug_3": "https://t.me/dhsaidqhndi/2284",
    "oltinvug_4": "https://t.me/dhsaidqhndi/2285",
    "oltinvug_5": "https://t.me/dhsaidqhndi/2286",
    "oltinvug_6": "https://t.me/dhsaidqhndi/2287",
    "oltinvug_7": "https://t.me/dhsaidqhndi/2288",
    "oltinvug_8": "https://t.me/dhsaidqhndi/2289",
    "oltinvug_9": "https://t.me/dhsaidqhndi/2290",
    "oltinvug_10": "https://t.me/dhsaidqhndi/2291",
    "oltinvug_11": "https://t.me/dhsaidqhndi/2292",
}

# ==================== MABUDLAR QOTILI ====================
@dp.message(F.text == "MABUDLAR QOTILI")
async def mabud_handler(message: types.Message):
    await message.answer("⚔️ *Mabudlar Qotili* qismlarini tanlang:", reply_markup=get_mabud_page_keyboard(1), parse_mode="Markdown")

@dp.callback_query(F.data.regexp(r"^mabud_page_\d+$"))
async def change_mabud_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_mabud_page_keyboard(page))
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^mabud_\d+$"))
async def send_mabud_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = mabud_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return
    qism = key.split("_")[-1]
    caption = (
        "🎬 <b>Nomi:</b> Mabudlar Qotili\n"
        "🎞 <b>Janr:</b> Fantastika, Jangovar, Sehrli\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniManhwa3D</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D\n"
    )
    await bot.send_video(callback.from_user.id, video_link, caption=caption, parse_mode="HTML", protect_content=True)

def get_mabud_page_keyboard(page: int):
    per_page=20; start=(page-1)*per_page; end=start+per_page
    keys=list(mabud_videolar.keys())[start:end]
    buttons=[[InlineKeyboardButton(text=f"🎬 {i+1}-qism",callback_data=f"mabud_{i+1}")] for i,_ in enumerate(keys,start=start)]
    nav=[]
    if page>1: nav.append(InlineKeyboardButton("⬅️ Oldingi",callback_data=f"mabud_page_{page-1}"))
    if end<len(mabud_videolar): nav.append(InlineKeyboardButton("➡️ Keyingi",callback_data=f"mabud_page_{page+1}"))
    if nav: buttons.append(nav)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎞 MABUDLAR QOTILI videolar ro'yxati
mabud_videolar = {
    "mabud_1": "https://t.me/dhsaidqhndi/1979",
    "mabud_2": "https://t.me/dhsaidqhndi/1980",
    "mabud_3": "https://t.me/dhsaidqhndi/1981",
    "mabud_4": "https://t.me/dhsaidqhndi/1982",
    "mabud_5": "https://t.me/dhsaidqhndi/1983",
    "mabud_6": "https://t.me/dhsaidqhndi/1984",
    "mabud_7": "https://t.me/dhsaidqhndi/1985",
    "mabud_8": "https://t.me/dhsaidqhndi/1986",
    "mabud_9": "https://t.me/dhsaidqhndi/1987",
    "mabud_10": "https://t.me/dhsaidqhndi/1988",
    "mabud_11": "https://t.me/dhsaidqhndi/1989",
    "mabud_12": "https://t.me/dhsaidqhndi/2129",
    "mabud_13": "https://t.me/dhsaidqhndi/2130",
    "mabud_14": "https://t.me/dhsaidqhndi/2131",
    "mabud_15": "https://t.me/dhsaidqhndi/2141",
}

# ==================== BOQIYLIKKA SAYOHAT ====================
@dp.message(F.text == "BOQIYLIKKA SAYOHAT")
async def boqiylik_handler(message: types.Message):
    await message.answer(
        "🌌 *Boqiylikka Sayohat* qismlarini tanlang:",
        reply_markup=get_boqiylik_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^boqiylik_page_\d+$"))
async def change_boqiylik_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(
        reply_markup=get_boqiylik_page_keyboard(page)
    )
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^boqiylik_\d+$"))
async def send_boqiylik_video(callback: types.CallbackQuery):
    key = callback.data
    link = boqiylik_videolar.get(key)

    if not link:
        await callback.answer("❌ Bu qism mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[1]

    caption = (
        f"🎬 <b>Nomi:</b> Boqiylikka Sayohat\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniMania_rasmiy</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniMania_rasmiy\n"
    )

    await bot.send_video(
        callback.from_user.id,
        link,
        caption=caption,
        parse_mode="HTML",
        protect_content=True
    )

def get_boqiylik_page_keyboard(page: int):
    PER_PAGE = 20
    keys = list(boqiylik_videolar.keys())

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    page_keys = keys[start:end]

    buttons = []
    for key in page_keys:
        qism = key.split("_")[1]  # masalan: boqiylik_7 → 7
        buttons.append([
            InlineKeyboardButton(
                text=f"🎬 {qism}-qism",
                callback_data=key
            )
        ])

    navigation = []
    if page > 1:
        navigation.append(
            InlineKeyboardButton("⬅️ Oldingi", callback_data=f"boqiylik_page_{page-1}")
        )
    if end < len(keys):
        navigation.append(
            InlineKeyboardButton("➡️ Keyingi", callback_data=f"boqiylik_page_{page+1}")
        )

    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎞 BOQIYLIKKA SAYOHAT videolar ro'yxati
boqiylik_videolar = {
    "boqiylik_1": "https://t.me/dhsaidqhndi/1999",
    "boqiylik_2": "https://t.me/dhsaidqhndi/2000",
    "boqiylik_3": "https://t.me/dhsaidqhndi/2001",
    "boqiylik_4": "https://t.me/dhsaidqhndi/2002",
    "boqiylik_5": "https://t.me/dhsaidqhndi/2003",
    "boqiylik_6": "https://t.me/dhsaidqhndi/2004",
    "boqiylik_7": "https://t.me/dhsaidqhndi/2005",
    "boqiylik_8": "https://t.me/dhsaidqhndi/2006",
    "boqiylik_9": "https://t.me/dhsaidqhndi/2007",
    "boqiylik_10": "https://t.me/dhsaidqhndi/2641",
    "boqiylik_11": "https://t.me/dhsaidqhndi/2642",
    "boqiylik_12": "https://t.me/dhsaidqhndi/2643",
}

# ==================== TALABALAR KARTALARI ====================
@dp.message(F.text == "TALABALAR KARTALARI")
async def karta_handler(message: types.Message):
    await message.answer(
        "🎓 *Talabalar Kartalari* qismlarini tanlang:",
        reply_markup=get_karta_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^karta_page_\d+$"))
async def change_karta_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_karta_page_keyboard(page))
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^karta_\d+$"))
async def send_karta_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = karta_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> TALABALAR KARTALARI\n"
        "🎞 <b>Janr:</b> Komediya | Akademiya | Fantastika\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "📌 <b>Premyera va yangi qismlar:</b> <b>@AniManhwa3D</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "🏷 #talabalar_kartalari"
    )

    await bot.send_video(
        callback.from_user.id,
        video_link,
        caption=caption,
        parse_mode="HTML",
        protect_content=True
    )

def get_karta_page_keyboard(page: int):
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page

    keys = list(karta_videolar.keys())[start:end]

    buttons = [
    [
        InlineKeyboardButton(
            text=f"🎬 {i+1}-qism",
            callback_data=f"karta_{i+1}"
        )
    ]
    for i, _ in enumerate(keys, start=start)
]

    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"karta_page_{page-1}"))
    if end < len(karta_videolar):
        nav.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"karta_page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎞 TALABALAR KARTALARI videolar ro'yxati
karta_videolar = {
    "karta_1": "https://t.me/dhsaidqhndi/2089",
    "karta_2": "https://t.me/dhsaidqhndi/2090",
    "karta_3": "https://t.me/dhsaidqhndi/2091",
    "karta_4": "https://t.me/dhsaidqhndi/2092",
    "karta_5": "https://t.me/dhsaidqhndi/2093",
}

# ==================== OSMON ILOHI ====================
@dp.message(F.text == "OSMON ILOHI")
async def osmon_ilohi_handler(message: types.Message):
    await message.answer(
        "🌌 *Osmon Ilohi* qismlarini tanlang:",
        reply_markup=get_osmon_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^osmon_page_\d+$"))
async def change_osmon_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_osmon_page_keyboard(page))
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^osmon_ilohi_\d+$"))
async def send_osmon_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = osmon_ilohi_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> OSMON ILOHI\n"
        "🎞 <b>Janr:</b> Fantastika | Sehrli | Jangovar | Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "📌 <b>Premyera va yangi qismlar:</b> <b>@Donghualar_uzb</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @Donghualar_uzb | @aust1n_griffin\n"
        "🏷 #osmon_ilohi\n"
        "───────────────\n"
        "💬 <i>“Osmonning kuchi — uni qalban munosiblarga ato etiladi.”</i> 🌌"
    )

    await bot.send_video(
        callback.from_user.id,
        video_link,
        caption=caption,
        parse_mode="HTML",
        protect_content=True
    )


def get_osmon_page_keyboard(page: int):
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page

    keys = list(osmon_ilohi_videolar.keys())[start:end]

    buttons = [
    [InlineKeyboardButton(text=f"🎬 {key.split('_')[-1]}-qism", callback_data=key)]
    for key in keys
]

    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"osmon_page_{page-1}"))
    if end < len(osmon_ilohi_videolar):
        nav.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"osmon_page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Osmon Ilohi videolar ro'yxati:
osmon_ilohi_videolar = {
    "osmon_ilohi_1": "https://t.me/dhsaidqhndi/2136",
    "osmon_ilohi_2": "https://t.me/dhsaidqhndi/2137",
    "osmon_ilohi_3": "https://t.me/dhsaidqhndi/2138",
    "osmon_ilohi_4": "https://t.me/dhsaidqhndi/2139",
    "osmon_ilohi_5": "https://t.me/dhsaidqhndi/2140",
}

# ==================== ASKAR AFSONASI ====================
@dp.message(F.text == "ASKAR AFSONASI")
async def askar_handler(message: types.Message):
    await message.answer(
        "🛡 *Askar Afsonasi* qismlarini tanlang:",
        reply_markup=get_askar_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^askar_page_\d+$"))
async def change_askar_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(
        reply_markup=get_askar_page_keyboard(page)
    )
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^askar_\d+$"))
async def send_askar_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = askar_videolar.get(key)

    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> ASKAR AFSONASI\n"
        "🛡 <b>Janr:</b> Harbiy | Jang | Sarguzasht\n"
        f"📺 <b>Qismi:</b> {qism}\n"
        "💿 <b>Sifati:</b> 720p HD\n"
        "🌐 <b>Til:</b> O‘zbek\n"
        "───────────────\n"
        "📌 <b>Premyera:</b> @AniManhwa3D\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "🏷 #askar_afsonasi\n"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption,
        parse_mode="HTML",
        protect_content=True
    )


def get_askar_page_keyboard(page: int):
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page

    keys = list(askar_videolar.keys())[start:end]

    buttons = [
    [InlineKeyboardButton(text=f"🎬 {key.split('_')[-1]}-qism", callback_data=key)]
    for key in keys
]

    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"askar_page_{page-1}"))
    if end < len(askar_videolar):
        nav.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"askar_page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Askar Afsonasi videolar ro'yxati:
askar_videolar = {
    "askar_1": "https://t.me/dhsaidqhndi/2255",
    "askar_2": "https://t.me/dhsaidqhndi/2294",
    "askar_3": "https://t.me/dhsaidqhndi/2256",
    "askar_4": "https://t.me/dhsaidqhndi/2257",
    "askar_5": "https://t.me/dhsaidqhndi/2258",
}

# ============= 📜 Mundareja 5-qism =============
@dp.message(F.text == "📜 Mundareja 5-qism")
async def mundareja_5_handler(message: types.Message):
    mundareja_5_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ENG BOY O'YINCHI")],
            [KeyboardButton(text="KATTA AKA")],
            [KeyboardButton(text="⬅️ Orqaga")],
        ],
        resize_keyboard=True
    )
    await message.answer("📜 Mundareja 5-qism bo‘limi:", reply_markup=mundareja_5_menu)

# ⬅️ Orqaga
@dp.message(F.text == "⬅️ Orqaga")
async def back_to_main(message: types.Message):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📜 Mundareja 1-qism")],
            [KeyboardButton(text="📜 Mundareja 2-qism")],
            [KeyboardButton(text="📜 Mundareja 3-qism")],
            [KeyboardButton(text="📜 Mundareja 4-qism")],
            [KeyboardButton(text="📜 Mundareja 5-qism")],
            [KeyboardButton(text="📜 KINOLAR")],
            [KeyboardButton(text="📢 Reklama va homiylik")],
            [KeyboardButton(text="📥 Video yuklab olish")],
            [KeyboardButton(text="📈 Statistika")],
            [KeyboardButton(text="👤 Admin")],
        ],
        resize_keyboard=True
    )
    await message.answer("🔙 Asosiy menyuga qaytdingiz", reply_markup=main_menu)

# ==================== ENG BOY O‘YINCHI ====================
# 💰 ENG BOY O‘YINCHI — Asosiy menyu
@dp.message(F.text == "ENG BOY O'YINCHI")
async def eng_boy_handler(message: types.Message):
    await message.answer(
        "💰 *Eng Boy O‘yinchi* qismlarini tanlang:",
        reply_markup=get_boy_page_keyboard(1),
        parse_mode="Markdown"
    )

# 📄 Sahifa almashtirish (pagination)
@dp.callback_query(F.data.regexp(r"^boy_page_\d+$"))
async def change_boy_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_boy_page_keyboard(page))
    await callback.answer()

# 🎬 Video yuborish (qismni tanlanganda)
@dp.callback_query(F.data.regexp(r"^eng_boy_\d+$"))
async def send_boy_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = boy_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = key.split("_")[-1]

    caption = (
        "🎬 <b>Nomi:</b> Eng Boy O‘yinchi\n"
        "───────────────\n"
        "🎮 <b>Janr:</b> Iqtisod, Sarguzasht, Jang, Fantastika\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek (AniManhwa3D))\n"
        "───────────────\n"
        "Premyeralari ushbu kanalda: <b>@AniManhwa3D</b>\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @AniManhwa3D | @aust1n_griffin\n"
        "💬 “Ba’zi o‘yinlar pul bilan o‘ynaladi, ammo eng muhimi — aql bilan yutiladi.” 💸"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=caption.replace("*", "").replace("_", ""),
        protect_content=True,
        parse_mode="HTML"
    )

# 🔘 Sahifalangan tugmalar — 20 ta per sahifa
def get_boy_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(boy_videolar.keys())[start:end]

    buttons = []
    for i, key in enumerate(keys, start=start):
        buttons.append([
            InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"eng_boy_{i+1}")
        ])

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"boy_page_{page-1}"))
    if end < len(boy_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"boy_page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Eng Boy O'yinchi videolar ro'yxati:
boy_videolar = {
    "eng_boy_1": "https://t.me/dhsaidqhndi/1761",
    "eng_boy_2": "https://t.me/dhsaidqhndi/1762",
    "eng_boy_3": "https://t.me/dhsaidqhndi/1763",
    "eng_boy_4": "https://t.me/dhsaidqhndi/1764",
}

# ==================== KATTA AKA ====================
# 👊 KATTA AKA — Asosiy menyu
@dp.message(F.text == "KATTA AKA")
async def katta_handler(message: types.Message):
    await message.answer(
        "👊 *Katta Aka* qismlarini tanlang:",
        reply_markup=get_katta_page_keyboard(1),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.regexp(r"^katta_page_\d+$"))
async def change_katta_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[2])
    await callback.message.edit_reply_markup(reply_markup=get_katta_page_keyboard(page))
    await callback.answer()

@dp.callback_query(F.data.regexp(r"^katta_\d+$"))
async def send_katta_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = katta_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return
    qism_raqami = key.split("_")[-1]
    caption = (
        "🎬 <b>Nomi:</b> Katta Aka\n"
        "🥋 <b>Janr:</b> Jang, Drama, Motivatsiya\n"
        f"📺 <b>Qismi:</b> {qism_raqami}\n"
        "💿 <b>Sifati:</b> 1080p HD\n"
        "🌐 <b>Til:</b> O‘zbek(AniMania)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @Animania_rasmiy\n"
        "#katta_aka_animania"
    )
    await bot.send_video(chat_id=callback.from_user.id, video=video_link, caption=caption, protect_content=True, parse_mode="HTML")

def get_katta_page_keyboard(page: int):
    VIDEOS_PER_PAGE = 20
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(katta_videolar.keys())[start:end]
    buttons = [[InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=f"katta_{i+1}")] for i, key in enumerate(keys, start=start)]
    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"katta_page_{page-1}"))
    if end < len(katta_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"katta_page_{page+1}"))
    if navigation:
        buttons.append(navigation)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Katta Aka videolar ro'yxati:
katta_videolar = {
    "katta_1": "https://t.me/dhsaidqhndi/1834",
    "katta_2": "https://t.me/dhsaidqhndi/1835",
    "katta_3": "https://t.me/dhsaidqhndi/1836",
    "katta_4": "https://t.me/dhsaidqhndi/1837",
    "katta_5": "https://t.me/dhsaidqhndi/1838",
    "katta_6": "https://t.me/dhsaidqhndi/1839",
    "katta_7": "https://t.me/dhsaidqhndi/1840",
    "katta_8": "https://t.me/dhsaidqhndi/1841",
    "katta_9": "https://t.me/dhsaidqhndi/1842",
    "katta_10": "https://t.me/dhsaidqhndi/1843",
    "katta_11": "https://t.me/dhsaidqhndi/1844",
    "katta_12": "https://t.me/dhsaidqhndi/1845",
    "katta_13": "https://t.me/dhsaidqhndi/1846",
}

# ============= 📜 KINOLAR =============
@dp.message(F.text == "📜 KINOLAR")
async def mundareja_10_handler(message: types.Message):
    mundareja_10_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Qonli Luo Qit'asi")],
            [KeyboardButton(text="")],
            [KeyboardButton(text="")],
            [KeyboardButton(text="Ye-LAi-Ke-Si - Tojsiz qirol")],
            [KeyboardButton(text="⬅️ Orqaga")],
        ],
        resize_keyboard=True
    )
    await message.answer("📜 KINOLAR bo‘limi:", reply_markup=mundareja_10_menu)

# ⬅️ Orqaga
@dp.message(F.text == "⬅️ Orqaga")
async def back_to_main(message: types.Message):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📜 Mundareja 1-qism")],
            [KeyboardButton(text="📜 Mundareja 2-qism")],
            [KeyboardButton(text="📜 Mundareja 3-qism")],
            [KeyboardButton(text="📜 Mundareja 4-qism")],
            [KeyboardButton(text="📜 Mundareja 5-qism")],
            [KeyboardButton(text="📜 KINOLAR")],
            [KeyboardButton(text="📢 Reklama va homiylik")],
            [KeyboardButton(text="📥 Video yuklab olish")],
            [KeyboardButton(text="📈 Statistika")],
            [KeyboardButton(text="👤 Admin")],
        ],
        resize_keyboard=True
    )
    await message.answer("🔙 Asosiy menyuga qaytdingiz", reply_markup=main_menu)

# ==================== Qonli Luo Qit'asi ====================
@dp.message(F.text == "Qonli Luo Qit'asi")
async def yelaikesi_handler(message: types.Message):
    video_link = "https://t.me/dhsaidqhndi/2900"  # 🔗 bu yerga video (film) linkini joylashtir

    caption = (
        "🎬 <b>Nomi:</b> Ye-LAi-Ke-Si — Tojsiz Qirol\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Jang, Sarguzasht\n"
        "💿 <b>Sifati:</b> 1080p Full HD\n"
        "🌐 <b>Til:</b> O‘zbek (Dublyaj)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @Uzdubgo | @bananatv_uz\n"
        "#yelaikesi_animania\n\n"
        "💬 “U tojni istamadi, ammo taqdir uni shohga aylantirdi. "
        "Ba’zan eng buyuk kuch — yurakdagi rahm va sadoqatdadir.” ⚔️"
    )

    await bot.send_video(
        chat_id=message.chat.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

# ==================== Qonli Luo Qit'asi ====================
@dp.message(F.text == "Ye-LAi-Ke-Si - Tojsiz qirol")
async def yelaikesi_handler(message: types.Message):
    video_link = "https://t.me/dhsaidqhndi/13"  # 🔗 bu yerga video (film) linkini joylashtir

    caption = (
        "🎬 <b>Nomi:</b> Qonli Luo Qit'asi\n"
        "───────────────\n"
        "🎞 <b>Janr:</b> Fantastika, Jang, Sarguzasht\n"
        "💿 <b>Sifati:</b> 1080p Full HD\n"
        "🌐 <b>Til:</b> O‘zbek (Dublyaj)\n"
        "───────────────\n"
        "👑 <b>Kanal:</b> @Uzdubgo\n"
    )

    await bot.send_video(
        chat_id=message.chat.id,
        video=video_link,
        caption=caption,
        protect_content=True,
        parse_mode="HTML"
    )

# 📥 Video yuklab olish
@dp.message(F.text == "📥 Video yuklab olish")
async def ask_video(message: Message):
    await message.answer("📎 Video link yuboring:")

@dp.message(F.text.regexp(r'https?://'))
async def handle_video_link(message: Message):
    url = message.text
    await message.answer("⏳ Video yuklanmoqda... Biroz kuting")

    try:
        # yt-dlp options, HLS stream orqali
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'merge_output_format': 'mp4',
            'ffmpeg_location': 'ffmpeg',  # ffmpeg PATH bo'lishi kerak
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)  # download=False => faqat info oladi

            video_url = info.get('url')  # streaming URL
            # Video ni to'g'ridan-to'g'ri foydalanuvchiga yuborish
            async with aiohttp.ClientSession() as session:
                async with session.get(video_url) as resp:
                    await message.answer_video(resp.content, caption=info.get('title'))

    except Exception as e:
        await message.answer("❌ Videoni yuklab bo‘lmadi! Link xato yoki sayt qo‘llab-quvvatlanmaydi.")
        print("ERROR:", e)

@dp.message(F.text == "📢 Reklama va homiylik")
async def reklama_start(message: Message, state: FSMContext):
    await message.answer("💼 Iltimos, ism yoki tashkilot nomingizni kiriting:")
    await state.set_state(ReklamaForm.name)


@dp.message(ReklamaForm.name)
async def reklama_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📞 Aloqa uchun raqamingiz yoki telegram useringizni kiriting:")
    await state.set_state(ReklamaForm.contact)


@dp.message(ReklamaForm.contact)
async def reklama_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer("📝 Reklama yoki homiylik haqida qisqacha ma’lumot yozing:")
    await state.set_state(ReklamaForm.content)


@dp.message(ReklamaForm.content)
async def reklama_finish(message: Message, state: FSMContext):
    await state.update_data(content=message.text)
    data = await state.get_data()

    # === ADMIN ID (sizning Telegram ID raqamingizni yozing) ===
    ADMIN_ID = 6760161876  

    text = (
        "📢 *Yangi reklama / homiylik so‘rovi!* \n\n"
        f"👤 Nomi: {data['name']}\n"
        f"📞 Aloqa: {data['contact']}\n"
        f"📝 Ma’lumot: {data['content']}\n\n"
        f"🕒 Foydalanuvchi: @{message.from_user.username}"
    )

    await message.bot.send_message(ADMIN_ID, text, parse_mode="Markdown")
    await message.answer("✅ So‘rovingiz yuborildi! Tez orada admin siz bilan bog‘lanadi.", parse_mode="Markdown")
    await state.clear()

@dp.message(F.text == "📈 Statistika")
async def show_stats(message: Message):
    now = datetime.now(timezone.utc)
    oy = now.month
    yil = now.year

    count = count_month_users(yil, oy)

    await message.answer(
        f"📊 <b>Oylik Statistika</b>\n\n"
        f"📅 Oy: {yil}-{oy:02d}\n"
        f"👥 Yangi obunachilar: {count} ta"
    )

# 👤 Admin tugmasi
@dp.message(F.text == "👤 Admin")
async def admin_handler(message: types.Message):
    await message.answer("👨‍💻 Admin: Sirli insonni topish qiyin")

async def main():
    print("✅ Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())