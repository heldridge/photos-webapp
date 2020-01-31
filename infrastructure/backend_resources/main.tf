resource "aws_s3_bucket" "terraform-state-storage" {
  bucket_prefix = "terraform-remote-state-prod-"
  acl           = "private"

  tags = {
    Name = "Terraform Remote State Store"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
