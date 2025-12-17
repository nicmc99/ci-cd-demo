pipeline {
  agent any
  options { timestamps() }

  environment {
    REGISTRY      = "docker.io"
    IMAGE_NAME    = "nicmc99/ci-cd-demo"
    TAG           = "latest"
    PORTAINER_URL = "http://host.docker.internal:9000"
    ENDPOINT_ID   = "3"
    STACK_ID      = "3"
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Docker Build') {
      steps {
        sh '''
          set -e

          GIT_SHA=$(git rev-parse --short=7 HEAD)
          VERSION_TAG="${BUILD_NUMBER}-${GIT_SHA}"

          echo "Building image with APP_VERSION=${VERSION_TAG}"
          docker build \
            --build-arg APP_VERSION="${VERSION_TAG}" \
            -t ${IMAGE_NAME}:latest .
        '''
      }
    }

    stage('Test Image') {
      steps {
        sh '''
          set -e
          echo "Running pytest inside the image..."
          docker run --rm ${IMAGE_NAME}:latest pytest -q
        '''
      }
    }

    stage('Docker Login & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            set -e

            GIT_SHA=$(git rev-parse --short=7 HEAD)
            VERSION_TAG="${BUILD_NUMBER}-${GIT_SHA}"

            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin ${REGISTRY}

            echo "Pushing latest image..."
            docker push ${IMAGE_NAME}:latest

            echo "Tagging and pushing versioned image: ${IMAGE_NAME}:${VERSION_TAG}"
            docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:${VERSION_TAG}
            docker push ${IMAGE_NAME}:${VERSION_TAG}

            echo "Pushed tags:"
            echo "  - ${IMAGE_NAME}:latest"
            echo "  - ${IMAGE_NAME}:${VERSION_TAG}"
          '''
        }
      }
    }

    stage('Portainer Redeploy') {
      steps {
        withCredentials([string(credentialsId: 'portainer-token', variable: 'PORTAINER_TOKEN')]) {
          sh """
            curl -sS -X POST \\
              "$PORTAINER_URL/api/stacks/${STACK_ID}/redeploy?endpointId=${ENDPOINT_ID}&pullImage=true" \\
              -H "Authorization: Bearer $PORTAINER_TOKEN" \\
              -H "Content-Type: application/json"
          """
        }
      }
    }
  }

  post {
    success {
      echo "✅ Deployed ${IMAGE_NAME}:${TAG}"
    }
    failure {
      echo "❌ Build or deploy failed — check console output."
    }
  }
}
