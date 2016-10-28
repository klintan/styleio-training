import preprocess_a

if __name__ == "__main__":
    im = preprocess_a.preprocess_image_batch(['dog.jpg'], color_mode="rgb")

    # Test pretrained model
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model = convnet('alexnet',weights_path="weights/alexnet_weights.h5", heatmap=True)
    model.compile(optimizer=sgd, loss='mse')

    out = model.predict(im)
    heatmap = out[0,ids,:,:].sum(axis=0)