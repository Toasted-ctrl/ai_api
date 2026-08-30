#!/usr/bin/env bash
set -euo pipefail
# ─────────────────────────────────────────────
# build.sh — AI API Build Script
# ─────────────────────────────────────────────
# Usage:
#   ./build.sh --patch               # Build + auto-increment PATCH
#   ./build.sh --minor               # Bump MINOR, reset PATCH to 0
#   ./build.sh --major               # Bump MAJOR, reset MINOR & PATCH to 0
#   ./build.sh --push                # Push current version to registry
#   ./build.sh --patch --push        # Bump, build, and push in one step
#   ./build.sh --no-cache --patch    # Build without Docker layer cache
#
# Image naming:
#   storage01/artificial-intelligence-api:<version>
#   storage01/artificial-intelligence-api:latest
# ─────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ─── Image & registry config ──────────────
IMAGE_NAME="artificial-intelligence-api"
REGISTRY="storage01:5000"
VERSION_FILE="${SCRIPT_DIR}/.version"

# ─── Docker config ─────────────────────────
export DOCKER_BUILDKIT=1

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ─── Helpers ────────────────────────────────
log()   { echo -e "${CYAN}[build]${NC} $*"; }
ok()    { echo -e "${GREEN}[  ok ]${NC} $*"; }
warn()  { echo -e "${YELLOW}[warn ]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }

usage() {
    echo ""
    echo -e "${BOLD}AI API Build System${NC}"
    echo ""
    echo "Usage:"
    echo "  $0 [--major|--minor|--patch] [--no-cache] [--push]"
    echo ""
    echo "Options:"
    echo "  --patch      Increment patch version (default bump)"
    echo "  --minor      Bump minor version, reset patch to 0"
    echo "  --major      Bump major version, reset minor & patch to 0"
    echo "  --no-cache   Pass --no-cache to docker build"
    echo "  --push       Push image to registry after build"
    echo ""
    echo "Images are tagged as:"
    echo "  ${REGISTRY}/${IMAGE_NAME}:<version>"
    echo "  ${REGISTRY}/${IMAGE_NAME}:latest"
    echo ""
    echo "Examples:"
    echo "  $0 --patch                # 0.1.0 → 0.1.1"
    echo "  $0 --minor                # 0.1.1 → 0.2.0"
    echo "  $0 --major                # 0.2.0 → 1.0.0"
    echo "  $0 --minor --push         # bump minor, build, push"
    echo "  $0 --push                 # push current version only"
    echo ""
    [[ -f "$VERSION_FILE" ]] && echo "Current version: $(cat "$VERSION_FILE" | tr -d '[:space:]')"
    echo ""
    exit 1
}

# ─── Version management ────────────────────
read_version() {
    if [[ ! -f "$VERSION_FILE" ]]; then
        echo "0.0.0" > "$VERSION_FILE"
        warn "No .version file found — initialized to 0.0.0"
    fi
    cat "$VERSION_FILE" | tr -d '[:space:]'
}

bump_version() {
    local current="$1"
    local bump_type="$2"
    local major minor patch

    IFS='.' read -r major minor patch <<< "$current"
    major="${major:-0}"
    minor="${minor:-0}"
    patch="${patch:-0}"

    case "$bump_type" in
        major) major=$((major + 1)); minor=0; patch=0 ;;
        minor) minor=$((minor + 1)); patch=0 ;;
        patch) patch=$((patch + 1)) ;;
        *)     err "Unknown bump type: $bump_type"; exit 1 ;;
    esac

    echo "${major}.${minor}.${patch}"
}

write_version() {
    echo "$1" > "$VERSION_FILE"
}

# ─── Entry point ────────────────────────────
main() {
    local bump_type=""
    local docker_flags=""
    local push=false

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --major|--minor|--patch)
                if [[ -n "$bump_type" ]]; then
                    err "Cannot combine multiple version bumps."
                    exit 1
                fi
                bump_type="${1#--}"
                shift
                ;;
            --no-cache)  docker_flags="--no-cache"; shift ;;
            --push)      push=true;                 shift ;;
            --help|-h)   usage ;;
            -*)          err "Unknown option: $1"; usage ;;
            *)           err "Unknown argument: $1"; usage ;;
        esac
    done

    [[ -z "$bump_type" && "$push" == false ]] && usage

    echo ""
    echo "╔══════════════════════════════════════════════════╗"
    echo "║              AI API Build System                 ║"
    printf "║              Registry: %-25s ║\n" "$REGISTRY"
    echo "╚══════════════════════════════════════════════════╝"

    local current_version
    current_version="$(read_version)"

    # ─── Build (with version bump) ────────
    if [[ -n "$bump_type" ]]; then
        local new_version
        new_version="$(bump_version "$current_version" "$bump_type")"

        local image_tagged="${IMAGE_NAME}:${new_version}"
        local image_latest="${IMAGE_NAME}:latest"

        echo ""
        echo "╭──────────────────────────────────────────────────╮"
        printf "│  %-48s │\n" "${IMAGE_NAME}"
        printf "│  %-48s │\n" "${current_version} → ${new_version}  (${bump_type})"
        printf "│  %-48s │\n" "${image_tagged}"
        echo "╰──────────────────────────────────────────────────╯"

        log "Building Docker image..."
        if ! docker build \
            --build-arg VERSION="${new_version}" \
            ${docker_flags} \
            -t "$image_tagged" \
            -t "$image_latest" \
            --label "app.name=${IMAGE_NAME}" \
            --label "app.version=${new_version}" \
            --label "app.registry=${REGISTRY}" \
            --label "app.built=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
            "$SCRIPT_DIR"; then
            err "Docker build FAILED — version not incremented"
            exit 1
        fi

        write_version "$new_version"
        sed -i '/^\[project\]/,/^\[/ s/^version = ".*"/version = "'"${new_version}"'"/' "${SCRIPT_DIR}/pyproject.toml"
        ok "Image built: ${image_tagged}"
        current_version="$new_version"

    fi

    # ─── Push ─────────────────────────────
    if [[ "$push" == true ]]; then
        local registry_tagged="${REGISTRY}/${IMAGE_NAME}:${current_version}"
        local registry_latest="${REGISTRY}/${IMAGE_NAME}:latest"

        echo ""
        echo "╭──────────────────────────────────────────────────╮"
        printf "│  %-48s │\n" "Pushing to ${REGISTRY}"
        printf "│  %-48s │\n" "${registry_tagged}"
        printf "│  %-48s │\n" "${registry_latest}"
        echo "╰──────────────────────────────────────────────────╯"

        log "Tagging for registry..."
        docker tag "${IMAGE_NAME}:${current_version}" "$registry_tagged"
        docker tag "${IMAGE_NAME}:latest" "$registry_latest"
        ok "Tagged ${registry_tagged}"

        log "Pushing ${registry_tagged}..."
        docker push "$registry_tagged"
        ok "Pushed ${registry_tagged}"

        log "Pushing ${registry_latest}..."
        docker push "$registry_latest"
        ok "Pushed ${registry_latest}"
    fi

    # ─── Summary ──────────────────────────
    echo ""
    echo "────────────────────────────────────────"
    ok "${IMAGE_NAME} @ v${current_version} ✓"
}

main "$@"