import preprocess_a
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

if __name__ == "__main__":
    datagen = ImageDataGenerator()

    im_list = imtools.get_imlist(sys.argv[1])

    im = preprocess_a.preprocess_image_batch(image_paths=['.jpg'], color_mode="rgb")

    # Test pretrained model
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model = convnet('alexnet',weights_path="weights/alexnet_weights.h5", heatmap=True)
    model.compile(optimizer=sgd, loss='mse')

    out = model.predict(im)
    heatmap = out[0,ids,:,:].sum(axis=0)