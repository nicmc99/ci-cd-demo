pipeline {
  agent any
  options { timestamps() }

  environment {
    REGISTRY      = "docker.io"
    IMAGE_NAME    = "nicmc99/ci-cd-demo"     // change to your Docker Hub username/repo
    TAG           = "latest"
    PORTAINER_URL = "http://localhost:9000"  // or http://<your-server-ip>:9000
    ENDPOINT_ID   = "1"                      // Portainer endpoint ID
    STACK_ID      = "12"                     // Portainer stack ID
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Docker Build') {
      steps {
        sh """
          docker build -t ${IMAGE_NAME}:${TAG} .
        """
      }
    }

    stage('Docker Login & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh """
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin ${REGISTRY}
            docker push ${IMAGE_NAME}:${TAG}
          """
        }
      }
    }

    stage('Portainer Redeploy') {
      steps {
        withCredentials([string(credentialsId: 'portainer-token', variable: 'PORTAINER_TOKEN')]) {
          sh """
            curl -sS -X POST "${PORTAINER_URL}/api/stacks/${STACK_ID}/redeploy?endpointId=${ENDPOINT_ID}&pullImage=true" \
              -H "Authorization: Bearer ${PORTAINER_TOKEN}" \
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
