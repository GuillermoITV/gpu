
import os
from imageai.Prediction import ImagePrediction

execution_path = os.getcwd()
prediction = ImagePrediction()
prediction.setModelTypeAsResNet()
#prediction.setModelPath( execution_path + "\resnet50_weights_tf_dim_ordering_tf_kernels.h5")
prediction.setModelPath("resnet50_weights_tf_dim_ordering_tf_kernels.h5")
prediction.loadModel()

predictions, percentage_probabilities = prediction.predictImage("sample.jpeg", result_count=5)
for index in range(len(predictions)):
    print (predictions[index] , " : " , percentage_probabilities[index])
