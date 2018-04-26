/*#include <opencv2\highgui\highgui.hpp>
#include <iostream>

using namespace cv;

int main() {
	Mat img(500, 1000, CV_8UC3, Scalar(0, 0, 100)); //create an image ( 3 channels, 8 bit image depth, 500 high, 1000 wide, (0, 0, 100) assigned for Blue, Green and Red plane respectively. )

	if (img.empty()) //check whether the image is loaded or not
		std::cout << "Error : Image cannot be loaded..!!" << std::endl;

	namedWindow("MyWindow", CV_WINDOW_AUTOSIZE); //create a window with the name "MyWindow"
	imshow("MyWindow", img); //display the image which is stored in the 'img' in the "MyWindow" window

	waitKey(0); //wait infinite time for a keypress

	destroyWindow("MyWindow"); //destroy the window with the name, "MyWindow"
}*/

//
// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
//
#include "CNTKLibrary.h"
#include <functional>

using namespace CNTK;

Dictionary CreateCifarMinibatchSource(size_t epochSize)
{
	size_t imageHeight = 32;
	size_t imageWidth = 32;
	size_t numChannels = 3;
	size_t numClasses = 10;
	auto mapFilePath = L"cifar-10-batches-py/train_map.txt";
	auto meanFilePath = L"cifar-10-batches-py/CIFAR-10_mean.xml";

	Dictionary cropTransformConfig;
	cropTransformConfig[L"type"] = L"Crop";
	cropTransformConfig[L"cropType"] = L"RandomSide";
	cropTransformConfig[L"sideRatio"] = L"0.8";
	cropTransformConfig[L"jitterType"] = L"uniRatio";

	Dictionary scaleTransformConfig;
	scaleTransformConfig[L"type"] = L"Scale";
	scaleTransformConfig[L"width"] = imageWidth;
	scaleTransformConfig[L"height"] = imageHeight;
	scaleTransformConfig[L"channels"] = numChannels;
	scaleTransformConfig[L"interpolations"] = L"linear";

	Dictionary meanTransformConfig;
	meanTransformConfig[L"type"] = L"Mean";
	meanTransformConfig[L"meanFile"] = meanFilePath;

	std::vector<DictionaryValue> allTransforms = { cropTransformConfig, scaleTransformConfig, meanTransformConfig };

	Dictionary featuresStreamConfig;
	featuresStreamConfig[L"transforms"] = allTransforms;

	Dictionary labelsStreamConfig;
	labelsStreamConfig[L"labelDim"] = numClasses;

	Dictionary inputStreamsConfig;
	inputStreamsConfig[L"features"] = featuresStreamConfig;
	inputStreamsConfig[L"labels"] = labelsStreamConfig;

	Dictionary deserializerConfiguration;
	deserializerConfiguration[L"type"] = L"ImageDeserializer";
	deserializerConfiguration[L"file"] = mapFilePath;
	deserializerConfiguration[L"input"] = inputStreamsConfig;

	Dictionary minibatchSourceConfiguration;
	minibatchSourceConfiguration[L"epochSize"] = epochSize;
	minibatchSourceConfiguration[L"deserializers"] = std::vector<DictionaryValue>({ deserializerConfiguration });

	return minibatchSourceConfiguration;
}

int main() {
	CreateCifarMinibatchSource(3);
}