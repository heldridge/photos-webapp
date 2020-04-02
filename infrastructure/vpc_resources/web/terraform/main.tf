resource "aws_security_group" "main" {
  name        = "WebMain"
  description = "For the main webserver"

  tags = {
    Name = "WebMain"
  }
}

# Allow ssh from my IP
resource "aws_security_group_rule" "main_allow_ssh" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["96.255.57.191/32"]
  security_group_id = aws_security_group.main.id

  description = "Allow ssh from my home IP"
}

resource "aws_security_group_rule" "main_allow_https" {
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  security_group_id = aws_security_group.main.id
  cidr_blocks       = ["96.255.57.191/32"]

  description = "Allow https from anywhere"
}

resource "aws_security_group_rule" "main_allow_http" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  security_group_id = aws_security_group.main.id
  cidr_blocks       = ["96.255.57.191/32"]

  description = "Allow http from anywhere"
}

resource "aws_security_group_rule" "main_allow_outbound" {
  type        = "egress"
  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.main.id
  description       = "Allow all outbound"
}

data "aws_ami" "ubuntu_18_04" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_key_pair" "main" {
  key_name   = "WebMain"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3MDhU4c8lJCQ0QA+s1ObOC7Plx5cr+bhA9vvkH4XKzcDpQRiSeMLRlVTy0cf4icy7UqOQEtQHe4JD4WeJ4o/Q41EjYdVdp0zvHOIhco9qSo7Fwq7hwU4kfvsNMsQmiTjRXW+UfTCiaUSEW0CP2sdLdwrVcGUD9CiI6VIee5UKa7lOlQhMxz42+Qcy348SPGoGxAnSX1g+fx2flLslHDOv/KjeN7My543fEXqJnflWNzVQmJUNqh+m6YWOipShcBrlOA/txgtLMJscYqRKhOBiRpDzUC6G6H2E+DUwRRg3dT/Xjs8rheDRWOr3JB4xUUJZ1bs9syTz5RMtto1kpXHj harry.eldridge@C02VXAGWHTD5"
}

resource aws_instance "main" {
  ami           = data.aws_ami.ubuntu_18_04.id
  instance_type = "t2.micro"

  tags = {
    Name = "WebMain"
  }

  security_groups = [aws_security_group.main.name]
  key_name        = aws_key_pair.main.key_name
}

resource aws_eip "main" {
  instance = aws_instance.main.id
}

##################################
# Give Django user access to ses #
##################################
data "terraform_remote_state" "media" {
  backend = "s3"

  config = {
    bucket = "terraform-remote-state-prod-20200131000633966100000001"
    key    = "media/terraform.tfstate"
    region = "us-east-1"
  }
}

data "aws_iam_policy_document" "django_ses" {
  statement {
    sid = "djangoUserS3"

    actions = [
      "ses:SendRawEmail"
    ]

    resources = [
      "arn:aws:ses:us-east-1:453433582457:identity/lewdix.com"
    ]
  }
}

resource "aws_iam_user_policy" "django_ses" {
  name = "django-ses-access"
  user = data.terraform_remote_state.media.outputs.django_user_name

  policy = data.aws_iam_policy_document.django_ses.json
}
