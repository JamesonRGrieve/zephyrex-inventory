import base64
import io

import pyqrcode


def qr_data_uri(text, scale=6):
	"""Return a QR code for `text` as a data URI that can go straight into an <img> tag."""
	buf = io.BytesIO()
	pyqrcode.create(text).svg(buf, scale=scale, background="white", module_color="black")
	return "data:image/svg+xml;base64," + base64.b64encode(buf.getvalue()).decode()
