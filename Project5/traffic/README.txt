Precess Logs:

Firsts i will seach more what are the options for layers 
and how to implement them using tensorFlow

I looked at the keras layers, I will try to use the conv2d layer
I will try the max and the average pooling

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

During my earlier reserch, I foud that is more suited to use conv3d, since it does have 3 
dimentions ( width, height and rgb color )
I chose to test with my original guess of 2d so I could compare their behavior 

Test 3:
    test with 3d convolution 