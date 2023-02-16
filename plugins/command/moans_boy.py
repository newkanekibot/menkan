import config
import re

from pyrogram import Client, enums, types
from plugins import Database, Helper

async def moans_boy_handler(client: Client, msg: types.Message):
    db = Database(msg.from_user.id)
    talent = db.get_data_bot(client.id_bot).talent
    top_rate = [] # total rate mb
    top_id = [] # id mb
    if len(moansboy) == 0:
        return await msg.reply('<b>Saat ini tidak ada mb yang tersedia.</b>', True, enums.ParseMode.HTML)
    else:
        for uid in moansboy:
            rate = moansboy[str(uid)]['rate']
            if rate >= 0:
                top_rate.append(rate)
                top_id.append(uid)
        top_rate.sort(reverse=True)
        pesan = "<b>Daftar Talent Fwb</b>\n\n"
        pesan += "No — Talent — Rating\n"
        index = 1
        for i in top_rate:
            if index > config.batas_moansboy:
                break
            for j in top_id:
                if moansboy[j]['rate'] == i:
                    pesan += f"<b> {str(index)}.</b> {moansboy[j]['username']} ➜ {str(moans_boy[j]['rate'])} 🍓\n"
                    top_id.remove(j)
                    index += 1
                    
        pesan += f"\nmenampilkan {config.batas_moansboy} mb dengan ratinf tertinggi\n"
        pesan += "berikan rating untuk mb favoritmu dengan perintah <code>/rate id</code>\n"
        pesan += "contoh <code>/rate 37339222</code>"
        await msg.reply(pesan, True, enums.ParseMode.HTML)

async def tambah_moans_boy_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    if re.search(r"^[\/]addboy(\s|\n)*$", msg.text or msg.caption):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah Moans boy</b>\n\n<code>/addboy id_user</code>\n\nContoh :\n<code>/addboy 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    y = re.search(r"^[\/]addboy(\s|\n)*(\d+)$", msg.text or msg.caption)
    if y:
        target = y.group(2)
        db = Database(int(target))
        if target in db.get_data_bot(client.id_bot).ban:
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={str(target)}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan Moans girl", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        if await db.cek_user_didatabase():
            status = [
                'admin', 'owner', 'talent', 'daddy sugar', 'moans girl',
                'moans boy', 'girlfriend rent', 'boyfriend rent'
            ]
            member = db.get_data_pelanggan()
            if member.status in status:
                return await msg.reply_text(
                    text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()} tidak dapat ditambahkan menjadi Moans boy</i>", quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
            try:
                a = await client.get_chat(target)
                nama = await helper.escapeHTML(a.first_name if not a.last_name else a.first_name + ' ' + a.last_name)
                await client.send_message(
                    int(target),
                    text=f"<i>Kamu telah menjadi Moans boy</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                    parse_mode=enums.ParseMode.HTML
                )
                await db.tambah_moans_boy(int(target), client.id_bot, nama)
                return await msg.reply_text(
                    text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil menjadi Moans girl</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>", quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception as e:
                return await msg.reply_text(
                    text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
    else:
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah Moans boy</b>\n\n<code>/addboy id_user</code>\n\nContoh :\n<code>/addboy 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
async def hapus_moans_boy_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]hapus(\s|\n)*$", msg.text or msg.caption):
        return await msg.reply_text(
            text="<b>Cara penggunaan hapus moansb</b>\n\n<code>/hapus id_user</code>\n\nContoh :\n<code>/hapus 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    x = re.search(r"^[\/]hapus_moans_boy(\s|\n)*(\d+)$", msg.text or msg.caption)
    if x:
        target = x.group(2)
        db = Database(int(target))
        if await db.cek_user_didatabase():
            member = db.get_data_pelanggan()
            if member.status == 'owner' or member.status == 'admin':
                return await msg.reply_text(
                    text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()}</i>", quote=True,
                    parse_mode=enums.ParseMode.HTML
                )
            if member.status == 'moansb':
                try:
                    await client.send_message(int(target),
                        text=f"<i>Sayangnya owner telah mencabut jabatanmu sebagai moansb</i>\n└Diturunkan oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                        parse_mode=enums.ParseMode.HTML
                    )
                    await db.hapus_moans_boy(int(target), client.id_bot)
                    return await msg.reply_text(
                        text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil diturunkan menjadi member</i>\n└Diturunkan oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>", quote=True,
                        parse_mode=enums.ParseMode.HTML
                    )
                except Exception as e:
                    return await msg.reply_text(
                        text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", quote=True,
                        parse_mode=enums.ParseMode.HTML
                    )
    else:
        return await msg.reply_text(
            text="<b>Cara penggunaan hapus talent</b>\n\n<code>/hapus id_user</code>\n\nContoh :\n<code>/hapus 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )

async def rate_talent_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]rate(\s|\n)*$", msg.text or msg.caption):
        return await msg.reply_text(
            text="perintah salah, gunakan perintah /rate id untuk memberikan rating kepada talent", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    x = re.search(r"^[\/]rate_talent(\s|\n)*(\d+)$", msg.text)
    if x:
        target = x.group(2)
        db = Database(msg.from_user.id)
        user = db.get_data_pelanggan()
        db_bot = db.get_data_bot(client.id_bot)
        my_coin = user.coin
        if msg.from_user.id == int(target):
            return await msg.reply('tidak dapat memberi rating kepada diri sendiri', True)
        
        if target in db_bot.talent:
            if my_coin <= config.biaya_talent:
                return await msg.reply(f'coin kamu kurang untuk memberikan rating ke talent fwb. biaya rate adalah {str(config.biaya_talent)} coin', True)  
            to_talent = my_coin - config.biaya_talent
            await db.rate_talent(target, client.id_bot, to_talent)
            return await msg.reply(f'kamu berhasil memberikan 1 🍓 kepada {target}', True)
        else:
            await msg.reply(f'{target} bukan seorang talent .', True)
