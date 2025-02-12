import torch
from diffusers import StableDiffusionXLPipeline
import argparse
import boto3

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument(
    '--output',
    default='/opt/artifact',
    help='出力先ディレクトリを指定します。',
)
arg_parser.add_argument(
    '--prompt',
    default='',
    help='プロンプト',
)
arg_parser.add_argument(
    '--negative',
    default='',
    help='プロンプト（ネガティブ）',
)
arg_parser.add_argument(
    '--width',
    default=800,
    help='画像幅',
)
arg_parser.add_argument(
    '--height',
    default=600,
    help='画像高',
)
arg_parser.add_argument(
    '--id',
    default='',
    help='タスクIDを指定します。',
)
arg_parser.add_argument('--s3-bucket', help='S3のバケットを指定します。')
arg_parser.add_argument('--s3-endpoint', help='S3互換エンドポイントのURLを指定します。')
arg_parser.add_argument('--s3-secret', help='S3のシークレットアクセスキーを指定します。')
arg_parser.add_argument('--s3-token', help='S3のアクセスキーIDを指定します。')

args = arg_parser.parse_args()

s3 = None
if args.s3_token and args.s3_secret and args.s3_bucket:
    # S3クライアントの作成
    s3 = boto3.client(
        's3',
        endpoint_url=args.s3_endpoint if args.s3_endpoint else None,
        aws_access_key_id=args.s3_token,
        aws_secret_access_key=args.s3_secret)

pipe = StableDiffusionXLPipeline.from_pretrained(
    "cagliostrolab/animagine-xl-4.0",
    torch_dtype=torch.float16,
    use_safetensors=True,
    custom_pipeline="lpw_stable_diffusion_xl",
    add_watermarker=False
)
pipe.to('cuda')
print(args)
image = pipe(
    args.prompt,
    negative_prompt=args.negative,
    width=int(args.width),
    height=int(args.height),
    guidance_scale=6,
    num_inference_steps=25
).images[0]

save_path = f'{args.output}/{args.id}.png'
image.save(save_path)

if s3 is not None:
    s3.upload_file(
        Filename=save_path,
        Bucket=args.s3_bucket,
        Key=os.path.basename(save_path))

