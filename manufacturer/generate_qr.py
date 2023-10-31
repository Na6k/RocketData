import qrcode
from io import BytesIO
from PIL import Image


def generate_qr_code(network):
    contact_info = (
        f"Name: {network.name}\nEmail: {network.email}\nAddress: {network.country}, {network.city}, {network.street}"
    )

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(contact_info)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Сохраните изображение QR-кода в байтовом потоке
    img_byte_stream = BytesIO()
    img.save(img_byte_stream, format="PNG")

    return img_byte_stream.getvalue()
