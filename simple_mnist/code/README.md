#### Introduction
The python code in this directory trains a model using the MNIST dataset. There is also a Dockerfile to build a container for the code and run it as a docker container.

#### Setup
1. Download the training and test files from [here]([http://yann.lecun.com/exdb/mnist/). The test files are optional for training a model.

2. Create and download a service account with at least the `Storage Object Admin` role.

3. Set the following environment variables:

```
PROJECT=<your gcp project>
CONTAINER_NAME=<your chosen name for the container, e.g. mnist-trainer:v1>
SERVICE_ACCOUNT_FOLDER=<your local directory containing the service account file>
SERVICE_ACCOUNT_FILE=<the service account file name>
TRAINING_IMAGES_FILE=<GCS path to the training images file>
TRAINING_LABELS_FILE=<GCS path to the training labels file>
TEST_IMAGES_FILE=<GCS path to the test images file>
TEST_LABELS_FILE=<GCS path to the test labels file>
OUTPUT_MODEL=<GCS path for the output model, e.g. gs://my_bucket/my_model.h5>
```

4. Build the docker container:

```
docker build . -t gcr.io/${PROJECT}/${CONTAINER_NAME}
```

5. Push the container to GCR:

```
docker push gcr.io/${PROJECT}/${CONTAINER_NAME}
```

#### Running the Code

Once the container is created and pushed to GCR, we can run it to train a model for MNIST. The environment variables for testing (`TEST_IMAGES_FILE` and `TEST_LABELS_FILE`) are optional in the following command, and you may remove them:

```
docker run -it
            -v $SERVICE_ACCOUNT_FOLDER:/config
            -e GOOGLE_APPLICATION_CREDENTIALS=/config/${SERVICE_ACCOUNT_FILE}
            gcr.io/${PROJECT}/${CONTAINER_NAME}
            --training_images ${TRAINING_IMAGES_FILE}
            --training_labels ${TRAINING_LABELS_FILE}
            --test_images ${TEST_IMAGES_FILE}
            --test_labels ${TEST_LABELS_FILE}
            --model ${OUTPUT_MODEL}
            --epochs 2
            --batch 128
```
