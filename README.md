# Gitops-CI/CD-Demo

End-to-end GitOps CI/CD pipeline using **GitHub Actions**, **Docker**, **Helm**, **Argo CD**, and **Kubernetes (Kind)**.

This project demonstrates a complete GitOps workflow: a Flask app is built and containerized by GitHub Actions on every push, the resulting image is pushed to a container registry, the Helm chart's image tag is updated automatically, and Argo CD syncs the change into a local Kind cluster - no manual `kubectl apply` required.

## Architecture

```
Developer Push (main)
        │
        ▼
GitHub Actions (ci-cd.yml)
   ├─ Build Docker image (flask-demo)
   ├─ Push image to registry
   └─ Update image tag in Helm values
        │
        ▼
Git repo (source of truth)
        │
        ▼
Argo CD (watching repo)
        │
        ▼
Kind Cluster (local Kubernetes)
        │
        ▼
Flask App Running
```

## Tech Stack

- **Application**: Python (Flask)
- **Containerization**: Docker
- **CI**: GitHub Actions
- **Package/Deploy**: Helm
- **GitOps/CD**: Argo CD
- **Cluster**: Kubernetes via Kind (Kubernetes IN Docker)

## Project Structure

```
gitops-cicd-demo/
├── .github/workflows/     # GitHub Actions CI/CD pipeline (ci-cd.yml)
├── flask-demo/            # Flask application source and Helm chart
├── static/                # CSS / static assets
├── templates/              # HTML templates
├── Dockerfile              # Image build definition
├── app.py                  # Flask application entrypoint
├── requirements.txt        # Python dependencies
├── kind-config.yml         # Kind cluster configuration
└── README.md
```

## Prerequisites

- Docker
- [Kind](https://kind.sigs.k8s.io/)
- kubectl
- Helm
- Argo CD CLI (optional, for manual syncs)
- A GitHub account with Actions enabled

## Getting Started

### 1. Create the Kind cluster

```bash
kind create cluster --config kind-config.yml
```

### 2. Install Argo CD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 3. Point Argo CD at this repo

Create an Argo CD `Application` pointing to the Helm chart in this repo, targeting the Kind cluster context.

### 4. Push to `main`

Any push to `main` triggers the GitHub Actions workflow, which builds and pushes a new image and updates the Helm chart's image tag. Argo CD detects the change and syncs it to the cluster automatically.

## CI/CD Pipeline

The workflow defined in `.github/workflows/ci-cd.yml`:

1. Checks out the repository
2. Builds the Docker image from `flask-demo/`
3. Pushes the image to the container registry
4. Updates the image tag reference in the Helm chart
5. Commits the updated manifest back to the repo (triggering Argo CD sync)

## Notes

- This is a local/demo GitOps setup using **Kind** rather than a managed cluster (e.g. EKS) — intended to showcase the pipeline mechanics end to end without cloud costs.
- Argo CD continuously watches the Git repo, so deployments are pull-based rather than pushed by CI directly.

## Author

[jeenicj97](https://github.com/jeenicj97)
