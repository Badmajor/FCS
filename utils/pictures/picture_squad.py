from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from utils.db_api.get_data_db import get_list_id_squad_3_line, get_data_user_list


async def picture_squad(user_id):
    list_squad_id = await get_list_id_squad_3_line(user_id)
    squad_img = Image.open('img/squad_pic.gif')
    idraw = ImageDraw.Draw(squad_img)
    font_size = 30
    list_lame_horizontal = [405, 405, 675, 675, 675, 675, 945, 945, 945, 945, 945, 945, 945, 945]
    list_lame_vertical = [389, 1431, 156, 656, 1156, 1656, 35, 285, 535, 785, 1035, 1285, 1535, 1785]
    step = 0
    ref_user_data_dict_list = await get_data_user_list(list_squad_id)
    for _ in list_squad_id:
        ref_user_data_dict = ref_user_data_dict_list[step]
        if ref_user_data_dict is None:
            name, phone = 'Свободно', ''
        else:
            name, phone = ref_user_data_dict.get('user_name'), ref_user_data_dict.get('phone')
        font = ImageFont.truetype("font/arial.ttf", size=font_size)
        idraw.text((list_lame_horizontal[step] - len(name)/4 * font_size,
                    list_lame_vertical[step]), name, font=font, fill=(0, 56, 70))
        idraw.text((list_lame_horizontal[step] - len(phone)/4 * font_size,
                    list_lame_vertical[step] + 70), phone, font=font, fill=(0, 56, 70))
        step += 1
    bio = BytesIO()
    bio.name = f'{user_id}.gif'
    squad_img.save(bio, 'GIF')
    bio.seek(0)
    return bio
