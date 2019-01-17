#### Introduction
The python code in this directory trains a model using the MNIST dataset. There is also a Dockerfile to build a container for the code and run it as a docker container.

#### Setup
1. Download the training and test files from [here](http://yann.lecun.com/exdb/mnist/). You may upload a copy of these files to a GCS bucket.

2. Set the following environment variables:

```bash
PROJECT=<your gcp project>
CONTAINER_NAME=<your chosen name for the container, e.g. mnist-trainer:v1>
SERVICE_ACCOUNT_FOLDER=<your local directory containing the service account file>
SERVICE_ACCOUNT_FILE=<the service account file name>
TRAINING_IMAGES_FILE=<GCS path to the training images file, e.g. gs://mnist-bucket/training-images>
TRAINING_LABELS_FILE=<GCS path to the training labels file, e.g. gs://mnist-bucket/training-labels>
TEST_IMAGES_FILE=<GCS path to the test images file, e.g. gs://mnist-bucket/test-images>
TEST_LABELS_FILE=<GCS path to the test labels file, e.g. gs://mnist-bucket/test-files>
```

3. Activate your project
```bash
gcloud config set project $PROJECT
```

4. Create and download a service account with at least the `Storage Object Admin` role. You can do it by visting the [GCP website](https://pantheon.corp.google.com/iam-admin/serviceaccounts).

5. Build the docker container:

```bash
docker build . -t gcr.io/${PROJECT}/${CONTAINER_NAME}
```

6. Push the container to GCR:

```bash
docker push gcr.io/${PROJECT}/${CONTAINER_NAME}
```

#### Running the Docker container

Once the container is created and pushed to GCR, we can run it to train a model for MNIST.

```bash
docker run -it
           -v $SERVICE_ACCOUNT_FOLDER:/config
           -e GOOGLE_APPLICATION_CREDENTIALS=/config/${SERVICE_ACCOUNT_FILE}
           -e TRAINING_IMAGES_FILE ${TRAINING_IMAGES_FILE}
           -e TRAINING_LABELS_FILE ${TRAINING_LABELS_FILE}
           -e TEST_IMAGES_FILE ${TEST_IMAGES_FILE}
           -e TEST_LABELS_FILE ${TEST_LABELS_FILE}
           gcr.io/${PROJECT}/${CONTAINER_NAME}
```
