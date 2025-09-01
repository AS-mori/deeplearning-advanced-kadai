from django.shortcuts import render
from .form import ImageUploadForm
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from io import BytesIO
import os
# import random

def predict(request):
    if request.method == 'GET':
        # GETリクエストによるアクセス時の処理
        form = ImageUploadForm()
        return render(request, 'home.html', {'form': form})
    if request.method == 'POST':
        # POSTリクエストによるアクセス時の処理
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data['image']
            # 画像ファイル（img_file）の前処理
            img_file = BytesIO(img_file.read())
            img = load_img(img_file, target_size=(256, 256))
            img_array = img_to_array(img)
            img_array = img_array.reshape((1, 256, 256, 3))
            img_array = img_array/255
            # 判定結果のロジック
            model_path = os.path.join(settings.BASE_DIR, 'prediction', 'models', 'model.h5')
            model = load_model(model_path)
            # ← ここに追記する
            for i, layer in enumerate(model.layers[:6]):  # 先頭5〜6層ぐらいでOK
                print(i, layer.name, layer.__class__.__name__)

            print("input_shape:", model.input_shape)   # 例: (None, 224, 224, 3)
            print("output_shape:", model.output_shape) # 例: (None, 2) or (None, 1)
            result = model.predict(img_array)
            print("raw result:", result)               # 例: [[0.8, 0.2]] or [[0.8]]
            if result[0][0] > result[0][1]:
                prediction = '猫'
            else:
                prediction = '犬'
            img_data = request.POST.get('img_data')
            # prediction = random.choice(["猫", "犬"])
            # 暫定で、ダミーの判定結果としてpredictionにランダムで「猫」か「犬」を格納
            return render(request, 'home.html', {'form': form, 'prediction': prediction, 'img_data': img_data})
        else:
            form = ImageUploadForm()
            return render(request, 'home.html', {'form': form})
