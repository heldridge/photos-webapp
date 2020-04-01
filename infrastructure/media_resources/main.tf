resource "aws_s3_bucket" "qlbhmmvpym" {
  bucket = "media.qlbhmmvpym.club"
  acl    = "private"
  policy = file("policy.json")

  tags = {
    Name = "Bucket for media files -dev domain"
  }

  cors_rule {
    allowed_origins = ["http://localhost:8000", "http://3.89.61.10/"]
    allowed_methods = ["GET"]
    max_age_seconds = 3000
    allowed_headers = ["Content-*", "Host"]
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
      "arn:aws:s3:::${aws_s3_bucket.qlbhmmvpym.id}/*",
      "arn:aws:s3:::${aws_s3_bucket.qlbhmmvpym.id}"
    ]
  }
}

resource "aws_iam_user_policy" "django_s3_access" {
  name = "django-s3-access"
  user = aws_iam_user.django.name

  policy = data.aws_iam_policy_document.django_user.json
}
