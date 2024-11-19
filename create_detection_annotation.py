"""
review_object_detection_metrics ツールを使用するために、検出アノテーションファイルを作成する。
各画像に対してオブジェクト情報が書かれたテキストファイルを作成する。
フォーマット: クラスID 信頼度 x y x2 y2
"""

import torch
from torchvision import transforms

from train.TrafficLightDataset import TrafficLightDataset

TEST_ANNOTATION_PATH = "./dataset2/test/annotations.xml"
TEST_IMG_DIR_PATH = "./dataset2/test/images/"
MODEL_PATH = "./models/model_dataset2_b8_e200_lr0.005.pth"
IMG_SIZE = (1080, 1920)
DEVICE = torch.device("cuda") if torch.cuda.is_available else torch.device("cpu")

SCORE_THRESHOLD = 0

torch.cuda.empty_cache()

model = torch.jit.load(MODEL_PATH, map_location="cpu")
model.to(DEVICE)

resize = transforms.Resize(IMG_SIZE)
to_tensor = transforms.ToTensor()
test_transform = transforms.Compose([resize, to_tensor])
test_dataset = TrafficLightDataset(
    annotation_path=TEST_ANNOTATION_PATH,
    img_dir_path=TEST_IMG_DIR_PATH,
    img_size=IMG_SIZE,
    transforms=test_transform,
)

img_path_all = test_dataset.img_path_all

model.eval()
for i in range(test_dataset.__len__()):
    img, target = test_dataset.__getitem__(i)
    imgs = []
    imgs.append(img.to(DEVICE))
    img_name = img_path_all[i].split("/")[-1].split(".")[0]
    print(img_name)

    with torch.no_grad():
        predictions = model(imgs)[1]
        print(predictions)

    f = open(f"./dets_annotation/{img_name}.txt", mode="a")

    for i, prediction in enumerate(predictions):
        len_box = len(prediction["boxes"])
        for j, box in enumerate(prediction["boxes"]):
            box = box.tolist()
            class_id = prediction["labels"].tolist()[j]
            score = prediction["scores"].tolist()[j]
            x = int(box[0])
            y = int(box[1])
            x2 = int(box[2])
            y2 = int(box[3])
            if score > SCORE_THRESHOLD:
                # f.write(f"{class_id} {score:.2f} {x:.2f} {y:.2f} {x2:.2f} {y2:.2f}")
                f.write(f"{class_id} {score:.2f} {x} {y} {x2} {y2}")
                if j < len_box - 1:
                    f.write("\n")
            # w = box[2] - box[0]
            # h = box[3] - box[1]
            # x_c = box[0] + w / 2
            # y_c = box[1] + h / 2
            # if score > SCORE_THRESHOLD:
            #     f.write(f"{class_id} {score:.2f} {x_c:.2f} {y_c:.2f} {w:.2f} {h:.2f}")
            #     if j < len_box - 1:
            #         f.write("\n")

    f.close()

# GPUキャッシュをクリア
torch.cuda.empty_cache()
