#in real worlkd use s3 or any other storge service

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}