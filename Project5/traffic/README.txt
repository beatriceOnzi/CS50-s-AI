Precess Logs:

Firsts i will seach more what are the options for layers 
and how to implement them using tensorFlow

I looked at the keras layers, I will try to use the conv2d layer
I will try the max and the average pooling

Using gtsrb-small

Test 1:
    Conv2D(32, 3, activation='relu')
    MaxPooling2D(pool_size=(2, 2))
    Flatten()
    Dense(32, activation='relu')
    Dense(43, activation='softmax')

    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]

    accuracy: 0.6310 - loss: 1.0986


Test 2:
    added 1 more layer of pooling and 1 more layer of conv2d, with the same params

    accuracy: 0.6607 - loss: 1.0986


reserched in the Youtube and found some aditional layers that are going to be usefull


Test 3:
    changed to average pooling

    accuracy: 0.6190 - loss: 1.0986

I changed back to MaxPooling


Test 4:
    added BatchNormalization

    accuracy: 1.0000 - loss: 0,00021916


Test 5: 
    tripled layers.Conv2D(32, 3 , activation='relu'),      with 32, 64 and 128 filters
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.BatchNormalization()
    
    accuracy: 1.0000 - loss: 0.0054

Why adding more layers increased the loss?
    Test with double Conv2D, MaxPooling2D and BatchNormalization() 
    loss: 0.0010


Conclusion:
Adding more layers does not equal less loss. 
More layers are not worth it in this case.

Returning to just one Conv2D, MaxPooling2D and BatchNormalization() 

Test 6:
    adding dropout to help with overfitting

    accuracy: 1.0000 - loss: 0.0037

Test 7:
    adding one more dense layer

    accuracy: 0.9970 - loss: 0.0133

Test 8:
    changing final dense layer function from relu to linear

    accuracy: 1.0000 - loss: 0,00051965


Final Test with gtsrb:
    model = tf.keras.Sequential(
        [
            layers.InputLayer(input_shape=[IMG_WIDTH, IMG_HEIGHT, 3]),
            layers.Conv2D(32, 3 , activation='relu'),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.BatchNormalization(),
            layers.Flatten(),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(NUM_CATEGORIES, 'linear'),
            layers.Activation('softmax')
        ]
    )
    
    accuracy: 0.9637 - loss: 0.1676