terraform {
  backend "s3" {
    encrypt = true
    bucket  = "terraform-remote-state-prod-20200131000633966100000001"
    region  = "us-east-1"
    key     = "general/terraform.tfstate"
  }
}
