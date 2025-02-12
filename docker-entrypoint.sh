#!/bin/bash
 
set -ue
shopt -s nullglob

export TZ=${TZ:-Asia/Tokyo}

# アウトプット先ディレクトリ（自動付与） /opt/artifact固定です
if [ -z "${SAKURA_ARTIFACT_DIR:-}" ]; then
  echo "Environment variable SAKURA_ARTIFACT_DIR is not set" >&2
  exit 1
fi

# DOKのタスクID（自動付与）
if [ -z "${SAKURA_TASK_ID:-}" ]; then
  echo "Environment variable SAKURA_TASK_ID is not set" >&2
  exit 1
fi

# 画像生成用プロンプト
if [ -z "${PROMPT:-}" ]; then
  echo "Environment variable PROMPT is not set" >&2
  exit 1
fi

# 画像生成用プロンプト（ネガティブ）
if [ -z "${NEGATIVE:-}" ]; then
  echo "Environment variable NEGATIVE is not set" >&2
  exit 1
fi

# 画像の幅
if [ -z "${WIDTH:-}" ]; then
  WIDTH=800
  exit 1
fi

# 画像の高さ
if [ -z "${HEIGHT:-}" ]; then
  HEIGHT=600
  exit 1
fi



# S3_はすべてboto3用の環境変数です
pushd /app
  python3 runner.py \
    --id="${SAKURA_TASK_ID}" \
    --output="${SAKURA_ARTIFACT_DIR}" \
    --prompt="${PROMPT}" \
    --negative="${NEGATIVE}" \
    --width="${WIDTH}" \
    --height="${HEIGHT}" \
    --s3-bucket="${S3_BUCKET:-}" \
    --s3-endpoint="${S3_ENDPOINT:-}" \
    --s3-secret="${S3_SECRET:-}" \
    --s3-token="${S3_TOKEN:-}"
popd
