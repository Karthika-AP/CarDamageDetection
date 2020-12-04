from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import gc
import tensorflow.keras.backend as bk

basedir = 'Damageapp/static'


def data_generator(damage):
    test_data_gen = ImageDataGenerator(rescale=1. / 255)
    validation_generator = test_data_gen.flow_from_directory(
        os.path.join(basedir, damage),
        target_size=(224, 224),
        shuffle=False,
        class_mode='binary',
    )
    return validation_generator


def is_car(view):
    model = load_model(os.path.join(basedir, "model/car.h5"))
    generator = data_generator("upload/Folders/"+view)
    prediction = model.predict(generator)
    print(prediction)
    a = (prediction <= 0.55)  # 0.5)
    generator = None
    gc.collect()
    bk.clear_session()
    print(a)
    if a.all():
        return True
    else:
        return False


def is_bumper():
    model = load_model(os.path.join(basedir, "model/front.h5"))
    generator = data_generator("upload/Folders/Front")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False


def is_front():
    model = load_model(os.path.join(basedir, "model/front.h5"))
    generator = data_generator("upload/Folders/Front")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False


def is_hood():
    model = load_model(os.path.join(basedir, 'model/hood.h5'))
    generator = data_generator("upload/Folders/Front")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False


def is_windshield():
    model = load_model(os.path.join(basedir, 'model/winshield.h5'))
    generator = data_generator("upload/Folders/Front")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.4:
        return True
    else:
        return False

def is_window_left():
    model = load_model(os.path.join(basedir, 'model/window.h5'))
    generator = data_generator("upload/Folders/Left")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False


def is_side_left():
    model = load_model(os.path.join(basedir, 'model/side.h5'))
    generator = data_generator("upload/Folders/Left")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False


def is_door_left():
    model = load_model(os.path.join(basedir, 'model/door.h5'))
    generator = data_generator("upload/Folders/Left")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False
    
def is_window_right():
    model = load_model(os.path.join(basedir, 'model/window.h5'))
    generator = data_generator("upload/Folders/Right")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False


def is_side_right():
    model = load_model(os.path.join(basedir, 'model/side.h5'))
    generator = data_generator("upload/Folders/Right")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False


def is_door_right():
    model = load_model(os.path.join(basedir, 'model/door.h5'))
    generator = data_generator("upload/Folders/Right")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False


def is_boot():
    model = load_model(os.path.join(basedir, 'model/hood.h5'))
    generator = data_generator("upload/Folders/Rear")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False


def is_rear():
    model = load_model(os.path.join(basedir, 'model/rear.h5'))
    generator = data_generator("upload/Folders/Rear")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.5:
        return True
    else:
        return False


def is_windshield_rear():
    model = load_model(os.path.join(basedir, 'model/winshield.h5'))
    generator = data_generator("upload/Folders/Rear")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False


def is_bumper_rear():
    model = load_model(os.path.join(basedir, "model/rear.h5"))
    generator = data_generator("upload/Folders/Rear")
    prediction = model.predict(generator)
    generator = None
    gc.collect()
    bk.clear_session()
    if prediction <= 0.55:  # 0.5:
        return True
    else:
        return False
