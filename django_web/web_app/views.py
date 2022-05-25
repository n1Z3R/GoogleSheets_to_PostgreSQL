import base64
import io

import pandas as pd
from django.shortcuts import render
import matplotlib.pyplot as plt

from web_app.models import GoogleSheetsModel


def home(request):
    df = pd.DataFrame(list(GoogleSheetsModel.objects.all().values()))
    plt.plot(df["id"], df["price_rub"])
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.figure(figsize=(10, 10))
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return render(request, 'home.html', {'data': graphic})
