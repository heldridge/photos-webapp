# Static and media storage bucket
resource "aws_s3_bucket" "static_media_storage" {
  bucket_prefix = "lewdix-media-stage-"
  acl           = "private"

  tags = {
    Name = "Bucket for media files -stage"
  }
}

# Django user
resource "aws_iam_user" "django" {
  name = "django"

  tags = {
    Name = "django"
  }
}


data "aws_iam_policy_document" "django_user" {
  statement {
    sid = "djangoUserS3"

    actions = [
      "s3:PutObject",
      "s3:GetObjectAcl",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:DeleteObject",
      "s3:PutObjectAcl"
    ]

    resources = [
      "arn:aws:s3:::${aws_s3_bucket.static_media_storage.id}/*",
      "arn:aws:s3:::${aws_s3_bucket.static_media_storage.id}"
    ]
  }
}

resource "aws_iam_user_policy" "django_s3_access" {
  name = "django-s3-access"
  user = aws_iam_user.django.name

  policy = data.aws_iam_policy_document.django_user.json
}

