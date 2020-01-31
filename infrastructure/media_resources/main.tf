resource "aws_s3_bucket" "terraform-state-storage" {
  bucket_prefix = "lewdix-media-stage-"
  acl           = "private"

  tags = {
    Name = "Bucket for media files -stage"
  }

}
