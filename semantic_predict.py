from models.model_builder import semantic_model, test_model
from utils.load_semantic_datasets import SemanticGenerator
import argparse
import time
import os
import tensorflow as tf
from tqdm import tqdm
import matplotlib.pyplot as plt
from tensorflow.keras.applications.imagenet_utils import preprocess_input
import tensorflow_addons as tfa
import cv2

def demo_prepare(path):
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img)

    return (img)


tf.keras.backend.clear_session()

parser = argparse.ArgumentParser()
parser.add_argument("--batch_size",     type=int,
                    help="배치 사이즈값 설정", default=1)
parser.add_argument("--model_name",     type=str,   help="저장될 모델 이름",
                    default=str(time.strftime('%m%d', time.localtime(time.time()))))
parser.add_argument("--dataset_dir",    type=str,
                    help="데이터셋 다운로드 디렉토리 설정", default='./datasets/')
parser.add_argument("--result_dir", type=str,
                    help="Test result dir", default='./results/')
parser.add_argument("--checkpoint_dir", type=str,
                    help="모델 저장 디렉토리 설정", default='./checkpoints/')
parser.add_argument("--weight_name", type=str,
                    help="모델 가중치 이름", default='/0622/_0622_320-180_8_50_0.001_adam_single_EFFNet_best_iou.h5')

args = parser.parse_args()
BATCH_SIZE = args.batch_size
SAVE_MODEL_NAME = args.model_name
DATASET_DIR = args.dataset_dir
RESULT_DIR = args.result_dir
CHECKPOINT_DIR = args.checkpoint_dir
WEIGHT_NAME = args.weight_name
MASK_RESULT_DIR = RESULT_DIR + 'mask_result/'
IMAGE_SIZE = (640, 320)
demo = False

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(MASK_RESULT_DIR, exist_ok=True)

TRAIN_INPUT_IMAGE_SIZE = IMAGE_SIZE
VALID_INPUT_IMAGE_SIZE = IMAGE_SIZE

test_dataset_config = SemanticGenerator(
    DATASET_DIR, TRAIN_INPUT_IMAGE_SIZE, BATCH_SIZE, mode='validation')
test_set = test_dataset_config.get_testData(test_dataset_config.valid_data)
test_steps = test_dataset_config.number_valid // BATCH_SIZE

if demo:
    filenames = os.listdir('./demo_images')
    filenames.sort()
    test_set = tf.data.Dataset.list_files('./demo_images/' + '*', shuffle=False)
    test_set = test_set.map(demo_prepare)
    test_set = test_set.batch(1)
    test_steps = len(filenames) // 1


model = test_model(image_size=IMAGE_SIZE)
# model.load_weights(CHECKPOINT_DIR + WEIGHT_NAME)
model.summary()

# warm up
model.predict(tf.zeros((1, 640, 320, 3)))


batch_idx = 0
avg_duration = 0
for x, label, original in tqdm(test_set, total=test_steps):



    # img = tf.cast(x, tf.float32)

    # img = tf.image.resize(img, size=(IMAGE_SIZE[0], IMAGE_SIZE[1]),
    #     method=tf.image.ResizeMethod.BILINEAR)

    start = time.process_time()

    pred = model.predict(x)
    duration = (time.process_time() - start)

    avg_duration += duration

    batch_idx += 1

    # 0.13917000932443477sec. -> seperable conv + transposed
    # 0.1392808986529772sec... -> conv + transposed

    # 0.13598978692402514sec -> seperable conv+ upsampling
    # 0.1388885202587266sec -> upsampling

    # 0.1397708012381925sec. -> deep sep + upsampling
    # 0.13894884432443516sec. -> deep sep + trasnposed
print(f"avg inference time : {(avg_duration / test_dataset_config.number_valid)}sec.")