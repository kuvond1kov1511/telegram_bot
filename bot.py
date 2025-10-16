from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio, random, string, time
from datetime import datetime
from aiogram import Router
import aiosqlite
import asyncio

codes = {}
router = Router()

# --- BAZANI YARATISH BLOKI ---
async def setup_db():
    async with aiosqlite.connect("bot.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS verified_users (
                user_id INTEGER PRIMARY KEY
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS codes (
                code TEXT PRIMARY KEY,
                expire_time REAL
            )
        """)
        await db.commit()

asyncio.run(setup_db())

ADMIN_ID = 6760161876
TOKEN = "8319503755:AAHhWvRTr-CSQnPfznNg6Ef1EKjnyghhDEQ"
CHANNELS = ["@Kuvond1kov", "@aust1n_griffin", "@bananatv_uz"]

# ⏱ Bot ishga tushgan vaqti
start_time = datetime.now()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

# 🎞 1–180 gacha “TAXT MUHRI” videolari
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
}
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
        "5-qism": "mavjud emas",
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
        "74-qism": "mavjud emas",
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
    }

}

# 🎞 1–110 gacha "RENEGADE O'LMAS” videolari
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
    "renegade_olmas_99": "https://t.me/dhsaidqhndi/597",
    "renegade_olmas_100": "https://t.me/dhsaidqhndi/598",
    "renegade_olmas_101": "https://t.me/dhsaidqhndi/590",
    "renegade_olmas_102": "https://t.me/dhsaidqhndi/599",
    "renegade_olmas_103": "https://t.me/dhsaidqhndi/600",
    "renegade_olmas_104": "https://t.me/dhsaidqhndi/601",
    "renegade_olmas_105": "https://t.me/dhsaidqhndi/591",
    "renegade_olmas_106": "https://t.me/dhsaidqhndi/592",
    "renegade_olmas_107": "https://t.me/dhsaidqhndi/593",
    "renegade_olmas_108": "https://t.me/dhsaidqhndi/594",
    "renegade_olmas_109": "https://t.me/dhsaidqhndi/595",
    "renegade_olmas_110": "https://t.me/dhsaidqhndi/596",
    }

VIDEOS_PER_PAGE = 10

# yordamchi funksiyalar
def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

async def is_subscribed(user_id: int, channel: str) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

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

# /start: avvalo obuna, keyin kod, keyin menyu
@dp.message(F.text == "/start")
async def start_cmd(message: types.Message):
    # 1) Kanallarga obuna tekshiruvi
    not_subscribed = await check_user_subscriptions(message.from_user.id)
    if not_subscribed:
        keyboard = InlineKeyboardMarkup(inline_keyboard = [
            [InlineKeyboardButton(text="📢 Kanal 1", url="https://t.me/Kuvond1kov")],
            [InlineKeyboardButton(text="📺 Kanal 2", url="https://t.me/aust1n_griffin")],
            [InlineKeyboardButton(text="📺 Kanal 3", url="https://t.me/bananatv_uz")],
            [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub")]
        ])

        await message.answer("Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling 👇", reply_markup=keyboard)
        return

    # 2) Kod tekshiruvi — faqat obuna bo'lsa so'raladi
    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT 1 FROM verified_users WHERE user_id = ?", (message.from_user.id,)) as cursor:
            row = await cursor.fetchone()

    if not row:
        await message.answer("🔐 Botdan foydalanish uchun avval kodni yoki /admin (faqat admin uchun) kiriting:")
        return

    # 3) Hammasi yaxshi — asosiy menyu
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📜 Mundareja")],
            [KeyboardButton(text="👤 Admin"), KeyboardButton(text="🎁 Hadya qilish")]
        ], resize_keyboard=True
    )
    await message.answer("🎉 Botga xush kelibsiz!\nKerakli bo‘limni tanlang:", reply_markup=main_menu)

# Kodni foydalanuvchi kiritganda ishlaydi
@dp.message(F.text.regexp(r"^[A-Z0-9]{6}$"))  # 6 ta harf-raqamli kodlarni ushlaydi
async def check_code(message: types.Message):
    text = message.text.strip().upper()
    now = time.time()

    async with aiosqlite.connect("bot.db") as db:
        async with db.execute("SELECT expire_time FROM codes WHERE code = ?", (text,)) as cursor:
            row = await cursor.fetchone()

        if not row:
            await message.answer("❌ Noto‘g‘ri yoki muddati o‘tgan kod.")
            return

        expire_time = row[0]
        if now < expire_time:
            # ✅ Kod to‘g‘ri
            await db.execute("INSERT OR REPLACE INTO verified_users (user_id) VALUES (?)", (message.from_user.id,))
            await db.execute("DELETE FROM codes WHERE code = ?", (text,))
            await db.commit()

            main_menu = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="📜 Mundareja")],
                    [KeyboardButton(text="👤 Admin"), KeyboardButton(text="🎁 Hadya qilish")]
                ],
                resize_keyboard=True
            )
            await message.answer("✅ Kod tasdiqlandi! Endi /start ni yozing.", reply_markup=main_menu)

        else:
            # ❌ Kod muddati tugagan bo‘lsa
            await db.execute("DELETE FROM codes WHERE code = ?", (text,))
            await db.commit()

            # 🧹 Chatni tozalash
            try:
                async for msg in bot.iter_history(message.chat.id, limit=200):
                    try:
                        await bot.delete_message(message.chat.id, msg.message_id)
                        await asyncio.sleep(0.05) # serverga yuk tushmasligi uchun
                    except Exception:
                        pass
            except Exception as e:
                print("Chatni o‘chirishda xato:", e)

            # ⏰ Xabar berish
            await message.answer("⏰ Kodning amal qilish muddati tugagan.\nChat tozalandi. /start ni qayta yozing.")

# 🔐 Admin uchun kod yaratish menyusi
@dp.message(Command("admin"))
async def admin_menu(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return  # oddiy foydalanuvchiga hech narsa chiqmaydi

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🕐 24 soatlik kod", callback_data="create_code_86400")],
        [InlineKeyboardButton(text="🕓 48 soatlik kod", callback_data="create_code_172800")],
        [InlineKeyboardButton(text="🗓 7 kunlik kod", callback_data="create_code_604800")]
    ])
    await message.answer("⏱ Kod amal qilish muddatini tanlang:", reply_markup=keyboard)

# 🔑 Kod yaratish (faqat admin uchun)
@dp.callback_query(F.data.startswith("create_code_"))
async def create_code(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return await callback.answer("❌ Siz admin emassiz.", show_alert=True)

    seconds = int(callback.data.split("_")[-1])
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    expire_time = time.time() + seconds

    async with aiosqlite.connect("bot.db") as db:
        await db.execute("INSERT INTO codes (code, expire_time) VALUES (?, ?)", (code, expire_time))
        await db.commit()

    await callback.message.answer(
        f"✅ Kod yaratildi!\n\n"
        f"🔑 Kod: `{code}`\n"
        f"⏳ Amal qilish muddati: {seconds // 3600} soat\n"
        f"⚠️ 1 martalik ishlatish uchun mo‘ljallangan.",
        parse_mode="Markdown"
    )

# === "✅ Tekshirish" tugmasi ===
@dp.callback_query(F.data == "check_sub")
async def check_sub_callback(callback: types.CallbackQuery):
    not_subscribed = await check_user_subscriptions(callback.from_user.id)
    if not_subscribed:
        await callback.answer("❌ Hali barcha kanallarga obuna bo‘lmadingiz!", show_alert=True)
    else:
        await callback.message.edit_text("✅ Obuna tasdiqlandi! Endi /start ni yozing.")

# 📜 Mundareja
@dp.message(F.text == "📜 Mundareja")
async def mundareja_handler(message: types.Message):
    mundareja_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="TAXT MUHRI")],
            [KeyboardButton(text="RENEGADE O‘LMAS")],
            [KeyboardButton(text="MUKAMMAL DUNYO")],
            [KeyboardButton(text="Osmondagi janglar")],
            [KeyboardButton(text="SIANXU AFSONASI")],
            [KeyboardButton(text="Ye-LAi-Ke-Si - Tojsiz qirol")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )
    await message.answer("📜 Mundareja bo‘limi:", reply_markup=mundareja_menu)

# ⬅️ Orqaga
@dp.message(F.text == "⬅️ Orqaga")
async def back_to_main(message: types.Message):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📜 Mundareja")],
            [KeyboardButton(text="👤 Admin"), KeyboardButton(text="🎁 Hadya qilish")]
        ],
        resize_keyboard=True
    )
    await message.answer("🔙 Asosiy menyuga qaytdingiz", reply_markup=main_menu)

# 🌌 OSMONDAGI JANGLAR menyusi
@dp.message(F.text == "Osmondagi janglar")
async def osmon_menu(message: types.Message):
    # 1–5 fasl tugmalarini chiqaryapti
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
def generate_osmon_keyboard(fasl: str, page: int=1):
    per_page = 30 if fasl == "5-fasl" else 50

    all_items = list(osmon_videolar[fasl].items())  # [(qism, url), ...]
    start = (page - 1) * per_page
    end = start + per_page
    items = all_items[start:end]

    keyboard = []
    # Har bir qism uchun tugma (callback_data orqali tanlashni amalga oshiramiz)
    for name, url in items:
        # callback_data: osmon_video_{fasl}:{qism_nomi}
        keyboard.append([InlineKeyboardButton(text=name, callback_data=f"osmon_video_{fasl}:{name}")])

    # Navigatsiya tugmalari
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
    # callback.data misol: "osmon_page_5-fasl_2"
    # "osmon_page_" dan keyingi qismni ajratamiz
    data = callback.data[len("osmon_page_"):]  # "5-fasl_2"
    fasl, page_str = data.rsplit("_", 1)       # oxirgi '_' bo'yicha ajratamiz
    page = int(page_str)

    await callback.message.edit_text(
        f"☁️ Osmondagi janglar — {fasl}\n\nQuyidagi qismlardan birini tanlang 👇",
        reply_markup=generate_osmon_keyboard(fasl, page)
    )

# 🔹 VIDEO TANLANGANDA
@dp.callback_query(F.data.startswith("osmon_video_"))
async def osmon_video(callback: types.CallbackQuery):
    data = callback.data.replace("osmon_video_", "")
    fasl, qism = data.split(":")
    link = osmon_videolar[fasl].get(qism)

    if not link or link == "mavjud emas":
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    qism_raqami = qism.replace("qism", "").strip()

    caption = (
        "🎬 Nomi: ⚔️ Osmondagi janglar ⚔️\n"
        "───────────────────────────────\n"
        f"🎞 Janr: Fantastika, Jangovar, Romantika, Sarguzasht\n"
        f"📺 Qismi: {qism_raqami}\n"
        "💿 Sifati: 1080p HD\n"
        "🌐 Til: O‘zbek (Uzdub)\n"
        "───────────────────────────────\n"
        "👑 Kanal: @Uzdubgo, @bananatv_uz\n"
        "#osmondagi_janglar_uzdub\n\n"
        "💬“Haqiqiy kuch — yurakdagi qat’iyat va hech qachon taslim bo‘lmaslikda.”⚡"
    )

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=link,
        caption=caption,
        protect_content=True
    )
    await callback.answer()

# 🎥 TAXT MUHRI
@dp.message(F.text == "TAXT MUHRI")
async def renegade_olmas_handler(message: types.Message):
    await message.answer("👑 Taxt Muhri qismlarini tanlang:", reply_markup=get_page_keyboard(1))

# 📄 Sahifa almashtirish
@dp.callback_query(F.data.regexp(r"^page_\d+$"))
async def change_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[1])
    await callback.message.edit_reply_markup(reply_markup=get_page_keyboard(page))
    await callback.answer()

# 🎬 Video yuborish
@dp.callback_query(F.data.regexp(r"^taxt_muhri_\d+$"))
async def send_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = taxt_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=f"🎬 {key.replace('_', ' ').title()}",
        protect_content=True
    )
    await callback.answer()

# 🔘 Sahifalangan tugmalar
def get_page_keyboard(page: int):
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(taxt_videolar.keys())[start:end]

    buttons = [
        [InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=key)]
        for i, key in enumerate(keys, start=start)
    ]

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"page_{page-1}"))
    if end < len(taxt_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🎥 Renegade O'lmas
@dp.message(F.text == "RENEGADE O‘LMAS")
async def renegade_olmas_handler(message: types.Message):
    await message.answer("👑 RENEGADE O‘LMAS qismlarini tanlang:", reply_markup=get_page_keyboard(1))

# 📄 Sahifa almashtirish
@dp.callback_query(F.data.regexp(r"^page_\d+$"))
async def change_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[1])
    await callback.message.edit_reply_markup(reply_markup=get_page_keyboard(page))
    await callback.answer()

# 🎬 Video yuborish
@dp.callback_query(F.data.regexp(r"^renegade_olmas_\d+$"))
async def send_video(callback: types.CallbackQuery):
    key = callback.data
    video_link = renegade_videolar.get(key)
    if not video_link:
        await callback.answer("❌ Bu qism hali mavjud emas!", show_alert=True)
        return

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=video_link,
        caption=f"🎬 {key.replace('_', ' ').title()}",
        protect_content=True
    )
    await callback.answer()

# 🔘 Sahifalangan tugmalar
def get_page_keyboard(page: int):
    start = (page - 1) * VIDEOS_PER_PAGE
    end = start + VIDEOS_PER_PAGE
    keys = list(renegade_videolar.keys())[start:end]

    buttons = [
        [InlineKeyboardButton(text=f"🎬 {i+1}-qism", callback_data=key)]
        for i, key in enumerate(keys, start=start)
    ]

    navigation = []
    if page > 1:
        navigation.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"page_{page-1}"))
    if end < len(taxt_videolar):
        navigation.append(InlineKeyboardButton(text="➡️ Keyingi", callback_data=f"page_{page+1}"))
    if navigation:
        buttons.append(navigation)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# 🔹 VIDEO TANLANGANDA
@dp.callback_query(F.data.regexp(r"^renegade_olmas_\d+$"))
async def send_video(callback: types.CallbackQuery):
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
        "🌐 Til: O‘zbek (AniMAnia)\n"
        "───────────────────────────────\n"
        "👑 Kanal: @Uzdubgo, @bananatv_uz, @AniMania_rasmiy\n"
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

# 👤 Admin tugmasi
@dp.message(F.text == "👤 Admin")
async def admin_handler(message: types.Message):
    await message.answer("👨‍💻 Admin: Sirli insonni topish qiyin")

# 🎁 Hadya qilish tugmasi
@dp.message(F.text == "🎁 Hadya qilish")
async def gift_handler(message: types.Message):
    await message.answer("🎁 Do‘stlaringizga bot havolasini yuboring:\n👉 t.me/your_bot_username")

# 🔄 Botni ishga tushurish
async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
